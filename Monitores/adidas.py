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

url = 'https://www.adidas.com.br/novidades'
url_p = 'https://www.adidas.com.br/api/search/product/'
disp = 'https://www.adidas.com.br/api/products/{}/availability'

header = {'User-Agent': user_agent_rotator.get_random_user_agent()}

esgotados = []
estoque = []

def index(proxy):
    def monitor_post(color):
        data = {
            'username': 'Adidas Monitor',
            'avatar_url': 'https://images.rappi.com.br/store_type/adidas-1585611585.png?d=200x200',
            'embeds': [{
                'title': nome,
                'description': description,
                'url': link,
                'thumbnail': {'url': imagem},
                'color': color,
                'timestamp': str(datetime.utcnow()),
                'fields': [
                    {'name': 'Cores:', 'value': cores},
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
            print("Payload delivered successfully, code {}.".format(
                result.status_code))

    webhook = 'https://discord.com/api/webhooks/857347905051689000/DD3Jinegpu4CGs0UO_L1Gl3lbo_aXI6nYrIabVcToN6-PKjtHhTy-Xr1OFOL7TFHj8t0'

    source = rq.get(url, headers=header, proxies=proxy)
    soup = BeautifulSoup(source.text, 'html.parser')

    item = soup.find_all("div", class_="grid-item___3rAkS")
    detalhes = soup.find_all("div", class_="gl-product-card__details")

    try:
        if estoque == []:
            for i in range(len(detalhes)):
                id_p = item[i]['data-grid-id']
                disponivel = rq.get(disp.format(id_p), headers=header)
                produto = rq.get(url_p+id_p, headers=header)
                d = json.loads(disponivel.text)
                p = json.loads(produto.text)
                status = d['availability_status']
                link = f'https://www.adidas.com.br{p["link"]}'
                if status == 'IN_STOCK':
                    estoque.append(link)
        for i in range(len(detalhes)):
            try:
                id_p = item[i]['data-grid-id']
                disponivel = rq.get(disp.format(id_p), headers=header)
                produto = rq.get(url_p+id_p, headers=header)
                d = json.loads(disponivel.text)
                p = json.loads(produto.text)
                status = d['availability_status']
                link = f'https://www.adidas.com.br{p["link"]}'
                nome = detalhes[i].getText()
                preco = p['price']
                imagem = p['image']['src']
                cores = p['color']
                
                if status == 'NOT_AVAILABLE' and link not in esgotados and link not in estoque:
                    esgotados.append(link)
                elif status == 'NOT_AVAILABLE' and link in estoque:
                    estoque.remove(link)
                    esgotados.append(link)
                elif link not in estoque and status == 'IN_STOCK':
                    description = 'Produto disponível para compra'
                    estoque.append(link)
                    monitor_post(green)
                elif link in esgotados and status == 'IN_STOCK':
                    description = 'PRODUTO DE VOLTA AO ESTOQUE!!'
                    esgotados.remove(link)
                    estoque.append(link)
                    monitor_post(red)
            except Exception as e:
                print(e)


        time.sleep(1.5)
    except Exception as erro:
        print(erro)
