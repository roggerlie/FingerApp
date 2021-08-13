from finger import *


def main():
    print_header("AVAILABLE MENU")
    print_info("1. Lihat Data Pegawai\n"
               "2. Tambah Data Pegawai\n"
               "3. Edit Nama Pegawai\n"
               "4. Tambah Data Pegawai By CSV\n"
               "5. Daftar Sidik Jari\n"
               "6. Log Presensi\n"
               "7. Clear Log Presensi\n"
               "8. Exit")
    print("\n")
    chos = input("Pilih : ")
    if chos == '1':
        datapegawai()
        main()

    elif chos == '2':
        nopeg = input('[!] Masukkan No Pegawai >> ')
        napeg = input('[!] Masukkan Nama Pegawai >> ')
        tambahdatapegawai(nopeg, napeg)
        main()

    elif chos == '3':
        nopeg = input('[!] Masukkan No Pegawai >> ')
        napeg = input('[!] Masukkan Nama Pegawai >> ')
        editdatapegawai(nopeg, napeg)
        main()

    elif chos == '4':
        namafile = input('[!] Masukkan Nama Filenya >> ')
        tambahdatapegawaicsv(namafile)
        main()
    elif chos == '5':
        datapegawai()
        nopeg = input('[!] Masukkan No Pegawai >> ')
        nojari = input('[!] Masukkan No Jari >> ')
        daftarsidikjari(nopeg, nojari)
    elif chos == '6':
        logpresensi()
        main()
    elif chos == '7':
        logpresensi()
        clearlogpresensi()
        main()
    elif chos == '8':
        exit()


if __name__ == '__main__':
    main()
