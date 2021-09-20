import requests as rq
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
from random_user_agent.params import SoftwareName, HardwareType
from random_user_agent.user_agent import UserAgent
import re
import get_proxys

software_names = [SoftwareName.CHROME.value]
hardware_type = [HardwareType.MOBILE__PHONE]
user_agent_rotator = UserAgent(
    software_names=software_names, hardware_type=hardware_type)

esgotados = []
estoque = []

red = '16711680'
green = '32768'

header = {'User-Agent': user_agent_rotator.get_random_user_agent()}

while True:
    p = get_proxys.get_proxys()
    proxy = {'http': 'http://{}'.format(p)}

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
                {'name': 'Tamanho:', 'value': tamanho},
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

    webhook = ''
    try:
        headers = {'User-Agent': user_agent_rotator.get_random_user_agent()}

        source = rq.get(url, proxies=proxy)
        soup = BeautifulSoup(source.text, 'html.parser')

        nome_produto = soup.find_all("h2", class_="produto__detalhe-titulo")
        link = soup.find_all("a", class_="aspect-radio-box")
        imagens = soup.find_all('img', class_='aspect-radio-box-inside')


        if estoque == []:
            try:
                for i in range(len(nome_produto)):
                    url_p = link[i]['href']
                    nome = nome_produto[i].getText()
                    r = rq.get(url_p, headers=headers, proxies=proxy)

                    source2 = r.text
                    soup2 = BeautifulSoup(source2, "lxml")

                    t = soup2.find_all('script')
                    html = str(t[9])

                    match = re.search(r'SKUsCorTamanho = (.*})', html, flags=re.DOTALL)
                    t = match[1]
                    j = json.loads(t)

                    for tamanho, v in j.items():
                        stock = int(v["TemEstoque"])
                        produto = f'{nome}-{tamanho}'
                        if stock == 0:
                            esgotados.append(produto)
                        else:
                            estoque.append(produto)
            except Exception as erro:
                print(erro)
        try:
            for i in range(len(nome_produto)):
                url_p = link[i]['href']
                nome = nome_produto[i].getText()
                r = rq.get(url_p, headers=headers, proxies=proxy)

                source2 = r.text
                soup2 = BeautifulSoup(source2, "lxml")

                price = soup2.find_all("span", class_="js-valor-por")
                t = soup2.find_all('script')
                html = str(t[9])

                match = re.search(r'SKUsCorTamanho = (.*})', html, flags=re.DOTALL)
                t = match[1]
                j = json.loads(t)

                for tamanho, v in j.items():
                    stock = int(v["TemEstoque"])
                    produto = f'{nome}-{tamanho}'

                    print(type(tamanho))
                    if stock == 0:
                        if produto in estoque and produto not in esgotados:
                            estoque.remove(produto)
                            esgotados.append(produto)
                    else:
                        if produto not in estoque and produto not in esgotados:
                            description = 'PRODUTO DISPONÍVEL'
                            estoque.append(produto)
                            imagem = imagens[i]['data-src']
                            print(nome)
                            print(description)
                            monitor_post(green)
                        elif produto not in estoque and produto in esgotados:
                            description = 'RESTOCK'
                            imagem = imagens[i]['data-src']
                            esgotados.remove(produto)
                            estoque.append(produto)
                            print(nome)
                            print(description)
                            monitor_post(red)
        except Exception as erro:
            print(erro)
    except Exception as erro:
        print(erro)
    time.sleep(2)