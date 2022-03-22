import os
import orjson

# Current file location
current_location = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)

# Text actions dictionary
text_actions = {}


def load_actions(action_text_files):
    # Load action text files
    for text_file in action_text_files:
        try:
            current_file_path = os.path.join(current_location, "..", "static", "action-texts", f"{text_file}.json")
            with open(current_file_path, "r") as cf:
                json_data = orjson.loads(cf.read())
                text_actions[text_file] = json_data

            print(f"Loaded {text_file}.json into memory.")
        except Exception as error:
            print(f"{text_file} could not be loaded. Stack:\n{error}")
