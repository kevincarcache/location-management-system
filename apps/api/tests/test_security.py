from app.core.security import create_access_token, create_refresh_token, decode_token


def test_access_token_contains_subject_and_type() -> None:
    token = create_access_token("admin@example.com")
    claims = decode_token(token)
    assert claims["sub"] == "admin@example.com"
    assert claims["type"] == "access"


def test_refresh_token_contains_refresh_type() -> None:
    token = create_refresh_token("admin@example.com")
    claims = decode_token(token)
    assert claims["sub"] == "admin@example.com"
    assert claims["type"] == "refresh"
