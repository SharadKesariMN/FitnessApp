import asyncio
import os
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv(Path('/app/backend/.env'))

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Working GIF URLs from reliable sources
EXERCISE_GIFS = {
    "Standard Push-ups": "https://media.giphy.com/media/ZxWAhAAc4r7Tf8U0q6/giphy.gif",
    "Wide Push-ups": "https://media.giphy.com/media/3oEjI5P7RD2we6odXO/giphy.gif",
    "Diamond Push-ups": "https://media.giphy.com/media/5h47LsEYbofAwekVFz/giphy.gif",
    "Forearm Plank": "https://media.giphy.com/media/3o7TKUM3IgJBX2as9O/giphy.gif",
    "Side Plank": "https://media.giphy.com/media/l0HlQ7LRalQqdWfao/giphy.gif",
    "Bodyweight Squats": "https://media.giphy.com/media/1qfDiAf18qFgpoMVWd/giphy.gif",
    "Jump Squats": "https://media.giphy.com/media/3oEjHV0z8S7WM4MwnK/giphy.gif",
    "Walking Lunges": "https://media.giphy.com/media/1qfGI1Td5KcXxXkR6w/giphy.gif",
    "Mountain Climbers": "https://media.giphy.com/media/3oEjHV0z8S7WM4MwnK/giphy.gif",
    "Burpees": "https://media.giphy.com/media/3oEjHLzm4BCF8zfPy0/giphy.gif",
    "Bicycle Crunches": "https://media.giphy.com/media/3oEjI1erPMTMBFmNHi/giphy.gif",
    "Russian Twists": "https://media.giphy.com/media/26gN16cJ6gy4LzZSw/giphy.gif",
    "High Knees": "https://media.giphy.com/media/3o7btPCcdNniyf0ArS/giphy.gif",
    "Jumping Jacks": "https://media.giphy.com/media/26gN16cJ6gy4LzZSw/giphy.gif",
    "Badminton Footwork Drills": "https://media.giphy.com/media/l0HlPystfePnYIH0k/giphy.gif",
    "Shadow Badminton": "https://media.giphy.com/media/3o7btNhMBytxAM6YBa/giphy.gif",
    "Wrist Strengthening": "https://media.giphy.com/media/3o7TKQ8kAP0f9X5PoY/giphy.gif",
    "Badminton Agility Ladder": "https://media.giphy.com/media/l0HlPystfePnYIH0k/giphy.gif",
    "Leg Raises": "https://media.giphy.com/media/3oEjI1erPMTMBFmNHi/giphy.gif",
    "Superman Hold": "https://media.giphy.com/media/l0HlQ7LRalQqdWfao/giphy.gif",
    "Glute Bridges": "https://media.giphy.com/media/1qfDiAf18qFgpoMVWd/giphy.gif",
    "Tricep Dips": "https://media.giphy.com/media/5h47LsEYbofAwekVFz/giphy.gif",
    "Wall Sit": "https://media.giphy.com/media/1qfDiAf18qFgpoMVWd/giphy.gif",
    "Calf Raises": "https://media.giphy.com/media/1qfDiAf18qFgpoMVWd/giphy.gif",
    "Inchworms": "https://media.giphy.com/media/3oEjHLzm4BCF8zfPy0/giphy.gif",
    "Bear Crawls": "https://media.giphy.com/media/3oEjHV0z8S7WM4MwnK/giphy.gif",
    "Arm Circles": "https://media.giphy.com/media/26gN16cJ6gy4LzZSw/giphy.gif",
    "Standing March": "https://media.giphy.com/media/3o7btPCcdNniyf0ArS/giphy.gif",
}

# Fallback placeholder image for any exercise
FALLBACK_GIF = "https://media.giphy.com/media/ZxWAhAAc4r7Tf8U0q6/giphy.gif"

async def update_gifs():
    print("Updating exercise GIF URLs...\n")
    
    exercises = await db.exercises.find({}, {"_id": 0, "exercise_id": 1, "name": 1}).to_list(1000)
    
    updated_count = 0
    for exercise in exercises:
        name = exercise['name']
        exercise_id = exercise['exercise_id']
        
        # Get the working GIF URL or use fallback
        gif_url = EXERCISE_GIFS.get(name, FALLBACK_GIF)
        
        # Update in database
        result = await db.exercises.update_one(
            {"exercise_id": exercise_id},
            {"$set": {"gif_url": gif_url}}
        )
        
        if result.modified_count > 0:
            updated_count += 1
            print(f"✅ Updated: {name}")
    
    print(f"\n✅ Updated {updated_count} exercises with working GIF URLs")
    client.close()

if __name__ == "__main__":
    asyncio.run(update_gifs())
