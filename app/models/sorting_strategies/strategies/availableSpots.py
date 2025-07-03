from ..sorting_strategy import SortingStrategy

class AvailableSpotsStrategy(SortingStrategy):
    def sort(self, tutorials):
        return sorted(
            tutorials,
            key=lambda t: t.capacity - len(t.student_list),
            reverse=True  # Más cupos primero
        )
