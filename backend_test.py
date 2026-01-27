import requests
import sys
import json
from datetime import datetime

class FitFlexAPITester:
    def __init__(self, base_url="https://activehub-17.preview.emergentagent.com"):
        self.base_url = base_url
        self.session = requests.Session()  # Use session to maintain cookies
        self.user_id = None
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        test_headers = {'Content-Type': 'application/json'}
        
        if headers:
            test_headers.update(headers)

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = self.session.get(url, headers=test_headers)
            elif method == 'POST':
                response = self.session.post(url, json=data, headers=test_headers)
            elif method == 'PUT':
                response = self.session.put(url, json=data, headers=test_headers)
            elif method == 'DELETE':
                response = self.session.delete(url, headers=test_headers)

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
                print(f"   Response: {response.text[:200]}")
                self.failed_tests.append({
                    'name': name,
                    'expected': expected_status,
                    'actual': response.status_code,
                    'response': response.text[:200]
                })
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            self.failed_tests.append({
                'name': name,
                'error': str(e)
            })
            return False, {}

    def test_guest_auth(self):
        """Test guest authentication"""
        success, response = self.run_test(
            "Guest Authentication",
            "POST",
            "api/auth/guest",
            200
        )
        if success and 'user_id' in response:
            self.user_id = response['user_id']
            # Extract session token from response headers if available
            print(f"   Guest user created: {self.user_id}")
            return True
        return False

    def test_onboarding(self):
        """Test user onboarding"""
        onboarding_data = {
            "height": 175.0,
            "weight": 70.0,
            "date_of_birth": "1990-01-01",
            "age": 34,
            "selected_sports": ["Basketball"]
        }
        
        success, response = self.run_test(
            "User Onboarding",
            "PUT",
            "api/user/onboarding",
            200,
            data=onboarding_data
        )
        return success

    def test_fitness_goal(self):
        """Test fitness goal setting"""
        goal_data = {
            "fitness_goal": "Sports",
            "selected_sport": "Basketball"
        }
        
        success, response = self.run_test(
            "Set Fitness Goal",
            "PUT",
            "api/user/fitness-goal",
            200,
            data=goal_data
        )
        return success

    def test_workout_plan_generation(self):
        """Test workout plan generation"""
        success, response = self.run_test(
            "Generate Workout Plan",
            "POST",
            "api/workout/generate-plan",
            200
        )
        return success

    def test_get_current_plan(self):
        """Test getting current workout plan"""
        success, response = self.run_test(
            "Get Current Plan",
            "GET",
            "api/workout/current-plan",
            200
        )
        return success

    def test_get_day_workout(self, day=1):
        """Test getting specific day workout"""
        success, response = self.run_test(
            f"Get Day {day} Workout",
            "GET",
            f"api/workout/day/{day}",
            200
        )
        return success

    def test_complete_day(self, day=1):
        """Test completing a workout day"""
        success, response = self.run_test(
            f"Complete Day {day}",
            "POST",
            f"api/workout/complete-day?day_number={day}",
            200
        )
        return success

    def test_get_progress(self):
        """Test getting workout progress"""
        success, response = self.run_test(
            "Get Progress",
            "GET",
            "api/workout/progress",
            200
        )
        return success

    def test_get_exercises(self):
        """Test getting exercises"""
        success, response = self.run_test(
            "Get Exercises",
            "GET",
            "api/exercises",
            200
        )
        return success

    def test_get_user_profile(self):
        """Test getting user profile"""
        success, response = self.run_test(
            "Get User Profile",
            "GET",
            "api/user/profile",
            200
        )
        return success

    def test_ai_recommendations(self):
        """Test AI recommendations"""
        success, response = self.run_test(
            "AI Recommendations",
            "POST",
            "api/ai/recommendations",
            200
        )
        if success:
            print(f"   AI Response: {response.get('recommendations', 'No recommendations')[:100]}...")
        return success

    def test_with_cookies(self):
        """Test using cookies instead of headers"""
        print("\n🔍 Testing with cookie-based authentication...")
        
        # Create guest session and get cookie
        response = self.session.post(f"{self.base_url}/api/auth/guest")
        
        if response.status_code == 200:
            print("✅ Guest session created with cookies")
            
            # Test profile endpoint with cookies
            profile_response = self.session.get(f"{self.base_url}/api/user/profile")
            if profile_response.status_code == 200:
                print("✅ Profile access with cookies works")
                return True
            else:
                print(f"❌ Profile access failed: {profile_response.status_code}")
        else:
            print(f"❌ Guest session creation failed: {response.status_code}")
        
        return False

def main():
    print("🚀 Starting Fit & Flex API Testing...")
    print("=" * 50)
    
    tester = FitFlexAPITester()
    
    # Test guest authentication first
    if not tester.test_guest_auth():
        print("❌ Guest authentication failed, stopping tests")
        return 1
    
    # Test core user flow
    tester.test_onboarding()
    tester.test_fitness_goal()
    tester.test_workout_plan_generation()
    tester.test_get_current_plan()
    tester.test_get_day_workout(1)
    tester.test_complete_day(1)
    tester.test_get_progress()
    
    # Test other endpoints
    tester.test_get_exercises()
    tester.test_get_user_profile()
    tester.test_ai_recommendations()
    
    # Print results
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {tester.tests_passed}/{tester.tests_run} passed")
    
    if tester.failed_tests:
        print("\n❌ Failed Tests:")
        for test in tester.failed_tests:
            error_msg = test.get('error', f"Expected {test.get('expected')}, got {test.get('actual')}")
            print(f"   - {test['name']}: {error_msg}")
    
    success_rate = (tester.tests_passed / tester.tests_run) * 100 if tester.tests_run > 0 else 0
    print(f"\n📈 Success Rate: {success_rate:.1f}%")
    
    return 0 if success_rate >= 70 else 1

if __name__ == "__main__":
    sys.exit(main())