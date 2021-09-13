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
            'username': 'Pegasos Monitor',
            'avatar_url': 'https://cdn.discordapp.com/avatars/874073826013609994/94d1cfe8fdb62e96c278b4c6673876a2.png?size=128',
            'embeds': [{
                'title': nome,
                'description': description,
                'url': link,
                'thumbnail': {'url': imagem},
                'color': color,
                'timestamp': str(datetime.utcnow()),
                'fields': [
                    {'name': nparcela, 'value': f'de {vparcela}'},
                    {'name': 'à vista', 'value': preco},
                    {'name': 'ou',
                        'value': f'{boleto} via Boleto Bancário'},
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

    url = 'https://www.pegasos.com.br/'
    header = {'User-Agent': user_agent_rotator.get_random_user_agent()}

    webhook = 'https://discord.com/api/webhooks/875710007763693599/YmMTILN_scGeqwOCqbmbsFsL7hyvahO7SqA7YK29lo40sm6zLHi2BEGZ8zKprWetLHxg'

    try:
        urls = []

        response = rq.get(url, headers=header, proxies=proxy)
        soup = BeautifulSoup(response.text, 'html.parser')

        produtos = soup.find_all('ul', class_='produtos-carrossel')
        info = produtos[0].find_all('div', 'preco-produto destaque-parcela')
        nomes = produtos[0].find_all('a', class_='nome-produto cor-secundaria')
        precos = produtos[0].find_all('strong', class_='preco-promocional')
        n_parcelas = produtos[0].find_all('span', class_='preco-parcela')
        v_parcelas = produtos[0].find_all(
            'strong', class_='cor-principal titulo')
        boletos = produtos[0].find_all('strong', class_='cor-secundaria')
        imagens = produtos[0].find_all('img', class_='imagem-principal')

        for i in range(len(nomes)):
            urls.append(nomes[i]['href'])

        if estoque == []:
            for i in range(len(nomes)):
                estoque.append(nomes[i]['href'])

        for i in range(len(nomes)):
            try:
                nome = nomes[i].getText()
                preco = precos[i].getText().strip()
                if len(info[i]) == 11:
                    nparcela = n_parcelas[i].getText()[:3].strip()
                    vparcela = v_parcelas[i].getText()
                link = nomes[i]['href']
                boleto = boletos[i].getText()
                imagem = imagens[i]['src']

                if link in estoque and link not in urls:
                    estoque.remove(link)
                    esgotados.append(link)
                elif link in urls and link not in estoque:
                    estoque.append(link)
                    description = 'Produto disponível para compra'
                    monitor_post(green)
                elif link in esgotados and link in urls:
                    esgotados.remove(link)
                    estoque.append(link)
                    description = 'PRODUTO DE VOLTA PARA O ESTOQUE!!'
                    monitor_post(red)
            except Exception as e:
                print(e)
    except Exception as erro:
        print(erro)
