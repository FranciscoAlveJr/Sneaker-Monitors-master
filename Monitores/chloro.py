from enum import IntEnum
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

estoque = []
esgotados = []

header = {'User-Agent': user_agent_rotator.get_random_user_agent()}

webhook = 'https://discord.com/api/webhooks/880190499879788554/KWivsk6fdoKjXadUOIgvdk-Ikf59lT-W_mYb0I7oOr_WKQD7KV-GOP3Dzox8CuEbyYmI'

def index(proxy):
    def monitor_post(color):
        data = {
            'username': 'Chloro Monitor',
            'avatar_url': 'https://cdn.discordapp.com/avatars/874073826013609994/94d1cfe8fdb62e96c278b4c6673876a2.png?size=128',
            'embeds': [{
                'title': nome,
                'description': description,
                'url': link,
                'thumbnail': {'url': imagem},
                'color': color,
                'timestamp': str(datetime.utcnow()),
                'fields': [
                    {'name': 'A partir de ',
                        'value': f'R${preco}'},
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

    url = 'https://www.chloro.com.br/marcas'
    source = rq.get(url, headers=header, proxies=proxy)
    soup = BeautifulSoup(source.text, 'html.parser')

    links = soup.find_all('a', class_='info-product')

    if estoque == []:
        while True:
            source = rq.get(url, headers=header, proxies=proxy)
            soup = BeautifulSoup(source.text, 'html.parser')

            next = soup.find('a', attrs={'rel':'next'})
            current = soup.find('span', class_= 'page-current')
            links = soup.find_all('a', class_='info-product')
            pro_price = soup.find_all('div', class_='product-price')

            for i in range(len(links)):
                link = links[i]['href']
                dispo = pro_price[i].text

                if dispo != 'Indisponível':
                    estoque.append(link)
                else:
                    esgotados.append(link)

            if next == None:
                break

            n_page = next['href'] 
            url = n_page

        print(esgotados)

    while True:
        source = rq.get(url, headers=header, proxies=proxy)
        soup = BeautifulSoup(source.text, 'html.parser')

        next = soup.find('a', attrs={'rel':'next'})
        current = soup.find('span', class_= 'page-current')
        links = soup.find_all('a', class_='info-product')
        pro_price = soup.find_all('div', class_='product-price')


        for i in range(len(links)):
            link = links[i]['href']
            dispo = pro_price[i].text

            s = rq.get(link, headers=header, proxies=proxy)
            soup2 = BeautifulSoup(s.text, 'html.parser')

            id = soup2.find('input', attrs={'name':'ProductComment[product_id]'})
            p_id = id['value']
            d_url = 'https://www.chloro.com.br/web_api/products/'
            p_url = d_url+p_id

            produto = rq.get(p_url, headers=header, proxies=proxy)
            p = json.loads(produto.text)
            item = p['Product']
            nome = item['name']
            preco = item['price']
            imagem = item['ProductImage'][0]['https']

            if dispo == 'Indisponível':
                if link not in esgotados:
                    esgotados.append(link)
                if link in estoque:
                    estoque.remove(link)
            else:
                if link not in estoque and link not in esgotados:
                    estoque.append(link)
                    description = 'Produto disponível para compra'
                    monitor_post(green)
                elif link in esgotados and link not in estoque:
                    esgotados.remove(link)
                    estoque.append(link)
                    description = 'PRODUTO DE VOLTA AO ESTOQUE!!!'
                    monitor_post(red)
        if next == None:
            break

        n_page = next['href'] 
        url = n_page

        