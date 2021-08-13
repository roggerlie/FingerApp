import datetime

import requests
import time

import lib.pyzk as pyzk
from lib.zkmodules.defs import *
from utils import *

global ip
global db

print_header("Pilih Mesin")
print_info("1. Finger Sekyas\n"
           "2. Finger SMP\n"
           "3. Exit")

chos = input("Pilih : ")
if chos == '1':
    ip = "192.168.1.30"
    db = "fp_sekyas"
elif chos == '2':
    ip = "192.168.1.35"
    db = "fingerprint"

time.sleep(0)
ip_address = ip
machine_port = 4370

z = pyzk.ZKSS()
z.connect_net(ip_address, machine_port)
z.disable_device()


# PUT
def put(body):
    url = "http://aplikasi.pancabudi.id/api/finger/put_hr_staff_info"
    token = "xF8RLsgNAb"
    head = {
        'Content-Type': 'application/json',
        'id_token': token
    }
    link = requests.patch(url, data=body, headers=head)
    response = link.content
    return response


def datapegawai():
    print_header("List Data Pegawai")
    z.read_all_user_id()
    z.read_all_fptmp()
    z.print_users_summary()


def tambahdatapegawai(nopeg, napeg):
    print_header("Tambah Data Pegawai")
    z.read_all_user_id()
    if z.id_exists(nopeg):
        print('Id Sudah Ada')
    else:
        z.set_user_info(user_id=str(nopeg), name=napeg,
                        admin_lv=0, neg_enabled=0,
                        user_group=1)
        print("User Sukses Di Tambah")
        data = {
            'db': db,
            'FID': nopeg,
            'Nama': napeg,
            'NIK': nopeg,
            'DEPT_NAME': 'a000000001',
            'JABATAN': '',
            'TGL_MASUK': datetime.datetime.now().strftime("%d/%m/%Y"),
            'Notelp': '',
            'BE_Active': 'a'
        }
        # param = json.dumps(data)
        # pa = put(param)
        # print(pa)
        # z.read_all_user_id()
        # z.read_all_fptmp()
        # z.print_user_summary()

def editdatapegawai(nopeg, napeg):
    print_header("Edit Pegawai")
    z.read_all_user_id()
    if z.id_exists(nopeg):
        z.set_user_info(user_id=str(nopeg), name=napeg,
                        admin_lv=0, neg_enabled=0,
                        user_group=1)
        print("User Sukses Di Ubah")
    else:
        print_info('Id Tidak Terdaftar')
    datapegawai()

def tambahdatapegawaicsv(file):
    print_header("Tambah Data Pegawai By File")
    users_fn = file
    n = 0
    added_users_ids = []
    print_info("Reading users from %s file" % users_fn)
    with open(users_fn, 'r') as infile:
        infile.readline()
        for line in infile.read().splitlines():
            # extract fields from a line
            user_fields = line.split(',')
            user_id = user_fields[0]
            user_name = user_fields[1]
            added_users_ids += [user_id]

            if z.id_exists(user_id):
                print("OOOPS, user exists with the given id, "
                      "ID = %s, name = % s" % \
                      (user_id, z.users[z.id_to_sn(user_id)].user_name))
            else:
                print("User ID = %s, name = % s" % (user_id, user_name))
                tambahdatapegawai(user_id, user_name)
                n += 1
    print_info("After creating users")
    z.read_all_user_id()
    z.print_user_summary()


def daftarsidikjari(nopeg, nojari):
    print_header("Daftar Sidik Jari Pegawai")
    z.disable_device()
    z.enable_device()
    idpeg = nopeg
    jari = int(nojari)
    print_info("Tempelkan Jari Anda")
    z.enroll(idpeg, jari, 1)
    try:
        while True:
            # read user ids
            z.disable_device()
            z.read_all_user_id()
            z.enable_device()

            # enable the report of rt packets
            z.enable_realtime()
            z.recv_event()
            ev = z.get_last_event()
            if ev == EF_FPFTR:
                print("EF_FPFTR: ")
                print("Score: %i" % z.parse_score_fp_event())
            elif ev == EF_ENROLLFINGER:
                print("EF_ENROLLFINGER: Enroll finger finished")
                print("Successful: %s, user ID: %s, finger index: %s, "
                      "size fp template: %i" %
                      tuple(z.parse_event_enroll_fp()))
                z.disconnect()
                break
                exit(0)

    except KeyboardInterrupt:
        print_info("\nExiting...")

def logpresensi():
    print_header("Log Presensi")
    z.read_att_log()
    z.print_attlog()

def clearlogpresensi():
    print_header("Clear Log Presensi")
    z.read_att_log()
    z.clear_att_log()
