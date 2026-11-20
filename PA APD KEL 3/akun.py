# Mengambil data akun dan sesi program.
from data import data_user, sesi
# Mengambil fitur untuk memeriksa login, nama, dan angka.
from validasi import cek_login, validasi_nama, validasi_angka
# Mengambil fitur untuk mengelola dan menghubungkan data pengguna.
from logika import data_milik, hubungkan_data_ke_akun
# Mengambil fitur untuk menerima masukan pengguna.
from input import (
    input_nama, input_angka, input_password, input_username_baru, input_password_baru
)
# Mengambil fitur untuk menampilkan tabel, memberi jeda, dan meminta konfirmasi.
from tampilan import buat_tabel, jeda, konfirmasi
# Mengambil fitur untuk menyimpan data.
from penyimpanan import simpan_data

# Untuk menghentikan program yang sedang berjalan.
def keluar_program():
    sesi["program_berjalan"] = False
    print("Terima Kasih Telah Menggunakan Sistem Data Vaksin")


# Untuk memproses login dan memeriksa username serta password pengguna.
def proses_login():
    print("LOGIN")
    username = input("Username: ").strip().lower()
    password = input_password("Password: ")

    try:
        role = cek_login(username, password)
    except ValueError as e:
        print(e)
    else:
        sesi["user_aktif"] = {"username": username, "role": role}
        print(f"Login berhasil, {username}!")
    finally:
        jeda()


# Untuk mendaftarkan akun baru dan menyimpan data pengguna.
def proses_register():
    print("REGISTER AKUN BARU")
    print("Ketik '0' pada Username untuk kembali ke menu awal")
    username = input_username_baru()

    if username is None:
        print("Registrasi dibatalkan")
    else:
        nama = input_nama("Nama Lengkap: ")
        umur = input_angka("Umur (1-120): ", "Umur", 1, 120)
        password = input_password_baru()
        data_user[username] = {"password": password, "role": "user", "nama": nama, "umur": umur}
        terhubung = hubungkan_data_ke_akun(username)
        simpan_data()
        print("Registrasi berhasil! Silakan login.")

        if terhubung > 0:
            print(f"{terhubung} data vaksinasi atas nama {nama} otomatis terhubung ke akunmu.")

    jeda()


# Untuk mengeluarkan pengguna dari akun yang sedang aktif.
def proses_logout():
    sesi["user_aktif"] = None
    print("Logout berhasil.")


# Untuk menampilkan daftar seluruh akun yang sudah terdaftar.
def proses_lihat_akun():
    baris = []

    for username, akun in data_user.items():
        baris.append([username, akun["nama"], akun["umur"], akun["role"]])

    buat_tabel(
        "DAFTAR AKUN TERDAFTAR",
        ["Username", "Nama", "Umur", "Peran"],
        baris
    )


# Untuk menampilkan informasi akun pengguna yang sedang login.
def proses_lihat_data_diri():
    username = sesi["user_aktif"]["username"]
    akun = data_user[username]
    baris = [
        ["Username", username],
        ["Nama Lengkap", akun["nama"]],
        ["Umur", akun["umur"]],
        ["Peran", akun["role"]],
    ]
    buat_tabel("DATA DIRI", ["Keterangan", "Isi"], baris)


# Untuk mengubah nama, umur, atau password akun pengguna.
def proses_ubah_data_diri():
    username = sesi["user_aktif"]["username"]
    akun = data_user[username]
    proses_lihat_data_diri()

    print("(Kosongkan lalu tekan Enter jika tidak ingin mengubah)")
    nama_baru = input(f"Nama [{akun['nama']}]: ").strip()
    umur_baru = input(f"Umur [{akun['umur']}]: ").strip()
    ganti_password = konfirmasi("Ganti password?")

    print()

    if nama_baru != "":
        try:
            akun["nama"] = validasi_nama(nama_baru)
        except ValueError as e:
            print(f"{e}, nama tidak diubah.")

    if umur_baru != "":
        try:
            akun["umur"] = validasi_angka(umur_baru, "Umur", 1, 120)
        except ValueError as e:
            print(f"{e}, umur tidak diubah.")

    if ganti_password:
        akun["password"] = input_password_baru()
        print("Password berhasil diganti.")

    for d in data_milik(username).values():
        d["nama"] = akun["nama"]
        d["umur"] = akun["umur"]

    simpan_data()
    print("Proses ubah data diri selesai.")

#komentar dari salwa