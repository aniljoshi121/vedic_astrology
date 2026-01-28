import requests
import sys
import json
from datetime import datetime

class VedicAstrologyAPITester:
    def __init__(self, base_url="https://astrocraft-1.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.chart_id = None
        self.session_id = f"test_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    def run_test(self, name, method, endpoint, expected_status, data=None, params=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)

            print(f"   Status: {response.status_code}")
            
            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - {name}")
                try:
                    return success, response.json()
                except:
                    return success, response.text
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_root_endpoint(self):
        """Test API root endpoint"""
        return self.run_test("API Root", "GET", "", 200)

    def test_birth_chart_calculation(self):
        """Test birth chart calculation"""
        test_data = {
            "name": "Test User",
            "gender": "Male",
            "date_of_birth": "15-08-1990",
            "time_of_birth": "14:30",
            "place_of_birth": "Mumbai, Maharashtra, India"
        }
        
        success, response = self.run_test(
            "Birth Chart Calculation",
            "POST",
            "birth-chart",
            200,
            data=test_data
        )
        
        if success and isinstance(response, dict) and 'id' in response:
            self.chart_id = response['id']
            print(f"   Chart ID saved: {self.chart_id}")
            
            # Validate response structure
            required_fields = ['name', 'lagna', 'moon_rashi', 'nakshatra', 'planets', 'houses']
            missing_fields = [field for field in required_fields if field not in response]
            if missing_fields:
                print(f"   ⚠️  Missing fields: {missing_fields}")
            else:
                print(f"   ✅ All required fields present")
        
        return success

    def test_get_birth_chart(self):
        """Test retrieving a saved birth chart"""
        if not self.chart_id:
            print("❌ Skipping - No chart ID available")
            return False
            
        return self.run_test(
            "Get Birth Chart",
            "GET",
            f"birth-chart/{self.chart_id}",
            200
        )[0]

    def test_kundli_matching(self):
        """Test Kundli matching calculation"""
        test_data = {
            "person1": {
                "name": "Person 1",
                "gender": "Male",
                "date_of_birth": "15-08-1990",
                "time_of_birth": "14:30",
                "place_of_birth": "Mumbai, Maharashtra, India"
            },
            "person2": {
                "name": "Person 2",
                "gender": "Female",
                "date_of_birth": "20-05-1992",
                "time_of_birth": "10:00",
                "place_of_birth": "Delhi, India"
            }
        }
        
        success, response = self.run_test(
            "Kundli Matching",
            "POST",
            "kundli-matching",
            200,
            data=test_data
        )
        
        if success and isinstance(response, dict):
            matching_result = response.get('matching_result', {})
            if 'total_score' in matching_result and 'kootas' in matching_result:
                print(f"   ✅ Gun Milan Score: {matching_result['total_score']}/36")
                print(f"   ✅ Kootas count: {len(matching_result['kootas'])}")
            else:
                print(f"   ⚠️  Missing matching result fields")
        
        return success

    def test_daily_horoscope(self):
        """Test daily horoscope generation"""
        test_rashis = ['Aries', 'Leo', 'Scorpio']
        
        for rashi in test_rashis:
            success, response = self.run_test(
                f"Daily Horoscope - {rashi}",
                "GET",
                f"daily-horoscope/{rashi}",
                200
            )
            
            if success and isinstance(response, dict):
                required_fields = ['career', 'finance', 'health', 'relationships', 'lucky_number']
                missing_fields = [field for field in required_fields if field not in response]
                if missing_fields:
                    print(f"   ⚠️  Missing fields: {missing_fields}")
                else:
                    print(f"   ✅ All horoscope fields present")
            
            if not success:
                return False
        
        return True

    def test_ai_chat(self):
        """Test AI chat functionality"""
        test_message = {
            "message": "What does my birth chart say about my personality?",
            "session_id": self.session_id,
            "chart_id": self.chart_id
        }
        
        success, response = self.run_test(
            "AI Chat",
            "POST",
            "chat",
            200,
            data=test_message
        )
        
        if success and isinstance(response, dict):
            if 'response' in response and 'session_id' in response:
                print(f"   ✅ AI Response length: {len(response['response'])} chars")
                print(f"   ✅ Session ID: {response['session_id']}")
            else:
                print(f"   ⚠️  Missing response fields")
        
        return success

    def test_pdf_generation(self):
        """Test PDF generation"""
        if not self.chart_id:
            print("❌ Skipping - No chart ID available")
            return False
            
        success, response = self.run_test(
            "PDF Generation",
            "POST",
            f"generate-pdf/{self.chart_id}",
            200
        )
        
        if success:
            print(f"   ✅ PDF generated successfully")
        
        return success

    def test_chat_history(self):
        """Test chat history retrieval"""
        success, response = self.run_test(
            "Chat History",
            "GET",
            f"chat-history/{self.session_id}",
            200
        )
        
        if success and isinstance(response, dict):
            if 'messages' in response:
                print(f"   ✅ Chat history retrieved: {len(response['messages'])} messages")
            else:
                print(f"   ⚠️  Missing messages field")
        
        return success

def main():
    print("🚀 Starting Vedic Astrology API Tests")
    print("=" * 50)
    
    tester = VedicAstrologyAPITester()
    
    # Test sequence
    tests = [
        ("API Root", tester.test_root_endpoint),
        ("Birth Chart Calculation", tester.test_birth_chart_calculation),
        ("Get Birth Chart", tester.test_get_birth_chart),
        ("Kundli Matching", tester.test_kundli_matching),
        ("Daily Horoscope", tester.test_daily_horoscope),
        ("AI Chat", tester.test_ai_chat),
        ("PDF Generation", tester.test_pdf_generation),
        ("Chat History", tester.test_chat_history)
    ]
    
    failed_tests = []
    
    for test_name, test_func in tests:
        try:
            if not test_func():
                failed_tests.append(test_name)
        except Exception as e:
            print(f"❌ {test_name} - Exception: {str(e)}")
            failed_tests.append(test_name)
    
    # Print results
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {tester.tests_passed}/{tester.tests_run} passed")
    print(f"✅ Success Rate: {(tester.tests_passed/tester.tests_run)*100:.1f}%")
    
    if failed_tests:
        print(f"\n❌ Failed Tests:")
        for test in failed_tests:
            print(f"   - {test}")
    else:
        print(f"\n🎉 All tests passed!")
    
    return 0 if len(failed_tests) == 0 else 1

if __name__ == "__main__":
    sys.exit(main())