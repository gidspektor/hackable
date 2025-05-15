from hackable_api.services.auth_service import AuthService


def test_create_access_token():
    """Test creating an access token"""

    # Mock the data to be encoded
    data = {"sub": "3", "exp": 3600}

    # Create the access token
    token = AuthService.create_access_token(data, 60)

    # Verify the token is created and has the expected structure
    assert isinstance(token, str)
    assert len(token.split(".")) == 3  # JWT has three parts separated by dots


def test_verify_token():
    """Test verifying a token"""

    # Mock the data to be encoded
    data = {"sub": "3", "exp": 3600}

    # Create the access token
    token = AuthService.create_access_token(data, 60)

    # Verify the token
    payload = AuthService.verify_token(token)

    assert payload["sub"] == "3"
    assert "exp" in payload


def test_verify_bad_token():
    """Test verifying a bad token"""

    # Verify the token
    payload = AuthService.verify_token("blabla")

    assert payload == None
