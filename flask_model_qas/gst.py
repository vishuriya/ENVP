import requests

r = requests.get("https://appyflow.in/api/verifyGST")
print(r.json())