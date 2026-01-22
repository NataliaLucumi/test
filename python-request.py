import requests

response = requests.get('https://http.cat/status/400')
propiedades={"status": response.status_code,
             "content_type": response.content}

print(f"Response de la petición: {propiedades}")