def test_profile_displays_name_and_role(client, auth):
    # Register and log in a test user
    auth.register(email="user@test.com", password="TestPass1!", name="Tatiana", role="Student")
    auth.login(email="user@test.com", password="TestPass1!")

    # Access the profile page
    response = client.get("/profile/", follow_redirects=True)

    # Check that the user's name and role are shown
    assert b"Tatiana" in response.data
    assert b"Student" in response.data
    assert response.status_code == 200


def test_profile_requires_authentication(client):
    # Try to access the profile page without logging in
    response = client.get("/profile/", follow_redirects=True)

    # The system should redirect to the login page
    assert b"<form" in response.data  # Check for form presence
    assert b"Log in" in response.data or b"Login" in response.data
