import os
import jwt
from datetime import datetime, timedelta

# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------
# Secret key for signing JWT tokens.
# Make sure to set it in your environment:
#   export SECRET_KEY="your_secret_here"   (Linux/macOS)
#   setx SECRET_KEY "your_secret_here"     (Windows)
# -------------------------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY")

# -------------------------------------------------------------------
# Mock calendar data structure
# -------------------------------------------------------------------
# A simple in-memory representation of available sales and service agents.
# Each agent has a list of booked appointment slots (as datetime strings).
# -------------------------------------------------------------------
MOCK_CALENDAR = {
    "Sales": {
        "Sarah Johnson": [],
        "Mike Rodriguez": [],
        "Jennifer Chen": []
    },
    "Service": {
        "Tom Wilson": [],
        "Lisa Martinez": [],
        "David Park": []
    }
}


def create_session(user_id: str) -> str:
    """
    Create a JWT session token for a given user.

    Args:
        user_id (str): Unique identifier of the user.

    Returns:
        str: Encoded JWT token valid for 1 hour.
    """
    payload = {
        "user_id": user_id,
        "exp": datetime.now() + timedelta(hours=1)  # token expiration
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def verify_session(token: str) -> bool:
    """
    Validate a JWT session token.

    Args:
        token (str): JWT token to validate.

    Returns:
        bool: True if token is valid and not expired, False otherwise.
    """
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return True
    except jwt.ExpiredSignatureError:
        # Token has expired
        return False
    except jwt.InvalidTokenError:
        # Token is malformed or invalid
        return False

def get_availability(agent_name: str) -> list[str]:
    """
    Get the next 5 available appointment slots for an agent.

    Slots are spaced at 1-hour intervals from the current time.

    Args:
        agent_name (str): Name of the agent.

    Returns:
        list[str]: List of available slot strings (YYYY-MM-DD HH:MM).
    """
    now = datetime.now()
    slots = []
    for i in range(1, 6):  # next 5 hours
        slot = now + timedelta(hours=i)
        slot_str = slot.strftime("%Y-%m-%d %H:%M")

        # Check if slot is already booked in either Sales or Service calendars
        if slot_str not in MOCK_CALENDAR["Sales"].get(agent_name, []) \
           and slot_str not in MOCK_CALENDAR["Service"].get(agent_name, []):
            slots.append(slot_str)
    return slots


def book_appointment(agent_type: str, agent_name: str, time_slot: str) -> str:
    """
    Book an appointment with a given agent if the slot is free.

    Args:
        agent_type (str): "Sales" or "Service".
        agent_name (str): Name of the agent.
        time_slot (str): Desired slot in format YYYY-MM-DD HH:MM.

    Returns:
        str: Confirmation or error message.
    """
    user_token=SECRET_KEY
    # Verify user session before booking
    if not verify_session(user_token):
        return "❌ Invalid or expired session."

    # Check if agent exists in the mock calendar
    if agent_type not in MOCK_CALENDAR or agent_name not in MOCK_CALENDAR[agent_type]:
        return f"❌ Agent {agent_name} not found."

    # Check if the slot is already booked
    if time_slot in MOCK_CALENDAR[agent_type][agent_name]:
        return f"❌ Slot {time_slot} is already booked."

    # Book the appointment
    MOCK_CALENDAR[agent_type][agent_name].append(time_slot)
    return f"✅ Appointment booked with {agent_name} ({agent_type}) at {time_slot}"