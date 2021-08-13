import time

import lib.pyzk as pyzk
from lib.zkmodules.defs import *
from utils import *

time.sleep(0)

ip_address = '192.168.1.30'  # set the ip address of the device to test
machine_port = 4370

print_header("TEST OF DATA-USER FUNCTIONS")

z = pyzk.ZKSS()
z.connect_net(ip_address, machine_port)
z.disable_device()

print_header("1.Read all user info")

# delete user if it exists
user1_id = input(" User ID : ")
z.read_all_user_id()
z.read_all_fptmp()
z.print_users_summary()

ans = input("Delete user %s, y/n: " % user1_id)
if ans == 'y':
    if z.id_exists(user1_id):
        z.delete_user(user1_id)
    else:
        print("No User ID")
else:
    print_info("Now you may go and test both finger templates")

print_header("")
z.read_all_user_id()
z.read_all_fptmp()
z.print_users_summary()

z.enable_device()
z.disconnect()
