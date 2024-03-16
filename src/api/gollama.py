import requests

data = {"model": "llama\\2", "keep_alive": 0}
response = requests.post('http://localhost:11434/api/generate', json=data)

if response.status_code == 200:
    print(response.text)  # Do something with the response data
else:
    print('Error:', response.status_code)
