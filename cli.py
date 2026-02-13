from sys import exit
from memory import DigitalMemory, FILENAME, PREVIEW
from ollama_assistant import OllamaMemoryAssistant

OPTION_TITLE = 'option_title'
OPTION_ACTION = 'option_action'


def clean_up():
    print("\nBye!")
    exit(0)


def main():
    def list_all_notes():
        notes = memory.list_notes()
        print("\nYour Notes:")
        for i, note in enumerate(notes, 1):
            print(f"{i}. {note[FILENAME]}")
            print(f"Preview: {note[PREVIEW]}\n")

    def view_note():
        notes = memory.list_notes()
        print("\nSelect note number:")
        for i, note in enumerate(notes, 1):
            print(f"{i}. {note[FILENAME]}")

        try:
            selected_note = int(input("Number: ")) - 1
            if selected_note < 0 or selected_note >= len(notes):
                print("Invalid note!")
                return

            note_filename = notes[selected_note][FILENAME]
            note_path = f"{memory.notes_path}/{note_filename}"

            with open(note_path, 'r') as file:
                print(f"\n--- {note_filename} ---")
                print(file.read())

        except ValueError:
            print("Only numbers allowed!")

    def ask_assistant():
        question = input("\nYour question: ")
        print("\nThinking...")
        answer = assistant.ask(question)
        print(f"\nAnswer: {answer}")

    assistant = OllamaMemoryAssistant()
    memory = DigitalMemory()
    options = [
        {OPTION_TITLE: "Ask a question", OPTION_ACTION: ask_assistant},
        {OPTION_TITLE: "List all notes", OPTION_ACTION: list_all_notes},
        {OPTION_TITLE: "View a note", OPTION_ACTION: view_note},
        {OPTION_TITLE: "Exit", OPTION_ACTION: clean_up}
    ]

    while True:
        print("\nDigital Memory")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option[OPTION_TITLE]}")

        selected_option_value = -1
        try:
            selected_option_value = int(input("\nChoice: ").strip())
        except ValueError:
            print("Only numbers allowed!")
            continue

        if selected_option_value < 1 or selected_option_value > len(options):
            print("Invalid option!")
            continue

        selected_option = options[selected_option_value-1]
        if OPTION_ACTION not in selected_option:
            print("No Action available!")
            continue

        selected_option[OPTION_ACTION]()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clean_up()
