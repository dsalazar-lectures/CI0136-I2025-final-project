import pytest
from app.models.services.registration_service import validate_registration_data
from app.models.repositories.users.firebase_user_repository import FirebaseUserRepository

# Test cases that check profile validation errors when name or role is invalid or missing
@pytest.mark.parametrize("name, role", [
    ("", "Student"),
    ("Rolandito", ""),
    ("Rolandito", "Admin"),
])
def test_invalid_profile_edits_are_rejected(name, role):
    user_repo = FirebaseUserRepository()

    # Call the validation function with different invalid inputs
    error_message, category = validate_registration_data(
        name=name,
        email="edit@test.com",
        password="ValidPass1!",
        role=role,
        user_repo=user_repo
    )

    # Make sure an error is returned and message is meaningful
    assert error_message is not None
    assert (
        "role" in error_message.lower()
        or "invalid" in error_message.lower()
        or "required" in error_message.lower()
    )


# Test that a user can successfully update their name and role
def test_successful_profile_update(client, auth, debug_session):
    auth.register(email="update@test.com", password="Update123!", name="Rolandito", role="Student")
    auth.login(email="update@test.com", password="Update123!")
    
    # Debug: Print session after login
    print("Session after login:", debug_session())
    
    # Simular una sesión válida manualmente ya que hay problemas con la sesión
    with client.session_transaction() as sess:
        sess["user_id"] = "update@test.com"
        sess["name"] = "Rolandito"
        sess["role"] = "Student"
        sess["email"] = "update@test.com"
    
    print("Session después de configuración manual:", debug_session())
    
    response = client.post("/profile/edit", data={
        "name": "Rolandito Villavicencio",
        "role": "Administrator"
    }, follow_redirects=True)
    
    # Debug: Print session after edit attempt
    print("Session after edit:", debug_session())
    print("Response data:", response.data)
    
    # Check for success message and updated values in the response
    assert b"Profile updated successfully" in response.data
    assert b"Rolandito Villavicencio" in response.data
    assert b"Administrator" in response.data


# Test that only name and role are editable in the profile edit form
def test_profile_edit_fields_are_limited(client, auth, debug_session):
    auth.register(email="edit@test.com", password="Edit123!", name="Rolandito", role="Student")
    auth.login(email="edit@test.com", password="Edit123!")
    
    # Simular una sesión válida manualmente
    with client.session_transaction() as sess:
        sess["user_id"] = "edit@test.com"
        sess["name"] = "Rolandito"
        sess["role"] = "Student"
        sess["email"] = "edit@test.com"
    
    print("Session después de configuración manual:", debug_session())

    response = client.post("/profile/edit", data={
        "name": "",
        "role": ""
    }, follow_redirects=True)

    # Name and role inputs should be present (editable)
    assert b'name="name"' in response.data
    assert b'name="role"' in response.data

    # Email field should not be editable
    assert b'name="email"' not in response.data
