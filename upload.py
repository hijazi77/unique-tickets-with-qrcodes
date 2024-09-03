from tqdm import tqdm
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from openpyxl import load_workbook

base_url = "https://spotevents.co/pb/"


def update_excel_with_uploaded(tickets, file_path):
    # open the excel file
    workbook = load_workbook(file_path)
    sheet = workbook.active
    for ticket in tickets:
        sheet["D" + str(ticket["rowNumber"])].value = "Uploaded"
        sheet["E" + str(ticket["rowNumber"])].value = ticket["pb"]
    workbook.save(file_path)


def send_ticket(ticket):
    payload = ticket  # Ensure this is a dictionary

    # Create a session with retry mechanism
    session = requests.Session()
    retry = Retry(
        total=5,  # Total number of retries
        backoff_factor=1,  # Wait 1, 2, 4, 8, 16 seconds between retries
        status_forcelist=[429, 500, 502, 503, 504],  # Retry on these HTTP status codes
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    try:
        response = session.post(
            f"{base_url}api/collections/tickets/records", json=payload, timeout=10
        )  # Set timeout
        response.raise_for_status()  # Raise an exception for HTTP errors
        if response.status_code == 200:
            ticket["pb"] = response.json()["id"]
            return {"success": True, "ticket": ticket}
        else:
            return {"success": False, "ticket": ticket}
    except requests.exceptions.RequestException as e:
        return {"success": False, "ticket": ticket}


def upload_tickets(list, xlsx_file):
    failed = []
    success = []
    for i in tqdm(
        range(int(len(list))), desc="Uplaod tickets… ", ascii=False, ncols=75
    ):
        res = send_ticket(list[i])
        if res["success"] == False:
            failed.append(res["ticket"])
        if res["success"] == True:
            success.append(res["ticket"])
    update_excel_with_uploaded(success, xlsx_file)
