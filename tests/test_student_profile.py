def test_student_dashboard_access(client, auth):
    # Registrar y loguear estudiante
    auth.register(email='student@test.com', password='StudentPass1!', role='Student')
    auth.login(email='student@test.com', password='StudentPass1!')
    
    response = client.get('/student/dashboard')
    assert b'Mis Tutorias Inscritas' in response.data

def test_non_student_redirect(client, auth):
    auth.login(email='admin@example.com', password='Admin1@')
    response = client.get('/student/dashboard')
    assert response.status_code == 302