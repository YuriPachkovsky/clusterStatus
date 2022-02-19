import requests
import time

PROMETHEUS = 'http://prometheus-core.mon.svc.cluster.local:9091'

TOKEN = ''

MESSAGE = """
Текущий статус по работе.
1. Утилизация ресурсов (%):  CPU-{}, Memory-{}, Storage-{}.
2. Суммарная загрузка на сетевых интерфейсах NetIn - {} Мбит/c , NetOut - {} Мбит/c.
"""

dict_query = {
#cpu stat utilization
'cpu':'avg(100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100))',
#memory utilz
'memory':'avg((1-node_memory_MemAvailable_bytes/node_memory_MemTotal_bytes)*100)',
#filesystem stat utilizations
'fs':'100 - avg(sum(node_filesystem_avail_bytes{mountpoint="/",fstype!="rootfs"}) by (instance) / sum(node_filesystem_size_bytes{mountpoint="/",fstype!="rootfs"}) by (instance)) * 100',
#net incom utilz
'netin':'sum(rate(node_network_receive_bytes_total{device="internal"}[5m])*8)/1024/1024',
#net out
'netout':"sum(rate(node_network_transmit_bytes_total{device='internal'}[5m])*8)/1024/1024"
}

if __name__ == '__main__':
    result = []

    for key,query in dict_query.items():
        res = requests.get(PROMETHEUS + '/api/v1/query',auth=('admin-core', '9?DZAsBR9(UsZ>_5'), params={'query': query})
        value = res.json().get('data').get('result')[0].get('value')[1]
        result.append(round(float(value),1))

    print(MESSAGE.format(*result))

    res = requests.get(f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id=-1001426350990&text={MESSAGE.format(*result)}')
