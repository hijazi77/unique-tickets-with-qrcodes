import requests
import openpyxl

file_path = "hawar.xlsx"
base_url = "https://spotevents.co/"
list = []
event = 6
price = 0
workbook = openpyxl.load_workbook(file_path)
sheet = workbook.active
for row in sheet.iter_rows(min_row=2, values_only=True):
    print(row)
    id,code, code_type = row
    print(f"Code: {code}, Type: {code_type}")
    list.append(
        [
            code,
            code_type,
            price,
            event,
        ]
    )
r = requests.post(f"{base_url}api/insert_tickets", json={"code": list})
