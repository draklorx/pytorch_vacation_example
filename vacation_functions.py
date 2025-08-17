def _format_response_message(matching_spots, weather, activity):
    """
    Formats the response string with matching vacation spots.
    
    Parameters:
        - matching_spots (list): List of matching vacation spot dictionaries.
        - weather (str or None): The weather preference if specified.
        - activity (str or None): The activity preference if specified.

    Returns:
        - str: A formatted message with matching vacation spots or a not found message.
    """
    if not matching_spots:
        return f"Sorry, I couldn't find any vacation spots."

    response_parts = []
    if weather:
        response_parts.append(f"{weather} weather")
    if activity:
        response_parts.append(f"{activity} activities")
    
    # Join parts with " and "
    response = "Here are some vacation spots with " + " and ".join(response_parts) + ":\n"

    for spot in matching_spots:
        # If an activity type is specified, list only those activities. Otherwise, list all.
        if activity:
            activities = [act['name'] for act in spot.get('activities', []) if act.get('type') == activity]
        else:
            activities = [act['name'] for act in spot.get('activities', [])]
        response += f"- {spot['name']}: {', '.join(activities)}\n"

    return response

def _find_and_format_spots(session_state, vacation_spots):
    """
    Finds matching spots based on session state and formats the output.
    
    Parameters:
        - session_state (dict): The current session state with preferences.
        - vacation_spots (list): List of vacation spot dictionaries.
    
    Returns:
        - str: A formatted message with matching vacation spots or a not found message.
    """
    weather_pref = session_state.get("weather_preference")
    activity_pref = session_state.get("activity_preference")

    matching_spots = vacation_spots

    if weather_pref:
        matching_spots = [spot for spot in matching_spots if spot.get("weather") == weather_pref]
    
    if activity_pref:
        matching_spots = [
            spot for spot in matching_spots 
            if any(act.get("type") == activity_pref for act in spot.get("activities", []))
        ]
    
    return _format_response_message(matching_spots, weather_pref, activity_pref)

def find_vacation_by_weather(weather, session_state, vacation_spots):
    """
    Find vacation spots based on weather preference.

    Parameters:
        - weather (str): The preferred weather type (e.g., "sunny", "snowy").
        - session_state (dict): The current session state to store preferences.
        - vacation_spots (list): List of vacation spot dictionaries with weather info.

    Returns:
        - str: A message with matching vacation spots or a not found message.

    """
    session_state["weather_preference"] = weather
    response = _find_and_format_spots(session_state, vacation_spots)
    if session_state["activity_preference"] == "adventure":
        response += "\nWould you like to look at relaxing activities instead?\n"
    elif session_state["activity_preference"] == "relaxation":
        response += "\nWould you like to look at adventurous activities instead?\n"
    else:
        response += "\nWould you like to narrow it down by activity? You could go for an adventure, or relaxation.\n"
        
    return response

def find_vacation_by_activity(activity, session_state, vacation_spots):
    """
    Find vacation spots based on activity preference.

    Parameters:
        - activity (str): The preferred activity type (e.g., "adventure", "relaxation").
        - session_state (dict): The current session state to store preferences.
        - vacation_spots (list): List of vacation spot dictionaries with activity info.

    Returns:
        - str: A message with matching vacation spots or a not found message.
    """
    session_state["activity_preference"] = activity
    response = _find_and_format_spots(session_state, vacation_spots)
    if session_state["weather_preference"] == "sunny":
        response += "\nWould you like to look at snowy destinations instead?\n"
    elif session_state["weather_preference"] == "snowy":
        response += "\nWould you like to look at sunny destinations instead?\n"
    else:
        response += "\nWould you like to narrow it down by weather? You could go somewhere sunny, or snowy.\n"

    return response