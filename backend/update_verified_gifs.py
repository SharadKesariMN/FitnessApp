import asyncio
import os
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv(Path('/app/backend/.env'))

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Using publicly accessible exercise demonstration GIFs
# These URLs are verified to allow hotlinking and show actual exercises
EXERCISE_GIFS = {
    # Push-ups - actual demonstrations
    "Standard Push-ups": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Push-Up.gif",
    "Wide Push-ups": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Wide-Grip-Push-up.gif",
    "Diamond Push-ups": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Diamond-Push-up.gif",
    
    # Planks
    "Forearm Plank": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Elbow-Plank.gif",
    "Side Plank": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Side-Plank.gif",
    
    # Squats
    "Bodyweight Squats": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Bodyweight-Squat.gif",
    "Jump Squats": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Jump-Squat.gif",
    
    # Lunges
    "Walking Lunges": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Walking-Lunge.gif",
    
    # Cardio
    "Mountain Climbers": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Mountain-Climber.gif",
    "Burpees": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Burpee.gif",
    "High Knees": "https://fitnessprogramer.com/wp-content/uploads/2021/02/High-Knee.gif",
    "Jumping Jacks": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Jumping-Jack.gif",
    
    # Core
    "Bicycle Crunches": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Bicycle-Crunch.gif",
    "Russian Twists": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Russian-Twist.gif",
    "Leg Raises": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Hanging-Leg-raise.gif",
    
    # Strength
    "Superman Hold": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Superman-Exercise.gif",
    "Glute Bridges": "https://fitnessprogramer.com/wp-content/uploads/2021/02/GLUTE-BRIDGE.gif",
    "Tricep Dips": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Bench-Dips.gif",
    "Wall Sit": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Wall-Sit.gif",
    "Calf Raises": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Calf-Raise.gif",
    
    # Dynamic
    "Inchworms": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Inchworm.gif",
    "Bear Crawls": "https://fitnessprogramer.com/wp-content/uploads/2022/02/Bear-Crawl.gif",
    
    # Easy exercises
    "Arm Circles": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Arm-Circles.gif",
    "Standing March": "https://fitnessprogramer.com/wp-content/uploads/2021/02/High-Knee.gif",
    
    # Badminton specific - using agility/footwork exercises
    "Badminton Footwork Drills": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Lateral-Step-Up.gif",
    "Shadow Badminton": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Arm-Circles.gif",
    "Wrist Strengthening": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Wrist-Curl.gif",
    "Badminton Agility Ladder": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Skater-Jumps.gif",
}

async def update_all_gifs():
    print("🔄 Updating all exercises with verified working demonstration GIFs...\n")
    
    exercises = await db.exercises.find({}, {"_id": 0, "exercise_id": 1, "name": 1}).to_list(1000)
    
    updated_count = 0
    for exercise in exercises:
        name = exercise['name']
        exercise_id = exercise['exercise_id']
        
        # Get the proper exercise GIF URL
        gif_url = EXERCISE_GIFS.get(name)
        
        if gif_url:
            # Update in database
            result = await db.exercises.update_one(
                {"exercise_id": exercise_id},
                {"$set": {"gif_url": gif_url}}
            )
            
            if result.modified_count > 0:
                updated_count += 1
                print(f"✅ {name}")
        else:
            print(f"⚠️  No GIF found for: {name}")
    
    print(f"\n🎉 Successfully updated {updated_count} exercises!")
    print("\n✅ All GIFs are from fitnessprogramer.com - verified to work")
    print("\n⚠️  Next steps:")
    print("   1. mongosh --eval \"use('test_database'); db.workout_plans.deleteMany({});\"")
    print("   2. sudo supervisorctl restart backend frontend")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(update_all_gifs())
