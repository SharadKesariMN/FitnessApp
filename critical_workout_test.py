#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime
from collections import Counter

class CriticalWorkoutTester:
    def __init__(self, base_url="https://activehub-17.preview.emergentagent.com"):
        self.base_url = base_url
        self.session_token = None
        self.user_id = None
        self.tests_run = 0
        self.tests_passed = 0
        self.session = requests.Session()
        self.critical_issues = []

    def log_test(self, name, success, details=""):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name}")
        else:
            print(f"❌ {name} - {details}")
            if "CRITICAL" in name.upper():
                self.critical_issues.append(f"{name}: {details}")
        
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
            
            if success and response.content:
                try:
                    json_data = response.json()
                    return success, json_data
                except:
                    return success, {}
            else:
                error_msg = f"Expected {expected_status}, got {response.status_code}"
                if response.content:
                    try:
                        error_data = response.json()
                        error_msg += f" - {error_data.get('detail', '')}"
                    except:
                        pass
                return success, {"error": error_msg}

        except Exception as e:
            return False, {"error": str(e)}

    def setup_user(self):
        """Setup guest user with complete profile"""
        print("🔧 Setting up test user...")
        
        # Create guest session
        success, response = self.run_api_test(
            "Guest Authentication",
            "POST",
            "auth/guest",
            200
        )
        
        if not success:
            return False
            
        if 'user_id' in response:
            self.user_id = response['user_id']
            cookies = self.session.cookies
            if 'session_token' in cookies:
                self.session_token = cookies['session_token']
            else:
                return False
        else:
            return False

        # Complete onboarding
        onboarding_data = {
            "height": 175.0,
            "weight": 70.0,
            "date_of_birth": "1990-01-01",
            "age": 34,
            "selected_sports": ["Badminton"]
        }
        
        success, _ = self.run_api_test(
            "User Onboarding",
            "PUT",
            "user/onboarding",
            200,
            onboarding_data
        )
        
        if not success:
            return False

        # Set fitness goal
        goal_data = {
            "fitness_goal": "Build Strength",
            "selected_sport": "Badminton"
        }
        
        success, _ = self.run_api_test(
            "Set Fitness Goal",
            "PUT",
            "user/fitness-goal",
            200,
            goal_data
        )
        
        return success

    def test_critical_5_exercises_per_day(self):
        """CRITICAL TEST: Verify each day has exactly 5 exercises"""
        print("\n🎯 CRITICAL TEST: 5 Exercises Per Day")
        print("-" * 40)
        
        # Generate workout plan
        success, plan_response = self.run_api_test(
            "Generate Workout Plan",
            "POST",
            "workout/generate-plan",
            200
        )
        
        if not success:
            self.log_test("CRITICAL: Plan Generation", False, "Failed to generate plan")
            return False

        daily_exercises = plan_response.get('daily_exercises', [])
        if not daily_exercises:
            self.log_test("CRITICAL: Plan Structure", False, "No daily exercises found")
            return False

        # Check each day has exactly 5 exercises
        failed_days = []
        exercise_counts = []
        
        for day_data in daily_exercises:
            day_num = day_data.get('day', 0)
            exercises = day_data.get('exercises', [])
            exercise_count = len(exercises)
            exercise_counts.append(exercise_count)
            
            if exercise_count != 5:
                failed_days.append(f"Day {day_num}: {exercise_count} exercises")

        # Log results
        if failed_days:
            self.log_test("CRITICAL: 5 Exercises Per Day", False, 
                         f"Failed days: {failed_days[:5]}{'...' if len(failed_days) > 5 else ''}")
        else:
            self.log_test("CRITICAL: 5 Exercises Per Day", True, 
                         f"All {len(daily_exercises)} days have exactly 5 exercises")

        # Additional statistics
        min_exercises = min(exercise_counts) if exercise_counts else 0
        max_exercises = max(exercise_counts) if exercise_counts else 0
        avg_exercises = sum(exercise_counts) / len(exercise_counts) if exercise_counts else 0
        
        print(f"   📊 Exercise count stats: Min={min_exercises}, Max={max_exercises}, Avg={avg_exercises:.1f}")
        
        return len(failed_days) == 0

    def test_workout_variety_detailed(self):
        """Test workout variety with detailed analysis"""
        print("\n📊 DETAILED VARIETY ANALYSIS")
        print("-" * 40)
        
        # Get current plan
        success, plan_response = self.run_api_test(
            "Get Current Plan",
            "GET",
            "workout/current-plan",
            200
        )
        
        if not success:
            return False

        daily_exercises = plan_response.get('daily_exercises', [])
        first_10_days = daily_exercises[:10]
        
        # Collect all exercises from first 10 days
        all_exercises = []
        day_details = []
        
        for day_data in first_10_days:
            day_num = day_data['day']
            exercises = day_data['exercises']
            all_exercises.extend(exercises)
            day_details.append(f"Day {day_num}: {len(exercises)} exercises")

        # Calculate variety metrics
        unique_exercises = len(set(all_exercises))
        total_exercises = len(all_exercises)
        exercise_counts = Counter(all_exercises)
        max_repetition = max(exercise_counts.values()) if exercise_counts else 0
        variety_score = unique_exercises / total_exercises if total_exercises else 0
        
        # Log detailed results
        print(f"   📈 Total exercises in 10 days: {total_exercises}")
        print(f"   🎯 Unique exercises: {unique_exercises}")
        print(f"   🔄 Max repetition: {max_repetition}")
        print(f"   📊 Variety score: {variety_score:.3f}")
        
        # Test requirements
        self.log_test("Variety Score ≥0.7", variety_score >= 0.7, f"Score: {variety_score:.3f}")
        self.log_test("Unique Exercises ≥20", unique_exercises >= 20, f"Found: {unique_exercises}")
        self.log_test("Max Repetition ≤3", max_repetition <= 3, f"Max: {max_repetition}")
        
        return variety_score >= 0.7

    def test_sport_specific_frequency(self):
        """Test sport-specific exercise frequency"""
        print("\n🏸 SPORT-SPECIFIC FREQUENCY TEST")
        print("-" * 40)
        
        # Get current plan
        success, plan_response = self.run_api_test(
            "Get Current Plan",
            "GET",
            "workout/current-plan",
            200
        )
        
        if not success:
            return False

        daily_exercises = plan_response.get('daily_exercises', [])
        sport_exercise_days = []
        
        # Check first 20 days for sport exercises
        for day_data in daily_exercises[:20]:
            day_num = day_data['day']
            exercises = day_data['exercises']
            
            # Check if any exercise is sport-specific
            has_sport_exercise = False
            for exercise_id in exercises:
                success, exercise_data = self.run_api_test(
                    f"Get Exercise {exercise_id}",
                    "GET",
                    f"exercises/{exercise_id}",
                    200
                )
                if success and exercise_data.get('sport_category') == 'Badminton':
                    has_sport_exercise = True
                    break
            
            if has_sport_exercise:
                sport_exercise_days.append(day_num)

        # Expected pattern: every 5 days (1, 6, 11, 16)
        expected_days = [1, 6, 11, 16]
        actual_days = sport_exercise_days[:4]  # First 4 occurrences
        
        frequency_correct = set(actual_days) == set(expected_days)
        
        print(f"   🎯 Expected sport days: {expected_days}")
        print(f"   📅 Actual sport days: {actual_days}")
        
        self.log_test("Sport Exercise Frequency", frequency_correct, 
                     f"Pattern: {actual_days} vs expected {expected_days}")
        
        return frequency_correct

    def test_individual_day_workouts(self):
        """Test individual day workout retrieval"""
        print("\n📅 INDIVIDUAL DAY TESTS")
        print("-" * 40)
        
        test_days = [1, 5, 10, 15, 20]
        all_passed = True
        
        for day_num in test_days:
            success, day_data = self.run_api_test(
                f"Get Day {day_num} Workout",
                "GET",
                f"workout/day/{day_num}",
                200
            )
            
            if success:
                exercises = day_data.get('exercises', [])
                exercise_count = len(exercises)
                
                if exercise_count == 5:
                    self.log_test(f"Day {day_num} Exercise Count", True, f"{exercise_count} exercises")
                else:
                    self.log_test(f"Day {day_num} Exercise Count", False, f"Only {exercise_count} exercises")
                    all_passed = False
                    
                # Check exercise details
                valid_exercises = 0
                for exercise in exercises:
                    if all(field in exercise for field in ['exercise_id', 'name', 'gif_url']):
                        valid_exercises += 1
                
                self.log_test(f"Day {day_num} Exercise Validity", valid_exercises == exercise_count, 
                             f"{valid_exercises}/{exercise_count} valid")
            else:
                self.log_test(f"Day {day_num} Retrieval", False, "Failed to get day data")
                all_passed = False
        
        return all_passed

    def run_critical_tests(self):
        """Run all critical tests"""
        print("🏋️ CRITICAL WORKOUT VERIFICATION")
        print("=" * 50)
        
        # Setup
        if not self.setup_user():
            print("❌ User setup failed - stopping tests")
            return False
        
        print("✅ User setup completed")
        
        # Run critical tests
        test_results = []
        
        test_results.append(self.test_critical_5_exercises_per_day())
        test_results.append(self.test_workout_variety_detailed())
        test_results.append(self.test_sport_specific_frequency())
        test_results.append(self.test_individual_day_workouts())
        
        # Summary
        print("\n" + "=" * 50)
        print(f"📊 Test Results: {self.tests_passed}/{self.tests_run} passed")
        success_rate = (self.tests_passed / self.tests_run) * 100 if self.tests_run > 0 else 0
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if self.critical_issues:
            print("\n🚨 CRITICAL ISSUES:")
            for issue in self.critical_issues:
                print(f"   • {issue}")
        
        return len(self.critical_issues) == 0 and success_rate >= 90

def main():
    tester = CriticalWorkoutTester()
    success = tester.run_critical_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())