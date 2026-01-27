import requests
import sys
import json
from datetime import datetime
from collections import Counter

class EnhancedFitFlexTester:
    def __init__(self, base_url="https://activehub-17.preview.emergentagent.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.user_id = None
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []
        self.detailed_results = {}

    def run_test(self, name, method, endpoint, expected_status, data=None):
        """Run a single API test with detailed logging"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            if method == 'GET':
                response = self.session.get(url, headers=headers)
            elif method == 'POST':
                response = self.session.post(url, json=data, headers=headers)
            elif method == 'PUT':
                response = self.session.put(url, json=data, headers=headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    return True, response.json()
                except:
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:300]}")
                self.failed_tests.append({
                    'name': name,
                    'expected': expected_status,
                    'actual': response.status_code,
                    'response': response.text[:300]
                })
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            self.failed_tests.append({'name': name, 'error': str(e)})
            return False, {}

    def test_exercise_library_expansion(self):
        """Test that exercise library has 32+ exercises with varied categories"""
        print("\n🎯 TESTING EXERCISE LIBRARY EXPANSION")
        success, response = self.run_test(
            "Get All Exercises",
            "GET",
            "api/exercises",
            200
        )
        
        if success and isinstance(response, list):
            exercise_count = len(response)
            categories = set(ex.get('sport_category', '') for ex in response)
            
            print(f"   📊 Found {exercise_count} exercises")
            print(f"   📊 Categories: {sorted(categories)}")
            
            # Check for specific exercises mentioned in requirements
            exercise_names = [ex.get('name', '').lower() for ex in response]
            required_exercises = ['push-ups', 'planks', 'squats', 'lunges', 'hill climbing']
            found_exercises = []
            
            for req_ex in required_exercises:
                for ex_name in exercise_names:
                    if req_ex.replace('-', ' ') in ex_name or req_ex.replace('-', '') in ex_name:
                        found_exercises.append(req_ex)
                        break
            
            print(f"   📊 Required exercises found: {found_exercises}")
            
            self.detailed_results['exercise_library'] = {
                'total_exercises': exercise_count,
                'categories': list(categories),
                'required_exercises_found': found_exercises,
                'has_32_plus': exercise_count >= 32,
                'has_varied_categories': len(categories) >= 5
            }
            
            return exercise_count >= 32 and len(categories) >= 5
        
        return False

    def test_workout_plan_variety(self):
        """Test that workout plans have different exercises each day"""
        print("\n🎯 TESTING WORKOUT PLAN VARIETY")
        
        # Setup user and generate plan
        self.setup_test_user()
        
        success, plan_response = self.run_test(
            "Generate Workout Plan for Variety Test",
            "POST",
            "api/workout/generate-plan",
            200
        )
        
        if not success:
            return False
        
        # Get first 10 days to check variety
        daily_exercises = []
        exercise_frequency = Counter()
        
        for day in range(1, 11):  # Check first 10 days
            success, day_response = self.run_test(
                f"Get Day {day} for Variety Check",
                "GET",
                f"api/workout/day/{day}",
                200
            )
            
            if success and 'exercises' in day_response:
                day_exercises = [ex.get('exercise_id') for ex in day_response['exercises']]
                daily_exercises.append(day_exercises)
                
                for ex_id in day_exercises:
                    exercise_frequency[ex_id] += 1
        
        # Analyze variety
        total_unique_exercises = len(exercise_frequency)
        max_repetition = max(exercise_frequency.values()) if exercise_frequency else 0
        
        print(f"   📊 Unique exercises across 10 days: {total_unique_exercises}")
        print(f"   📊 Max exercise repetition: {max_repetition}")
        
        # Check if same exercises appear every day (bad)
        variety_score = total_unique_exercises / (len(daily_exercises) * 5) if daily_exercises else 0
        
        self.detailed_results['workout_variety'] = {
            'unique_exercises_10_days': total_unique_exercises,
            'max_repetition': max_repetition,
            'variety_score': variety_score,
            'has_good_variety': variety_score > 0.7 and max_repetition <= 5
        }
        
        return variety_score > 0.7 and max_repetition <= 5

    def test_sport_specific_periodicity(self):
        """Test that sport-specific exercises appear periodically"""
        print("\n🎯 TESTING SPORT-SPECIFIC EXERCISE PERIODICITY")
        
        # Setup user with specific sport
        self.setup_test_user_with_sport("Badminton")
        
        success, plan_response = self.run_test(
            "Generate Sport-Specific Plan",
            "POST",
            "api/workout/generate-plan",
            200
        )
        
        if not success:
            return False
        
        # Check first 20 days for sport-specific exercises
        sport_exercise_days = []
        
        for day in range(1, 21):
            success, day_response = self.run_test(
                f"Get Day {day} for Sport Check",
                "GET",
                f"api/workout/day/{day}",
                200
            )
            
            if success and 'exercises' in day_response:
                for exercise in day_response['exercises']:
                    if exercise.get('sport_category') == 'Badminton':
                        sport_exercise_days.append(day)
                        break
        
        print(f"   📊 Sport-specific exercises found on days: {sport_exercise_days}")
        
        # Check if they appear every 4-5 days (approximately)
        has_periodic_pattern = len(sport_exercise_days) >= 3  # At least 3 occurrences in 20 days
        
        self.detailed_results['sport_periodicity'] = {
            'sport_exercise_days': sport_exercise_days,
            'frequency': len(sport_exercise_days),
            'has_periodic_pattern': has_periodic_pattern
        }
        
        return has_periodic_pattern

    def test_streak_functionality(self):
        """Test streak counter functionality"""
        print("\n🎯 TESTING STREAK FUNCTIONALITY")
        
        self.setup_test_user()
        
        # Generate plan
        self.run_test("Generate Plan for Streak Test", "POST", "api/workout/generate-plan", 200)
        
        # Check initial progress
        success, initial_progress = self.run_test(
            "Get Initial Progress",
            "GET",
            "api/workout/progress",
            200
        )
        
        if not success:
            return False
        
        initial_streak = initial_progress.get('current_streak', 0)
        print(f"   📊 Initial streak: {initial_streak}")
        
        # Complete day 1
        success, _ = self.run_test(
            "Complete Day 1 for Streak",
            "POST",
            "api/workout/complete-day?day_number=1",
            200
        )
        
        if not success:
            return False
        
        # Check updated progress
        success, updated_progress = self.run_test(
            "Get Updated Progress After Day 1",
            "GET",
            "api/workout/progress",
            200
        )
        
        if success:
            new_streak = updated_progress.get('current_streak', 0)
            longest_streak = updated_progress.get('longest_streak', 0)
            
            print(f"   📊 Streak after day 1: {new_streak}")
            print(f"   📊 Longest streak: {longest_streak}")
            
            streak_increased = new_streak > initial_streak
            
            self.detailed_results['streak_functionality'] = {
                'initial_streak': initial_streak,
                'streak_after_completion': new_streak,
                'longest_streak': longest_streak,
                'streak_increased': streak_increased
            }
            
            return streak_increased
        
        return False

    def test_achievement_system(self):
        """Test achievement badge system"""
        print("\n🎯 TESTING ACHIEVEMENT SYSTEM")
        
        success, achievements = self.run_test(
            "Get Available Achievements",
            "GET",
            "api/achievements/available",
            200
        )
        
        if success and isinstance(achievements, list):
            milestone_days = [ach.get('days_required') for ach in achievements]
            expected_milestones = [5, 10, 20, 30, 45]
            
            print(f"   📊 Achievement milestones: {sorted(milestone_days)}")
            print(f"   📊 Expected milestones: {expected_milestones}")
            
            has_all_milestones = all(day in milestone_days for day in expected_milestones)
            
            # Check achievement structure
            sample_achievement = achievements[0] if achievements else {}
            has_proper_structure = all(
                key in sample_achievement 
                for key in ['name', 'description', 'badge', 'days_required', 'earned']
            )
            
            self.detailed_results['achievement_system'] = {
                'total_achievements': len(achievements),
                'milestone_days': sorted(milestone_days),
                'has_all_milestones': has_all_milestones,
                'has_proper_structure': has_proper_structure
            }
            
            return has_all_milestones and has_proper_structure
        
        return False

    def test_gif_urls(self):
        """Test that exercise GIFs have valid URLs"""
        print("\n🎯 TESTING EXERCISE GIF URLS")
        
        success, exercises = self.run_test(
            "Get Exercises for GIF Check",
            "GET",
            "api/exercises",
            200
        )
        
        if success and isinstance(exercises, list):
            gif_urls = [ex.get('gif_url', '') for ex in exercises]
            valid_gifs = [url for url in gif_urls if url.startswith('http') and 'giphy.com' in url]
            
            print(f"   📊 Total exercises: {len(exercises)}")
            print(f"   📊 Valid GIF URLs: {len(valid_gifs)}")
            
            gif_coverage = len(valid_gifs) / len(exercises) if exercises else 0
            
            self.detailed_results['gif_urls'] = {
                'total_exercises': len(exercises),
                'valid_gif_urls': len(valid_gifs),
                'gif_coverage': gif_coverage,
                'has_good_coverage': gif_coverage >= 0.9
            }
            
            return gif_coverage >= 0.9
        
        return False

    def setup_test_user(self):
        """Setup a test user with basic onboarding"""
        # Create guest user
        self.run_test("Create Guest User", "POST", "api/auth/guest", 200)
        
        # Complete onboarding
        onboarding_data = {
            "height": 175.0,
            "weight": 70.0,
            "date_of_birth": "1990-01-01",
            "age": 34,
            "selected_sports": ["Basketball"]
        }
        self.run_test("Complete Onboarding", "PUT", "api/user/onboarding", 200, onboarding_data)
        
        # Set fitness goal
        goal_data = {"fitness_goal": "Sports", "selected_sport": "Basketball"}
        self.run_test("Set Fitness Goal", "PUT", "api/user/fitness-goal", 200, goal_data)

    def setup_test_user_with_sport(self, sport):
        """Setup a test user with specific sport"""
        # Create guest user
        self.run_test("Create Guest User", "POST", "api/auth/guest", 200)
        
        # Complete onboarding
        onboarding_data = {
            "height": 175.0,
            "weight": 70.0,
            "date_of_birth": "1990-01-01",
            "age": 34,
            "selected_sports": [sport]
        }
        self.run_test("Complete Onboarding", "PUT", "api/user/onboarding", 200, onboarding_data)
        
        # Set fitness goal
        goal_data = {"fitness_goal": "Sports", "selected_sport": sport}
        self.run_test("Set Fitness Goal", "PUT", "api/user/fitness-goal", 200, goal_data)

def main():
    print("🚀 Starting Enhanced Fit & Flex Feature Testing...")
    print("=" * 60)
    
    tester = EnhancedFitFlexTester()
    
    # Test new features
    feature_tests = [
        ("Exercise Library Expansion", tester.test_exercise_library_expansion),
        ("Workout Plan Variety", tester.test_workout_plan_variety),
        ("Sport-Specific Periodicity", tester.test_sport_specific_periodicity),
        ("Streak Functionality", tester.test_streak_functionality),
        ("Achievement System", tester.test_achievement_system),
        ("Exercise GIF URLs", tester.test_gif_urls),
    ]
    
    feature_results = {}
    
    for feature_name, test_func in feature_tests:
        try:
            result = test_func()
            feature_results[feature_name] = result
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"\n{status} {feature_name}")
        except Exception as e:
            feature_results[feature_name] = False
            print(f"\n❌ FAIL {feature_name} - Error: {str(e)}")
    
    # Print detailed results
    print("\n" + "=" * 60)
    print("📊 DETAILED FEATURE TEST RESULTS")
    print("=" * 60)
    
    for feature, passed in feature_results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {feature}")
    
    # Print summary
    passed_features = sum(feature_results.values())
    total_features = len(feature_results)
    success_rate = (passed_features / total_features) * 100 if total_features > 0 else 0
    
    print(f"\n📈 Feature Success Rate: {passed_features}/{total_features} ({success_rate:.1f}%)")
    
    # Print detailed analysis
    if hasattr(tester, 'detailed_results'):
        print(f"\n📋 DETAILED ANALYSIS:")
        for key, details in tester.detailed_results.items():
            print(f"\n{key.upper()}:")
            for detail_key, detail_value in details.items():
                print(f"  - {detail_key}: {detail_value}")
    
    return 0 if success_rate >= 80 else 1

if __name__ == "__main__":
    sys.exit(main())