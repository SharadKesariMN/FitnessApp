from fastapi import FastAPI, APIRouter, HTTPException, Request, Response, Depends
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone, timedelta
import requests
from emergentintegrations.llm.chat import LlmChat, UserMessage

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI()
api_router = APIRouter(prefix="/api")

# Helper function to get user from session
async def get_current_user(request: Request) -> Optional[Dict[str, Any]]:
    session_token = request.cookies.get("session_token")
    if not session_token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            session_token = auth_header.split(" ")[1]
    
    if not session_token:
        return None
    
    session_doc = await db.user_sessions.find_one({"session_token": session_token}, {"_id": 0})
    if not session_doc:
        return None
    
    expires_at = session_doc["expires_at"]
    if isinstance(expires_at, str):
        expires_at = datetime.fromisoformat(expires_at)
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at < datetime.now(timezone.utc):
        return None
    
    user_doc = await db.users.find_one({"user_id": session_doc["user_id"]}, {"_id": 0})
    return user_doc

# Auth dependency
async def require_auth(request: Request) -> Dict[str, Any]:
    user = await get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

# Models
class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    user_id: str
    email: EmailStr
    name: str
    picture: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    date_of_birth: Optional[str] = None
    age: Optional[int] = None
    bmi: Optional[float] = None
    selected_sports: Optional[List[str]] = []
    fitness_goal: Optional[str] = None
    selected_sport: Optional[str] = None
    current_plan_id: Optional[str] = None
    is_guest: bool = False
    is_admin: bool = False
    created_at: datetime

class UserSession(BaseModel):
    model_config = ConfigDict(extra="ignore")
    user_id: str
    session_token: str
    expires_at: datetime
    created_at: datetime

class OnboardingData(BaseModel):
    height: float
    weight: float
    date_of_birth: str
    age: int
    selected_sports: Optional[List[str]] = []

class FitnessGoalData(BaseModel):
    fitness_goal: str
    selected_sport: Optional[str] = None

class WorkoutPlan(BaseModel):
    model_config = ConfigDict(extra="ignore")
    plan_id: str
    user_id: str
    plan_type: str
    sport: Optional[str] = None
    duration_days: int = 45
    daily_exercises: List[Dict[str, Any]]
    created_at: datetime

class Exercise(BaseModel):
    model_config = ConfigDict(extra="ignore")
    exercise_id: str
    name: str
    description: str
    duration_minutes: int
    gif_url: str
    sport_category: str
    difficulty: str
    instructions: List[str]

class UserProgress(BaseModel):
    model_config = ConfigDict(extra="ignore")
    progress_id: str
    user_id: str
    plan_id: str
    day_number: int
    completed: bool
    completed_at: Optional[datetime] = None
    notes: Optional[str] = None

# Auth endpoints
@api_router.post("/auth/session")
async def create_session(request: Request, response: Response):
    data = await request.json()
    session_id = data.get("session_id")
    
    if not session_id:
        raise HTTPException(status_code=400, detail="session_id required")
    
    try:
        resp = requests.get(
            "https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data",
            headers={"X-Session-ID": session_id},
            timeout=10
        )
        resp.raise_for_status()
        session_data = resp.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to get session data: {str(e)}")
    
    email = session_data.get("email")
    name = session_data.get("name")
    picture = session_data.get("picture")
    session_token = session_data.get("session_token")
    
    existing_user = await db.users.find_one({"email": email}, {"_id": 0})
    
    if existing_user:
        user_id = existing_user["user_id"]
        await db.users.update_one(
            {"user_id": user_id},
            {"$set": {"name": name, "picture": picture}}
        )
    else:
        user_id = f"user_{uuid.uuid4().hex[:12]}"
        user_doc = {
            "user_id": user_id,
            "email": email,
            "name": name,
            "picture": picture,
            "is_guest": False,
            "is_admin": False,
            "created_at": datetime.now(timezone.utc)
        }
        await db.users.insert_one(user_doc)
    
    expires_at = datetime.now(timezone.utc) + timedelta(days=7)
    session_doc = {
        "user_id": user_id,
        "session_token": session_token,
        "expires_at": expires_at,
        "created_at": datetime.now(timezone.utc)
    }
    await db.user_sessions.insert_one(session_doc)
    
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=True,
        samesite="none",
        path="/",
        max_age=7 * 24 * 60 * 60
    )
    
    user = await db.users.find_one({"user_id": user_id}, {"_id": 0})
    return user

@api_router.get("/auth/me")
async def get_me(user: Dict = Depends(require_auth)):
    return user

@api_router.post("/auth/logout")
async def logout(request: Request, response: Response, user: Dict = Depends(require_auth)):
    session_token = request.cookies.get("session_token")
    if session_token:
        await db.user_sessions.delete_one({"session_token": session_token})
    response.delete_cookie("session_token", path="/")
    return {"message": "Logged out successfully"}

@api_router.post("/auth/guest")
async def create_guest_session(response: Response):
    user_id = f"guest_{uuid.uuid4().hex[:12]}"
    session_token = f"guest_session_{uuid.uuid4().hex}"
    
    user_doc = {
        "user_id": user_id,
        "email": f"{user_id}@guest.local",
        "name": "Guest User",
        "is_guest": True,
        "is_admin": False,
        "created_at": datetime.now(timezone.utc)
    }
    await db.users.insert_one(user_doc)
    
    expires_at = datetime.now(timezone.utc) + timedelta(days=1)
    session_doc = {
        "user_id": user_id,
        "session_token": session_token,
        "expires_at": expires_at,
        "created_at": datetime.now(timezone.utc)
    }
    await db.user_sessions.insert_one(session_doc)
    
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=True,
        samesite="none",
        path="/",
        max_age=24 * 60 * 60
    )
    
    user = await db.users.find_one({"user_id": user_id}, {"_id": 0})
    return user

# User profile endpoints
@api_router.put("/user/onboarding")
async def update_onboarding(data: OnboardingData, user: Dict = Depends(require_auth)):
    bmi = data.weight / ((data.height / 100) ** 2)
    
    await db.users.update_one(
        {"user_id": user["user_id"]},
        {"$set": {
            "height": data.height,
            "weight": data.weight,
            "date_of_birth": data.date_of_birth,
            "age": data.age,
            "bmi": round(bmi, 2),
            "selected_sports": data.selected_sports
        }}
    )
    
    updated_user = await db.users.find_one({"user_id": user["user_id"]}, {"_id": 0})
    return updated_user

@api_router.put("/user/fitness-goal")
async def update_fitness_goal(data: FitnessGoalData, user: Dict = Depends(require_auth)):
    await db.users.update_one(
        {"user_id": user["user_id"]},
        {"$set": {
            "fitness_goal": data.fitness_goal,
            "selected_sport": data.selected_sport
        }}
    )
    
    updated_user = await db.users.find_one({"user_id": user["user_id"]}, {"_id": 0})
    return updated_user

@api_router.get("/user/profile")
async def get_user_profile(user: Dict = Depends(require_auth)):
    return user

# Workout plan endpoints
@api_router.post("/workout/generate-plan")
async def generate_workout_plan(user: Dict = Depends(require_auth)):
    import random
    
    fitness_goal = user.get("fitness_goal")
    selected_sport = user.get("selected_sport")
    
    if not fitness_goal:
        raise HTTPException(status_code=400, detail="Fitness goal not set")
    
    # Get sport-specific exercises
    sport_exercises = []
    if selected_sport:
        sport_exercises = await db.exercises.find(
            {"sport_category": selected_sport},
            {"_id": 0}
        ).to_list(1000)
    
    # Get general fitness exercises
    fitness_exercises = await db.exercises.find(
        {"sport_category": "Fitness"},
        {"_id": 0}
    ).to_list(1000)
    
    # Get hobby/easy exercises
    hobby_exercises = await db.exercises.find(
        {"sport_category": "Hobby"},
        {"_id": 0}
    ).to_list(1000)
    
    # Combine available exercises
    all_exercises = sport_exercises + fitness_exercises + hobby_exercises
    if not all_exercises:
        all_exercises = await db.exercises.find({}, {"_id": 0}).to_list(1000)
    
    if len(all_exercises) < 5:
        raise HTTPException(status_code=500, detail="Not enough exercises in database")
    
    # Generate varied daily workouts
    daily_exercises = []
    used_exercise_indices = set()
    
    for day in range(1, 46):
        day_workout = []
        
        # For sport-specific plans, include sport exercise every 4-5 days
        if sport_exercises and day % 5 == 1:
            sport_ex = random.choice(sport_exercises)
            day_workout.append(sport_ex["exercise_id"])
        
        # Fill rest with varied exercises
        available_exercises = [e for i, e in enumerate(all_exercises) if i not in used_exercise_indices]
        if len(available_exercises) < 4:
            used_exercise_indices.clear()
            available_exercises = all_exercises
        
        # Randomly select 4-5 exercises ensuring variety
        num_exercises = random.randint(4, 5)
        selected = random.sample(available_exercises, min(num_exercises, len(available_exercises)))
        
        for ex in selected:
            if ex["exercise_id"] not in day_workout:
                day_workout.append(ex["exercise_id"])
                idx = next((i for i, e in enumerate(all_exercises) if e["exercise_id"] == ex["exercise_id"]), None)
                if idx is not None:
                    used_exercise_indices.add(idx)
        
        daily_exercises.append({
            "day": day,
            "exercises": day_workout[:5]
        })
    
    plan_id = f"plan_{uuid.uuid4().hex[:12]}"
    plan_doc = {
        "plan_id": plan_id,
        "user_id": user["user_id"],
        "plan_type": fitness_goal,
        "sport": selected_sport,
        "duration_days": 45,
        "daily_exercises": daily_exercises,
        "created_at": datetime.now(timezone.utc)
    }
    await db.workout_plans.insert_one(plan_doc)
    
    await db.users.update_one(
        {"user_id": user["user_id"]},
        {"$set": {"current_plan_id": plan_id, "current_streak": 0}}
    )
    
    plan = await db.workout_plans.find_one({"plan_id": plan_id}, {"_id": 0})
    return plan

@api_router.get("/workout/current-plan")
async def get_current_plan(user: Dict = Depends(require_auth)):
    plan_id = user.get("current_plan_id")
    if not plan_id:
        return None
    
    plan = await db.workout_plans.find_one({"plan_id": plan_id}, {"_id": 0})
    return plan

@api_router.get("/workout/day/{day_number}")
async def get_day_workout(day_number: int, user: Dict = Depends(require_auth)):
    plan_id = user.get("current_plan_id")
    if not plan_id:
        raise HTTPException(status_code=404, detail="No active plan")
    
    plan = await db.workout_plans.find_one({"plan_id": plan_id}, {"_id": 0})
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    day_data = next((d for d in plan["daily_exercises"] if d["day"] == day_number), None)
    if not day_data:
        raise HTTPException(status_code=404, detail="Day not found")
    
    exercises = []
    for exercise_id in day_data["exercises"]:
        exercise = await db.exercises.find_one({"exercise_id": exercise_id}, {"_id": 0})
        if exercise:
            exercises.append(exercise)
    
    progress = await db.user_progress.find_one(
        {"user_id": user["user_id"], "plan_id": plan_id, "day_number": day_number},
        {"_id": 0}
    )
    
    return {
        "day": day_number,
        "exercises": exercises,
        "completed": progress["completed"] if progress else False
    }

@api_router.post("/workout/complete-day")
async def complete_day(day_number: int, user: Dict = Depends(require_auth)):
    plan_id = user.get("current_plan_id")
    if not plan_id:
        raise HTTPException(status_code=404, detail="No active plan")
    
    existing = await db.user_progress.find_one(
        {"user_id": user["user_id"], "plan_id": plan_id, "day_number": day_number},
        {"_id": 0}
    )
    
    if existing:
        await db.user_progress.update_one(
            {"progress_id": existing["progress_id"]},
            {"$set": {"completed": True, "completed_at": datetime.now(timezone.utc)}}
        )
    else:
        progress_id = f"progress_{uuid.uuid4().hex[:12]}"
        progress_doc = {
            "progress_id": progress_id,
            "user_id": user["user_id"],
            "plan_id": plan_id,
            "day_number": day_number,
            "completed": True,
            "completed_at": datetime.now(timezone.utc)
        }
        await db.user_progress.insert_one(progress_doc)
    
    # Update streak
    await update_user_streak(user["user_id"])
    
    # Check for new achievements
    await check_achievements(user["user_id"])
    
    return {"message": "Day completed"}

async def update_user_streak(user_id: str):
    # Get all completed days sorted by date
    progress_list = await db.user_progress.find(
        {"user_id": user_id, "completed": True},
        {"_id": 0}
    ).sort("completed_at", -1).to_list(1000)
    
    if not progress_list:
        return
    
    # Calculate current streak
    current_streak = 1
    last_date = progress_list[0]["completed_at"]
    if isinstance(last_date, str):
        last_date = datetime.fromisoformat(last_date)
    if last_date.tzinfo is None:
        last_date = last_date.replace(tzinfo=timezone.utc)
    
    for i in range(1, len(progress_list)):
        curr_date = progress_list[i]["completed_at"]
        if isinstance(curr_date, str):
            curr_date = datetime.fromisoformat(curr_date)
        if curr_date.tzinfo is None:
            curr_date = curr_date.replace(tzinfo=timezone.utc)
        
        # Check if consecutive days
        diff = (last_date.date() - curr_date.date()).days
        if diff == 1:
            current_streak += 1
            last_date = curr_date
        else:
            break
    
    # Update user's streak
    user = await db.users.find_one({"user_id": user_id}, {"_id": 0})
    longest_streak = user.get("longest_streak", 0)
    
    await db.users.update_one(
        {"user_id": user_id},
        {"$set": {
            "current_streak": current_streak,
            "longest_streak": max(current_streak, longest_streak)
        }}
    )

async def check_achievements(user_id: str):
    # Get completed days count
    completed_count = await db.user_progress.count_documents(
        {"user_id": user_id, "completed": True}
    )
    
    # Achievement milestones
    milestones = [
        {"days": 5, "name": "First Steps", "description": "Completed 5 days", "badge": "🎯"},
        {"days": 10, "name": "Momentum Builder", "description": "Completed 10 days", "badge": "💪"},
        {"days": 20, "name": "Halfway Hero", "description": "Completed 20 days", "badge": "⚡"},
        {"days": 30, "name": "Consistent Champion", "description": "Completed 30 days", "badge": "🔥"},
        {"days": 45, "name": "Peak Performance", "description": "Completed 45 days", "badge": "🏆"},
    ]
    
    # Check which achievements user has earned
    for milestone in milestones:
        if completed_count >= milestone["days"]:
            # Check if achievement already exists
            existing = await db.achievements.find_one(
                {"user_id": user_id, "name": milestone["name"]},
                {"_id": 0}
            )
            
            if not existing:
                achievement_doc = {
                    "achievement_id": f"ach_{uuid.uuid4().hex[:12]}",
                    "user_id": user_id,
                    "name": milestone["name"],
                    "description": milestone["description"],
                    "badge": milestone["badge"],
                    "days_required": milestone["days"],
                    "earned_at": datetime.now(timezone.utc)
                }
                await db.achievements.insert_one(achievement_doc)

@api_router.get("/workout/progress")
async def get_progress(user: Dict = Depends(require_auth)):
    plan_id = user.get("current_plan_id")
    if not plan_id:
        return {
            "total_days": 0,
            "completed_days": 0,
            "progress_percentage": 0,
            "current_streak": 0,
            "longest_streak": 0
        }
    
    progress_list = await db.user_progress.find(
        {"user_id": user["user_id"], "plan_id": plan_id, "completed": True},
        {"_id": 0}
    ).to_list(1000)
    
    completed_days = len(progress_list)
    total_days = 45
    progress_percentage = (completed_days / total_days) * 100
    
    return {
        "total_days": total_days,
        "completed_days": completed_days,
        "progress_percentage": round(progress_percentage, 2),
        "current_streak": user.get("current_streak", 0),
        "longest_streak": user.get("longest_streak", 0)
    }

@api_router.get("/achievements")
async def get_achievements(user: Dict = Depends(require_auth)):
    achievements = await db.achievements.find(
        {"user_id": user["user_id"]},
        {"_id": 0}
    ).to_list(1000)
    return achievements

@api_router.get("/achievements/available")
async def get_available_achievements(user: Dict = Depends(require_auth)):
    # Return all possible achievements with earned status
    completed_count = await db.user_progress.count_documents(
        {"user_id": user["user_id"], "completed": True}
    )
    
    milestones = [
        {"days": 5, "name": "First Steps", "description": "Complete 5 workout days", "badge": "🎯"},
        {"days": 10, "name": "Momentum Builder", "description": "Complete 10 workout days", "badge": "💪"},
        {"days": 20, "name": "Halfway Hero", "description": "Complete 20 workout days", "badge": "⚡"},
        {"days": 30, "name": "Consistent Champion", "description": "Complete 30 workout days", "badge": "🔥"},
        {"days": 45, "name": "Peak Performance", "description": "Complete all 45 days", "badge": "🏆"},
    ]
    
    earned_achievements = await db.achievements.find(
        {"user_id": user["user_id"]},
        {"_id": 0}
    ).to_list(1000)
    
    earned_names = {ach["name"] for ach in earned_achievements}
    
    result = []
    for milestone in milestones:
        result.append({
            **milestone,
            "earned": milestone["name"] in earned_names,
            "progress": min(completed_count, milestone["days"]),
            "earned_at": next((ach["earned_at"] for ach in earned_achievements if ach["name"] == milestone["name"]), None)
        })
    
    return result

# Exercise endpoints
@api_router.get("/exercises")
async def get_exercises(sport_category: Optional[str] = None):
    query = {"sport_category": sport_category} if sport_category else {}
    exercises = await db.exercises.find(query, {"_id": 0}).to_list(1000)
    return exercises

@api_router.get("/exercises/{exercise_id}")
async def get_exercise(exercise_id: str):
    exercise = await db.exercises.find_one({"exercise_id": exercise_id}, {"_id": 0})
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise

# AI Recommendation endpoint
@api_router.post("/ai/recommendations")
async def get_ai_recommendations(user: Dict = Depends(require_auth)):
    api_key = os.environ.get('EMERGENT_LLM_KEY')
    if not api_key:
        raise HTTPException(status_code=500, detail="AI service not configured")
    
    user_profile = f"""User Profile:
    - Name: {user.get('name', 'User')}
    - Age: {user.get('age', 'N/A')}
    - BMI: {user.get('bmi', 'N/A')}
    - Fitness Goal: {user.get('fitness_goal', 'N/A')}
    - Selected Sport: {user.get('selected_sport', 'N/A')}
    """
    
    chat = LlmChat(
        api_key=api_key,
        session_id=f"recommendations_{user['user_id']}",
        system_message="You are a fitness expert providing personalized workout recommendations. Keep responses concise and motivating."
    ).with_model("openai", "gpt-5.2")
    
    message = UserMessage(
        text=f"{user_profile}\n\nProvide 3 personalized workout tips and motivation for this user's fitness journey. Keep it under 150 words."
    )
    
    try:
        response = await chat.send_message(message)
        return {"recommendations": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")

# Admin endpoints
@api_router.get("/admin/users")
async def get_all_users(user: Dict = Depends(require_auth)):
    if not user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    users = await db.users.find({}, {"_id": 0}).to_list(1000)
    return users

@api_router.delete("/admin/users/{user_id}")
async def delete_user(user_id: str, user: Dict = Depends(require_auth)):
    if not user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    await db.users.delete_one({"user_id": user_id})
    await db.user_sessions.delete_many({"user_id": user_id})
    await db.workout_plans.delete_many({"user_id": user_id})
    await db.user_progress.delete_many({"user_id": user_id})
    
    return {"message": "User deleted"}

@api_router.get("/admin/exercises")
async def get_all_exercises_admin(user: Dict = Depends(require_auth)):
    if not user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    exercises = await db.exercises.find({}, {"_id": 0}).to_list(1000)
    return exercises

@api_router.post("/admin/exercises")
async def create_exercise(exercise: Exercise, user: Dict = Depends(require_auth)):
    if not user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    exercise_doc = exercise.model_dump()
    await db.exercises.insert_one(exercise_doc)
    return exercise

@api_router.put("/admin/exercises/{exercise_id}")
async def update_exercise(exercise_id: str, exercise: Exercise, user: Dict = Depends(require_auth)):
    if not user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    exercise_doc = exercise.model_dump()
    await db.exercises.update_one({"exercise_id": exercise_id}, {"$set": exercise_doc})
    return exercise

@api_router.delete("/admin/exercises/{exercise_id}")
async def delete_exercise(exercise_id: str, user: Dict = Depends(require_auth)):
    if not user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    await db.exercises.delete_one({"exercise_id": exercise_id})
    return {"message": "Exercise deleted"}

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()