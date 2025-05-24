from abc import ABC, abstractmethod

class ITutorialRepository(ABC):
    @abstractmethod
    def get_tutorial_by_id(self, id):
        pass

    @abstractmethod
    def get_tutorias_by_tutor(self, tutor_id):
        pass

    @abstractmethod
    def get_tutorias_by_student(self, student_id):
        pass

    @abstractmethod
    def create_tutorial(self, title_tutoring, tutor_id, tutor, subject, date, start_time, description, method, capacity):
        pass
    @abstractmethod
    def list_tutorials(self):
        pass
    @abstractmethod
    def register_in_tutoria(self, id_student, name_student, id_tutoria):
        pass

    