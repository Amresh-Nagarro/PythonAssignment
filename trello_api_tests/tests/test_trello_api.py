import pytest
import logging
import json
from models import TrelloBoard, TrelloList, TrelloCard

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load test data and reads the test data from data/test_data.json
# This data includes API keys, tokens, and test payloads.
def load_test_data(filename='test_data.json'):
    with open(filename, 'r') as file:
        return json.load(file)

# Initialize test data
test_data = load_test_data()

@pytest.fixture(scope="module")
def headers():
    return {
        "Content-Type": "application/json"
    }

@pytest.fixture(scope="module")
def create_board(headers):
    board = TrelloBoard(name="Test Board", description="A board for testing")
    response = board.create_board(headers, test_data['api_key'], test_data['token'])
    logging.info(f"Board creation response: {response}")
    assert response['name'] == "Test Board", "Failed to create board or board name does not match"
    yield response
    board.delete_board(response['id'], headers, test_data['api_key'], test_data['token'])
    logging.info(f"Deleted board with ID: {response['id']}")

@pytest.fixture(scope="module")
def create_list(headers, create_board):
    list_ = TrelloList(name="Test List")
    response = list_.create_list(create_board['id'], headers, test_data['api_key'], test_data['token'])
    logging.info(f"List creation response: {response}")
    assert response['name'] == "Test List", "Failed to create list or list name does not match"
    yield response
    list_.delete_list(response['id'], headers, test_data['api_key'], test_data['token'])
    logging.info(f"Deleted list with ID: {response['id']}")

@pytest.fixture(scope="module")
def create_card(headers, create_list):
    card = TrelloCard(name="Test Card", description="A card for testing", due="2024-12-31T12:00:00Z")
    response = card.create_card(create_list['id'], headers, test_data['api_key'], test_data['token'])
    logging.info(f"Card creation response: {response}")
    assert response['name'] == "Test Card", "Failed to create card or card name does not match"
    yield response
    card.delete_card(response['id'], headers, test_data['api_key'], test_data['token'])
    logging.info(f"Deleted card with ID: {response['id']}")

def test_board_creation(headers):
    board = TrelloBoard(name="Another Test Board", description="Another board for testing")
    response = board.create_board(headers, test_data['api_key'], test_data['token'])
    logging.info(f"Board creation response: {response}")
    assert response['name'] == "Another Test Board", "Failed to create board or board name does not match"

def test_list_creation(headers, create_board):
    list_ = TrelloList(name="Another Test List")
    response = list_.create_list(create_board['id'], headers, test_data['api_key'], test_data['token'])
    logging.info(f"List creation response: {response}")
    assert response['name'] == "Another Test List", "Failed to create list or list name does not match"

def test_card_creation(headers, create_list):
    card = TrelloCard(name="Another Test Card", description="Another card for testing", due="2024-12-31T12:00:00Z")
    response = card.create_card(create_list['id'], headers, test_data['api_key'], test_data['token'])
    logging.info(f"Card creation response: {response}")
    assert response['name'] == "Another Test Card", "Failed to create card or card name does not match"

def test_board_deletion(headers):
    board = TrelloBoard(name="Temporary Board", description="A board to be deleted")
    response = board.create_board(headers, test_data['api_key'], test_data['token'])
    assert response['name'] == "Temporary Board", "Failed to create board or board name does not match"
    board.delete_board(response['id'], headers, test_data['api_key'], test_data['token'])
    logging.info(f"Deleted board with ID: {response['id']}")

def test_list_deletion(headers, create_board):
    list_ = TrelloList(name="Temporary List")
    response = list_.create_list(create_board['id'], headers, test_data['api_key'], test_data['token'])
    assert response['name'] == "Temporary List", "Failed to create list or list name does not match"
    list_.delete_list(response['id'], headers, test_data['api_key'], test_data['token'])
    logging.info(f"Deleted list with ID: {response['id']}")

def test_card_deletion(headers, create_list):
    card = TrelloCard(name="Temporary Card", description="A card to be deleted", due="2024-12-31T12:00:00Z")
    response = card.create_card(create_list['id'], headers, test_data['api_key'], test_data['token'])
    assert response['name'] == "Temporary Card", "Failed to create card or card name does not match"
    card.delete_card(response['id'], headers, test_data['api_key'], test_data['token'])
    logging.info(f"Deleted card with ID: {response['id']}")
