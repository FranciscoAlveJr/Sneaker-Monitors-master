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
            'username': 'Magic Feet Monitor',
            'avatar_url': 'https://cdn.discordapp.com/avatars/874073826013609994/94d1cfe8fdb62e96c278b4c6673876a2.png?size=128',
            'embeds': [{
                'title': nome,
                'description': description,
                'url': link,
                'thumbnail': {'url': imagem},
                'color': color,
                'timestamp': str(datetime.utcnow()),
                'fields': [
                    {'name': 'Preço:',
                        'value': f'R${str(preco)}'},
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

    url = 'https://www.magicfeet.com.br/lancamentos'
    header = {'User-Agent': user_agent_rotator.get_random_user_agent()}

    webhook = 'https://discord.com/api/webhooks/880195379352723527/5bH5TCluFJ_ImcXKcNMLqj16TtaNhkOf61nQ0GpBptRfKKMQQkvXiyJ4MEYByyPyVZ07'

    try:
        response = rq.get(url, headers=header, proxies=proxy)
        soup = BeautifulSoup(response.text, 'html.parser')

        p_link = soup.find_all('a', class_='js--lazyload has--lazyload')

        urls = []

        for i in range(len(p_link)):
            urls.append(p_link[i]['href'])

        if estoque == []:
            for i in range(len(p_link)):
                estoque.append(p_link[i]['href'])

        for i in range(len(p_link)):
            try:
                url = p_link[i]['href']

                response2 = rq.get(url, headers=header)
                soup2 = BeautifulSoup(response2.text, 'html.parser')

                sku = soup2.find_all(
                    "script", attrs={'type': "text/javascript"})

                for s in sku[1]:
                    i = s

                skuid = (i[9:])
                d = json.loads(skuid[:-1])
                ids = d['skus'].split(';')
                id = ids[0]

                url = rq.get(
                    f'https://www.magicfeet.com.br/api/catalog_system/pub/products/search?&fq=skuId:{id}', headers=header)
                p = json.loads(url.text)
                item = p[0]

                nome = item['productName']
                link = item['link']
                preco = item['items'][0]['sellers'][0]['commertialOffer']['Price']
                imagem = item['items'][0]['images'][0]['imageUrl']

                if link in estoque and link not in urls:
                    estoque.remove(link)
                    esgotados.append(link)
                elif link in urls and link not in estoque:
                    description = 'Produto disponível para compra'
                    estoque.append(link)
                    monitor_post(green)
                elif link in urls and link in esgotados:
                    description = 'PRODUTO DE VOLTA AO ESTOQUE!!'
                    esgotados.remove(link)
                    estoque.append(link)
                    monitor_post(red)
            except Exception as e:
                print(e)
            time.sleep(2)
    except Exception as erro:
        print(erro)
