def test_tutor_profile_access(client, auth):
  auth.login(email='tutor@example.com', password='TutorPass1')
  response = client.get('/tutor/profile')
  assert b'Mis Tutorias' in response.data

def test_non_tutor_redirect(client, auth):
  auth.login(email='student@example.com', password='StudentPass1')
  response = client.get('/tutor/profile')
  assert response.status_code == 302