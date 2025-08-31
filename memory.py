"""
Memory management for Phin AI Assistant
Handles conversation memory and context persistence
"""
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any

class ConversationMemory:
    def __init__(self, memory_file="memory/conversation_memory.json"):
        self.memory_file = memory_file
        self.memory_dir = os.path.dirname(memory_file)
        self.ensure_memory_dir()
        self.memory_data = self.load_memory()
    
    def ensure_memory_dir(self):
        """Ensure memory directory exists"""
        if not os.path.exists(self.memory_dir):
            os.makedirs(self.memory_dir)
    
    def load_memory(self) -> Dict[str, Any]:
        """Load memory from file"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except:
                return self.get_default_memory()
        return self.get_default_memory()
    
    def get_default_memory(self) -> Dict[str, Any]:
        """Get default memory structure"""
        return {
            "user_preferences": {},
            "conversation_topics": [],
            "important_facts": [],
            "user_context": {},
            "last_updated": datetime.now().isoformat()
        }
    
    def save_memory(self):
        """Save memory to file"""
        self.memory_data["last_updated"] = datetime.now().isoformat()
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.memory_data, f, indent=2)
        except Exception as e:
            print(f"Error saving memory: {e}")
    
    def add_user_preference(self, key: str, value: Any):
        """Add or update user preference"""
        self.memory_data["user_preferences"][key] = value
        self.save_memory()
    
    def get_user_preference(self, key: str, default=None):
        """Get user preference"""
        return self.memory_data["user_preferences"].get(key, default)
    
    def add_conversation_topic(self, topic: str, context: str = ""):
        """Add conversation topic to memory"""
        topic_entry = {
            "topic": topic,
            "context": context,
            "timestamp": datetime.now().isoformat()
        }
        self.memory_data["conversation_topics"].append(topic_entry)
        
        # Keep only last 50 topics
        if len(self.memory_data["conversation_topics"]) > 50:
            self.memory_data["conversation_topics"] = self.memory_data["conversation_topics"][-50:]
        
        self.save_memory()
    
    def add_important_fact(self, fact: str, category: str = "general"):
        """Add important fact to memory"""
        fact_entry = {
            "fact": fact,
            "category": category,
            "timestamp": datetime.now().isoformat()
        }
        self.memory_data["important_facts"].append(fact_entry)
        
        # Keep only last 100 facts
        if len(self.memory_data["important_facts"]) > 100:
            self.memory_data["important_facts"] = self.memory_data["important_facts"][-100:]
        
        self.save_memory()
    
    def update_user_context(self, key: str, value: Any):
        """Update user context information"""
        self.memory_data["user_context"][key] = {
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
        self.save_memory()
    
    def get_memory_context(self) -> str:
        """Get formatted memory context for AI"""
        context_parts = []
        
        # User preferences
        if self.memory_data["user_preferences"]:
            context_parts.append("User Preferences:")
            for key, value in self.memory_data["user_preferences"].items():
                context_parts.append(f"- {key}: {value}")
        
        # Recent conversation topics
        recent_topics = self.memory_data["conversation_topics"][-10:]
        if recent_topics:
            context_parts.append("\nRecent Conversation Topics:")
            for topic in recent_topics:
                context_parts.append(f"- {topic['topic']}")
        
        # Important facts
        recent_facts = self.memory_data["important_facts"][-20:]
        if recent_facts:
            context_parts.append("\nImportant Facts:")
            for fact in recent_facts:
                context_parts.append(f"- {fact['fact']} ({fact['category']})")
        
        # User context
        if self.memory_data["user_context"]:
            context_parts.append("\nUser Context:")
            for key, data in self.memory_data["user_context"].items():
                context_parts.append(f"- {key}: {data['value']}")
        
        return "\n".join(context_parts) if context_parts else ""
    
    def analyze_and_store_conversation(self, messages: List[Dict[str, str]]):
        """Analyze conversation and extract important information"""
        if not messages:
            return
        
        # Get recent messages for analysis
        recent_messages = messages[-5:] if len(messages) > 5 else messages
        
        # Extract topics and facts (simple keyword-based approach)
        for message in recent_messages:
            if message["role"] == "user":
                content = message["content"].lower()
                
                # Detect preferences
                if "i like" in content or "i prefer" in content:
                    # Simple preference extraction
                    if "i like" in content:
                        pref = content.split("i like")[1].split(".")[0].strip()
                        self.add_user_preference("likes", pref)
                    elif "i prefer" in content:
                        pref = content.split("i prefer")[1].split(".")[0].strip()
                        self.add_user_preference("prefers", pref)
                
                # Detect important statements
                important_keywords = ["my name is", "i am", "i work", "i study", "i live"]
                for keyword in important_keywords:
                    if keyword in content:
                        fact = content.split(keyword)[1].split(".")[0].strip()
                        self.add_important_fact(f"User {keyword} {fact}", "personal")
                        break
        
        # Add conversation topic based on last user message
        if messages and messages[-1]["role"] == "user":
            last_message = messages[-1]["content"]
            # Extract first sentence as topic
            topic = last_message.split(".")[0][:100]
            self.add_conversation_topic(topic)

# Global memory instance
conversation_memory = ConversationMemory()
