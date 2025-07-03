from app.models.sorting_strategies.strategies.ascending_date import AscendingDateStrategy
from app.models.sorting_strategies.strategies.descending_date import DescendingDateStrategy
from app.models.sorting_strategies.strategies.availableSpots import AvailableSpotsStrategy

def filter_and_sort_tutorials(tutorials, search=None, subject=None, sort=None):
    # Búsqueda por título, asignatura o descripción
    if search:
        search = search.lower()
        tutorials = [
            t for t in tutorials
            if search in t.title.lower()
            or search in t.subject.lower()
            or search in t.description.lower()
        ]

    # Filtro por materia
    if subject:
        tutorials = [t for t in tutorials if t.subject == subject]

    # Estrategia de ordenamiento
    strategy = None
    if sort == "asc":
        strategy = AscendingDateStrategy()
    elif sort == "desc":
        strategy = DescendingDateStrategy()
    elif sort == "spots":
        strategy = AvailableSpotsStrategy()

    if strategy:
        tutorials = strategy.sort(tutorials)

    return tutorials
