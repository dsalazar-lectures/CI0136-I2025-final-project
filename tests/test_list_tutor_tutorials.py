import pytest
from app import app
from app.models.repositories.tutorial.repoTutorials import Tutorial_mock_repo

@pytest.fixture
def repo():
    return Tutorial_mock_repo()

def test_list_tutor_tutorials_basic(repo):
    tutor_id = 1
    results = repo.list_tutor_tutorials(tutor_id)
    
    assert all(t.tutor_id == tutor_id for t in results)
    assert len(results) > 0

def test_list_tutor_tutorials_search(repo):
    tutor_id = 1
    search_term = "c++"
    results = repo.list_tutor_tutorials(tutor_id, search=search_term)

    assert all(
        search_term in t.title.lower() or search_term in t.subject.lower()
        for t in results
    )

def test_list_tutor_tutorials_sort_asc(repo):
    tutor_id = 1
    results = repo.list_tutor_tutorials(tutor_id, sort='asc')

    dates = [t.date for t in results]
    assert dates == sorted(dates)

def test_list_tutor_tutorials_sort_desc(repo):
    tutor_id = 1
    results = repo.list_tutor_tutorials(tutor_id, sort='desc')

    dates = [t.date for t in results]
    assert dates == sorted(dates, reverse=True)
