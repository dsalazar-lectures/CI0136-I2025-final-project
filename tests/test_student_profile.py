def test_student_dashboard_access(client, auth):
    # Registrar y loguear estudiante
    auth.login(email='user@test.com', password='TestPass1!')
    
    response = client.get('/student/profile')
    assert b'Mis Tutorias Inscritas' in response.data

def test_non_student_redirect(client, auth):
    auth.login(email='tutor@example.com', password='Tutor1@@')
    response = client.get('/student/profile')
    assert response.status_code == 302