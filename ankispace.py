import requests
from bs4 import BeautifulSoup
import json

# Scrape BrightSpace
def scrape_brightspace(url, username, password):
    session = requests.Session()
    login_data = {
        'username': username,
        'password': password,
    }
    login_url = 'https://your-brightspace-url/login'
    session.post(login_url, data=login_data)
    
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    lecture_notes = soup.find_all('div', class_='lecture-note-class')
    
    notes = []
    for note in lecture_notes:
        title = note.find('h2').text
        content = note.find('p').text
        notes.append((title, content))
    
    return notes

# Create Flashcards in Anki
def create_flashcard(deck_name, front, back):
    url = 'http://localhost:8765'
    headers = {'Content-Type': 'application/json'}
    
    payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deck_name,
                "modelName": "Basic",
                "fields": {
                    "Front": front,
                    "Back": back
                },
                "tags": []
            }
        }
    }
    
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# Main function to run the process
def main():
    url = "https://brightspace-link-to-course"
    username = "your-username"
    password = "your-password"
    notes = scrape_brightspace(url, username, password)
    
    for title, content in notes:
        create_flashcard("YourDeck", title, content)
        print(f"Added flashcard: {title} -> {content}")

if __name__ == '__main__':
    main()
