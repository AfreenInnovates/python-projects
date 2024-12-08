import json
import os

FILE_PATH = "data/notes.json"

def load_notes():
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, 'r') as file:
        return json.load(file)

def save_notes(notes):
    with open(FILE_PATH, 'w') as file:
        json.dump(notes, file, indent=4)

def backup_notes(notes):
    backup_path = "data/backup_notes.json"
    with open(backup_path, 'w') as file:
        json.dump(notes, file, indent=4)

def reset_notes():
    if os.path.exists(FILE_PATH):
        os.remove(FILE_PATH)
    if os.path.exists("data/encryption_key.key"):
        os.remove("data/encryption_key.key")
