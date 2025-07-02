from ..sorting_strategy import SortingStrategy

class AscendingDateStrategy(SortingStrategy):
    def sort(self, tutorials):
        return sorted(tutorials, key=lambda t: t.date)
