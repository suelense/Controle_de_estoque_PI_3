import requests


url = 'http://127.0.0.1:5000'  


response = requests.get(url)


if response.status_code == 200:
    
   with open('log.txt', 'a') as file:
        file.write('Teste da API bem-sucedido!\n')
else:

   with open('log.txt', 'a') as file:
        file.write(f'Falha ao testar a API: {response.status_code}\n')

