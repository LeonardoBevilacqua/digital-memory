from memory import DigitalMemory
from memory import CONTENT, FILENAME
import requests


class OllamaMemoryAssistant:
    def __init__(self, model="phi3:mini"):
        self.memory = DigitalMemory()
        self.model = model
        self.ollama_url = "http://localhost:11434/api/generate"

    def ask(self, question: str) -> str:
        relevant_notes = self.memory.search_notes(question)

        context = ""
        if relevant_notes:
            context = "Based on your notes:\n\n"
            for note in relevant_notes[:3]:
                context += f"From {note[FILENAME]}:\n{note[CONTENT][:300]}\n\n"
        else:
            context = "No relevant notes found."

        prompt = f"""
        You are a personal memory assistant.
        Answer questions based on the user's notes below.
        {context}
        Question: {question}
        Rules:
            - Answer based only on the notes provided.
            - Do not try to guess the meaning of the note if ambiguous,
        just mention the note.
            - The notes is in markdown, use this to filter context by title when needed.
            - Do not make suggestion unless requested.
            - If handling a checklist: [x] means completed and [ ] means pending.
            - If the answer isn't in the notes, say so politely.
            """

        response = requests.post(self.ollama_url, json={
            "model": self.model,
            "prompt": prompt,
            "stream": False
        })

        return response.json()["response"]
