# Personal Knowledge Base Manager

## Project Introduction

The **Personal Knowledge Base Manager** is a Python-based application that helps users efficiently organize, search, and manage their personal notes with encryption capabilities. This tool provides a secure environment for creating, managing, and organizing personal notes with features like password protection and security question recovery.

### Key Features
- **Secure Note Management**: Create, edit, and delete notes with optional encryption
- **Password Protection**: Encrypt sensitive notes with password-based protection
- **Security Recovery**: Password recovery through security questions
- **Auto-Timestamps**: Track note creation and modification times
- **Categories**: Organize notes into categories (study, work, personal, etc.)
- **Search Functionality**: Find notes by keywords in titles or content
- **Visual Organization**: View notes as an interactive graph based on categories
- **Backup System**: Built-in backup functionality to prevent data loss
- **Chronological Sorting**: Notes automatically sorted by creation date
- **JSON Storage**: Data stored in JSON format for easy portability

## Demo
[Watch the demo on YouTube](https://youtu.be/kCGsy19PXRk)

## Usage

1. Start the application:

2. Available options:
- Create Note (1): Add new notes with optional encryption
- Edit Note (2): Modify existing notes (requires password for encrypted notes)
- Delete Note (3): Remove notes (requires password confirmation for encrypted notes)
- Search Notes (4): Find notes using keywords
- View Notes Graph (5): Visualize note relationships
- Backup Notes (6): Create a backup of all notes
- View All Notes (7): List all notes with management options
- Reset All Notes (8): Clear all notes and reset encryption (use with caution)

### Security Features

1. **Note Encryption**:
   - Optional password protection for sensitive notes
   - Security question backup for password recovery
   - Encrypted notes show [Encrypted] instead of content in listings

2. **Password Recovery**:
   - Security question: "What is your favorite fruit?"
   - Prevents unauthorized access while providing recovery options

### Data Storage

- Notes are stored in `data/notes.json`
- Backups are created in `data/backup_notes.json`
- Encryption keys are securely stored in `data/encryption_key.key`
