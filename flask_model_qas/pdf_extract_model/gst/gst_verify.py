import requests

response = requests.get('https://einv-apisandbox.nic.in/version1.04/get-gstin-details/eivital/v1.04/Master/gstin/24AEGPN3982E1ZH')

print(response)