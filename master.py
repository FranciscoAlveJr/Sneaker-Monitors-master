from random_user_agent.params import SoftwareName, HardwareType
from random_user_agent.user_agent import UserAgent
import requests as rq
from time import sleep
from Monitores import nike

software_names = [SoftwareName.CHROME.value]
hardware_type = [HardwareType.MOBILE__PHONE]
user_agent_rotator = UserAgent(
    software_names=software_names, hardware_type=hardware_type)
    
headers = {'User-Agent': user_agent_rotator.get_random_user_agent()}
proxies = {
    'http': 'http://f4qci:bpnwdqqw@162.219.27.154:6007',
    'https': 'http://f4qci:bpnwdqqw@162.219.27.154:6007'
}
response = rq.get('http://api.privateproxy.me:10738', proxies=proxies)

id = response.text.strip('\n')
proxy = {'http': 'http://{}:6007'.format(id)}
print(proxy)
# print('>>>>>MONITOR INICIADO<<<<<')

while True:
    try:
        nike.index(proxy)
#         adidas.index(proxy)
        # artwalk.index(proxy)
#         cartel011.index(proxy)
#         authentic.index(proxy)
#         Guadalupe.index(proxy)
#         nike.index(proxy)
#         magic.index(proxy)
#         maze.index(proxy)
#         newskull.index(proxy)
#         pegasus.index(proxy)
#         yourid.index(proxy)

#         sleep(10)
    except Exception as erro:
        print(erro)
