import random
import string
from typing import Dict

def generate_profile() -> Dict[str, str]:
    """
    Generates a fake victim profile for simulation purposes.
    """
    names = ['Alex', 'Jordan', 'Taylor', 'Morgan', 'Casey', 'Riley', 'Skyler', 'Quinn']
    locations = ['New York', 'London', 'Berlin', 'Sydney', 'Toronto', 'Tokyo', 'Paris']
    username = random.choice(names) + str(random.randint(100, 999))
    location = random.choice(locations)
    email = username.lower() + '@example.com'
    profile = {
        'username': username,
        'location': location,
        'email': email,
        'session_id': ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    }
    return profile 