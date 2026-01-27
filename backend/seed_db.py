import asyncio
import sys
import os
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import uuid

load_dotenv(Path(__file__).parent / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

EXERCISES_DATA = [
    # Badminton Exercises
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Footwork Drills",
        "description": "Enhance your court movement with quick footwork patterns",
        "duration_minutes": 10,
        "gif_url": "https://media.giphy.com/media/l0HlPystfePnYIH0k/giphy.gif",
        "sport_category": "Badminton",
        "difficulty": "Intermediate",
        "instructions": [
            "Start in a ready position at the center of the court",
            "Move quickly to each corner using small, rapid steps",
            "Return to center after each corner movement",
            "Repeat for 30 seconds, rest 15 seconds",
            "Complete 4 sets"
        ]
    },
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Shadow Badminton",
        "description": "Practice strokes without a shuttlecock to build muscle memory",
        "duration_minutes": 8,
        "gif_url": "https://media.giphy.com/media/3o7btNhMBytxAM6YBa/giphy.gif",
        "sport_category": "Badminton",
        "difficulty": "Beginner",
        "instructions": [
            "Stand in playing position",
            "Execute overhead smashes without shuttlecock",
            "Practice forehand and backhand clears",
            "Focus on proper form and follow-through",
            "Continue for 8 minutes"
        ]
    },
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Wrist Strengthening",
        "description": "Build wrist power for stronger smashes",
        "duration_minutes": 6,
        "gif_url": "https://media.giphy.com/media/3o7TKQ8kAP0f9X5PoY/giphy.gif",
        "sport_category": "Badminton",
        "difficulty": "Beginner",
        "instructions": [
            "Hold your arm straight out",
            "Rotate wrist in circular motions",
            "Perform wrist curls up and down",
            "Do 15 reps clockwise, 15 counter-clockwise",
            "Repeat with both wrists"
        ]
    },
    # Athletics Exercises
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "High Knees",
        "description": "Build explosive power and improve running form",
        "duration_minutes": 5,
        "gif_url": "https://media.giphy.com/media/3o7btPCcdNniyf0ArS/giphy.gif",
        "sport_category": "Athletics",
        "difficulty": "Intermediate",
        "instructions": [
            "Stand with feet hip-width apart",
            "Drive one knee up toward chest",
            "Alternate legs in rapid succession",
            "Keep torso upright and core engaged",
            "Perform for 30 seconds, rest 15 seconds, repeat 5 times"
        ]
    },
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Agility Ladder",
        "description": "Improve coordination and foot speed",
        "duration_minutes": 8,
        "gif_url": "https://media.giphy.com/media/l0HlQ7LRalQqdWfao/giphy.gif",
        "sport_category": "Athletics",
        "difficulty": "Intermediate",
        "instructions": [
            "Set up imaginary ladder on ground (or use tape)",
            "Step in each square with both feet",
            "Progress to lateral movements",
            "Try one-foot hops through squares",
            "Complete 3 sets of each pattern"
        ]
    },
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Plyometric Bounds",
        "description": "Develop explosive leg power",
        "duration_minutes": 7,
        "gif_url": "https://media.giphy.com/media/3o7TKo6DqSW4xkz3W0/giphy.gif",
        "sport_category": "Athletics",
        "difficulty": "Advanced",
        "instructions": [
            "Start with feet together",
            "Jump forward as far as possible",
            "Land softly and immediately bound forward again",
            "Use arms to generate momentum",
            "Complete 10 bounds, rest 1 minute, repeat 3 times"
        ]
    },
    # Basketball Exercises
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Defensive Slides",
        "description": "Build lateral quickness and defensive stance",
        "duration_minutes": 6,
        "gif_url": "https://media.giphy.com/media/l0HlHJGHe3yAMhdQY/giphy.gif",
        "sport_category": "Basketball",
        "difficulty": "Intermediate",
        "instructions": [
            "Get into defensive stance (knees bent, back straight)",
            "Slide laterally without crossing feet",
            "Keep weight on balls of feet",
            "Slide for 10 seconds right, 10 seconds left",
            "Repeat for 6 minutes"
        ]
    },
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Jump Training",
        "description": "Increase vertical leap and explosive power",
        "duration_minutes": 8,
        "gif_url": "https://media.giphy.com/media/3o7TKMeCOV3oXSb5bq/giphy.gif",
        "sport_category": "Basketball",
        "difficulty": "Advanced",
        "instructions": [
            "Stand with feet shoulder-width apart",
            "Squat down and explode upward",
            "Reach as high as possible",
            "Land softly with bent knees",
            "Do 15 jumps, rest 30 seconds, repeat 4 sets"
        ]
    },
    # Fitness/Hobby Exercises
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Bodyweight Squats",
        "description": "Build leg strength and core stability",
        "duration_minutes": 5,
        "gif_url": "https://media.giphy.com/media/1qfDiAf18qFgpoMVWd/giphy.gif",
        "sport_category": "Fitness",
        "difficulty": "Beginner",
        "instructions": [
            "Stand with feet shoulder-width apart",
            "Lower body by bending knees and hips",
            "Keep chest up and core tight",
            "Push through heels to return to start",
            "Complete 3 sets of 15 reps"
        ]
    },
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Push-ups",
        "description": "Upper body strength and core endurance",
        "duration_minutes": 5,
        "gif_url": "https://media.giphy.com/media/3oEjI5P7RD2we6odXO/giphy.gif",
        "sport_category": "Fitness",
        "difficulty": "Beginner",
        "instructions": [
            "Start in plank position, hands shoulder-width apart",
            "Lower chest toward ground",
            "Keep elbows close to body",
            "Push back up to starting position",
            "Do 3 sets of 10-15 reps"
        ]
    },
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Plank Hold",
        "description": "Core strength and stability",
        "duration_minutes": 5,
        "gif_url": "https://media.giphy.com/media/3o7TKqm1mNujcBPSpy/giphy.gif",
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
        "name": "Jumping Jacks",
        "description": "Full body cardio warm-up",
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
        "name": "Mountain Climbers",
        "description": "Dynamic full body movement",
        "duration_minutes": 6,
        "gif_url": "https://media.giphy.com/media/3oEjHV0z8S7WM4MwnK/giphy.gif",
        "sport_category": "Fitness",
        "difficulty": "Intermediate",
        "instructions": [
            "Start in plank position",
            "Drive right knee toward chest",
            "Quickly switch legs",
            "Maintain steady pace",
            "Continue for 30 seconds, rest 15 seconds, repeat 6 times"
        ]
    },
    # Soccer/Running exercises
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Burpees",
        "description": "Total body conditioning",
        "duration_minutes": 7,
        "gif_url": "https://media.giphy.com/media/3oEjHLzm4BCF8zfPy0/giphy.gif",
        "sport_category": "Soccer",
        "difficulty": "Advanced",
        "instructions": [
            "Start standing, drop to squat position",
            "Place hands on ground and kick feet back",
            "Do a push-up",
            "Jump feet back to squat, then jump up",
            "Complete 3 sets of 10 reps"
        ]
    },
    {
        "exercise_id": f"ex_{uuid.uuid4().hex[:12]}",
        "name": "Lunges",
        "description": "Leg strength and balance",
        "duration_minutes": 6,
        "gif_url": "https://media.giphy.com/media/1qfGI1Td5KcXxXkR6w/giphy.gif",
        "sport_category": "Running",
        "difficulty": "Beginner",
        "instructions": [
            "Stand with feet hip-width apart",
            "Step forward with right leg",
            "Lower hips until both knees bent at 90 degrees",
            "Push back to start position",
            "Alternate legs for 3 sets of 12 reps each leg"
        ]
    },
]

async def seed_exercises():
    # Clear existing exercises
    await db.exercises.delete_many({})
    
    # Insert new exercises
    if EXERCISES_DATA:
        await db.exercises.insert_many(EXERCISES_DATA)
        print(f"✅ Seeded {len(EXERCISES_DATA)} exercises")
    
    # Create an admin user if none exists
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
        print("✅ Created admin user (email: admin@fitandflex.com)")
    
    print("\n🎉 Database seeding completed!")
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_exercises())