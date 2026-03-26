from tools.base import BaseTool
import requests


class DictionaryTool(BaseTool):

    def __init__(self) -> None:
        super().__init__("dictionary", "Get meanings of words and compare words")

    def get_definitions(self, word: str):
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        response = requests.get(url)

        if response.status_code != 200:
            return None

        data = response.json()
        definitions = []

        for meaning in data[0].get("meanings", []):
            part_of_speech = meaning.get("partOfSpeech", "unknown")
            for item in meaning.get("definitions", []):
                definition = item.get("definition")
                if definition:
                    definitions.append(f"{part_of_speech}: {definition}")

                if len(definitions) == 3:
                    return definitions

        return definitions

    # main logic
    def execute(self, args: dict) -> str:
        word = args.get("word", "").lower()
        compare_word = args.get("compare_word", "").lower()

        try:
            if not word:
                return "word not found"

            definitions = self.get_definitions(word)
            if not definitions:
                return "word not found"

            if compare_word:
                compare_definitions = self.get_definitions(compare_word)
                if not compare_definitions:
                    return f"{word}: " + "; ".join(definitions) + f"\n{compare_word}: word not found"

                result = []
                result.append(f"{word}: " + "; ".join(definitions))
                result.append(f"{compare_word}: " + "; ".join(compare_definitions))
                result.append(f"Difference: {word} and {compare_word} are different words with different meanings shown above.")
                return "\n".join(result)

            return f"{word}: " + "; ".join(definitions)

        except Exception as e:
            return f"error: {e}"

    # schema
    def get_declaration(self) -> dict:
      return {
        "name": "dictionary",
        "description": "Use this tool to define a word, give multiple meanings of a word, compare two words, or explain the difference between two words",
        "parameters": {
            "type": "object",
            "properties": {
                "word": {
                    "type": "string",
                    "description": "the main word to define or explain"
                },
                "compare_word": {
                    "type": "string",
                    "description": "optional second word to compare with the main word when the user asks for a difference or comparison"
                }
            },
            "required": ["word"]
        }
    }
