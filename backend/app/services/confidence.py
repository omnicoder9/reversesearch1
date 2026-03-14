from difflib import SequenceMatcher


def score_account_confidence(username: str, candidate_url: str, source_reliability: float = 0.8) -> int:
    handle = candidate_url.rstrip("/").split("/")[-1].lower()
    similarity = SequenceMatcher(None, username.lower(), handle).ratio()
    cross_matches = 1.0 if similarity > 0.95 else 0.5
    score = (similarity * 0.7) + (source_reliability * 0.2) + (cross_matches * 0.1)
    return max(0, min(100, round(score * 100)))
