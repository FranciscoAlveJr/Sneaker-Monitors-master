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

def index(proxy):
    def monitor_post(color):
        data = {
            'username': 'Your ID Monitor',
            'avatar_url': 'https://cdn.discordapp.com/avatars/874073826013609994/94d1cfe8fdb62e96c278b4c6673876a2.png?size=128',
            'embeds': [{
                'title': nome,
                'url': link,
                'description': description,
                'thumbnail': {'url': img},
                'color': color,
                'timestamp': str(datetime.utcnow()),
                'fields': [
                    {'name': 'Preço:', 'value': preco},
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

    url = 'https://youridstore.com.br/novidades'
    header = {'User-Agent': user_agent_rotator.get_random_user_agent()}


    webhook = 'https://discord.com/api/webhooks/875540617738993755/MpPWvS6mK7zZ8zEaRa7Iol48tekmZo9JCC9Lax7URGyBcdHpYwdJlOT6Kc2an1siLitP'

    try:
        response = rq.get(url, headers=header, proxies=proxy)
        soup = BeautifulSoup(response.text, 'html.parser')

        urls = []

        precos = soup.find_all('span', class_='regular-price')
        nomes = soup.find_all('h2', class_='product-name')
        links = soup.find_all('a', class_='product-image')
        marcas = soup.find_all('h3', class_='brand_name_cat')

        for i in range(len(links)):
            urls.append(links[i]['href'])

        if estoque == []:
            for i in range(len(links)):
                estoque.append(links[i]['href'])

        for i in range(len(nomes)):
            try:
                nome = nomes[i].text
                preco = precos[i].text.strip()
                link = links[i]['href']
                imagem = links[i].find_all('img')
                img = imagem[0]['src']

                if link in estoque and link not in urls:
                    estoque.remove(link)
                    esgotados.append(link)
                elif link in urls and link not in estoque:
                    description = 'Produto disponível para compra'
                    estoque.append(link)
                    monitor_post(green)
                elif link in urls and link in esgotados:
                    description = 'PRODUTO DE VOLTA PARA O ESTOQUE!!'
                    esgotados.remove(link)
                    estoque.append(link)
                    monitor_post(red)
            except Exception as e:
                print(e)
        time.sleep(2)
    except Exception as erro:
        print(erro)
