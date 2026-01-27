#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime
from collections import Counter

class FitFlexAPITester:
    def __init__(self, base_url="https://activehub-17.preview.emergentagent.com"):
        self.base_url = base_url
        self.session_token = None
        self.user_id = None
        self.tests_run = 0
        self.tests_passed = 0
        self.session = requests.Session()

    def log_test(self, name, success, details=""):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name}")
        else:
            print(f"❌ {name} - {details}")
        
        if details and success:
            print(f"   {details}")

    def run_api_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.base_url}/api/{endpoint}"
        
        if headers is None:
            headers = {'Content-Type': 'application/json'}
        
        if self.session_token:
            headers['Authorization'] = f'Bearer {self.session_token}'

        try:
            if method == 'GET':
                response = self.session.get(url, headers=headers)
            elif method == 'POST':
                response = self.session.post(url, json=data, headers=headers)
            elif method == 'PUT':
                response = self.session.put(url, json=data, headers=headers)

            success = response.status_code == expected_status
            details = f"Status: {response.status_code}"
            
            if success and response.content:
                try:
                    json_data = response.json()
                    self.log_test(name, success, details)
                    return success, json_data
                except:
                    self.log_test(name, success, details)
                    return success, {}
            else:
                error_msg = f"Expected {expected_status}, got {response.status_code}"
                if response.content:
                    try:
                        error_data = response.json()
                        error_msg += f" - {error_data.get('detail', '')}"
                    except:
                        pass
                self.log_test(name, success, error_msg)
                return success, {}

        except Exception as e:
            self.log_test(name, success, f"Error: {str(e)}")
            return False, {}

    def test_guest_auth(self):
        """Test guest authentication"""
        success, response = self.run_api_test(
            "Guest Authentication",
            "POST",
            "auth/guest",
            200
        )
        
        if success and 'user_id' in response:
            self.user_id = response['user_id']
            # Extract session token from cookies
            cookies = self.session.cookies
            if 'session_token' in cookies:
                self.session_token = cookies['session_token']
                return True
        return False

    def test_onboarding(self):
        """Test user onboarding"""
        onboarding_data = {
            "height": 175.0,
            "weight": 70.0,
            "date_of_birth": "1990-01-01",
            "age": 34,
            "selected_sports": ["Badminton"]
        }
        
        success, response = self.run_api_test(
            "User Onboarding",
            "PUT",
            "user/onboarding",
            200,
            onboarding_data
        )
        return success

    def test_fitness_goal(self):
        """Test fitness goal setting"""
        goal_data = {
            "fitness_goal": "Build Strength",
            "selected_sport": "Badminton"
        }
        
        success, response = self.run_api_test(
            "Set Fitness Goal",
            "PUT",
            "user/fitness-goal",
            200,
            goal_data
        )
        return success

    def test_exercise_library(self):
        """Test exercise library"""
        success, response = self.run_api_test(
            "Get All Exercises",
            "GET",
            "exercises",
            200
        )
        
        if success:
            exercise_count = len(response)
            categories = set(ex.get('sport_category', '') for ex in response)
            
            # Check if we have 32 exercises
            if exercise_count >= 32:
                self.log_test("Exercise Count (≥32)", True, f"Found {exercise_count} exercises")
            else:
                self.log_test("Exercise Count (≥32)", False, f"Only {exercise_count} exercises found")
            
            # Check required exercises
            exercise_names = [ex.get('name', '').lower() for ex in response]
            required_exercises = ['push-ups', 'squats', 'lunges', 'hill climbing']
            
            for req_ex in required_exercises:
                found = any(req_ex in name for name in exercise_names)
                self.log_test(f"Required Exercise: {req_ex.title()}", found)
            
            # Check categories
            expected_categories = ['Fitness', 'Badminton', 'Athletics', 'Basketball', 'Soccer', 'Running']
            for cat in expected_categories:
                found = cat in categories
                self.log_test(f"Category: {cat}", found)
                
            return True
        return False

    def test_workout_plan_generation(self):
        """Test workout plan generation and analyze variety"""
        success, response = self.run_api_test(
            "Generate Workout Plan",
            "POST",
            "workout/generate-plan",
            200
        )
        
        if not success:
            return False
            
        # Analyze workout variety for first 10 days
        daily_exercises = response.get('daily_exercises', [])
        if len(daily_exercises) < 10:
            self.log_test("Workout Plan Length", False, f"Only {len(daily_exercises)} days generated")
            return False
            
        # Test 1: Exercise variety across 10 days
        first_10_days = daily_exercises[:10]
        all_exercises = []
        sport_exercise_days = []
        
        for day_data in first_10_days:
            day_num = day_data['day']
            exercises = day_data['exercises']
            all_exercises.extend(exercises)
            
            # Check if this day has sport-specific exercises
            # We need to check actual exercise data to determine sport category
            has_sport_exercise = self.check_day_for_sport_exercises(exercises)
            if has_sport_exercise:
                sport_exercise_days.append(day_num)
        
        # Calculate variety metrics
        unique_exercises = len(set(all_exercises))
        exercise_counts = Counter(all_exercises)
        max_repetition = max(exercise_counts.values()) if exercise_counts else 0
        variety_score = unique_exercises / len(all_exercises) if all_exercises else 0
        
        # Test variety requirements
        self.log_test("Unique Exercises (≥20)", unique_exercises >= 20, f"Found {unique_exercises} unique exercises")
        self.log_test("Max Repetition (≤3)", max_repetition <= 3, f"Max repetition: {max_repetition}")
        self.log_test("Variety Score (≥0.7)", variety_score >= 0.7, f"Variety score: {variety_score:.2f}")
        
        # Test 2: Sport-specific exercise frequency
        expected_sport_days = [1, 6]  # Days 1 and 6 in first 10 days (every 5 days)
        sport_frequency_correct = set(sport_exercise_days) == set(expected_sport_days)
        self.log_test("Sport Exercise Frequency", sport_frequency_correct, 
                     f"Sport exercises on days: {sport_exercise_days}, expected: {expected_sport_days}")
        
        # Test 3: Plan structure
        self.log_test("45-Day Plan", len(daily_exercises) == 45, f"Plan has {len(daily_exercises)} days")
        
        return True

    def check_day_for_sport_exercises(self, exercise_ids):
        """Check if any exercises in the day are sport-specific"""
        for exercise_id in exercise_ids:
            success, exercise_data = self.run_api_test(
                f"Get Exercise {exercise_id}",
                "GET",
                f"exercises/{exercise_id}",
                200
            )
            if success and exercise_data.get('sport_category') == 'Badminton':
                return True
        return False

    def test_progress_tracking(self):
        """Test progress and streak functionality"""
        # Get initial progress
        success, progress = self.run_api_test(
            "Get Initial Progress",
            "GET",
            "workout/progress",
            200
        )
        
        if not success:
            return False
            
        initial_streak = progress.get('current_streak', 0)
        
        # Complete day 1
        success, _ = self.run_api_test(
            "Complete Day 1",
            "POST",
            "workout/complete-day?day_number=1",
            200
        )
        
        if not success:
            return False
            
        # Check updated progress
        success, updated_progress = self.run_api_test(
            "Get Updated Progress",
            "GET",
            "workout/progress",
            200
        )
        
        if success:
            new_streak = updated_progress.get('current_streak', 0)
            completed_days = updated_progress.get('completed_days', 0)
            
            self.log_test("Streak Increment", new_streak > initial_streak, 
                         f"Streak: {initial_streak} → {new_streak}")
            self.log_test("Completed Days", completed_days >= 1, f"Completed: {completed_days}")
            
        return success

    def test_achievements(self):
        """Test achievement system"""
        success, achievements = self.run_api_test(
            "Get Available Achievements",
            "GET",
            "achievements/available",
            200
        )
        
        if success:
            # Check for 5 milestone achievements
            expected_milestones = [5, 10, 20, 30, 45]
            found_milestones = [ach.get('days') for ach in achievements if 'days' in ach]
            
            milestone_match = set(found_milestones) == set(expected_milestones)
            self.log_test("Achievement Milestones", milestone_match, 
                         f"Found milestones: {sorted(found_milestones)}")
            
            # Check achievement structure
            for ach in achievements:
                has_required_fields = all(field in ach for field in ['name', 'description', 'badge', 'earned'])
                if not has_required_fields:
                    self.log_test("Achievement Structure", False, f"Missing fields in {ach.get('name', 'unknown')}")
                    return False
                    
            self.log_test("Achievement Structure", True, "All achievements have required fields")
            
        return success

    def test_ai_recommendations(self):
        """Test AI recommendations"""
        success, response = self.run_api_test(
            "AI Recommendations",
            "POST",
            "ai/recommendations",
            200
        )
        
        if success:
            recommendations = response.get('recommendations', '')
            has_content = len(recommendations) > 50  # Should have meaningful content
            self.log_test("AI Content Quality", has_content, f"Response length: {len(recommendations)} chars")
            
        return success

    def run_comprehensive_test(self):
        """Run all tests"""
        print("🏋️ Starting Fit & Flex API Testing")
        print("=" * 50)
        
        # Authentication
        if not self.test_guest_auth():
            print("❌ Authentication failed - stopping tests")
            return False
            
        # User setup
        self.test_onboarding()
        self.test_fitness_goal()
        
        # Core functionality
        self.test_exercise_library()
        self.test_workout_plan_generation()
        self.test_progress_tracking()
        self.test_achievements()
        self.test_ai_recommendations()
        
        # Summary
        print("\n" + "=" * 50)
        print(f"📊 Test Results: {self.tests_passed}/{self.tests_run} passed")
        success_rate = (self.tests_passed / self.tests_run) * 100 if self.tests_run > 0 else 0
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        return success_rate >= 80

def main():
    tester = FitFlexAPITester()
    success = tester.run_comprehensive_test()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())