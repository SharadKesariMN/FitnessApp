# Fit & Flex - Complete Setup Guide

## ✅ Recent Updates Implemented

### 1. Email/Password Authentication
✅ **Sign Up for Free** - Create account with name, email, password
✅ **Sign In** - Login with email/password OR Google OAuth
✅ **Landing page updated** - Three buttons: Sign In, Sign Up for Free, Try as Guest

### 2. Increased Workout Duration  
✅ **6-7 exercises per day** (was 5)
✅ **35-45 minutes total** (was 25-30 minutes)
✅ **Same 20% sport + 80% general ratio maintained**

### 3. Admin Access Configured
✅ **Admin user created**
✅ **Full CRUD operations** for users and exercises
✅ **Progress monitoring** capabilities

---

## 🔐 Admin Login Credentials

**Email:** admin@fitandflex.com  
**Password:** admin123

### How to Access Admin Panel:

1. **Go to Sign In page:** Click "Sign In" on landing page
2. **Enter credentials:**
   - Email: admin@fitandflex.com
   - Password: admin123
3. **Access Admin Panel:** After login, click "Admin" button in dashboard header
4. **Admin Features:**
   - View all users
   - Delete users
   - View all exercises
   - Create/Edit/Delete exercises
   - Monitor user progress

---

## 📊 Database Access

### Method 1: MongoDB Shell (Recommended)

```bash
# Connect to database
mongosh

# Switch to database
use('test_database')

# View all users
db.users.find({}, {password_hash: 0, _id: 0}).pretty()

# View specific user
db.users.findOne({email: "admin@fitandflex.com"}, {_id: 0})

# Count users
db.users.countDocuments({})

# View exercises
db.exercises.find({}, {_id: 0}).limit(5).pretty()

# View workout plans
db.workout_plans.find({}, {_id: 0}).limit(1).pretty()

# View user progress
db.user_progress.find({}, {_id: 0}).limit(5).pretty()

# View achievements
db.achievements.find({}, {_id: 0}).pretty()
```

### Method 2: Through Backend API

```bash
API_URL="https://activehub-17.preview.emergentagent.com"

# Get all exercises
curl "$API_URL/api/exercises"

# Check single exercise
curl "$API_URL/api/exercises/EXERCISE_ID"
```

### Method 3: Python Script

```bash
cd /app/backend
python3 << 'EOF'
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def view_data():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    
    # Get counts
    user_count = await db.users.count_documents({})
    exercise_count = await db.exercises.count_documents({})
    plan_count = await db.workout_plans.count_documents({})
    
    print(f"Users: {user_count}")
    print(f"Exercises: {exercise_count}")
    print(f"Workout Plans: {plan_count}")
    
    # Get latest users
    print("\nRecent Users:")
    users = await db.users.find({}, {"name": 1, "email": 1, "_id": 0}).limit(5).to_list(5)
    for user in users:
        print(f"  - {user['name']} ({user['email']})")
    
    client.close()

asyncio.run(view_data())
EOF
```

---

## 🔑 User Authentication Types

### 1. Email/Password Users
- **Sign Up:** Name, Email, Password
- **Sign In:** Email + Password
- **Data stored:** password_hash (SHA-256)

### 2. Google OAuth Users
- **Sign In:** Google account
- **Sign Up:** First-time Google login
- **Data stored:** email, name, picture from Google

### 3. Guest Users
- **Access:** "Try as Guest" button
- **Duration:** 24 hours
- **Limitation:** No data persistence beyond session

---

## 📈 Monitoring User Activity

### Check Active Users

```bash
mongosh --eval "
use('test_database');
print('Total Users: ' + db.users.countDocuments({}));
print('Admin Users: ' + db.users.countDocuments({is_admin: true}));
print('Guest Users: ' + db.users.countDocuments({is_guest: true}));
print('Regular Users: ' + db.users.countDocuments({is_guest: false, is_admin: false}));
"
```

### Check User Progress

```bash
mongosh --eval "
use('test_database');
var progress = db.user_progress.aggregate([
  {\\$group: {_id: '\\$user_id', total_completed: {\\$sum: 1}}},
  {\\$sort: {total_completed: -1}},
  {\\$limit: 5}
]).toArray();
progress.forEach(function(p) {
  var user = db.users.findOne({user_id: p._id}, {name: 1});
  print(user.name + ': ' + p.total_completed + ' days completed');
});
"
```

### Check Achievements Earned

```bash
mongosh --eval "
use('test_database');
var achievements = db.achievements.find({}, {_id: 0, name: 1, user_id: 1, earned_at: 1}).toArray();
print('Total Achievements Earned: ' + achievements.length);
achievements.forEach(function(a) {
  print('  ' + a.name + ' earned on ' + a.earned_at);
});
"
```

---

## 🛠️ Quick Admin Tasks

### Create New Admin User

```bash
cd /app/backend
python3 << 'EOF'
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os, hashlib, uuid
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

async def create_admin(email, password, name):
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    user_id = f"admin_{uuid.uuid4().hex[:12]}"
    
    await db.users.insert_one({
        "user_id": user_id,
        "email": email,
        "name": name,
        "password_hash": password_hash,
        "is_admin": True,
        "is_guest": False,
        "created_at": datetime.now(timezone.utc)
    })
    
    print(f"✅ Admin created: {email}")
    client.close()

asyncio.run(create_admin("NEW_EMAIL", "NEW_PASSWORD", "NEW_NAME"))
EOF
```

### Delete User

```bash
mongosh --eval "
use('test_database');
db.users.deleteOne({email: 'user@example.com'});
db.user_sessions.deleteMany({user_id: 'USER_ID'});
db.workout_plans.deleteMany({user_id: 'USER_ID'});
db.user_progress.deleteMany({user_id: 'USER_ID'});
print('User deleted');
"
```

### Reset User Password

```bash
cd /app/backend
python3 << 'EOF'
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os, hashlib
from dotenv import load_dotenv

load_dotenv()

async def reset_password(email, new_password):
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    
    password_hash = hashlib.sha256(new_password.encode()).hexdigest()
    
    result = await db.users.update_one(
        {"email": email},
        {"$set": {"password_hash": password_hash}}
    )
    
    if result.modified_count > 0:
        print(f"✅ Password reset for {email}")
    else:
        print("❌ User not found")
    
    client.close()

asyncio.run(reset_password("user@example.com", "NEW_PASSWORD"))
EOF
```

---

## 📊 Database Collections Overview

### users
- user_id (string)
- email (string)
- name (string)
- password_hash (string, optional)
- height, weight, bmi, age (numbers, optional)
- fitness_goal, selected_sport (strings, optional)
- is_admin, is_guest (booleans)
- created_at (datetime)

### user_sessions
- user_id (string)
- session_token (string)
- expires_at (datetime)
- created_at (datetime)

### exercises
- exercise_id (string)
- name (string)
- description (string)
- duration_minutes (number)
- gif_url (string)
- sport_category (string)
- difficulty (string)
- instructions (array)

### workout_plans
- plan_id (string)
- user_id (string)
- plan_type (string)
- sport (string, optional)
- duration_days (number, default 45)
- daily_exercises (array of objects)
- created_at (datetime)

### user_progress
- progress_id (string)
- user_id (string)
- plan_id (string)
- day_number (number)
- completed (boolean)
- completed_at (datetime)

### achievements
- achievement_id (string)
- user_id (string)
- name (string)
- description (string)
- badge (string, emoji)
- days_required (number)
- earned_at (datetime)

---

## 🚀 Current Status

✅ **Authentication:** Email/Password + Google OAuth + Guest Mode
✅ **Workout Plans:** 6-7 exercises per day (35-45 min)
✅ **Admin Access:** Full CRUD operations available
✅ **Database:** All collections properly structured
✅ **Exercise GIFs:** Placeholder images (ready for your content)

**Admin Login:** admin@fitandflex.com / admin123
