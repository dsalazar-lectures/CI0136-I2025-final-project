class Tutorial:
    def __init__(self, id_tutoring, title_tutoring, tutor_id, tutor, subject, date, start_time, description, method, capacity, meeting_link = None, student_list=None):
        self.id = id_tutoring
        self.title = title_tutoring
        self.tutor = tutor
        self.tutor_id = tutor_id
        self.subject = subject
        self.date = date
        self.start_time = start_time
        self.description = description
        self.method = method
        self.capacity = capacity
        self.meeting_link = meeting_link
        self.student_list = student_list if student_list else []
        