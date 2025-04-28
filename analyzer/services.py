import os
import json
import openai
from dotenv import load_dotenv

load_dotenv()

# Use the API key from .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def get_message_analysis(query):
    """
    Calls the OpenAI API to analyze the tone and intent of a message.
    
    Parameters:
    - query (str): The user's text message to analyze
    
    Returns:
    - dict: Dictionary containing 'tone' and 'intent' keys
    """
    try:
        print(f"Calling OpenAI API for query: {query}")
        
        # Create a more specific prompt for better results
        prompt = f"""
        Analyze this message: "{query}"
        
        First, identify the emotional tone. Choose one: 
        Neutral, Happy, Sad, Angry, Urgent, Confused, Curious, Hungry, Frustrated, Polite
        
        Second, identify the main intent. Choose one:
        Order Food, Find Recipe, Track Order, Need Help, Set Reminder, Read Reviews, Account Help, Share News, Unknown
        
        Format your response exactly like this:
        Tone: [selected tone]
        Intent: [selected intent]
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can use "gpt-4" for better results if you have access
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes messages to determine tone and intent."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # Lower temperature for more predictable results
            max_tokens=100
        )
        
        # Extract the response text
        if response and response.choices:
            text = response.choices[0].message.content
            print(f"Generated text: {text}")
            
            # Parse the response to extract tone and intent
            analysis = {}
            
            # Extract tone
            if "tone:" in text.lower():
                tone_text = text.lower().split("tone:")[1].split("\n")[0].strip()
                # Clean up any extra text that might be after the tone
                tone_text = tone_text.split(",")[0].strip() if "," in tone_text else tone_text
                analysis["tone"] = tone_text.capitalize()
            else:
                analysis["tone"] = "Neutral"  # Default
            
            # Extract intent
            if "intent:" in text.lower():
                intent_text = text.lower().split("intent:")[1].strip()
                # Clean up any line breaks
                intent_text = intent_text.split("\n")[0].strip()
                analysis["intent"] = intent_text.capitalize()
            else:
                analysis["intent"] = "Unknown"  # Default
            
            return analysis
        
        # Fall back to rule-based analysis if API call fails
        print("Falling back to rule-based analysis")
        return rule_based_analysis(query)
        
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return rule_based_analysis(query)

def rule_based_analysis(query):
    """
    A rule-based system for analyzing message tone and intent when the OpenAI API fails.
    
    Parameters:
    - query (str): The user's text message to analyze
    
    Returns:
    - dict: Dictionary containing 'tone' and 'intent' keys
    """
    query_lower = query.lower()
    
    # Intent detection with improved keyword matching
    intent = "Unknown"
    
    # Food related intents
    if any(word in query_lower for word in ["food", "pizza", "order", "eat", "hungry", "dinner", "lunch", "breakfast"]):
        intent = "Order Food"
    # Tracking related intents
    elif any(word in query_lower for word in ["track", "where", "delivery", "status", "arrived"]):
        intent = "Track Order"
    # Help related intents
    elif any(word in query_lower for word in ["help", "support", "assist", "problem", "issue", "trouble"]):
        intent = "Need Help"
    # Reminder related intents
    elif any(word in query_lower for word in ["remind", "remember", "forget", "later", "tomorrow", "tonight"]):
        intent = "Set Reminder"
    # Recipe related intents
    elif any(word in query_lower for word in ["recipe", "cook", "make", "homemade", "prepare"]):
        intent = "Find Recipe"
    # Review related intents
    elif any(word in query_lower for word in ["review", "rating", "star", "good", "bad", "recommend"]):
        intent = "Read Reviews"
    # Account related intents
    elif any(word in query_lower for word in ["account", "password", "login", "sign in", "register"]):
        intent = "Account Help"
    # News related intents
    elif any(word in query_lower for word in ["news", "share", "article", "story"]):
        intent = "Share News"
    
    # Enhanced tone detection
    tone = "Neutral"  # Default tone
    
    # Urgency indicators
    if any(word in query_lower for word in ["urgent", "immediately", "right now", "asap", "hurry", "emergency", "quick"]):
        tone = "Urgent"
    # Frustration indicators
    elif any(word in query_lower for word in ["frustrated", "annoyed", "upset", "angry", "mad", "waited", "already", "still waiting"]):
        tone = "Frustrated"
    # Happiness indicators
    elif any(word in query_lower for word in ["happy", "glad", "pleased", "delighted", "wonderful", "great", "excellent"]):
        tone = "Happy"
    # Sadness indicators
    elif any(word in query_lower for word in ["sad", "disappointed", "unhappy", "sorry"]):
        tone = "Sad"
    # Curiosity indicators
    elif any(word in query_lower for word in ["curious", "wondering", "how to", "can i", "is it possible", "learn"]):
        tone = "Curious"
    # Confusion indicators
    elif any(word in query_lower for word in ["confused", "don't understand", "unclear", "what does", "how does"]):
        tone = "Confused"
    # Hunger indicators
    elif any(word in query_lower for word in ["hungry", "starving", "famished", "want food", "want to eat"]):
        tone = "Hungry"
    # Politeness indicators
    elif any(word in query_lower for word in ["please", "thank you", "grateful", "appreciate"]):
        tone = "Polite"
    
    return {"tone": tone, "intent": intent}