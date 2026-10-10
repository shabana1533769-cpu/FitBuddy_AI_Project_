from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from .schemas import UserInput, FeedbackRequest
from .database import save_user, save_plan, get_latest_plan, update_plan, get_all_users
from .gemini_generator import generate_workout_gemini
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .updated_plan import update_workout_plan

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(
    request: Request,
    user_id: str = Form(...),
    name: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):
    try:
        data = UserInput(user_id=user_id, name=name, age=age, weight=weight, goal=goal, intensity=intensity)
        user = save_user(data)
        workout = generate_workout_gemini(data.name, data.age, data.weight, data.goal, data.intensity)
        tip = generate_nutrition_tip_with_flash(data.goal)
        plan = save_plan(user.id, workout, tip)
        return templates.TemplateResponse("result.html", {
            "request": request, "user": user, "plan": plan,
            "message": "Your personalized plan is ready!"
        })
    except Exception as exc:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": str(exc),
            "form": {"user_id": user_id, "name": name, "age": age, "weight": weight, "goal": goal, "intensity": intensity}
        }, status_code=400)

@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(request: Request, user_id: str = Form(...), feedback: str = Form(...)):
    try:
        data = FeedbackRequest(user_id=user_id, feedback=feedback)
        user, plan = get_latest_plan(data.user_id)
        if not user or not plan:
            return templates.TemplateResponse("feedback.html", {
                "request": request, "error": "No plan found for this User ID."
            }, status_code=404)

        updated = update_workout_plan(plan.updated_plan or plan.original_plan, data.feedback, user.goal, user.intensity)
        updated_record = update_plan(plan.id, updated, data.feedback)
        return templates.TemplateResponse("result.html", {
            "request": request, "user": user, "plan": updated_record,
            "message": "Your plan was updated using your feedback."
        })
    except Exception as exc:
        return templates.TemplateResponse("feedback.html", {"request": request, "error": str(exc)}, status_code=400)

@router.get("/feedback", response_class=HTMLResponse)
def feedback_page(request: Request):
    return templates.TemplateResponse("feedback.html", {"request": request})

@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request):
    users = get_all_users()
    return templates.TemplateResponse("all_users.html", {"request": request, "users": users})

@router.get("/health")
def health():
    return {"status": "ok", "service": "FitBuddy"}
