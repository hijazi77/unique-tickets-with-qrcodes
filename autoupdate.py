import json
import os
import requests
import shutil

from tqdm import tqdm

base_url = "https://spotevents.co/pb/"
version_url = base_url + "api/collections/versions/records"


def create_config():
    config = {"version": "1.0.0"}
    with open("config.json", "w") as config_file:
        json.dump(config, config_file, indent=4)

def update_config(version):
    config = {"version": version}
    with open("config.json", "w") as config_file:
        json.dump(config, config_file, indent=4)


def check_version():
    try:
        with open("config.json", "r") as config_file:
            try:
                config = json.load(config_file)
                current_version = config.get(
                    "version", "1.0.0"
                )  # Default to "1.0.0" if no version is found
                return current_version
            except json.JSONDecodeError:
                create_config()
                print("Invalid JSON in config file. Using default version '1.0.0'.")
                return "1.0.0"
    except FileNotFoundError:
        create_config()
        print("Config file not found. Using default version '1.0.0'.")
        return "1.0.0"


def get_latest_version():
    response = requests.get(version_url)
    return response.json()["items"][-1]["version"]


def get_latest_exe():
    response = requests.get(version_url)
    url = f'https://spotevents.co/pb/api/files/brti6wjfnnyomum/{response.json()["items"][-1]["id"]}/{response.json()["items"][-1]["file"]}'
    return url


def download_latest_exe(latest_version, download_url):
    print(f"New version available: {latest_version}. Updating...")
    # Download the latest version
    download_response = requests.get(download_url, stream=True)
    download_response.raise_for_status()

    # Save the downloaded file to a temporary location
    temp_file_path = "temp_new_version.exe"  # Adjust extension as needed
    with open(temp_file_path, "wb") as file:
        shutil.copyfileobj(download_response.raw, file)

    # Replace the old executable with the new one
    current_executable = os.path.basename(__file__)  # Current running script
    os.rename(
        current_executable, f"{current_executable}.bak"
    )  # Backup current executable
    os.rename(temp_file_path, current_executable)  # Replace with new version

def download_latest_exe2(latest_version, download_url):
    print(f"New version available: {latest_version}.")

    # Download the latest version with a progress bar
    with requests.get(download_url, stream=True) as download_response:
        download_response.raise_for_status()
        total_size = int(download_response.headers.get('content-length', 0))
        temp_file_path = "temp_new_version.exe"  # Adjust extension as needed

        with open(temp_file_path, "wb") as file, tqdm(
            desc=temp_file_path,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in download_response.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)

    # Replace the old executable with the new one
    update_config(latest_version)
    current_executable = os.path.basename(__file__)  # Current running script
    os.rename(
        current_executable, f"{current_executable}.bak"
    )  # Backup current executable
    os.rename(temp_file_path, current_executable)  # Replace with new version

def check_for_updates():
    """
    Check if a new version is available and update the application if it is.
    https://spotevents.co/pb/api/files/brti6wjfnnyomum/xybsobswk6ruqcx/tickets_generator_v2_IbfEWPEtyZ.exe
    
    
    Args:
        current_version (str): The current version of the application.
        version_url (str): The URL where the latest version number is hosted.
        download_url (str): The URL where the latest version of the application can be downloaded.
    """
    try:
        # Fetch the latest version number from the server
        current_version = check_version()
        latest_version = get_latest_version()
        download_url = get_latest_exe()
        # Compare versions
        if latest_version != current_version:
            download_latest_exe2(latest_version, download_url)
            print("Update successful. Please restart the application.")
        else:
            print("You are running the latest version.")


    except requests.RequestException as e:
        print(f"Error checking for updates: {e}")

