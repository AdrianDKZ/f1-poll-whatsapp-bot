import requests

url = "https://ergast.com/api/f1/2025.json"
response = requests.get(url)
data = response.json()

print(data["MRData"]["RaceTable"]["Races"][0]["date"])