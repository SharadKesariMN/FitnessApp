#!/usr/bin/env python3
\"\"\"
Quick Exercise GIF URL Updater
Usage: python3 quick_update_gif.py \"Exercise Name\" \"New GIF URL\"
Example: python3 quick_update_gif.py \"Standard Push-ups\" \"https://your-new-gif-url.gif\"
\"\"\"

import asyncio
import sys
import os
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv(Path('/app/backend/.env'))

async def update_single_gif(exercise_name: str, new_url: str):
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    # Check if exercise exists
    exercise = await db.exercises.find_one({\"name\": exercise_name}, {\"_id\": 0})
    
    if not exercise:
        print(f\"❌ Exercise '{exercise_name}' not found!\")
        print(\"\\nAvailable exercises:\")
        exercises = await db.exercises.find({}, {\"name\": 1, \"_id\": 0}).sort(\"name\", 1).to_list(1000)
        for ex in exercises:
            print(f\"  - {ex['name']}\")
        client.close()
        return
    
    # Update the GIF URL
    result = await db.exercises.update_one(
        {\"name\": exercise_name},
        {\"$set\": {\"gif_url\": new_url}}
    )
    
    if result.modified_count > 0:
        print(f\"✅ Successfully updated '{exercise_name}'!\")
        print(f\"   Old URL: {exercise.get('gif_url', 'None')}\")
        print(f\"   New URL: {new_url}\")
    else:
        print(f\"⚠️ No changes made (URL might be the same)\")
    
    client.close()

async def list_all_exercises():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    print(\"\\n=== All Exercises and Their GIF URLs ===\\n\")
    exercises = await db.exercises.find({}, {\"name\": 1, \"gif_url\": 1, \"_id\": 0}).sort(\"name\", 1).to_list(1000)
    
    for i, ex in enumerate(exercises, 1):
        print(f\"{i}. {ex['name']}\")
        print(f\"   {ex['gif_url']}\")
        print()
    
    client.close()

if __name__ == \"__main__\":
    if len(sys.argv) == 1 or sys.argv[1] == \"--list\":
        asyncio.run(list_all_exercises())
    elif len(sys.argv) == 3:
        exercise_name = sys.argv[1]
        new_url = sys.argv[2]
        asyncio.run(update_single_gif(exercise_name, new_url))
    else:
        print(\"Usage:\")
        print(\"  List all exercises:  python3 quick_update_gif.py --list\")
        print(\"  Update one exercise: python3 quick_update_gif.py \\\"Exercise Name\\\" \\\"New URL\\\"\")
        print()
        print(\"Example:\")
        print('  python3 quick_update_gif.py \"Standard Push-ups\" \"https://media.giphy.com/media/ABC123/giphy.gif\"')
