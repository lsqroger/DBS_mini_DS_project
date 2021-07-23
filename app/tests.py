from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_1():
    '''
    Test whether the router of getting a list of classified genres is working
    '''
    response = client.get('/classifiedGenres')
    assert response.status_code == 200


def test_2():
    '''
    Test whether the router of getting a list of titles under a given genre is working
    with a given genre being one of the existing genres present in the database
    '''
    response = client.get('/titles/pop')
    assert response.status_code == 200
    assert response.json()["Provided genre"] == ['pop']


def test_3():
    '''
    Test whether the router of getting a list of titles under a given genre is working
    with a given genre that is absent in the database
    '''
    response = client.get('/titles/not_existing_genre')
    assert response.status_code == 200
    assert response.json() == { "Provided genre": ["not_existing_genre"],
                                "Number of titles under the genre": [0],
                                "Titles under the genre": []}