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

estoque = []
esgotados = []

while True:
    p = get_proxys.get_proxys()
    proxy = {'http': 'http://{}'.format(p)}

    url = 'https://www.newskull.com.br/novidades'
    header = {'User-Agent': user_agent_rotator.get_random_user_agent()}

    webhook = ''

    try:
        urls = []

        response = rq.get(url, headers=header, proxies=proxy)
        soup = BeautifulSoup(response.text, 'html.parser')

        nomes = soup.find_all('h3', class_='spotTitle')
        spot_preco = soup.find_all('div', class_='spotPreco')
        precos = soup.find_all('div', class_='precoPor')
        links = soup.find_all('a', class_='spot-parte-um')
        imagens = soup.find_all('img', class_='jsImgSpot imagem-primaria')
        parcelas = soup.find_all('div', class_='details-content hide')

        for i in range(len(links)):
            urls.append(f'https://www.newskull.com.br/{links[i]["href"]}')

        if estoque == []:
            for i in range(len(nomes)):
                estoque.append(
                    f'https://www.newskull.com.br/{links[i]["href"]}')

        for i in range(len(nomes)):
            nome = nomes[i].getText().strip()
            sprecos_real = spot_preco[i].find('div', class_='precoDeVazio')
            cprecos_real = spot_preco[i].find('div', class_='precoDe')
            sreal = sprecos_real
            preco = precos[i].find('span', class_='fbits-valor')
            link = f'https://www.newskull.com.br/{links[i]["href"]}'
            imagem = imagens[i]['data-original']
            parc = parcelas[i].find_all('p')
            parc_p = parc[-1].getText().strip()[:-6]

            if link in estoque and link not in urls:
                estoque.remove(link)
                esgotados.append(link)
            elif link in urls and link not in estoque:
                estoque.append(link)
                description = 'Produto disponível para compra'
                if sreal in spot_preco[i]:
                    try:
                        data = {
                            'username': 'NewSkull Monitor',
                            'avatar_url': 'https://cdn.discordapp.com/avatars/874073826013609994/94d1cfe8fdb62e96c278b4c6673876a2.png?size=128',
                            'embeds': [{
                                'title': nome,
                                'description': description,
                                'url': link,
                                'thumbnail': {'url': imagem},
                                'color': green,
                                'timestamp': str(datetime.utcnow()),
                                'fields': [
                                    {'name': 'à vista',
                                        'value': f'R${preco.getText()}'},
                                    {'name': 'ou', 'value': f'em até {parc_p}'},
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
                    except Exception as e:
                        print(e)

                else:
                    cprecos_real = spot_preco[i].find(
                        'div', class_='precoDe')
                    valor = cprecos_real.find('span', class_='fbits-valor')
                    try:
                        data = {
                            'username': 'NewSkull Monitor',
                            'avatar_url': 'https://cdn.discordapp.com/avatars/874073826013609994/94d1cfe8fdb62e96c278b4c6673876a2.png?size=128',
                            'embeds': [{
                                'title': nome,
                                'description': description,
                                'url': link,
                                'thumbnail': {'url': imagem},
                                'color': green,
                                'timestamp': str(datetime.utcnow()),
                                'fields': [
                                    {'name': 'de', 'value': f'R${valor.getText()}'},
                                    {'name': 'por',
                                        'value': f'R${preco.getText()} à vista'},
                                    {'name': 'ou', 'value': f'em até {parc_p}'},
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
                    except Exception as e:
                        print(e)
            elif link in urls and link in esgotados:
                esgotados.remove(link)
                description = 'PRODUTO DE VOLTA PARA O ESTOQUE!!'
                if sreal in spot_preco[i]:
                    try:
                        data = {
                            'username': 'NewSkull Monitor',
                            'avatar_url': 'https://cdn.discordapp.com/avatars/874073826013609994/94d1cfe8fdb62e96c278b4c6673876a2.png?size=128',
                            'embeds': [{
                                'title': nome,
                                'description': description,
                                'url': link,
                                'thumbnail': {'url': imagem},
                                'color': red,
                                'timestamp': str(datetime.utcnow()),
                                'fields': [
                                    {'name': 'à vista',
                                        'value': f'R${preco.getText()}'},
                                    {'name': 'ou', 'value': f'em até {parc_p}'},
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
                    except Exception as e:
                        print(e)

                else:
                    cprecos_real = spot_preco[i].find(
                        'div', class_='precoDe')
                    valor = cprecos_real.find('span', class_='fbits-valor')
                    try:
                        data = {
                            'username': 'NewSkull Monitor',
                            'avatar_url': 'https://cdn.discordapp.com/avatars/874073826013609994/94d1cfe8fdb62e96c278b4c6673876a2.png?size=128',
                            'embeds': [{
                                'title': nome,
                                'description': description,
                                'url': link,
                                'thumbnail': {'url': imagem},
                                'color': red,
                                'timestamp': str(datetime.utcnow()),
                                'fields': [
                                    {'name': 'de', 'value': f'R${valor.getText()}'},
                                    {'name': 'por',
                                        'value': f'R${preco.getText()} à vista'},
                                    {'name': 'ou', 'value': f'em até {parc_p}'},
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
                    except Exception as e:
                        print(e)
    except Exception as erro:
        print(erro)
