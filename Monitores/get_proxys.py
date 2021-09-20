from bs4 import BeautifulSoup
import requests as rq
from random_user_agent.params import SoftwareName, HardwareType
from random_user_agent.user_agent import UserAgent
import random


software_names = [SoftwareName.CHROME.value]
hardware_type = [HardwareType.MOBILE__PHONE]
user_agent_rotator = UserAgent(
    software_names=software_names, hardware_type=hardware_type)


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
