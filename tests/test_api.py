import requests
from conftest import BASE_URL

def test_health_check():
    """check that health endpoint returns healthy
    Make sure app is running to test this"""

    #Arrange

    # Act
    response = requests.get(f"{BASE_URL}'/health'")
    data = response.json()
    # Assert
    assert response.status_code == 200
    assert data['status'] == 'healthy'

def test_create_event(auth_token):
    """check that we can create an event"""

    # Arrange event data
    event_data = """insert event data here as json string"""
    headers = {"Authorization": f"Bearer {auth_token}"}

    # Act
    response = requests.post(f"{BASE_URL}'/events'",                             json=event_data,
                             headers=headers)

    # Assert
    assert response.status_code == 201
