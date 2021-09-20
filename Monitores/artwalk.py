from bs4 import BeautifulSoup
import requests as rq
import json
from datetime import datetime
import random
from random_user_agent.params import SoftwareName, HardwareType
from random_user_agent.user_agent import UserAgent
import get_proxys
from time import sleep

p = get_proxys.get_proxys()
proxy = {'http': 'http://{}'.format(p)}


software_names = [SoftwareName.CHROME.value]
hardware_type = [HardwareType.MOBILE__PHONE]
user_agent_rotator = UserAgent(
    software_names=software_names, hardware_type=hardware_type)

red = '16711680'
green = '32768'

header = {'User-Agent': user_agent_rotator.get_random_user_agent()}

estoque = []
esgotados = []

def index(proxy):
    def monitor_post(color):
        data = {
            'username': 'Artwalk Monitor',
            'avatar_url': 'https://cdn.discordapp.com/avatars/874073826013609994/94d1cfe8fdb62e96c278b4c6673876a2.png?size=128',
            'embeds': [{
                'title': nome,
                'description': description,
                'url': link,
                'thumbnail': {'url': imagem},
                'color': color,
                'timestamp': str(datetime.utcnow()),
                'fields': [
                    {'name': 'Tamanho:', 'value': tamanho},
                    {'name': 'Preço:', 'value': f'R${str(preco)}'},
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

    url = 'https://www.artwalk.com.br/novidades?PS=24&O=OrderByReleaseDateDESC'

    webhook = ''

    try:
        source = rq.get(url, headers=header, proxies=proxy)
        soup = BeautifulSoup(source.text, 'html.parser')

        p_link = soup.find_all('a', class_='product-item__image')

        try:
            if estoque == []:
                for i in range(len(p_link)):
                    url_p = p_link[i]['href']
                    response2 = rq.get(url_p, headers=header, proxies=proxy)
                    soup2 = BeautifulSoup(response2.text, 'html.parser')

                    skus = soup2.find('input', attrs={'id':'___rc-p-sku-ids'})
                    id = skus['value'].split(',')[0]

                    url_a = rq.get(
                        f'https://www.artwalk.com.br/api/catalog_system/pub/products/search?&fq=skuId:{id}', headers=header, proxies=proxy)
                    p = json.loads(url_a.text)
                    item = p[0]
                    
                    for i in range(len(item['items'])):
                        acessivel = item['items'][i]['sellers'][0]['commertialOffer']['IsAvailable']
                        tamanho = item['items'][i]['Tamanho'][0]
                        nome = item['productName']
                        produto = f'{nome}-{tamanho}'
                        
                        if acessivel == True:
                            estoque.append(produto)
                        elif acessivel == False:
                            esgotados.append(produto)
        except Exception as e:
            print(e)
        print(estoque)
        print(esgotados)
        try:
            for i in range(len(p_link)):
                url_p = p_link[i]['href']

                response2 = rq.get(url_p, headers=header, proxies=proxy)
                soup2 = BeautifulSoup(response2.text, 'html.parser')

                skus = soup2.find('input', attrs={'id':'___rc-p-sku-ids'})
                id = skus['value'].split(',')[0]

                url_a = rq.get(
                    f'https://www.artwalk.com.br/api/catalog_system/pub/products/search?&fq=skuId:{id}', headers=header, proxies=proxy)
                p = json.loads(url_a.text)
                item = p[0]

                nome = item['productName']
                link = item['link']
                preco = item['items'][0]['sellers'][0]['commertialOffer']['Price']
                imagem = item['items'][0]['images'][0]['imageUrl']

                for i in range(len(item['items'])):
                    acessivel = item['items'][i]['sellers'][0]['commertialOffer']['IsAvailable']
                    tamanho = item['items'][i]['Tamanho'][0]
                    produto = f'{nome}-{tamanho}'
                
                    if acessivel == False and produto not in estoque and produto not in esgotados:
                        esgotados.append(produto)
                    elif acessivel == False and produto in estoque and produto not in esgotados:
                        estoque.remove(produto)
                        esgotados.append(produto)
                    elif acessivel == True and produto not in estoque and produto not in esgotados:
                        estoque.append(produto)
                        description = 'Produto disponível para compra!'
                        print(produto)
                        print(description)
                        monitor_post(green)
                    elif acessivel == True and produto in esgotados and produto not in estoque:
                        esgotados.remove(produto)
                        estoque.append(produto)
                        description = 'PRODUTO DE VOLTA PARA O ESTOQUE!!'
                        print(produto)
                        print(description)
                        monitor_post(red)
        except Exception as e:
            print(e)
    except Exception as erro:
        print(erro)
    sleep(2)

