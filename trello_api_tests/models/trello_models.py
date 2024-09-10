import logging

import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TrelloBoard:
    def __init__(self, name: str, description: str = ''):
        self.name = name
        self.description = description

    def create_board(self, headers, api_key, token):
        url = 'https://api.trello.com/1/boards/'
        params = {
            'name': self.name,
            'desc': self.description,
            'key': api_key,
            'token': token
        }
        response = requests.post(url, params=params, headers=headers)
        if response.status_code == 200:
            logging.info(f"Created board: {self.name}")
        else:
            logging.error(f"Failed to create board: {response.text}")
        return response.json()

    @staticmethod
    def delete_board(board_id, headers, api_key, token):
        url = f"https://api.trello.com/1/boards/{board_id}?key={api_key}&token={token}"
        response = requests.delete(url, headers=headers)
        if response.status_code == 200:
            logging.info(f"Deleted board with ID: {board_id}")
        else:
            logging.error(f"Failed to delete board: {response.text}")

class TrelloList:
    def __init__(self, name: str):
        self.name = name

    def create_list(self, board_id, headers, api_key, token):
        url = 'https://api.trello.com/1/lists/'
        params = {
            'name': self.name,
            'idBoard': board_id,
            'key': api_key,
            'token': token
        }
        response = requests.post(url, params=params, headers=headers)
        if response.status_code == 200:
            logging.info(f"Created list: {self.name}")
        else:
            logging.error(f"Failed to create list: {response.text}")
        return response.json()

    @staticmethod
    def delete_list(list_id, headers, api_key, token):
        url = f"https://api.trello.com/1/lists/{list_id}?key={api_key}&token={token}"
        response = requests.delete(url, headers=headers)
        if response.status_code == 200:
            logging.info(f"Deleted list with ID: {list_id}")
        else:
            logging.error(f"Failed to delete list: {response.text}")

class TrelloCard:
    def __init__(self, name: str, description: str = '', due: str = ''):
        self.name = name
        self.description = description
        self.due = due

    def create_card(self, list_id, headers, api_key, token):
        url = 'https://api.trello.com/1/cards/'
        params = {
            'name': self.name,
            'desc': self.description,
            'due': self.due,
            'idList': list_id,
            'key': api_key,
            'token': token
        }
        response = requests.post(url, params=params, headers=headers)
        if response.status_code == 200:
            logging.info(f"Created card: {self.name}")
        else:
            logging.error(f"Failed to create card: {response.text}")
        return response.json()

    @staticmethod
    def delete_card(card_id, headers, api_key, token):
        url = f"https://api.trello.com/1/cards/{card_id}?key={api_key}&token={token}"
        response = requests.delete(url, headers=headers)
        if response.status_code == 200:
            logging.info(f"Deleted card with ID: {card_id}")
        else:
            logging.error(f"Failed to delete card: {response.text}")
