import os
import json
from utils.encryption import encrypt_note, decrypt_note
from utils.file_manager import load_notes, save_notes, backup_notes, reset_notes
from utils.search import search_notes
from utils.graph import visualize_notes
from datetime import datetime, timedelta

def main_menu():
    print("\n" * 2)
    print("=" * 50)
    print("       Personal Knowledge Base Manager")
    print("=" * 50)
    print("\nPlease select an option:")
    print("\n1. Create Note")
    print("2. Edit Note")
    print("3. Delete Note")
    print("4. Search Notes")
    print("5. View Notes Graph")
    print("6. Backup Notes")
    print("7. View All Notes")
    print("8. View Calendar")
    print("9. Reset All Notes")
    print("0. Exit")

def format_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None

def display_calendar(notes):
    print("\nCalendar View")
    print("=" * 50)
    
    # Group notes by due date
    due_notes = {}
    for note in notes:
        if note.get('due_date'):
            date = datetime.fromisoformat(note['due_date']).date()
            if date not in due_notes:
                due_notes[date] = []
            due_notes[date].append(note)
    
    # Display notes by date
    if not due_notes:
        print("No notes with due dates!")
        return
        
    for date in sorted(due_notes.keys()):
        print(f"\n{date.strftime('%A, %B %d, %Y')}:")
        for note in due_notes[date]:
            status = "OVERDUE" if date.today() > date else "DUE"
            print(f"- {note['title']} ({status})")
            if note.get('reminder'):
                print(f"  Reminder: {note['reminder']}")

def check_reminders(notes):
    today = datetime.now().date()
    reminders = []
    
    for note in notes:
        if note.get('reminder'):
            reminder_date = datetime.fromisoformat(note['reminder']).date()
            if reminder_date == today:
                reminders.append(note)
    
    if reminders:
        print("\n🔔 REMINDERS TODAY 🔔")
        print("=" * 50)
        for note in reminders:
            due_date = datetime.fromisoformat(note['due_date']).date()
            days_left = (due_date - today).days
            print(f"- {note['title']}")
            print(f"  Due in {days_left} days ({due_date})")
        print("=" * 50)
        input("\nPress Enter to continue...")

def main():
    notes = load_notes()
    check_reminders(notes)  # Check reminders at startup
    while True:
        main_menu()
        choice = input("\nEnter your choice: ")
        if choice == "1":
            title = input("Enter note title: ")
            content = input("Enter note content: ")
            category = input("Enter note category: (study, work, personal, etc.) ")
            
            # Add due date
            has_due_date = input("Add a due date? (y/n): ").strip().lower()
            due_date = None
            reminder = None
            if has_due_date == 'y':
                while True:
                    date_str = input("Enter due date (YYYY-MM-DD): ")
                    due_date = format_date(date_str)
                    if due_date:
                        # Add reminder
                        add_reminder = input("Add a reminder? (y/n): ").strip().lower()
                        if add_reminder == 'y':
                            print("\nReminder options:")
                            print("1. On the due date")
                            print("2. 1 day before")
                            print("3. 1 week before")
                            reminder_choice = input("Choose reminder option (1-3): ")
                            
                            if reminder_choice == "1":
                                reminder = due_date
                            elif reminder_choice == "2":
                                reminder = due_date - timedelta(days=1)
                            elif reminder_choice == "3":
                                reminder = due_date - timedelta(days=7)
                        break
                    print("Invalid date format! Please use YYYY-MM-DD")
            
            encrypted = input("Encrypt note? (y/n): ").strip().lower()
            
            # Add password and security question for encrypted notes
            password = None
            security_answer = None
            if encrypted == "y":
                password = input("Enter a password for this note: ")
                print("\nSecurity Question (for password recovery)")
                security_answer = input("What is your favorite fruit? ").strip().lower()
                content = encrypt_note(content, password)
            
            note = {
                "title": title,
                "content": content,
                "category": category,
                "encrypted": encrypted,
                "created_at": datetime.now().isoformat(),
                "password": password if encrypted == "y" else None,
                "security_answer": security_answer if encrypted == "y" else None,
                "due_date": due_date.isoformat() if due_date else None,
                "reminder": reminder.isoformat() if reminder else None
            }
            notes.append(note)
            notes.sort(key=lambda x: x["created_at"], reverse=True)
            save_notes(notes)
            print("Note created successfully!")

        elif choice == "2":
            title = input("Enter a word from the title of the note you want to edit: ")
            note = next((n for n in notes if title in n["title"]), None)
            if not note:
                print("Note not found!")
            else:
                print(f"Editing note: {note['title']}")
                new_content = input("Enter new content: ")
                if note["encrypted"] == "y":
                    password = input("Enter the note's password: ")
                    if password == note["password"]:
                        note["content"] = encrypt_note(new_content, password)
                    else:
                        print("Incorrect password! Note not updated.")
                        continue
                else:
                    note["content"] = new_content
                save_notes(notes)
                print("Note updated successfully!")

        elif choice == "3":
            title = input("Enter a word from the title of the note you want to delete: ")
            note = next((n for n in notes if title in n["title"]), None)
            if not note:
                print("Note not found!")
            else:
                notes.remove(note)
                save_notes(notes)
                print("Note deleted successfully!")

        elif choice == "4":
            keyword = input("Enter a keyword to search for in the notes: ")
            results = search_notes(notes, keyword)
            if not results:
                print("No matching notes found!")
            else:
                print(f"Found {len(results)} matching notes:")
                for result in results:
                    print(f"- {result['title']}")
                    print(f"- {result['content']}")

        elif choice == "5":
            visualize_notes(notes)

        elif choice == "6":
            backup_notes(notes)
            print("Notes backed up successfully!")

        elif choice == "7":
            if not notes:
                print("No notes found!")
            else:
                print("\nAll Notes (Most Recent First):")
                print("-" * 50)
                for i, note in enumerate(notes, 1):
                    created_date = datetime.fromisoformat(note['created_at'])
                    formatted_date = created_date.strftime("%d{} %B, %Y, %A at %H:%M:%S").format(
                        'th' if 4 <= created_date.day <= 20 or 24 <= created_date.day <= 30
                        else ['st', 'nd', 'rd'][created_date.day % 10 - 1] if created_date.day % 10 <= 3
                        else 'th'
                    )
                    print(f"\n{i}. Title: {note['title']}")
                    print(f"   Category: {note['category']}")
                    print(f"   Created: {formatted_date}")
                    content = note['content']
                    if not note['encrypted'] == 'y':
                        print(f"   Content: {content}")
                    else:
                        print(f"   Content: [Encrypted]")
                    print("-" * 50)
                
                action = input("\nWould you like to: \n1. View a note\n2. Edit a note\n3. Delete a note\n4. Return to main menu\nEnter your choice: ")
                
                if action in ["1", "2", "3"]:
                    try:
                        note_num = int(input("Enter the note number: ")) - 1
                        if 0 <= note_num < len(notes):
                            if action == "1":  # View
                                note = notes[note_num]
                                print(f"\nViewing note: {note['title']}")
                                if note['encrypted'] == 'y':
                                    password = input("Enter the password for this note: ")
                                    if password == note['password']:
                                        decrypted_content = decrypt_note(note['content'], password)
                                        content = decrypted_content if decrypted_content is not None else "[Error: Unable to decrypt note]"
                                    else:
                                        print("Incorrect password!")
                                        retry = input("Would you like to try the security question? (y/n): ").strip().lower()
                                        if retry == 'y':
                                            security_attempt = input("What is your favorite fruit? ").strip().lower()
                                            if security_attempt == note['security_answer']:
                                                print("Security answer correct! Here's your note:")
                                                decrypted_content = decrypt_note(note['content'], note['password'])
                                                content = decrypted_content if decrypted_content is not None else "[Error: Unable to decrypt note]"
                                            else:
                                                print("Incorrect security answer!")
                                                content = "[Access denied: Incorrect password and security answer]"
                                        else:
                                            content = "[Access denied: Incorrect password]"
                                else:
                                    content = note['content']
                                print(f"Content: {content}")
                            elif action == "2":  # Edit
                                note = notes[note_num]
                                print(f"Editing note: {note['title']}")
                                new_content = input("Enter new content: ")
                                if note['encrypted'] == 'y':
                                    password = input("Enter the note's password: ")
                                    if password == note['password']:
                                        note['content'] = encrypt_note(new_content, password)
                                        save_notes(notes)
                                        print("Note updated successfully!")
                                    else:
                                        print("Incorrect password! Note not updated.")
                                else:
                                    note['content'] = new_content
                                    save_notes(notes)
                                    print("Note updated successfully!")
                            else:  # Delete
                                if notes[note_num]['encrypted'] == 'y':
                                    password = input("Enter the note's password to confirm deletion: ")
                                    if password != notes[note_num]['password']:
                                        print("Incorrect password! Deletion cancelled.")
                                        continue
                                notes.pop(note_num)
                                save_notes(notes)
                                print("Note deleted successfully!")
                        else:
                            print("Invalid note number!")
                    except ValueError:
                        print("Please enter a valid number!")
                
                input("\nPress Enter to continue...")

        elif choice == "8":
            display_calendar(notes)
            input("\nPress Enter to continue...")

        elif choice == "9":
            confirm = input("This will delete all notes and reset encryption. Are you sure? (y/n): ")
            if confirm.lower() == 'y':
                reset_notes()
                notes = []
                print("All notes have been reset. Please restart the program.")
                break

        elif choice == "0":
            print("Exiting the program...")
            break

        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
