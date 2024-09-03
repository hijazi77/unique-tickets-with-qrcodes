import json
import os
import requests
from colorama import init, Fore, Style
from tqdm import tqdm
init(autoreset=True)
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
                print(Fore.RED +"Invalid JSON in config file. Using default version '1.0.0'."+Style.RESET_ALL)
                return "1.0.0"
    except FileNotFoundError:
        create_config()
        print(Fore.RED+ "Config file not found. Using default version '1.0.0'."+Style.RESET_ALL)
        return "1.0.0"


def get_latest_version():
    response = requests.get(version_url)
    return response.json()["items"][-1]["version"]


def get_latest_exe():
    response = requests.get(version_url)
    url = f'https://spotevents.co/pb/api/files/brti6wjfnnyomum/{response.json()["items"][-1]["id"]}/{response.json()["items"][-1]["file"]}'
    return url



def download_latest_exe2(latest_version, download_url):
    print(Fore.GREEN+ f"New version available: {latest_version}."+Style.RESET_ALL)
    print(Fore.YELLOW+"please wait while we download the latest version Dont close the application"+ Style.RESET_ALL)
    print(Fore.RED+"PLEASE DON'T CLOSE THE APPLICATION"+ Style.RESET_ALL)

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
    #remove the temp file
    os.remove(f"{current_executable}.bak")
    os.remove(f"{temp_file_path}")


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
            print(Fore.GREEN+"Update successful. Please restart the application."+Style.RESET_ALL)
        else:
            print(Fore.BLUE+"You are running the latest version."+Style.RESET_ALL)


    except requests.RequestException as e:
        print(Fore.RED +f"Error checking for updates: {e}"+Style.RESET_ALL)

