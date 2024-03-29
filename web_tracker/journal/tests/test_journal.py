import pytest
from datetime import datetime
from model_bakery import baker
from rest_framework.test import APIClient

from web_tracker.journal.models import Visit


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def visits_factory():
    def factory(*args, **kwargs):
        return baker.make(Visit, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_get_visited_domains(client, visits_factory):
    db_data = visits_factory(_quantity=10)

    response = client.get("/visited_domains/")
    response_data = response.json()

    assert response.status_code == 200
    assert "status" in response_data
    assert len(response_data["domains"]) == len(set(i.domain for i in db_data))


@pytest.mark.django_db
@pytest.mark.parametrize(
    "visited_time, query_string, expected_entries_count",
    [
        (
            datetime(2010, 1, 1),
            {
                "from": int(datetime(2000, 1, 1).timestamp()),
                "to": int(datetime(2020, 1, 1).timestamp()),
            },
            1,
        ),
        (
            datetime.now(),
            {
                "from": int(datetime(2000, 1, 1).timestamp()),
                "to": int(datetime(2020, 1, 1).timestamp()),
            },
            0,
        ),
        (
            datetime.now(),
            {"from": int(datetime(2000, 1, 1).timestamp())},
            1,
        ),
    ],
)
def test_visited_domains_in_time_range(
    client, visits_factory, visited_time, query_string, expected_entries_count
):
    visits_factory(_quantity=1, time=visited_time)
    response = client.get("/visited_domains/", query_string)
    response_data = response.json()

    assert response.status_code == 200
    assert "status" in response_data
    assert len(response_data["domains"]) == expected_entries_count


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload, expected_db_count",
    [
        (
            {
                "links": [
                    "https://ya.ru/",
                    "https://ya.ru/search/?text=мемы+с+котиками",
                    "https://sber.ru",
                    "https://stackoverflow.com/questions/65724760/how-it-is",
                ]
            },
            4,
        ),
        (
            {
                "links": [
                    "https://ya.ru/",
                    "https://ya.ru/search/?text=мемы+с+котиками",
                ]
            },
            2,
        ),
        (
            {
                "links": "https://ya.ru/search/?text=мемы+с+котиками",
                "domain": "ya.ru",
            },
            1,
        ),
    ],
)
def test_post_visited_links(client, payload, expected_db_count):
    response = client.post("/visited_links/", payload, format="json")
    response_data = response.json()
    visits = Visit.objects.all()
    assert len(visits) == expected_db_count
    assert "status" in response_data


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload",
    [
        {"links": ["bad_url", "https://ya.ru/search/"]},
        {"links": ["", ""]},
        {"links": ["hello", "isiturl?"]},
    ],
)
def test_post_bad_request(client, payload):
    response = client.post("/visited_links/", payload, format="json")
    response_data = response.json()
    assert response_data["status"] == "Ooops"
