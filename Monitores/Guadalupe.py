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
            'username': 'Guadalupe Monitor',
            'avatar_url': 'https://cdn.discordapp.com/avatars/874073826013609994/94d1cfe8fdb62e96c278b4c6673876a2.png?size=128',
            'embeds': [{
                'title': nome,
                'description': description,
                'url': link,
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

    url = 'https://gdlp.com.br/lancamentos'
    header = {'User-Agent': user_agent_rotator.get_random_user_agent()}

    webhook = 'https://discord.com/api/webhooks/875540490047606846/tDiJ13UisbJaxidVt9L-CM9m_srKPwzJEOgxYjRnwsfdpIRqTufDhU8sdyjan0kl6IlW'

    try:

        source = rq.get(url, headers=header, proxies=proxy)
        soup = BeautifulSoup(source.text, 'html.parser')

        precos = soup.find_all('span', class_='price')
        nomes = soup.find_all('h2', class_='product-name')
        links = soup.find_all('a', class_='product-image')
        parcels = soup.find_all('span', class_='precoparcelado-parcels')
        price_box = soup.find_all('div', class_='price-box')

        for i in parcels:
            parcel = i.getText()

        if estoque == []:
            for i in links:
                estoque.append(i['href'])
        try:
            for i in range(len(nomes)):
                nome = nomes[i].getText()
                preco = precos[i].getText()
                link = links[i]['href']
                imagens = links[i].find_all('img')
                img = imagens[0]['src']
                source2 = rq.get(link, headers=header, proxies=proxy)
                soup2 = BeautifulSoup(source2.text, 'html.parser')

                status = soup2.find('p', class_='availability').find(
                    'span', class_='value').getText()

                if link in estoque and status == 'Sem estoque':
                    estoque.remove(link)
                    esgotados.append(link)
                elif status == 'Em estoque' and link not in estoque:
                    estoque.append(link)
                    description = 'Produto disponível para compra'
                    print(nome)
                    print(description)
                    monitor_post(green)
                elif link in esgotados and status == 'Em estoque':
                    esgotados.remove(link)
                    estoque.append(link)
                    description = 'PRODUTO DE VOLTA AO ESTOQUE!!'
                    print(nome)
                    print(description)
                    monitor_post(red)
        except Exception as e:
            print(e)

        time.sleep(1.5)
    except Exception as erro:
        print(erro)
