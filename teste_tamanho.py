from enum import IntEnum
from bs4 import BeautifulSoup
import requests as rq
import json
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

def get_proxys():
    header = {'User-Agent': user_agent_rotator.get_random_user_agent()}
    url = 'https://www.freeproxy.world/?country=BR'

    ip_list = []
    ports_list = []
    proxy_list = []

    try:
        response = rq.get(url, headers=header)
        soup = BeautifulSoup(response.text, 'html.parser')
        proxies = soup.find(
            'table', class_='layui-table').find_all('td', class_='show-ip-div')
        ports = soup.find('table', class_='layui-table').find_all('a')

        for p in proxies:
            ip_list.append(p.text.strip())

        for p in range(0, len(ports), 5):
            ports_list.append(ports[p].text.strip())

        for i in range(len(proxies)):
            proxy_list.append('{}:{}'.format(ip_list[i], ports_list[i]))

    except:
        return '169.57.157.148:80'

    return random.choice(proxy_list)


esgotados = []
estoque = []

red = '16711680'
green = '32768'

while True:
    p = get_proxys()
    proxy = {'http': 'http://{}'.format(p)}

    url1 = 'https://www.nike.com.br/lancamento-todos-110'
    url2 = 'https://www.nike.com.br/lancamento-todos-110?p=1&loja=&Fabricante=&Filtros=Marcas%3ANike%7CTipo+de+Produto%3ACal%E7ados&cor=&tamanho=&precode=&precoate=&ofertas=&ordenacao=6&limit=24&ordemFiltro=Tipo+de+Produto%7CMarcas&direto=1?p=1&loja=&Fabricante=&Filtros=Marcas%3ANike%7CTipo+de+Produto%3ACal%E7ados&cor=&tamanho=&precode=&precoate=&ofertas=&ordenacao=6&limit=24&ordemFiltro=Tipo+de+Produto%7CMarcas&direto=1'
    url3 = 'https://www.nike.com.br/lancamento-todos-110?p=1&loja=&Fabricante=&Filtros=Marcas%3AJordan%7CTipo+de+Produto%3ACal%E7ados&cor=&tamanho=&precode=&precoate=&ofertas=&ordenacao=1&limit=24&ordemFiltro=Tipo+de+Produto%7CMarcas&direto=1?p=1&loja=&Fabricante=&Filtros=Marcas%3AJordan%7CTipo+de+Produto%3ACal%E7ados&cor=&tamanho=&precode=&precoate=&ofertas=&ordenacao=1&limit=24&ordemFiltro=Tipo+de+Produto%7CMarcas&direto=1'
    urls = [url1, url2, url3]

    header = {'User-Agent': user_agent_rotator.get_random_user_agent()}

    webhook = 'https://discord.com/api/webhooks/854371528190722058/5reJgzW8T9vrBqDp-D9a4-uGGAIGkJ0ME2Z7d9SNJTZjPVU0a_ZfjBy7NONCE8G-4VLA'

    def monitor_post(color):
        data = {
            'username': 'Nike Monitor',
            'avatar_url': 'https://cdn.discordapp.com/avatars/874073826013609994/94d1cfe8fdb62e96c278b4c6673876a2.png?size=128',
            'embeds': [{
                'title': nome,
                'description': description,
                'url': link,
                'thumbnail': {'url': imagem},
                'color': color,
                'timestamp': str(datetime.utcnow()),
                'fields': [
                    {'name': 'Tamanho', 'value': size.text},
                    {'name': 'Preço', 'value': preco},
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

    # if estoque == []:
    #     for url in urls:
    #         source = rq.get(url, headers=header, proxies=proxy)
    #         soup = BeautifulSoup(source.text, 'html.parser')

    #         links = soup.find_all('a', class_= 'produto__nome')
    #         nomes = soup.find_all('a', class_='produto__nome')
    #         precos = soup.find_all('span', class_='produto__preco_por ws-nr')
            
    #         for i in range(len(links)):
    #             link = links[i]['href']
                
    #             source2 = rq.get(link, headers=header, proxies=proxy)
    #             soup2 = BeautifulSoup(source2.text, 'html.parser')

    #             tamanhos = soup2.find('div', class_='variacoes-tamanhos')
    #             tamanho = tamanhos.find_all('li')
    #             desab = tamanhos.find_all('li', class_='tamanho-desabilitado')
                
    #             for i in range(len(tamanho)):
    #                 size = tamanho[i]
    #                 if size not in desab:
    #                     estoque.append(size)
    #                 elif size in desab:
    #                     esgotados.append(size)

    for url in urls:
        print(url)

        source = rq.get(url, headers=header, proxies=proxy)
        soup = BeautifulSoup(source.text, 'html.parser')

        links = soup.find_all('a', class_= 'produto__nome')
        nomes = soup.find_all('a', class_='produto__nome')
        precos = soup.find_all('span', class_='produto__preco_por ws-nr')

        for i in range(len(links)):
            link = (links[i]['href'])
            
            source2 = rq.get(link, headers=header, proxies=proxy)
            soup2 = BeautifulSoup(source2.text, 'html.parser')

            img = soup2.find('div', class_='variacoes-cores-cor selected-item variacoes-cores_item').find('img', class_='lazy')
            imagem = img['data-src']
            # indisp = soup2.find('div', class_='detalhes-produto__indisponivel mt-2 mt-sm-5')
            # breve = soup2.find('div', class_='produto__tag produto__tag--prevenda js-pre-venda')
            nome = nomes[i].text
            preco = precos[i].text
            tamanhos = soup2.find('div', class_='variacoes-tamanhos')
            tamanho = tamanhos.find_all('li')
            desab = tamanhos.find_all('li', class_='tamanho-desabilitado')


            for i in range(len(tamanho)):
                size = tamanho[i]
                
                if size in desab and size not in esgotados:
                    esgotados.append(size)
                    if size in estoque:
                        estoque.remove(size)
                elif size not in desab and size not in estoque and size not in esgotados:
                    description = 'Produto disponível para compra'
                    estoque.append(link)
                    print(nome)
                    print(description)
                    monitor_post(green)
                elif size not in desab and size in esgotados and size not in estoque:
                    esgotados.remove(size)
                    estoque.append(size)
                    description = 'PRODUTO DE VOLTA AO ESTOQUE!!'
                    print(f'{nome}-{size.text}')
                    print(description)
                    monitor_post(red)  
            