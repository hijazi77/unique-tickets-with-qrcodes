base_url = "https://spotevents.co/pb/"

def uploadOneTicket(ticket):
    print(f"Uploading ticket: {ticket}")
    payload = ticket
    response =  requests.post(f"{base_url}api/collections/tickets/records", json=payload) 
    print(response,"response")
    #check if the ticket was uploaded successfully
    if response:
        print("Ticket uploaded successfully")
        return {"ticket": ticket, "success": True}
    else:
        print(f"Failed to upload ticket: {response.status}")
        return {"ticket": ticket, "status": False}


def upload_tickets(list):
    tasks = []
    for ticket in list:
        res = uploadOneTicket(ticket)
        if(res.status==False):
            tasks.append(res)
