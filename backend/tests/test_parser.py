from app.models.schemas import SearchInput
from app.services.input_parser import parse_search_input


def test_parse_search_input_email_and_username():
    parsed = parse_search_input(
        SearchInput(
            username="Alice",
            email="alice@example.com",
            consent_confirmed=True,
        )
    )
    assert "username" in parsed.normalized
    assert parsed.normalized["username"] == "alice"
    assert parsed.normalized["email"] == "alice@example.com"
