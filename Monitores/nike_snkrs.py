import requests as rq
from bs4 import BeautifulSoup
import json
import random
import time
from datetime import datetime
from random_user_agent.params import SoftwareName, HardwareType
from random_user_agent.user_agent import UserAgent

software_names = [SoftwareName.CHROME.value]
hardware_type = [HardwareType.MOBILE__PHONE]
user_agent_rotator = UserAgent(
    software_names=software_names, hardware_type=hardware_type)

esgotados = []
estoque = []

red = '16711680'
green = '32768'

header = {'User-Agent': user_agent_rotator.get_random_user_agent()}

def index(proxy):
    def monitor_post(color):
        data = {
            'username': 'Nike Monitor',
            'avatar_url': 'https://cdn.discordapp.com/avatars/874073826013609994/94d1cfe8fdb62e96c278b4c6673876a2.png?size=128',
            'embeds': [{
                'title': nome,
                'description': description,
                'url': url_p,
                'thumbnail': {'url': imagem},
                'color': color,
                'timestamp': str(datetime.utcnow()),
                'fields': [
                    {'name': 'Preço', 'value': price[0].getText()},
                ]
            }]
        }
        result = rq.post(webhook, data=json.dumps(data), headers={
                        "Content-Type": "application/json"}, proxies=proxy)

        try:
            result.raise_for_status()
        except rq.exceptions.HTTPError as err:
            print(err)
        else:
            print("Payload delivered successfully, code {}.".format(
                result.status_code))

    url = 'https://www.nike.com.br/Snkrs/Estoque'
    url2 = 'https://www.nike.com.br/Snkrs/feed'

    webhook = 'https://discord.com/api/webhooks/875539503371153428/MRBnYo_yrbSUuvXJoN80RmMaw7PUfLygNQUqk_DzC0wgtsqaFMYj0sCnOoUgQ5mcUTF4'
    try:
        headers = {'User-Agent': user_agent_rotator.get_random_user_agent()}

        source = rq.get(url, proxies=proxy)
        soup = BeautifulSoup(source.text, 'html.parser')

        nome_produto = soup.find_all("h2", class_="produto__detalhe-titulo")
        link = soup.find_all("a", class_="aspect-radio-box")
        imagens = soup.find_all('img', class_='aspect-radio-box-inside')
        status = soup.find_all("h3", class_="button")

        source1 = rq.get(url2, proxies=proxy)
        soup1 = BeautifulSoup(source1.text, 'html.parser')

        nome_produto1 = soup1.find_all("h2", class_="produto__detalhe-titulo")
        link1 = soup1.find_all("a", class_="aspect-radio-box")
        imagens1 = soup1.find_all('img', class_='aspect-radio-box-inside')
        status1 = soup1.find_all("h3", class_="button")

        if estoque == []:
            for i in range(len(status)):
                if status[i].getText() == 'Comprar':
                    estoque.append(link[i]['href'])
        
        if esgotados == []:
            for i in range(len(status1)):
                if status1[i].text == 'Esgotado':
                    esgotados.append(link1[i]['href'])

        for i in range(len(status)):
            url_p = link[i]['href']
            nome = nome_produto[i].getText()
            r = rq.get(url_p, headers=headers, proxies=proxy)

            html2 = r.text
            soup2 = BeautifulSoup(html2, "html.parser")
            price = soup2.find_all("span", class_="js-valor-por")
            acesso = status[i].getText()

            if acesso == 'Esgotado' and url_p in estoque:
                estoque.remove(url_p)
                esgotados.append(url_p)
            elif acesso == 'Comprar' and url_p not in estoque and url_p not in esgotados:
                description = 'Produto disponível para compra'
                estoque.append(url_p)
                imagem = imagens[i]['data-src']
                print(nome)
                print(description)
                monitor_post(green)
        
        for l in esgotados:
            r = rq.get(l, headers=headers, proxies=proxy)

            html2 = r.text
            soup2 = BeautifulSoup(html2, "html.parser")
            
            nome = soup2.find('div', class_='nome-preco-produto').text
            img = soup2.find('img', attrs={'itemprop':'image'})
            price = soup2.find_all("span", class_="js-valor-por")
            esgotado = soup2.find('p', class_='mb-0 mt-5 esgotado')
            disponivel = soup2.find('p', class_='mb-0 mt-5 esgotado hidden')

            if disponivel:
                description = 'PRODUTO DE VOLTA AO ESTOQUE!!'
                imagem = img['src']
                esgotados.remove(l)
                estoque.append(l)
                print(nome)
                print(description)
                monitor_post(red)
    except Exception as erro:
        print(erro)
