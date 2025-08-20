def calculate_risk_score(data):
    """
    Calculate a simple risk score based on which fields are filled.
    Returns a tuple: (score, risk_level)
    """
    score = 0
    max_score = 6  # Number of key fields
    if data.get('clipboard'): score += 1
    if data.get('username'): score += 1
    if data.get('password'): score += 1
    if data.get('system_info'): score += 1
    if data.get('file_uploaded'): score += 1
    if data.get('website'): score += 1
    percent = int((score / max_score) * 100)
    if percent >= 80:
        risk = 'High'
    elif percent >= 50:
        risk = 'Medium'
    else:
        risk = 'Low'
    return percent, risk 