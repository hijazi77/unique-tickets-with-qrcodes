import json
import requests
from cryptography.fernet import Fernet
# Secret key to send
#base = 'https://spotevents.co/'
base = "http://localhost:3000/"
url = base + 'api/version'
secret_key_to_send = 'allow2me@EXE0000'
# Create a Fernet key for encryption (should be securely stored)
# encryption_key = 'your_encryption_key_here'
encryption_key = '1QfHQHx48KVVMMpqxj-YDbwFHvKxEZF1zAVcTJjQu1s='
fernet = Fernet(encryption_key)

# Encrypt the secret key
encrypted_key = fernet.encrypt(secret_key_to_send.encode())
encrypted_key.decode()

# Create a dictionary with the encrypted secret key
data = {'encryptedSecretKey': encrypted_key}
print(data)
payload = json.dumps(data)
# Send the POST request
response = requests.post(url, json= data)

# Check the response
if response.status_code == 200:
    print('Key is valid')
elif response.status_code == 401:
    print('Key is invalid')
else:
    print('Unexpected error:', response.status_code)