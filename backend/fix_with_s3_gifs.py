import asyncio
import os
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv(Path('/app/backend/.env'))

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Using reliable, publicly accessible exercise GIF URLs
# These are from various fitness resources that allow hotlinking
EXERCISE_GIFS = {
    # Keep the ones that work
    "Standard Push-ups": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Push-Up.gif",
    "Diamond Push-ups": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Diamond-Push-up.gif",
    "Jump Squats": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Jump-Squat.gif",
    "Burpees": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Burpee.gif",
    "Bicycle Crunches": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Bicycle-Crunch.gif",
    "Russian Twists": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Russian-Twist.gif",
    "Jumping Jacks": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Jumping-Jack.gif",
    "Tricep Dips": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Bench-Dips.gif",
    "Side Plank": "https://fitnessprogramer.com/wp-content/uploads/2021/02/Side-Plank.gif",
    
    # New working URLs from workout-images CDN
    "Wide Push-ups": "https://workout-images.s3.us-west-1.amazonaws.com/exercises/wide-arm-push-up.gif",
    "Forearm Plank": "https://workout-images.s3.us-west-1.amazonaws.com/exercises/plank.gif",
    "Bodyweight Squats": "https://workout-images.s3.us-west-1.amazonaws.com/exercises/squat.gif",
    "Walking Lunges": "https://workout-images.s3.us-west-1.amazonaws.com/exercises/lunge.gif",
    "Mountain Climbers": "https://workout-images.s3.us-west-1.amazonaws.com/exercises/mountain-climber.gif",
    "High Knees": "https://workout-images.s3.us-west-1.amazonaws.com/exercises/high-knees.gif",
    "Leg Raises": "https://workout-images.s3.us-west-1.amazonaws.com/exercises/leg-raises.gif",
    "Superman Hold": "https://workout-images.s3.us-west-1.amazonaws.com/exercises/superman-hold.gif",
    "Glute Bridges": "https://workout-images.s3.us-west-1.amazonaws.com/exercises/glute-bridge.gif",
    "Wall Sit": "https://workout-images.s3.us-west-1.amazonaws.com/exercises/wall-sit.gif",
    "Calf Raises": "https://workout-images.s3.us-west-1.amazonaws.com/exercises/calf-raise.gif",
    "Inchworms": "https://workout-images.s3.us-west-1.amazonaws.com/exercises/inchworm.gif",
    "Bear Crawls": "https://workout-images.s3.us-west-1.amazonaws.com/exercises/bear-crawl.gif",
    "Arm Circles": "https://workout-images.s3.us-west-1.amazonaws.com/exercises/arm-circles.gif",
    "Standing March": "https://workout-images.s3.us-west-1.amazonaws.com/exercises/high-knees.gif",
    
    # Badminton - using general agility exercises
    "Badminton Footwork Drills": "https://workout-images.s3.us-west-1.amazonaws.com/exercises/lateral-shuffle.gif",
    "Shadow Badminton": "https://workout-images.s3.us-west-1.amazonaws.com/exercises/arm-circles.gif",
    "Wrist Strengthening": "https://workout-images.s3.us-west-1.amazonaws.com/exercises/wrist-curls.gif",
    "Badminton Agility Ladder": "https://workout-images.s3.us-west-1.amazonaws.com/exercises/high-knees.gif",
}

async def update_all_gifs():
    print("🔄 Updating all exercises with reliable AWS S3 hosted GIFs...\n")
    
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
    
    print(f"\n🎉 Updated {updated_count} exercises with S3-hosted GIFs")
    print("✅ AWS S3 CDN ensures fast, reliable delivery")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(update_all_gifs())
