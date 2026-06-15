"""
Test script for MindMate Chatbot
Run this to test the chatbot with sample student stress scenarios
"""

import requests
import json
from typing import Dict

BASE_URL = "http://localhost:8000"

class ChatbotTester:
    """Test the MindMate chatbot with various scenarios"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.user_id = "test_student_001"
    
    def test_api_health(self):
        """Test if API is running"""
        print("\n" + "="*60)
        print("TEST 1: API Health Check")
        print("="*60)
        try:
            response = requests.get(f"{self.base_url}/health")
            print(f"✅ API is running: {response.json()}")
            return True
        except Exception as e:
            print(f"❌ API not responding: {e}")
            return False
    
    def test_chat(self, message: str, scenario_name: str):
        """Test chatbot response"""
        print("\n" + "-"*60)
        print(f"SCENARIO: {scenario_name}")
        print("-"*60)
        print(f"User message: {message}\n")
        
        payload = {
            "user_id": self.user_id,
            "message": message,
            "use_structured_questions": True
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat",
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"🤖 Chatbot Response:")
                print(f"   {result['response']}\n")
                
                print(f"📊 Stress Analysis:")
                print(f"   Level: {result['stress_level']}")
                print(f"   Confidence: {result['confidence_score']:.2f}")
                print(f"   Needs Intervention: {result['needs_intervention']}")
                
                if result['suggested_follow_up']:
                    print(f"\n💡 Suggested Follow-up:")
                    print(f"   {result['suggested_follow_up']}")
                
                if result['stress_context']['possible_triggers']:
                    print(f"\n🎯 Stress Triggers Detected:")
                    for trigger in result['stress_context']['possible_triggers']:
                        print(f"   • {trigger}")
                
                return result
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"❌ Exception: {e}")
            return None
    
    def test_stress_summary(self):
        """Get stress summary for user"""
        print("\n" + "="*60)
        print("STRESS SUMMARY")
        print("="*60)
        
        try:
            response = requests.get(f"{self.base_url}/stress-summary/{self.user_id}")
            
            if response.status_code == 200:
                result = response.json()
                summary = result['summary']
                
                print(f"Total Messages: {summary['total_messages']}")
                print(f"Primary Stress Level: {summary['primary_stress_level']}")
                print(f"Average Stress Score: {summary['average_score']:.2f}")
                print(f"Escalating Pattern: {summary['escalating_pattern']}")
                print(f"Persistent Pattern: {summary.get('persistent_pattern', False)}")
                print(f"Needs Intervention: {summary['needs_intervention']}")
                
                if summary.get('main_stress_triggers'):
                    print(f"\nMain Stress Triggers:")
                    for trigger in summary['main_stress_triggers']:
                        print(f"  • {trigger}")
                
                return result
            else:
                print(f"❌ Error: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Exception: {e}")
            return None
    
    def test_conversation_history(self):
        """Get conversation history"""
        print("\n" + "="*60)
        print("CONVERSATION HISTORY")
        print("="*60)
        
        try:
            response = requests.get(f"{self.base_url}/conversation-history/{self.user_id}")
            
            if response.status_code == 200:
                result = response.json()
                history = result['history']
                
                print(f"Total Messages: {result['total_messages']}")
                print(f"Exchanges: {result['conversation_length']}\n")
                
                for i, msg in enumerate(history[-6:]):
                    role = "👤 Student" if msg['role'] == 'user' else "🤖 MindMate"
                    print(f"{role}: {msg['content'][:100]}...")
                    print()
                
                return result
            else:
                print(f"❌ Error: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Exception: {e}")
            return None
    
    def test_all_scenarios(self):
        """Run through all test scenarios"""
        print("\n" + "🧠" * 30)
        print("MindMate Chatbot Testing Suite")
        print("🧠" * 30)
        
        # Check API
        if not self.test_api_health():
            print("\n❌ API is not running. Please start with: python main.py")
            return
        
        # Test scenarios
        scenarios = [
            (
                "I have an exam next week and I'm really stressed about it. I've studied a bit but I don't feel prepared.",
                "Academic Stress - Exam Anxiety"
            ),
            (
                "I have so many assignments due this week. I feel like I can't manage it all and I'm panicking.",
                "Academic Stress - Workload Overwhelm"
            ),
            (
                "I had a fight with my best friend and now I feel really alone. I don't know how to fix it.",
                "Personal/Social Stress - Friendship Issues"
            ),
            (
                "I haven't been sleeping well because I keep worrying about everything. I'm so tired all the time.",
                "Health Stress - Sleep Problems"
            ),
            (
                "I got a B on my test and I feel like I'm a failure. I need to get all A's to be successful.",
                "Perfectionism and Self-Esteem"
            ),
            (
                "I'm feeling anxious about everything - my grades, my social life, my future. It's hard to focus.",
                "Anxiety and Multiple Stressors"
            )
        ]
        
        for message, scenario in scenarios:
            self.test_chat(message, scenario)
            print()
        
        # Get summary and history
        self.test_conversation_history()
        self.test_stress_summary()
        
        print("\n" + "="*60)
        print("✅ Testing Complete!")
        print("="*60)

# Run tests
if __name__ == "__main__":
    tester = ChatbotTester()
    tester.test_all_scenarios()
