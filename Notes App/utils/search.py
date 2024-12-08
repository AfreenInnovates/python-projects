def search_notes(notes, keyword):
    return [note for note in notes if keyword.lower() in note["title"].lower() or keyword.lower() in note["content"].lower()]
