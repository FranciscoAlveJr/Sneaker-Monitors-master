from bs4 import BeautifulSoup
import requests as rq
import json
from datetime import datetime
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

    def monitor_post(color):
        data = {
            'username': 'Cartel 011 Monitor',
            'avatar_url': 'https://cdn.discordapp.com/avatars/874073826013609994/94d1cfe8fdb62e96c278b4c6673876a2.png?size=128',
            'embeds': [{
                'title': nome,
                'description': description,
                'url': link,
                'thumbnail': {'url': imagem},
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

    url = 'https://shop.cartel011.com.br/novidades-cat.html'
    header = {'User-Agent': user_agent_rotator.get_random_user_agent()}

    webhook = ''

    try:
        urls = []

        source = rq.get(url, headers=header, proxies=proxy)
        soup = BeautifulSoup(source.text, 'html.parser')

        nomes = soup.find_all('h2', class_='product-name')
        precos = soup.find_all('span', class_='price')
        links = soup.find_all('a', class_='product-image')
        imagens = soup.find_all('img', class_='hoverImage')

        for i in range(len(links)):
            urls.append(links[i]['href'])

        if estoque == []:
            for i in range(len(links)):
                estoque.append(links[i]['href'])

        for i in range(len(nomes)):
            try:
                nome = nomes[i].find('a')['title']
                preco = precos[i].getText()
                link = links[i]['href']
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
                    description = 'PRODUTO DE VOLTA AO ESTOQUE!!'
                    monitor_post(red)
            except Exception as e:
                print(e)
    except Exception as erro:
        print(erro)
