import pytest
import json

# Load test data and reads the test data from data/test_data.json
# This data includes API keys, tokens, and test payloads.
def load_test_data(filename='test_data.json'):
    with open(filename, 'r') as file:
        return json.load(file)

# Initialize test data
test_data = load_test_data()

@pytest.fixture(scope="session")
def setup_api_credentials():
    """Fixture to set up and provide API credentials for the tests."""
    credentials = {
        'api_key': test_data['api_key'],
        'token': test_data['token']
    }
    return credentials

# Define a fixture for the API headers
@pytest.fixture(scope='session')
# Provides the HTTP headers required for making API requests.
def headers(setup_api_credentials):
    credentials = setup_api_credentials
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {credentials['token']}"
    }
    return headers

# Define a fixture for creating and deleting a board
@pytest.fixture(scope='module')
# Creates a Trello board and provides its details to tests.
# It also ensures the board is deleted after the tests are complete.
def create_board(headers):
    from models import TrelloBoard

    board = TrelloBoard(name="Test Board", description="A board for testing")
    response = board.create_board(headers, test_data['api_key'], test_data['token'])
    assert response['name'] == "Test Board", "Failed to create board or board name does not match"
    yield response
    board.delete_board(response['id'], headers, test_data['api_key'], test_data['token'])

# Define a fixture for creating a list within a board
@pytest.fixture(scope='module')
# Creates a Trello list within the created board.
# It also ensures the list is deleted after the tests are complete.
def create_list(headers, create_board):
    from models import TrelloList

    list_ = TrelloList(name="Test List")
    response = list_.create_list(create_board['id'], headers, test_data['api_key'], test_data['token'])
    assert response['name'] == "Test List", "Failed to create list or list name does not match"
    yield response
    list_.delete_list(response['id'], headers, test_data['api_key'], test_data['token'])

# Define a fixture for creating a card within a list
@pytest.fixture(scope='module')
# Creates a Trello card within the created list.
# It also ensures the card is deleted after the tests are complete.
def create_card(headers, create_list):
    from models import TrelloCard

    card = TrelloCard(name="Test Card", description="A card for testing", due="2024-12-31T12:00:00Z")
    response = card.create_card(create_list['id'], headers, test_data['api_key'], test_data['token'])
    assert response['name'] == "Test Card", "Failed to create card or card name does not match"
    yield response
    card.delete_card(response['id'], headers, test_data['api_key'], test_data['token'])

# Hook to handle setup and teardown at the session level
# Hook that runs before the test session starts.
# It can be used for initialization if needed.
def pytest_sessionstart(session):
    print("Starting the test session")

# Hook that runs after the test session finishes.
# It can be used for cleanup or logging.
def pytest_sessionfinish(session, exitstatus):
    print("Ending the test session")
