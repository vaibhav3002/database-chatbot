from functools import lru_cache


def read_file_content(file_path):
    try:
        with open(file_path, "r") as file:
            content = file.read()
            return content
    except FileNotFoundError:
        raise


@lru_cache(maxsize=None)
def read_prompt(prompt_type):
    return read_file_content(f"prompts/{prompt_type}.txt")
