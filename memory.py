from glob import glob
from pathlib import Path

CONTENT = 'content'
FILENAME = 'filename'
SCORE = 'score'
PREVIEW = 'preview'


class DigitalMemory:

    def __init__(self, notes_path="./notes"):
        self.notes_path = Path(notes_path)
        self.notes = {}
        self.embeddings = {}
        self.load_notes()

    def load_notes(self):
        md_files = glob(f"{self.notes_path}/*.md")
        for file_path in md_files:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            self.notes[file_path] = {
                CONTENT: content,
                # 'modified': os.path.getmtime(file_path) Check if is required
                FILENAME: Path(file_path).name
            }

    def search_notes(self, query: str) -> list[dict]:
        results = []
        query_lower = query.lower()
        words = query_lower.split()

        for path, note in self.notes.items():
            self.__append_scored_result(results, note, words)

        return sorted(
            results,
            key=lambda result: result[SCORE],
            reverse=True)

    def list_notes(self) -> list[dict]:
        return [
            {FILENAME: note[FILENAME],
             PREVIEW: note[CONTENT][:100] + '...'
             if len(note[CONTENT]) > 100 else
             note[CONTENT]}
            for note in self.notes.values()
        ]

    def __calculate_score(self, words: list[str], content_lower: str) -> int:
        score = 0
        for word in words:
            if word in content_lower:
                score += content_lower.count(word)

        return score

    def __append_scored_result(
            self,
            results: list[dict],
            note: dict,
            words: list[str]
    ):
        content_lower = note[CONTENT].lower()

        score = self.__calculate_score(words, content_lower)
        if score > 0:
            results.append(self.__generate_scored_result(note, score))

    def __generate_scored_result(self, note: dict, score: int) -> dict:
        return {
            FILENAME: note[FILENAME],
            CONTENT: note[CONTENT],
            SCORE: score
        }
