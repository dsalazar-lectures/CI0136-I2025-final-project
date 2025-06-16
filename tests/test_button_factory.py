import pytest
from app.models.builders.button_factory.button_factory import button_factory
import unittest
from app.controllers.tutorial_controller import measure_time_to_tutorial

class TestButtonFactory:
    def test_create_zoom_button(self):
        factory = button_factory("zoom")
        result = factory.create_button("https://zoom.us/j/123456789")
        assert "https://zoom.us/j/123456789" in result, "Zoom button should contain the meeting link"

    def test_invalid_button_type(self):
        with pytest.raises(ValueError, match="Unknown button type"):
            factory = button_factory("invalid_type")
            factory.create_button("https://example.com")
    
    def test_button_creation_conditions(self):
        user_role = "student"
        current_user = "John Doe"
        tutoring = {
            "student_list": [{"name": "John Doe"}, {"name": "Jane Smith"}],
            "meeting_link": "https://zoom.us/j/123456789"
        }

        def measure_time_to_tutorial(id):
            return 10  # Simula que el tutorial está dentro del rango de tiempo permitido

        # Caso positivo: todas las condiciones se cumplen
        if (
            user_role == "student" and
            tutoring["student_list"] and
            any(student.get("name") == current_user for student in tutoring["student_list"]) and
            -20 < measure_time_to_tutorial(1) <= 30
        ):
            factory = button_factory("zoom")
            button = factory.create_button(tutoring["meeting_link"])
        else:
            button = None

        assert button is not None, "El botón debería haberse creado"
        assert "https://zoom.us/j/123456789" in button, "El botón debería contener el enlace de la reunión"

        # Caso negativo: alguna condición no se cumple
        user_role = "teacher"  # Cambiamos el rol para que falle la condición
        if (
            user_role == "student" and
            tutoring["student_list"] and
            any(student.get("name") == current_user for student in tutoring["student_list"]) and
            -20 < measure_time_to_tutorial(1) <= 30
        ):
            factory = button_factory("zoom")
            button = factory.create_button(tutoring["meeting_link"])
        else:
            button = None

        assert button is None, "El botón no debería haberse creado"
    
    def test_measure_time_to_tutorial(self):
        # Caso de prueba: tiempo positivo
        start_time = 1622505600  # 1 de junio de 2021, 00:00:00
        end_time = 1625097600    # 1 de julio de 2021, 00:00:00
        expected_result = 2592000  # 30 días en segundos
        self.assertEqual(measure_time_to_tutorial(start_time, end_time), expected_result)

        # Caso de prueba: tiempo negativo
        start_time = 1625097600  # 1 de julio de 2021, 00:00:00
        end_time = 1622505600    # 1 de junio de 2021, 00:00:00
        expected_result = -2592000  # -30 días en segundos
        self.assertEqual(measure_time_to_tutorial(start_time, end_time), expected_result)

        # Caso de prueba: tiempo cero
        start_time = 1622505600  # 1 de junio de 2021, 00:00:00
        end_time = 1622505600    # 1 de junio de 2021, 00:00:00
        expected_result = 0
        self.assertEqual(measure_time_to_tutorial(start_time, end_time), expected_result)