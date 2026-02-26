import json
from typing import Dict
import os
import hashlib
import secrets
from pathlib import Path

CREDENTIALS_FOLDER = "src/data/credentials/"
USER_DATA_FOLDER = Path("src/data/game_data/")

# Hash passwords instead of encrypting them
def store_credentials(username: str, password: str) -> None:
    """
    Store a newly created user's credentials in a secure fashion.

    Args:
        username (str): The username of the newly created user.
        password (str): The password of the newly created user.

    Returns:
        None
    """

    # Create the directory to store credentials if it doesn't exist
    os.makedirs(CREDENTIALS_FOLDER, exist_ok=True)

    # Generate a secure key for hashing
    hashed_key = hashlib.sha256(secrets.token_bytes(32)).hexdigest()

    # Store the credentials in JSON format with hashing
    cred_data: Dict[str, str] = {
        'username': username,
        'password': hashlib.sha256(password.encode()).hexdigest(),
        'key': hashed_key
    }

    with open(os.path.join(CREDENTIALS_FOLDER, f"{username}.json"), "w") as file:
        json.dump(cred_data, file)


def check_credentials(username: str, provided_password: str) -> bool:
    """
    Check a user's credentials against those stored in the credentials file.

    Args:
        username (str): The username to be checked.
        provided_password (str): The password provided by the user.

    Returns:
        bool: True if the credentials match, False otherwise.
    """

    # Load the hashed credentials from the JSON file
    with open(os.path.join(CREDENTIALS_FOLDER, f"{username}.json"), "r") as file:
        stored_data: Dict[str, str] = json.load(file)
        print(stored_data)

    print(hashlib.sha256(provided_password.encode()).hexdigest(), "==", stored_data['password'])

    # Compare the provided password's hash to the stored hash
    return hashlib.sha256(provided_password.encode()).hexdigest() == stored_data['password']


def read_game_data_for_user(username:str, filename:str):
    """
    Reads a JSON file from USER_DATA_FOLDER/<username>/<filename>
    and returns its contents as a dict.

    Parameters
    ----------
    username : str
        Name of the user (folder name).
    filename : str
        JSON filename (with or without .json extension).

    Returns
    -------
    dict
        Parsed JSON data.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    json.JSONDecodeError
        If the file is not valid JSON.
    """

    # Ensure .json extension
    if not filename.endswith(".json"):
        filename += ".json"

    file_path = USER_DATA_FOLDER / username / filename

    if not file_path.exists():
        raise FileNotFoundError(f"No such file: {file_path}")

    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_game_data_for_user(username: str, filename: str, data: dict) -> None:
    """
    Writes a JSON file to USER_DATA_FOLDER/<username>/<filename>

    Parameters
    ----------
    username : str
        Name of the user (folder name).
    filename : str
        JSON filename (with or without .json extension).
    data : dict
        Data to save.

    Creates
    -------
    User folder if it does not exist.
    Overwrites file if it already exists.
    """

    # Ensure .json extension
    if not filename.endswith(".json"):
        filename += ".json"

    user_folder = USER_DATA_FOLDER / username
    user_folder.mkdir(parents=True, exist_ok=True)

    file_path = user_folder / filename

    with file_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

