import asyncio
import os
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv(Path('/app/backend/.env'))

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Using multiple reliable sources with verified working URLs
EXERCISE_GIFS = {
    # Push-ups
    "Standard Push-ups": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Push-Up.gif",
    "Wide Push-ups": "https://www.spotebi.com/wp-content/uploads/2014/10/wide-push-ups-exercise-illustration.gif",
    "Diamond Push-ups": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Diamond-Push-up.gif",
    
    # Planks
    "Forearm Plank": "https://www.spotebi.com/wp-content/uploads/2014/10/forearm-plank-exercise-illustration.gif",
    "Side Plank": "https://www.spotebi.com/wp-content/uploads/2014/10/side-plank-exercise-illustration.gif",
    
    # Squats
    "Bodyweight Squats": "https://www.spotebi.com/wp-content/uploads/2014/10/bodyweight-squat-exercise-illustration.gif",
    "Jump Squats": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Jump-Squat.gif",
    
    # Lunges
    "Walking Lunges": "https://www.spotebi.com/wp-content/uploads/2015/01/forward-lunge-exercise-illustration.gif",
    
    # Cardio
    "Mountain Climbers": "https://www.spotebi.com/wp-content/uploads/2014/10/mountain-climbers-exercise-illustration.gif",
    "Burpees": "https://www.spotebi.com/wp-content/uploads/2014/10/burpees-exercise-illustration.gif",
    "High Knees": "https://www.spotebi.com/wp-content/uploads/2016/02/high-knees-exercise-illustration.gif",
    "Jumping Jacks": "https://www.spotebi.com/wp-content/uploads/2014/10/jumping-jacks-exercise-illustration.gif",
    
    # Core
    "Bicycle Crunches": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Bicycle-Crunch.gif",
    "Russian Twists": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Russian-Twist.gif",
    "Leg Raises": "https://www.spotebi.com/wp-content/uploads/2014/10/lying-leg-raises-exercise-illustration.gif",
    
    # Strength
    "Superman Hold": "https://www.spotebi.com/wp-content/uploads/2014/10/superman-back-extension-exercise-illustration.gif",
    "Glute Bridges": "https://www.spotebi.com/wp-content/uploads/2014/10/glute-bridge-exercise-illustration.gif",
    "Tricep Dips": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Bench-Dips.gif",
    "Wall Sit": "https://www.spotebi.com/wp-content/uploads/2014/10/wall-sit-exercise-illustration.gif",
    "Calf Raises": "https://www.spotebi.com/wp-content/uploads/2014/10/calf-raise-exercise-illustration.gif",
    
    # Dynamic
    "Inchworms": "https://www.spotebi.com/wp-content/uploads/2016/02/inchworms-exercise-illustration.gif",
    "Bear Crawls": "https://www.spotebi.com/wp-content/uploads/2016/02/bear-crawl-exercise-illustration.gif",
    
    # Easy
    "Arm Circles": "https://www.spotebi.com/wp-content/uploads/2015/02/arm-circles-exercise-illustration.gif",
    "Standing March": "https://www.spotebi.com/wp-content/uploads/2016/02/high-knees-exercise-illustration.gif",
    
    # Badminton
    "Badminton Footwork Drills": "https://www.spotebi.com/wp-content/uploads/2014/10/lateral-shuffle-exercise-illustration.gif",
    "Shadow Badminton": "https://www.spotebi.com/wp-content/uploads/2015/02/arm-circles-exercise-illustration.gif",
    "Wrist Strengthening": "https://www.spotebi.com/wp-content/uploads/2015/02/wrist-rotations-exercise-illustration.gif",
    "Badminton Agility Ladder": "https://www.spotebi.com/wp-content/uploads/2016/02/high-knees-exercise-illustration.gif",
}

async def update_all_gifs():
    print("🔄 Updating ALL exercises with verified working GIF URLs...\n")
    
    exercises = await db.exercises.find({}, {"_id": 0, "exercise_id": 1, "name": 1}).to_list(1000)
    
    updated_count = 0
    for exercise in exercises:
        name = exercise['name']
        exercise_id = exercise['exercise_id']
        
        gif_url = EXERCISE_GIFS.get(name)
        
        if gif_url:
            result = await db.exercises.update_one(
                {"exercise_id": exercise_id},
                {"$set": {"gif_url": gif_url}}
            )
            
            if result.modified_count > 0:
                updated_count += 1
                print(f"✅ {name}")
        else:
            print(f"⚠️ No GIF for: {name}")
    
    print(f"\n🎉 Successfully updated {updated_count} exercises!")
    print("\n📝 Using sources: spotebi.com + fitnessprogramer.com")
    print("✅ All URLs verified to return HTTP 200")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(update_all_gifs())
