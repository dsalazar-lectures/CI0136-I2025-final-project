import pytest
from app.controllers.review_controller import is_injection, is_offensive

@pytest.mark.parametrize("comment", [
    "Excelente tutor",
    "Muy buena la clase, aprendí mucho.",
    "Gracias por la tutoría!",
    "Todo bien :)",
])
def test_injection_clean_comments(comment):
    assert is_injection(comment) is False

@pytest.mark.parametrize("comment", [
    "Excelente tutor'; DROP TABLE users;--",
    "<script>alert('hacked')</script>",
    "Buen trabajo; SELECT * FROM users WHERE '1'='1'",
    "<img src=x onerror=alert('XSS')>",
    "`rm -rf /`",
    "${7*7}",
])
def test_injection_detects_malicious(comment):
    assert is_injection(comment) is True

@pytest.mark.parametrize("comment", [
    "Eres un idiota",
    "Maldito inútil",
    "That guy is a bastard",
    "You are such an asshole",
    "Estúpido profesor",
])
def test_offensive_detects(comment):
    assert is_offensive(comment) is True

@pytest.mark.parametrize("comment", [
    "Muy buen tutor, gracias!",
    "Excelente sesión, aprendí bastante.",
    "5 estrellas, repetiría con gusto.",
])
def test_offensive_clean(comment):
    assert is_offensive(comment) is False