from app.services.confidence import score_account_confidence


def test_confidence_bounds():
    value = score_account_confidence("alice", "https://github.com/alice")
    assert 0 <= value <= 100
    assert value > 80
