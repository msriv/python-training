
def is_valid_score(score):
    """Checks if a score is non-negative and finite."""
    if not isinstance(score, (int, float)):
        return False
    if score is None or score < 0 or score != score: # score != score checks for NaN
        return False
    return True
