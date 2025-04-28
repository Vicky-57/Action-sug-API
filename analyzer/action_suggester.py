# analyzer/action_suggester.py

# Expanded predefined actions with more options
ACTIONS = {
    "ORDER_FOOD": {
        "action_code": "ORDER_FOOD",
        "display_text": "Order food online"
    },
    "FIND_RECIPE": {
        "action_code": "FIND_RECIPE",
        "display_text": "Find recipes"
    },
    "FIND_NEARBY_RESTAURANT": {
        "action_code": "FIND_NEARBY_RESTAURANT",
        "display_text": "Find nearby restaurants"
    },
    "TRACK_ORDER": {
        "action_code": "TRACK_ORDER",
        "display_text": "Track your order"
    },
    "CALL_RESTAURANT": {
        "action_code": "CALL_RESTAURANT",
        "display_text": "Call a restaurant"
    },
    "READ_REVIEWS": {
        "action_code": "READ_REVIEWS",
        "display_text": "Read restaurant reviews"
    },
    "SHARE_LOCATION": {
        "action_code": "SHARE_LOCATION",
        "display_text": "Share your location"
    },
    "SET_REMINDER": {
        "action_code": "SET_REMINDER",
        "display_text": "Set a reminder"
    },
    "SEARCH_WEB": {
        "action_code": "SEARCH_WEB",
        "display_text": "Search the web"
    },
    "ASK_HELP": {
        "action_code": "ASK_HELP",
        "display_text": "Ask for help"
    },
    "SHARE_NEWS": {
        "action_code": "SHARE_NEWS",
        "display_text": "Share news"
    },
    "CONTACT_SUPPORT": {
        "action_code": "CONTACT_SUPPORT",
        "display_text": "Contact customer support"
    },
    "FIND_NEARBY_PIZZERIA": {
        "action_code": "FIND_NEARBY_PIZZERIA",
        "display_text": "Find nearby pizza restaurants"
    },
    "PLACE_ONLINE_ORDER": {
        "action_code": "PLACE_ONLINE_ORDER",
        "display_text": "Place an online pizza order"
    },
    "VIEW_MENU": {
        "action_code": "VIEW_MENU",
        "display_text": "View restaurant menu"
    },
    "CHECK_OPENING_HOURS": {
        "action_code": "CHECK_OPENING_HOURS",
        "display_text": "Check restaurant opening hours"
    },
    "APPLY_DISCOUNT": {
        "action_code": "APPLY_DISCOUNT",
        "display_text": "Apply discount code"
    },
    "SAVE_FAVORITE": {
        "action_code": "SAVE_FAVORITE",
        "display_text": "Save to favorites"
    },
    "SEND_FEEDBACK": {
        "action_code": "SEND_FEEDBACK",
        "display_text": "Send feedback"
    },
    "RATE_EXPERIENCE": {
        "action_code": "RATE_EXPERIENCE", 
        "display_text": "Rate your experience"
    }
}

# Expanded intent-to-actions mapping with more options
INTENT_ACTIONS = {
    "Order Food": ["ORDER_FOOD", "FIND_NEARBY_RESTAURANT", "PLACE_ONLINE_ORDER", "VIEW_MENU"],
    "Find Recipe": ["FIND_RECIPE", "SEARCH_WEB", "SAVE_FAVORITE", "SHARE_NEWS"],
    "Track Order": ["TRACK_ORDER", "CONTACT_SUPPORT", "SHARE_LOCATION", "SEND_FEEDBACK"],
    "Need Help": ["ASK_HELP", "CONTACT_SUPPORT", "SEARCH_WEB", "SEND_FEEDBACK"],
    "Set Reminder": ["SET_REMINDER", "SAVE_FAVORITE", "SEARCH_WEB", "CHECK_OPENING_HOURS"],
    "Read Reviews": ["READ_REVIEWS", "FIND_NEARBY_RESTAURANT", "RATE_EXPERIENCE", "SEND_FEEDBACK"],
    "Account Help": ["CONTACT_SUPPORT", "ASK_HELP", "SEARCH_WEB", "SEND_FEEDBACK"],
    "Share News": ["SHARE_NEWS", "SEARCH_WEB", "SAVE_FAVORITE", "SEND_FEEDBACK"],
    "Unknown": ["SEARCH_WEB", "ASK_HELP", "CONTACT_SUPPORT", "SET_REMINDER"]
}

# Specific keywords for more granular matching
KEYWORD_ACTIONS = {
    "pizza": ["FIND_NEARBY_PIZZERIA", "PLACE_ONLINE_ORDER", "VIEW_MENU", "READ_REVIEWS"],
    "delivery": ["TRACK_ORDER", "SHARE_LOCATION", "CONTACT_SUPPORT", "RATE_EXPERIENCE"],
    "recipe": ["FIND_RECIPE", "SAVE_FAVORITE", "SEARCH_WEB", "SHARE_NEWS"],
    "review": ["READ_REVIEWS", "RATE_EXPERIENCE", "FIND_NEARBY_RESTAURANT", "SEND_FEEDBACK"],
    "restaurant": ["FIND_NEARBY_RESTAURANT", "CALL_RESTAURANT", "VIEW_MENU", "CHECK_OPENING_HOURS"],
    "location": ["SHARE_LOCATION", "FIND_NEARBY_RESTAURANT", "FIND_NEARBY_PIZZERIA", "SEARCH_WEB"],
    "discount": ["APPLY_DISCOUNT", "PLACE_ONLINE_ORDER", "VIEW_MENU", "SAVE_FAVORITE"],
    "menu": ["VIEW_MENU", "FIND_NEARBY_RESTAURANT", "ORDER_FOOD", "CHECK_OPENING_HOURS"]
}

# Tone modifiers - actions to add or prioritize based on tone
TONE_MODIFIERS = {
    "urgent": ["CONTACT_SUPPORT", "TRACK_ORDER", "CALL_RESTAURANT"],
    "frustrated": ["CONTACT_SUPPORT", "SEND_FEEDBACK", "CALL_RESTAURANT"],
    "hungry": ["ORDER_FOOD", "FIND_NEARBY_RESTAURANT", "PLACE_ONLINE_ORDER"],
    "curious": ["SEARCH_WEB", "READ_REVIEWS", "VIEW_MENU"],
    "confused": ["ASK_HELP", "CONTACT_SUPPORT", "SEARCH_WEB"],
    "happy": ["RATE_EXPERIENCE", "SAVE_FAVORITE", "SHARE_NEWS"],
    "polite": ["SEND_FEEDBACK", "RATE_EXPERIENCE"]
}

def suggest_actions(tone, intent):
    """
    Returns up to 4 suggested actions based on the identified tone and intent.
    
    Parameters:
    - tone (str): The detected emotional tone (e.g., 'Urgent', 'Happy')
    - intent (str): The detected user intent (e.g., 'Order Food', 'Need Help')
    
    Returns:
    - list: List of up to 4 suggested action dictionaries
    """
    suggested_actions = []
    
    # First, try to match the intent directly
    matched_intent = None
    for known_intent, actions in INTENT_ACTIONS.items():
        if known_intent.lower() in intent.lower() or intent.lower() in known_intent.lower():
            matched_intent = known_intent
            # Take the first three actions from the matched intent
            for action_code in actions[:3]:
                if action_code in ACTIONS and ACTIONS[action_code] not in suggested_actions:
                    suggested_actions.append(ACTIONS[action_code])
            break
    
    # If no intent match or not enough actions, look for specific keywords
    if len(suggested_actions) < 3:
        intent_lower = intent.lower()
        for keyword, actions in KEYWORD_ACTIONS.items():
            if keyword in intent_lower:
                for action_code in actions:
                    if action_code in ACTIONS and ACTIONS[action_code] not in suggested_actions:
                        suggested_actions.append(ACTIONS[action_code])
                        if len(suggested_actions) >= 3:
                            break
                if len(suggested_actions) >= 3:
                    break
    
    # Enhance with tone-based modifiers
    if tone:
        tone_lower = tone.lower()
        
        # Check if the tone matches any of our known modifiers
        for tone_key, tone_actions in TONE_MODIFIERS.items():
            if tone_key in tone_lower:
                # Try to add tone-specific actions
                for action_code in tone_actions:
                    if action_code in ACTIONS and ACTIONS[action_code] not in suggested_actions:
                        if len(suggested_actions) < 4:
                            suggested_actions.append(ACTIONS[action_code])
                        else:
                            # If we already have 4 suggestions, replace the last one
                            # with a tone-specific action to prioritize it
                            suggested_actions[3] = ACTIONS[action_code]
                        break
                break
    
    # Default if no actions found
    if not suggested_actions:
        suggested_actions = [ACTIONS["SEARCH_WEB"], ACTIONS["ASK_HELP"], 
                            ACTIONS["CONTACT_SUPPORT"], ACTIONS["SET_REMINDER"]]
    
    # Return up to 4 suggestions
    return suggested_actions[:4]