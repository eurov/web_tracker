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
    fetchall = visits_factory(_quantity=10)

    response = client.get("/visited_domains/")
    data = response.json()

    assert response.status_code == 200
    assert "status" in data
    assert len(data["domains"]) == len(set(i.domain for i in fetchall))


@pytest.mark.django_db
@pytest.mark.parametrize(
    "visited_time, query_string, expected_entries",
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
    client, visits_factory, visited_time, query_string, expected_entries
):
    visits_factory(_quantity=1, time=visited_time)
    response = client.get("/visited_domains/", query_string)
    data = response.json()
    assert response.status_code == 200
    assert "status" in data
    assert len(data["domains"]) == expected_entries
