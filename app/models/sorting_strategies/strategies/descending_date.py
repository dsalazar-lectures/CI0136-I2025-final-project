from ..sorting_strategy import SortingStrategy

class DescendingDateStrategy(SortingStrategy):
    def sort(self, tutorials):
        return sorted(tutorials, key=lambda t: t.date, reverse=True)
