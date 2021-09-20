from bs4 import BeautifulSoup
import requests as rq
import json
import time
from datetime import datetime
import random
from random_user_agent.params import SoftwareName, HardwareType
from random_user_agent.user_agent import UserAgent
import get_proxys

software_names = [SoftwareName.CHROME.value]
hardware_type = [HardwareType.MOBILE__PHONE]
user_agent_rotator = UserAgent(
    software_names=software_names, hardware_type=hardware_type)

red = '16711680'
green = '32768'

url = 'https://www.maze.com.br/categoria/tenis'
url_p = 'https://www.maze.com.br'

header = {'User-Agent': user_agent_rotator.get_random_user_agent()}

estoque = []
esgotados = []

while True:
    p = get_proxys.get_proxys()
    proxy = {'http': 'http://{}'.format(p)}

    def monitor_post(color):

        data = {
            'username': 'Maze Monitor',
            'avatar_url': 'https://cdn.discordapp.com/avatars/874073826013609994/94d1cfe8fdb62e96c278b4c6673876a2.png?size=128',
            'embeds': [{
                'title': nome,
                'description': description,
                'url': url_p+link_p,
                'thumbnail': {'url': f'https:{image}'},
                'color': color,
                'timestamp': str(datetime.utcnow()),
                'fields': [
                    {'name': 'Tamanho:', 'value': tamanho},
                    {'name': 'Preço', 'value': preco},
                ]
            }]
        }
        result = rq.post(webhook, data=json.dumps(data), headers={
            "Content-Type": "application/json"})

        try:
            result.raise_for_status()
        except rq.exceptions.HTTPError as err:
            print(err)
        else:
            print(
                f"Payload delivered successfully, code {result.status_code}.")

    webhook = ''
    try:
        if estoque == []:   
            response = rq.get(url, headers=header, proxies=proxy)
            soup = BeautifulSoup(response.text, 'html.parser')

            links = soup.find_all('a', class_='ui image fluid attached')
            
            for i in range(len(links)):
                link_p = links[i]['href']
                url_pro = url_p+link_p

                response2 = rq.get(url_pro, headers=header, proxies=proxy)
                soup2 = BeautifulSoup(response2.text, 'html.parser')
               
                tamanhos = soup2.find_all('input', {'id':'json-detail'})
                res = json.loads(tamanhos[0]['value'])

                for i in range(len(res['Variations'])):
                    tamanho = res['Variations'][i]['Name']
                    stock = res['Variations'][i]['Sku']['Stock']
                    produto_t = link_p+tamanho

                    if stock > 0:
                        estoque.append(produto_t)
                        print(produto_t)
                        print(stock)
                    else:
                        esgotados.append(produto_t)

        response = rq.get(url, headers=header, proxies=proxy)
        soup = BeautifulSoup(response.text, 'html.parser')

        info = soup.find_all('div', class_='dados')
        links = soup.find_all('a', class_='ui image fluid attached')
        imagens = soup.find_all('img', class_='visible content')

        for i in range(len(links)):
            try:
                nome = str(info[i].find('h3').getText()).strip()
                preco = str(info[i].find('span', class_='preco').text).strip()
                image = imagens[i]['data-src']
                link_p = links[i]['href']
                url_pro = url_p+link_p

                response2 = rq.get(url_pro, headers=header, proxies=proxy)
                soup2 = BeautifulSoup(response2.text, 'html.parser')
               
                tamanhos = soup2.find_all('input', {'id':'json-detail'})
                res = json.loads(tamanhos[0]['value'])

                for i in range(len(res['Variations'])):
                    tamanho = res['Variations'][i]['Name']
                    stock = res['Variations'][i]['Sku']['Stock']
                    produto_t = link_p+tamanho

                    if stock == 0 and produto_t not in esgotados:
                        esgotados.append(produto_t)
                        if produto_t in estoque:
                            estoque.remove(produto_t)

                    elif stock > 0 and produto_t not in estoque and produto_t not in esgotados:
                        description = 'PRODUTO DISPONÍVEL'
                        estoque.append(link_p)
                        monitor_post(green)

                    elif stock > 0 and produto_t in esgotados and produto_t not in estoque:
                        description = 'RESTOCK'
                        esgotados.remove(link_p)
                        estoque.append(link_p)
                        monitor_post(red)

            except Exception as e:
                print(e)
        time.sleep(2)
    except Exception as erro:
        print(erro)