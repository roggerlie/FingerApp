import json
import socket
from datetime import datetime

import requests
from time import sleep

from prettytable import PrettyTable

import lib.pyzk as pyzk
from lib.zkmodules.defs import *
from utils import *


# PUT
def put(body):
    url = "http://api.pancabudi.sch.id/log"
    token = "xF8RLsgNAb"
    head = {
        'Content-Type': 'application/json',
        'x-api-key': token
    }
    link = requests.post(url, data=body, headers=head)
    response = link.content
    return response


def is_connected():
    try:
        socket.create_connection(('192.168.1.30', 80))
        return True
    except OSError:
        pass
    return False


sleep(0)
ip_address = '192.168.1.30'
machine_port = 4370

z = pyzk.ZKSS()
z.connect_net(ip_address, machine_port)

z.disable_device()
z.read_all_user_id()
z.enable_device()

z.enable_realtime()
print_header("Waitting For Event SEKYAS")
try:
    while True:
        if not is_connected():
            print('Connecting ...')
            while True:
                if is_connected():
                    print('Connected !')
                    sleep(2)
                    break
        z.recv_event()
        ev = z.get_last_event()
        # process the event
        print("\n" + "#" * 50)
        print("Received event " + str(ev))
        if ev == EF_ATTLOG:
            print("EF_ATTLOG: New attendance entry")
            print("User id: %s, verify type %i, date: %s" %
                  tuple(z.parse_event_attlog()))

            dt = datetime.strptime(z.parse_event_attlog()[2], '%Y/%m/%d %H:%M:%S')
            Tanggal_Log = dt.strftime('%d/%m/%Y')
            Jam_Log = dt.strftime('%H:%M:%S')
            DateTime = dt.strftime('%d/%m/%Y %H:%M:%S')
            waktuFinger = dt.strftime('%Y-%m-%d %H:%M:%S')
            data = {
                'Fid': tuple(z.parse_event_attlog())[0],
                'Tanggal_Log': Tanggal_Log,
                'Jam_Log': Jam_Log,
                'DateTime': DateTime,
                'waktuFinger': waktuFinger,
                'typeAbsen': 'Auto'
            }

            param = json.dumps(data)
            pa = put(param)
            print(pa)
            # print_header('Tabel Realtime Finger Sekyas')
            t_headers = ['Fid', 'DateTime', 'Type']
            summ_table = PrettyTable(t_headers)
            summ_table.add_row([
                tuple(z.parse_event_attlog())[0],
                DateTime,
                'Auto'
            ])
            print(summ_table)

except KeyboardInterrupt:
    print_info("\nExiting...")

z.disconnect()
exit(0)
