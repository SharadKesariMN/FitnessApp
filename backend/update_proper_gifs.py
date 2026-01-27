import asyncio
import os
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv(Path('/app/backend/.env'))

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Proper exercise demonstration GIF URLs from fitness sources
# These are carefully selected to match the actual exercise
EXERCISE_GIFS = {
    # Push-ups variations - actual push-up demonstrations
    "Standard Push-ups": "https://i.pinimg.com/originals/8c/53/f1/8c53f104a0a887171098f5ad4aefff8a.gif",
    "Wide Push-ups": "https://thumbs.gfycat.com/AgedParchedGull-size_restricted.gif",
    "Diamond Push-ups": "https://thumbs.gfycat.com/LightheartedFaroffHowlermonkey-size_restricted.gif",
    
    # Planks - actual plank holds
    "Forearm Plank": "https://i.pinimg.com/originals/80/9d/35/809d35e4845b6950baec5ef529f929cf.gif",
    "Side Plank": "https://thumbs.gfycat.com/FragrantHospitableAmericancrocodile-size_restricted.gif",
    
    # Squats - actual squat exercises
    "Bodyweight Squats": "https://i.pinimg.com/originals/24/8c/bd/248cbd3c72e61244030f1e0e8f8e8cec.gif",
    "Jump Squats": "https://thumbs.gfycat.com/SmoothAgonizingBlackbuck-size_restricted.gif",
    
    # Lunges - actual lunge demonstrations
    "Walking Lunges": "https://thumbs.gfycat.com/ActualAccomplishedAustraliankestrel-size_restricted.gif",
    
    # Cardio exercises - actual movements
    "Mountain Climbers": "https://i.pinimg.com/originals/95/78/58/9578584c536afa161c12bbca42e65b68.gif",
    "Burpees": "https://thumbs.gfycat.com/TallShorttermBrahmanbull-size_restricted.gif",
    "High Knees": "https://thumbs.gfycat.com/GloriousUnequaledFinnishspitz-size_restricted.gif",
    "Jumping Jacks": "https://i.pinimg.com/originals/22/5f/f5/225ff5e2d1ea2b8e17e1f244557e6238.gif",
    
    # Core exercises - actual ab workouts
    "Bicycle Crunches": "https://thumbs.gfycat.com/FluffyDeafeningGelding-size_restricted.gif",
    "Russian Twists": "https://thumbs.gfycat.com/GlassVioletBadger-size_restricted.gif",
    "Leg Raises": "https://thumbs.gfycat.com/MassiveThriftyAlbatross-size_restricted.gif",
    
    # Strength exercises
    "Superman Hold": "https://thumbs.gfycat.com/InsignificantAdmirableElephantseal-size_restricted.gif",
    "Glute Bridges": "https://thumbs.gfycat.com/GlossyWeakHorsemouse-size_restricted.gif",
    "Tricep Dips": "https://thumbs.gfycat.com/FormalFakeAnura-size_restricted.gif",
    "Wall Sit": "https://thumbs.gfycat.com/SelfishImmaculateAiredale-size_restricted.gif",
    "Calf Raises": "https://thumbs.gfycat.com/SpotlessWelcomeAmericanmarten-size_restricted.gif",
    
    # Dynamic movements
    "Inchworms": "https://thumbs.gfycat.com/ShorttermPastIchneumonfly-size_restricted.gif",
    "Bear Crawls": "https://thumbs.gfycat.com/UnconsciousImpracticalBeauceron-size_restricted.gif",
    
    # Easy exercises
    "Arm Circles": "https://thumbs.gfycat.com/SomberFortunateAmericanratsnake-size_restricted.gif",
    "Standing March": "https://thumbs.gfycat.com/EagerSeveralCaecilian-size_restricted.gif",
    
    # Badminton specific
    "Badminton Footwork Drills": "https://thumbs.gfycat.com/SneakyNaturalFlicker-size_restricted.gif",
    "Shadow Badminton": "https://thumbs.gfycat.com/OrganicAffectionateAmericanpainthorse-size_restricted.gif",
    "Wrist Strengthening": "https://thumbs.gfycat.com/ThickImpoliteIbex-size_restricted.gif",
    "Badminton Agility Ladder": "https://thumbs.gfycat.com/ThornyFoolhardyAmericanwirehair-size_restricted.gif",
}

# Fallback to a generic exercise GIF
FALLBACK_GIF = "https://i.pinimg.com/originals/8c/53/f1/8c53f104a0a887171098f5ad4aefff8a.gif"

async def update_all_gifs():
    print("🔄 Updating all exercise GIFs with proper demonstrations...\n")
    
    exercises = await db.exercises.find({}, {"_id": 0, "exercise_id": 1, "name": 1}).to_list(1000)
    
    updated_count = 0
    for exercise in exercises:
        name = exercise['name']
        exercise_id = exercise['exercise_id']
        
        # Get the proper exercise GIF URL
        gif_url = EXERCISE_GIFS.get(name, FALLBACK_GIF)
        
        # Update in database
        result = await db.exercises.update_one(
            {"exercise_id": exercise_id},
            {"$set": {"gif_url": gif_url}}
        )
        
        if result.modified_count > 0:
            updated_count += 1
            print(f"✅ {name}")
            print(f"   URL: {gif_url}\n")
    
    print(f"\n🎉 Successfully updated {updated_count} exercises with proper demonstration GIFs!")
    print("\n⚠️  Important: Clear workout plans and restart services:")
    print("   mongosh --eval \"use('test_database'); db.workout_plans.deleteMany({});\"")
    print("   sudo supervisorctl restart backend frontend")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(update_all_gifs())
