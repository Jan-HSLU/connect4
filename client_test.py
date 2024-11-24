import requests


response = requests.get(url = f"http://localhost:5000/get_board")
response_dict = response.json()
print(response_dict)
