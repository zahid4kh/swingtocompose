from dotenv import load_dotenv
import os


def find_and_load_env():
    possible_paths = [
        os.path.dirname(os.path.abspath(__file__)),
        "/usr/share/swingtocompose/",
        os.path.expanduser("~/.config/swingtocompose/")
    ]

    for path in possible_paths:
        env_file = os.path.join(path, ".env")
        if os.path.exists(env_file):
            load_dotenv(env_file)
            return True

    load_dotenv()
    return False


find_and_load_env()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY not found in .env file")  # demo
