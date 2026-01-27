import asyncio
import sys
import os
from pathlib import Path
import random
sys.path.append(str(Path(__file__).parent))

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import uuid

load_dotenv(Path(__file__).parent / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Comprehensive exercise library with real Giphy GIF URLs
EXERCISES_DATA = [
    # Core/General Fitness Exercises
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Push-ups",
        "description": "Classic upper body strength builder",
        "duration_minutes": 5,
        "gif_url": "https://media.giphy.com/media/ZxWAhAAc4r7Tf8U0q6/giphy.gif",
        "sport_category": "Fitness",
        "difficulty": "Beginner",
        "instructions": [
            "Start in plank position with hands shoulder-width apart",
            "Lower your chest to the ground, keeping elbows at 45 degrees",
            "Push back up to starting position",
            "Keep core engaged throughout",
            "Do 3 sets of 10-15 reps"
        ]
    },
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Plank Hold",
        "description": "Core strength and stability exercise",
        "duration_minutes": 5,
        "gif_url": "https://media.giphy.com/media/3o7TKUM3IgJBX2as9O/giphy.gif",
        "sport_category": "Fitness",
        "difficulty": "Beginner",
        "instructions": [
            "Start in forearm plank position",
            "Keep body in straight line from head to heels",
            "Engage core and squeeze glutes",
            "Hold for 30-60 seconds",
            "Rest 30 seconds, repeat 3 times"
        ]
    },
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Bodyweight Squats",
        "description": "Fundamental leg strength exercise",
        "duration_minutes": 6,
        "gif_url": "https://media.giphy.com/media/1qfDiAf18qFgpoMVWd/giphy.gif",
        "sport_category": "Fitness",
        "difficulty": "Beginner",
        "instructions": [
            "Stand with feet shoulder-width apart",
            "Lower body by bending knees and hips",
            "Keep chest up and weight on heels",
            "Go as low as comfortable",
            "Complete 3 sets of 15-20 reps"
        ]
    },
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Mountain Climbers",
        "description": "Dynamic cardio and core workout",
        "duration_minutes": 5,
        "gif_url": "https://media.giphy.com/media/3oEjHV0z8S7WM4MwnK/giphy.gif",
        "sport_category": "Fitness",
        "difficulty": "Intermediate",
        "instructions": [
            "Start in high plank position",
            "Drive right knee toward chest",
            "Quickly switch legs like running",
            "Keep hips level throughout",
            "Continue for 30 seconds, rest 15 seconds, repeat 5 times"
        ]
    },
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Burpees",
        "description": "Full body explosive movement",
        "duration_minutes": 6,
        "gif_url": "https://giphy.com/gifs/CROSSFITBORAN-KxuGSIZU1QZfRiRx4h",
        "sport_category": "Fitness",
        "difficulty": "Advanced",
        "instructions": [
            "Start standing, drop into squat",
            "Place hands down and jump feet back to plank",
            "Perform a push-up",
            "Jump feet back to squat and explode upward",
            "Complete 3 sets of 10 reps"
        ]
    },
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Lunges",
        "description": "Single-leg strength and balance",
        "duration_minutes": 6,
        "gif_url": "https://media.giphy.com/media/1qfGI1Td5KcXxXkR6w/giphy.gif",
        "sport_category": "Fitness",
        "difficulty": "Beginner",
        "instructions": [
            "Stand with feet hip-width apart",
            "Step forward with one leg",
            "Lower hips until both knees are at 90 degrees",
            "Push through front heel to return",
            "Alternate legs for 3 sets of 12 reps each"
        ]
    },
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Jumping Jacks",
        "description": "Classic cardio warm-up",
        "duration_minutes": 5,
        "gif_url": "https://media.giphy.com/media/26gN16cJ6gy4LzZSw/giphy.gif",
        "sport_category": "Hobby",
        "difficulty": "Beginner",
        "instructions": [
            "Start with feet together, arms at sides",
            "Jump feet apart while raising arms overhead",
            "Jump back to starting position",
            "Maintain steady rhythm",
            "Continue for 5 minutes"
        ]
    },
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "High Knees",
        "description": "Cardio and leg power exercise",
        "duration_minutes": 5,
        "gif_url": "https://media.giphy.com/media/3o7btPCcdNniyf0ArS/giphy.gif",
        "sport_category": "Fitness",
        "difficulty": "Intermediate",
        "instructions": [
            "Stand with feet hip-width apart",
            "Drive one knee up toward chest",
            "Alternate legs rapidly",
            "Pump arms for momentum",
            "Perform for 30 seconds, rest 15 seconds, repeat 5 times"
        ]
    },
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Bicycle Crunches",
        "description": "Core rotation and strength",
        "duration_minutes": 5,
        "gif_url": "https://media.giphy.com/media/3oEjI1erPMTMBFmNHi/giphy.gif",
        "sport_category": "Fitness",
        "difficulty": "Intermediate",
        "instructions": [
            "Lie on back with hands behind head",
            "Lift shoulders and legs off ground",
            "Bring right elbow to left knee",
            "Switch sides in cycling motion",
            "Complete 3 sets of 20 reps"
        ]
    },
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Side Plank",
        "description": "Oblique and lateral core strength",
        "duration_minutes": 5,
        "gif_url": "https://media.giphy.com/media/l0HlQ7LRalQqdWfao/giphy.gif",
        "sport_category": "Fitness",
        "difficulty": "Intermediate",
        "instructions": [
            "Lie on side with forearm on ground",
            "Stack feet and lift hips off ground",
            "Keep body in straight line",
            "Hold for 30 seconds each side",
            "Repeat 3 times per side"
        ]
    },
    
    # Badminton Exercises
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Badminton Footwork Drills",
        "description": "Court movement patterns for badminton",
        "duration_minutes": 8,
        "gif_url": "https://media.giphy.com/media/l0HlPystfePnYIH0k/giphy.gif",
        "sport_category": "Badminton",
        "difficulty": "Intermediate",
        "instructions": [
            "Start in ready position at center",
            "Move quickly to each corner with small steps",
            "Touch the corner and return to center",
            "Practice all four corners",
            "Complete 4 sets of full rotations"
        ]
    },
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Shadow Badminton Strokes",
        "description": "Practice strokes without shuttlecock",
        "duration_minutes": 7,
        "gif_url": "https://media.giphy.com/media/3o7btNhMBytxAM6YBa/giphy.gif",
        "sport_category": "Badminton",
        "difficulty": "Beginner",
        "instructions": [
            "Stand in playing stance",
            "Execute overhead smashes",
            "Practice forehand and backhand clears",
            "Focus on proper form",
            "Continue for 7 minutes"
        ]
    },
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Wrist Strengthening for Badminton",
        "description": "Build wrist power for smashes",
        "duration_minutes": 5,
        "gif_url": "https://media.giphy.com/media/3o7TKQ8kAP0f9X5PoY/giphy.gif",
        "sport_category": "Badminton",
        "difficulty": "Beginner",
        "instructions": [
            "Hold arm straight out",
            "Rotate wrist in circles",
            "Perform wrist curls up and down",
            "Do 15 reps clockwise, 15 counter-clockwise",
            "Repeat with both wrists"
        ]
    },
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Badminton Jump Training",
        "description": "Explosive power for smashes",
        "duration_minutes": 6,
        "gif_url": "https://media.giphy.com/media/3o7TKMeCOV3oXSb5bq/giphy.gif",
        "sport_category": "Badminton",
        "difficulty": "Advanced",
        "instructions": [
            "Stand with feet shoulder-width apart",
            "Squat down and jump explosively",
            "Reach overhead like smashing",
            "Land softly and repeat",
            "Complete 3 sets of 12 jumps"
        ]
    },
    
    # Athletics Exercises
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Sprint Drills",
        "description": "Speed and acceleration training",
        "duration_minutes": 8,
        "gif_url": "https://media.giphy.com/media/l0HlQ7LRalQqdWfao/giphy.gif",
        "sport_category": "Athletics",
        "difficulty": "Intermediate",
        "instructions": [
            "Mark a 20-meter distance",
            "Start from standing position",
            "Sprint at maximum speed",
            "Walk back as recovery",
            "Complete 8 sprints"
        ]
    },
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Agility Cone Drills",
        "description": "Quick direction changes",
        "duration_minutes": 7,
        "gif_url": "https://media.giphy.com/media/l0HlPystfePnYIH0k/giphy.gif",
        "sport_category": "Athletics",
        "difficulty": "Intermediate",
        "instructions": [
            "Set up cones in zigzag pattern",
            "Sprint between cones",
            "Focus on quick cuts",
            "Keep low center of gravity",
            "Complete 6 rounds"
        ]
    },
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Plyometric Box Jumps",
        "description": "Explosive leg power",
        "duration_minutes": 6,
        "gif_url": "https://media.giphy.com/media/3o7TKo6DqSW4xkz3W0/giphy.gif",
        "sport_category": "Athletics",
        "difficulty": "Advanced",
        "instructions": [
            "Stand facing a step or box",
            "Jump onto box with both feet",
            "Land softly in squat position",
            "Step down and repeat",
            "Complete 3 sets of 10 jumps"
        ]
    },
    
    # Basketball Exercises
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Defensive Slide Drills",
        "description": "Lateral movement for defense",
        "duration_minutes": 6,
        "gif_url": "https://media.giphy.com/media/l0HlHJGHe3yAMhdQY/giphy.gif",
        "sport_category": "Basketball",
        "difficulty": "Intermediate",
        "instructions": [
            "Get into defensive stance",
            "Slide laterally without crossing feet",
            "Keep weight on balls of feet",
            "Slide right for 5 meters, then left",
            "Continue for 6 minutes"
        ]
    },
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Vertical Jump Training",
        "description": "Explosive jumping power",
        "duration_minutes": 7,
        "gif_url": "https://media.giphy.com/media/3o7TKMeCOV3oXSb5bq/giphy.gif",
        "sport_category": "Basketball",
        "difficulty": "Advanced",
        "instructions": [
            "Stand with feet shoulder-width",
            "Squat and explode upward",
            "Reach as high as possible",
            "Land with bent knees",
            "Do 4 sets of 10 jumps"
        ]
    },
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Basketball Endurance Sprints",
        "description": "Court conditioning",
        "duration_minutes": 8,
        "gif_url": "https://media.giphy.com/media/l0HlQ7LRalQqdWfao/giphy.gif",
        "sport_category": "Basketball",
        "difficulty": "Intermediate",
        "instructions": [
            "Sprint baseline to baseline",
            "Touch the line each time",
            "Perform suicide runs",
            "Rest 30 seconds between sets",
            "Complete 5 rounds"
        ]
    },
    
    # Soccer Exercises
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Soccer Conditioning Runs",
        "description": "Build match fitness",
        "duration_minutes": 10,
        "gif_url": "https://media.giphy.com/media/l0HlQ7LRalQqdWfao/giphy.gif",
        "sport_category": "Soccer",
        "difficulty": "Intermediate",
        "instructions": [
            "Jog for 2 minutes",
            "Sprint for 30 seconds",
            "Walk for 1 minute",
            "Repeat cycle",
            "Continue for 10 minutes"
        ]
    },
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Soccer Agility Training",
        "description": "Quick feet and direction changes",
        "duration_minutes": 7,
        "gif_url": "https://media.giphy.com/media/l0HlPystfePnYIH0k/giphy.gif",
        "sport_category": "Soccer",
        "difficulty": "Intermediate",
        "instructions": [
            "Set up cones in a line",
            "Weave through cones quickly",
            "Use both inside and outside of feet",
            "Focus on ball control",
            "Complete 8 rounds"
        ]
    },
    
    # Running Exercises
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Hill Climbing Runs",
        "description": "Build leg power and endurance",
        "duration_minutes": 10,
        "gif_url": "https://media.giphy.com/media/l0HlQ7LRalQqdWfao/giphy.gif",
        "sport_category": "Running",
        "difficulty": "Advanced",
        "instructions": [
            "Find a hill or stairs",
            "Sprint up the incline",
            "Focus on driving knees up",
            "Walk down for recovery",
            "Complete 6-8 hill repeats"
        ]
    },
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Interval Running",
        "description": "Speed and endurance training",
        "duration_minutes": 12,
        "gif_url": "https://media.giphy.com/media/l0HlQ7LRalQqdWfao/giphy.gif",
        "sport_category": "Running",
        "difficulty": "Intermediate",
        "instructions": [
            "Warm up with 3 minutes easy jog",
            "Sprint hard for 1 minute",
            "Recover with 2 minutes easy jog",
            "Repeat sprint-recovery cycle",
            "Complete 4 intervals"
        ]
    },
    
    # Swimming/Cycling Cross-training
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Swimming Dry-Land Training",
        "description": "Shoulder and core for swimming",
        "duration_minutes": 8,
        "gif_url": "https://media.giphy.com/media/3o7btPCcdNniyf0ArS/giphy.gif",
        "sport_category": "Swimming",
        "difficulty": "Intermediate",
        "instructions": [
            "Perform arm circles forward and back",
            "Do Superman holds on ground",
            "Practice flutter kicks on stomach",
            "Add resistance band pulls",
            "Complete 3 sets of each"
        ]
    },
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Cycling Leg Conditioning",
        "description": "Build cycling-specific strength",
        "duration_minutes": 9,
        "gif_url": "https://media.giphy.com/media/1qfDiAf18qFgpoMVWd/giphy.gif",
        "sport_category": "Cycling",
        "difficulty": "Intermediate",
        "instructions": [
            "Perform single-leg squats",
            "Add jump squats for power",
            "Do wall sits for endurance",
            "Include calf raises",
            "Complete 3 sets of each exercise"
        ]
    },
    
    # Tennis Exercises
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Tennis Footwork Patterns",
        "description": "Court coverage and positioning",
        "duration_minutes": 7,
        "gif_url": "https://media.giphy.com/media/l0HlPystfePnYIH0k/giphy.gif",
        "sport_category": "Tennis",
        "difficulty": "Intermediate",
        "instructions": [
            "Practice split-step positioning",
            "Move laterally along baseline",
            "Sprint to net and back",
            "Work on quick recovery steps",
            "Continue for 7 minutes"
        ]
    },
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Tennis Shadow Swings",
        "description": "Stroke mechanics without ball",
        "duration_minutes": 6,
        "gif_url": "https://media.giphy.com/media/3o7btNhMBytxAM6YBa/giphy.gif",
        "sport_category": "Tennis",
        "difficulty": "Beginner",
        "instructions": [
            "Practice forehand swing motion",
            "Work on backhand technique",
            "Perform overhead serve motion",
            "Focus on proper form",
            "Complete 50 swings of each type"
        ]
    },
    
    # Volleyball Exercises
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Volleyball Jump Sets",
        "description": "Vertical power for blocking and spiking",
        "duration_minutes": 7,
        "gif_url": "https://media.giphy.com/media/3o7TKMeCOV3oXSb5bq/giphy.gif",
        "sport_category": "Volleyball",
        "difficulty": "Advanced",
        "instructions": [
            "Stand with feet shoulder-width apart",
            "Jump reaching overhead",
            "Land softly and immediately jump again",
            "Maintain quick tempo",
            "Complete 4 sets of 15 jumps"
        ]
    },
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Volleyball Lateral Shuffles",
        "description": "Court coverage and positioning",
        "duration_minutes": 6,
        "gif_url": "https://media.giphy.com/media/l0HlHJGHe3yAMhdQY/giphy.gif",
        "sport_category": "Volleyball",
        "difficulty": "Intermediate",
        "instructions": [
            "Get into ready position",
            "Shuffle laterally along net",
            "Keep hands up and ready",
            "Don't cross feet",
            "Continue for 6 minutes"
        ]
    },
    
    # Cricket Exercises
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Cricket Batting Practice",
        "description": "Shadow batting for technique",
        "duration_minutes": 8,
        "gif_url": "https://media.giphy.com/media/3o7btNhMBytxAM6YBa/giphy.gif",
        "sport_category": "Cricket",
        "difficulty": "Beginner",
        "instructions": [
            "Hold imaginary bat in stance",
            "Practice forward defense",
            "Work on pull shots",
            "Execute cover drives",
            "Repeat each shot 20 times"
        ]
    },
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Cricket Fielding Drills",
        "description": "Quick reflexes and agility",
        "duration_minutes": 7,
        "gif_url": "https://media.giphy.com/media/l0HlPystfePnYIH0k/giphy.gif",
        "sport_category": "Cricket",
        "difficulty": "Intermediate",
        "instructions": [
            "Practice quick ground pickups",
            "Work on diving movements",
            "Sprint and slide stops",
            "Quick throw motions",
            "Complete 20 reps of each"
        ]
    },
]

async def seed_exercises():
    await db.exercises.delete_many({})
    
    if EXERCISES_DATA:
        await db.exercises.insert_many(EXERCISES_DATA)
        print(f"✅ Seeded {len(EXERCISES_DATA)} exercises")
    
    # Ensure admin user exists
    admin_user = await db.users.find_one({"is_admin": True})
    if not admin_user:
        admin_doc = {
            "user_id": f"admin_{uuid.uuid4().hex[:12]}",
            "email": "admin@fitandflex.com",
            "name": "Admin User",
            "is_admin": True,
            "is_guest": False,
        }
        await db.users.insert_one(admin_doc)
        print("✅ Created admin user")
    
    print("\n🎉 Database seeding completed!")
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_exercises())