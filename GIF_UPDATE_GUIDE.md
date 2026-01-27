# Exercise GIF Update Guide

## Problem Identified
The exercisedb.io API URLs were returning 500 errors, preventing exercise demonstration GIFs from loading.

## Solution Implemented
✅ **All 28 exercises updated with working Giphy GIF URLs**
✅ **GIFs are now loading successfully in the workout viewer**

## Current Status
- **Total Exercises**: 28 (21 Fitness, 4 Badminton, 3 Hobby)
- **GIF Source**: Giphy (reliable, fast CDN)
- **Loading Status**: ✅ WORKING

## How to Update GIFs for Specific Exercises

### Method 1: Using the Update Script (Recommended)

1. Edit `/app/backend/update_exercise_gifs.py`
2. Update the `EXERCISE_GIFS` dictionary with new URLs:

```python
EXERCISE_GIFS = {
    "Standard Push-ups": "YOUR_NEW_GIF_URL",
    "Bodyweight Squats": "YOUR_NEW_GIF_URL",
    # ... add more
}
```

3. Run the script:
```bash
cd /app/backend
python3 update_exercise_gifs.py
```

4. Restart services:
```bash
sudo supervisorctl restart backend frontend
```

### Method 2: Direct Database Update

```bash
mongosh --eval "
use('test_database');
db.exercises.updateOne(
  {name: 'Standard Push-ups'},
  {\$set: {gif_url: 'YOUR_NEW_GIF_URL'}}
);
"
```

### Method 3: Through Admin Panel
1. Go to `/admin` page
2. Navigate to Exercises tab
3. Edit exercise and update GIF URL
4. Save changes

## Finding Good Exercise GIF URLs

### Recommended Sources:

1. **Giphy** (Currently Used)
   - Search: https://giphy.com/search/exercise
   - Right-click GIF → Copy Image Address
   - Example: `https://media.giphy.com/media/[ID]/giphy.gif`

2. **Exercise Demonstration Sites**
   - Fitness Blender: Has exercise videos
   - ACE Fitness Exercise Library
   - Muscle & Fitness

3. **Creating Custom GIFs**
   - Record exercise video
   - Convert to GIF using ezgif.com
   - Upload to Imgur or Giphy
   - Use the direct GIF URL

## Verifying GIF URLs Work

Test URL before adding:
```bash
curl -I "YOUR_GIF_URL" | grep "HTTP"
# Should return: HTTP/2 200
```

## Common Issues and Solutions

### Issue: GIF not loading after update
**Solution**: 
```bash
# Clear workout plans to force refresh
mongosh --eval "use('test_database'); db.workout_plans.deleteMany({});"
# Restart services
sudo supervisorctl restart backend frontend
```

### Issue: GIF URL changed in DB but not reflecting
**Solution**: Clear browser cache or open in incognito mode

### Issue: GIF shows but it's not the right exercise
**Solution**: Update the specific exercise in the database with correct URL

## Bulk Update All Exercises

If you want to replace all GIFs at once:

```python
# In update_exercise_gifs.py, modify the EXERCISE_GIFS dictionary
# with all 28 exercise names and their new URLs

EXERCISE_GIFS = {
    # Fitness - Core
    "Standard Push-ups": "URL_HERE",
    "Wide Push-ups": "URL_HERE",
    "Diamond Push-ups": "URL_HERE",
    "Forearm Plank": "URL_HERE",
    "Side Plank": "URL_HERE",
    
    # Fitness - Legs
    "Bodyweight Squats": "URL_HERE",
    "Jump Squats": "URL_HERE",
    "Walking Lunges": "URL_HERE",
    
    # Fitness - Cardio
    "Mountain Climbers": "URL_HERE",
    "Burpees": "URL_HERE",
    "High Knees": "URL_HERE",
    "Jumping Jacks": "URL_HERE",
    
    # Fitness - Abs
    "Bicycle Crunches": "URL_HERE",
    "Russian Twists": "URL_HERE",
    "Leg Raises": "URL_HERE",
    
    # Fitness - Other
    "Superman Hold": "URL_HERE",
    "Glute Bridges": "URL_HERE",
    "Tricep Dips": "URL_HERE",
    "Wall Sit": "URL_HERE",
    "Calf Raises": "URL_HERE",
    "Inchworms": "URL_HERE",
    "Bear Crawls": "URL_HERE",
    
    # Hobby
    "Arm Circles": "URL_HERE",
    "Standing March": "URL_HERE",
    
    # Badminton
    "Badminton Footwork Drills": "URL_HERE",
    "Shadow Badminton": "URL_HERE",
    "Wrist Strengthening": "URL_HERE",
    "Badminton Agility Ladder": "URL_HERE",
}
```

## Notes
- Always use direct GIF URLs (ending in .gif)
- Avoid URLs that require authentication
- Test URLs in browser before adding
- GIF file size should be reasonable (<5MB for fast loading)
- Prefer square or 16:9 aspect ratio GIFs

## Current GIF URLs (Reference)
All exercises currently use Giphy URLs. Check the database for current URLs:
```bash
mongosh --eval "use('test_database'); db.exercises.find({}, {name: 1, gif_url: 1, _id: 0}).pretty();"
```
