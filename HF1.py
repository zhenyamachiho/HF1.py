import json
import datetime

class Note:
    def __init__(self, id, title, body):
        self.id = id
        self.title = title
        self.body = body
        self.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'created_at': self.created_at
        }

class NoteApp:
    def __init__(self, filepath):
        self.filepath = filepath
        self.notes = []
        self.load_notes()

    def load_notes(self):
        try:
            with open(self.filepath, 'r') as f:
                data = json.load(f)
                for note in data:
                    self.notes.append(Note(note['id'], note['title'], note['body']))
        except FileNotFoundError:
            with open(self.filepath, 'w') as f:
                json.dump([], f)

    def save_notes(self):
        with open(self.filepath, 'w') as f:
            json.dump([note.to_dict() for note in self.notes], f)

    def create_note(self, id, title, body):
        note = Note(id, title, body)
        self.notes.append(note)
        self.save_notes()

    def get_notes(self):
        return [note.to_dict() for note in self.notes]

    def get_note_by_id(self, id):
        for note in self.notes:
            if note.id == id:
                return note.to_dict()
        return None

    def update_note(self, id, title=None, body=None):
        for note in self.notes:
            if note.id == id:
                if title is not None:
                    note.title = title
                if body is not None:
                    note.body = body
                note.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save_notes()
                return True
        return False

    def delete_note(self, id):
        for i in range(len(self.notes)):
            if self.notes[i].id == id:
                del self.notes[i]
                self.save_notes()
                return True
        return False

def main():
    app = NoteApp('notes.json')
    while True:
        command = input("Введите команду (create/update/delete/list/quit): ")
        if command == "create":
            id = input("Введите ID: ")
            title = input("Введите заголовок: ")
            body = input("Введите текст заметки: ")
            app.create_note(id, title, body)
        elif command == "update":
            id = input("Введите ID заметки для редактирования: ")
            title = input("Введите новый заголовок (оставьте пустым для пропуска): ")
            body = input("Введите новый текст заметки (оставьте пустым для пропуска): ")
            app.update_note(id, title or None, body or None)
        elif command == "delete":
            id = input("Введите ID заметки для удаления: ")
            app.delete_note(id)
        elif command == "list":
            notes = app.get_notes()
            for note in notes:
                print(note)
        elif command == "quit":
            break

if __name__ == "__main__":
    main()
