from bs4 import BeautifulSoup
import requests as rq
import json
import time
from datetime import datetime
import random
from random_user_agent.params import SoftwareName, HardwareType
from random_user_agent.user_agent import UserAgent

software_names = [SoftwareName.CHROME.value]
hardware_type = [HardwareType.MOBILE__PHONE]
user_agent_rotator = UserAgent(
    software_names=software_names, hardware_type=hardware_type)

red = '16711680'
green = '32768'

c_url = 'https://www.maze.com.br/categoria/'
categorias = ['tenis', 'roupas', 'acessorios', 'skate']
url_p = 'https://www.maze.com.br'

header = {'User-Agent': user_agent_rotator.get_random_user_agent()}

estoque = []
esgotados = []

def index(proxy):
    def monitor_post(color=green):

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

    urls = []
    webhook = 'https://discord.com/api/webhooks/875540062241173596/80eTQu4MVAO1pV9Am53Mls3g7236OxuJAwcGRop17JzOcT9vyheA8-WlDimfIAeC9nPw'
    try:
        if estoque == []:   
            for c in categorias:
                url = c_url+c
                response = rq.get(url, headers=header, proxies=proxy)
                soup = BeautifulSoup(response.text, 'html.parser')

                info = soup.find_all('div', class_='dados')
                links = soup.find_all('a', class_='ui image fluid attached')
                imagens = soup.find_all('img', class_='visible content')
                
                for i in range(len(links)):
                    estoque.append(links[i]['href'])
        
        for c in categorias:
            url = c_url+c
            response = rq.get(url, headers=header, proxies=proxy)
            soup = BeautifulSoup(response.text, 'html.parser')

            info = soup.find_all('div', class_='dados')
            links = soup.find_all('a', class_='ui image fluid attached')
            imagens = soup.find_all('img', class_='visible content')

            for i in range(len(links)):
                urls.append(links[i]['href'])

            for i in range(len(info)):
                try:
                    nome = str(info[i].find('h3').getText()).strip()
                    preco = str(info[i].find('span', class_='preco').text).strip()
                    image = imagens[i]['data-src']
                    d = str(info[i].find('meta', attrs={'itemprop': 'availability'})['title'])
                    link_p = links[i]['href']

                    if d == 'disponível' and link_p not in estoque:
                        description = 'Produto disponível para compra'
                        estoque.append(link_p)
                        monitor_post()

                    elif d == 'disponível' and link_p in esgotados:
                        description = 'PRODUTO DE VOLTA AO ESTOQUE!!!'
                        esgotados.remove(link_p)
                        estoque.append(link_p)
                        monitor_post(red)

                except Exception as e:
                    print(e)
        for i in estoque:
            if i not in urls:
                estoque.remove(i)
                esgotados.append(i)
        time.sleep(2)
    except Exception as erro:
        print(erro)

