"""
Stress Analyzer - Enhanced Version
Analyzes user messages for stress indicators and patterns
"""

from typing import Dict, List, Tuple
from datetime import datetime
from enum import Enum

class StressLevel(str, Enum):
    """Stress level categories"""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"

class StressAnalyzer:
    """Analyzes stress indicators and patterns in user messages"""
    
    # Keywords indicating different stress levels
    CRITICAL_KEYWORDS = [
        "suicide", "harm", "hurt myself", "self-harm", "kill myself",
        "overdose", "cutting", "extreme pain", "unbearable", "can't take it",
        "want to die", "end it all", "don't want to live", "worthless",
        "nobody cares", "no point", "give up", "life is pointless"
    ]
    
    HIGH_STRESS_KEYWORDS = [
        "anxious", "panic", "terrified", "overwhelmed", "breakdown",
        "failing", "disaster", "worst", "can't cope", "desperate",
        "struggling", "hopeless", "exhausted", "burned out",
        "crying", "can't breathe", "chest pain", "very worried",
        "constantly anxious", "can't function", "falling apart"
    ]
    
    MODERATE_STRESS_KEYWORDS = [
        "stressed", "worried", "concerned", "tired", "pressure",
        "deadline", "exam", "assignment", "difficulty", "challenge",
        "nervous", "uneasy", "frustrated", "annoyed",
        "procrastinating", "behind", "struggling with",
        "not confident", "scared of failing"
    ]
    
    # Academic stress keywords
    ACADEMIC_KEYWORDS = [
        "exam", "test", "assignment", "project", "homework",
        "grade", "study", "school", "class", "subject",
        "professor", "teacher", "lecture", "midterm", "final",
        "essay", "research paper", "deadline", "gpa"
    ]
    
    # Personal/relationship stress keywords
    PERSONAL_KEYWORDS = [
        "friend", "relationship", "family", "parent", "social",
        "lonely", "alone", "bullied", "cyberbully", "argument",
        "conflict", "broken up", "cheated", "betrayed",
        "rejected", "embarrassed", "awkward", "peer pressure"
    ]
    
    # Sleep/health keywords
    HEALTH_KEYWORDS = [
        "sleep", "insomnia", "tired", "exhausted", "fatigue",
        "headache", "migraine", "stomach", "nauseous",
        "can't sleep", "nightmare", "no energy"
    ]
    
    # Perfectionism keywords
    PERFECTIONISM_KEYWORDS = [
        "perfectionist", "not good enough", "failure", "must be perfect",
        "can't make mistakes", "all or nothing", "disappointed in myself"
    ]
    
    def __init__(self):
        self.user_messages: List[Dict] = []
        self.user_contexts: Dict[str, str] = {}  # Track what user is stressed about
    
    def analyze_message(self, message: str) -> Tuple[StressLevel, float, Dict]:
        """
        Analyze a message for stress indicators.
        Returns: (stress_level, confidence_score, context_dict)
        """
        message_lower = message.lower()
        
        # Initialize context
        context = {
            "stress_type": "general",
            "keywords_found": [],
            "possible_triggers": []
        }
        
        # Check critical keywords
        if any(keyword in message_lower for keyword in self.CRITICAL_KEYWORDS):
            context["stress_type"] = "critical"
            context["keywords_found"] = [k for k in self.CRITICAL_KEYWORDS if k in message_lower]
            return StressLevel.CRITICAL, 0.95, context
        
        # Check high stress keywords
        if any(keyword in message_lower for keyword in self.HIGH_STRESS_KEYWORDS):
            context["stress_type"] = "high"
            context["keywords_found"] = [k for k in self.HIGH_STRESS_KEYWORDS if k in message_lower]
            
            # Identify triggers
            if any(k in message_lower for k in self.ACADEMIC_KEYWORDS):
                context["possible_triggers"].append("academic")
            if any(k in message_lower for k in self.PERSONAL_KEYWORDS):
                context["possible_triggers"].append("personal/social")
            if any(k in message_lower for k in self.HEALTH_KEYWORDS):
                context["possible_triggers"].append("health/sleep")
                
            return StressLevel.HIGH, 0.85, context
        
        # Check moderate stress keywords
        if any(keyword in message_lower for keyword in self.MODERATE_STRESS_KEYWORDS):
            context["stress_type"] = "moderate"
            context["keywords_found"] = [k for k in self.MODERATE_STRESS_KEYWORDS if k in message_lower]
            
            # Identify triggers
            if any(k in message_lower for k in self.ACADEMIC_KEYWORDS):
                context["possible_triggers"].append("academic")
            if any(k in message_lower for k in self.PERSONAL_KEYWORDS):
                context["possible_triggers"].append("personal/social")
            if any(k in message_lower for k in self.HEALTH_KEYWORDS):
                context["possible_triggers"].append("health/sleep")
            if any(k in message_lower for k in self.PERFECTIONISM_KEYWORDS):
                context["possible_triggers"].append("perfectionism")
                
            return StressLevel.MODERATE, 0.70, context
        
        return StressLevel.LOW, 0.30, context
    
    def store_message(self, user_id: str, message: str):
        """Store message for pattern analysis"""
        stress_level, score, context = self.analyze_message(message)
        self.user_messages.append({
            "user_id": user_id,
            "message": message,
            "stress_level": stress_level,
            "confidence": score,
            "context": context,
            "timestamp": datetime.now()
        })
        
        # Update user context
        if context["possible_triggers"]:
            self.user_contexts[user_id] = ", ".join(context["possible_triggers"])
    
    def detect_escalating_pattern(self, user_id: str, window: int = 5) -> bool:
        """
        Detect if user is showing escalating stress patterns.
        Returns True if there's a consistent escalation in stress levels.
        """
        user_msgs = [m for m in self.user_messages if m["user_id"] == user_id]
        recent_msgs = user_msgs[-window:] if len(user_msgs) >= window else user_msgs
        
        if len(recent_msgs) < 3:
            return False
        
        # Check if stress levels are escalating
        stress_scores = [
            {"low": 1, "moderate": 2, "high": 3, "critical": 4}[m["stress_level"]]
            for m in recent_msgs
        ]
        
        # Simple escalation detection
        escalation_count = 0
        for i in range(1, len(stress_scores)):
            if stress_scores[i] > stress_scores[i-1]:
                escalation_count += 1
        
        # If more than 50% of transitions are escalations, flag pattern
        return escalation_count > len(stress_scores) / 2
    
    def detect_persistent_pattern(self, user_id: str, window: int = 5) -> bool:
        """
        Detect if user has persistent high stress (not necessarily escalating).
        Returns True if most recent messages show high or critical stress.
        """
        user_msgs = [m for m in self.user_messages if m["user_id"] == user_id]
        recent_msgs = user_msgs[-window:] if len(user_msgs) >= window else user_msgs
        
        if len(recent_msgs) < 3:
            return False
        
        # Count high and critical stress messages
        high_or_critical = sum(
            1 for m in recent_msgs 
            if m["stress_level"] in [StressLevel.HIGH, StressLevel.CRITICAL]
        )
        
        # If more than 60% are high/critical, flag persistent pattern
        return high_or_critical > len(recent_msgs) * 0.6
    
    def needs_immediate_intervention(self, user_id: str) -> bool:
        """Check if user needs immediate counselor intervention"""
        # Get most recent message
        user_msgs = [m for m in self.user_messages if m["user_id"] == user_id]
        
        if not user_msgs:
            return False
        
        latest = user_msgs[-1]
        
        # Intervention needed if:
        # 1. Critical stress level detected
        # 2. High stress + escalating pattern
        # 3. High stress + persistent pattern
        if latest["stress_level"] == StressLevel.CRITICAL:
            return True
        
        if latest["stress_level"] == StressLevel.HIGH:
            return (self.detect_escalating_pattern(user_id) or 
                    self.detect_persistent_pattern(user_id))
        
        return False
    
    def get_user_stress_summary(self, user_id: str) -> Dict:
        """Get summary of user's stress indicators"""
        user_msgs = [m for m in self.user_messages if m["user_id"] == user_id]
        
        if not user_msgs:
            return {
                "total_messages": 0,
                "primary_stress_level": StressLevel.LOW,
                "average_score": 0,
                "escalating_pattern": False,
                "persistent_pattern": False,
                "needs_intervention": False,
                "main_stress_triggers": []
            }
        
        stress_levels = [m["stress_level"] for m in user_msgs]
        scores = [m["confidence"] for m in user_msgs]
        
        # Determine primary stress level
        level_counts = {
            StressLevel.CRITICAL: stress_levels.count(StressLevel.CRITICAL),
            StressLevel.HIGH: stress_levels.count(StressLevel.HIGH),
            StressLevel.MODERATE: stress_levels.count(StressLevel.MODERATE),
            StressLevel.LOW: stress_levels.count(StressLevel.LOW),
        }
        
        primary_level = max(level_counts, key=level_counts.get)
        
        # Get main stress triggers
        main_triggers = self.user_contexts.get(user_id, "").split(", ") if user_id in self.user_contexts else []
        main_triggers = [t for t in main_triggers if t]  # Remove empty strings
        
        return {
            "total_messages": len(user_msgs),
            "primary_stress_level": primary_level,
            "average_score": sum(scores) / len(scores) if scores else 0,
            "escalating_pattern": self.detect_escalating_pattern(user_id),
            "persistent_pattern": self.detect_persistent_pattern(user_id),
            "needs_intervention": self.needs_immediate_intervention(user_id),
            "main_stress_triggers": main_triggers
        }

# Initialize stress analyzer
stress_analyzer = StressAnalyzer()
