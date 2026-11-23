# Mengambil data akun pengguna dan informasi sesi yang sedang berjalan.
from data import data_user, sesi

# Mengambil fungsi untuk memeriksa login serta memvalidasi nama dan angka.
from validasi import cek_login, validasi_nama, validasi_angka

# Mengambil fungsi untuk mengakses data milik pengguna dan menghubungkannya dengan akun.
from logika import data_milik, hubungkan_data_ke_akun

# Mengambil fungsi untuk menerima input nama, angka, dan password.
from input import (
    input_nama, input_angka, input_password, input_username_baru, input_password_baru
)

# Mengambil fungsi untuk menampilkan tabel, memberi jeda, meminta konfirmasi, dan membersihkan tampilan.
from tampilan import buat_tabel, jeda, konfirmasi, layar_baru

# Mengambil fungsi untuk menyimpan perubahan data.
from penyimpanan import simpan_data

# Menentukan jumlah maksimal percobaan login sebanyak tiga kali.
BATAS_LOGIN = 3


# Fungsi untuk menghentikan program dan menampilkan pesan penutup.
def keluar_program():
    sesi["program_berjalan"] = False
    print("Terima Kasih Telah Menggunakan Sistem Data Vaksin")


# Fungsi untuk memproses login pengguna dengan batas percobaan tertentu.
def proses_login():
    # Menyiapkan daftar pesan yang akan ditampilkan pada layar login.
    pesan = []

    # Mengulang proses login sesuai batas percobaan yang ditentukan.
    for percobaan in range(1, BATAS_LOGIN + 1):
        # Menampilkan halaman login beserta pesan jika ada.
        layar_baru("LOGIN", pesan)
        username = input("Username: ").strip().lower()
        password = input_password("Password: ")

        try:
            # Memeriksa username dan password yang dimasukkan pengguna.
            role = cek_login(username, password)
        # Menangani kesalahan jika data login tidak sesuai.
        except ValueError as e:
            sisa = BATAS_LOGIN - percobaan
            pesan = [str(e)]

            # Menampilkan jumlah kesempatan login yang masih tersisa.
            if sisa > 0:
                pesan.append(f"sisa percobaan login {sisa}.")

            continue

        # Menyimpan informasi pengguna yang berhasil login ke dalam sesi.
        sesi["user_aktif"] = {"username": username, "role": role}
        print(f"Login berhasil, {username}!")
        jeda()
        return

    # Menampilkan pesan ketika seluruh percobaan login telah habis.
    layar_baru("LOGIN", pesan)
    print("Login Gagal.")
    sesi["program_berjalan"] = False


# Fungsi untuk mendaftarkan akun pengguna baru.
def proses_register():
    # Menentukan judul halaman pendaftaran akun.
    judul = "REGISTER AKUN BARU"
    print(judul)
    print("Ketik '0' Untuk Batal")
    username = input_username_baru()

    # Menampilkan pesan jika pengguna membatalkan pendaftaran.
    if username is None:
        print("Registrasi dibatalkan")
    else:
        # Menampilkan username sebelum meminta data tambahan.
        layar_baru(judul, [f"Username: {username}"])
        nama = input_nama("Nama Lengkap: ")
        umur = input_angka("Umur (1-120): ", "Umur", 1, 120)

        # Menampilkan data yang telah dimasukkan sebelum membuat password.
        layar_baru(judul, [f"Username: {username}", f"Nama: {nama}", f"Umur: {umur}"])
        password = input_password_baru()

        # Menyimpan akun baru beserta password, peran, nama, dan umur.
        data_user[username] = {"password": password, "role": "user", "nama": nama, "umur": umur}

        # Menghubungkan data vaksinasi yang sesuai dengan akun baru.
        terhubung = hubungkan_data_ke_akun(username)

        # Menyimpan akun dan perubahan data ke penyimpanan.
        simpan_data()
        print("Registrasi berhasil! Silakan login.")

        # Memberi tahu pengguna jika ada data vaksinasi yang berhasil dihubungkan.
        if terhubung > 0:
            print(f"{terhubung} data vaksinasi atas nama {nama} otomatis terhubung ke akunmu.")

    # Memberi jeda setelah proses pendaftaran selesai.
    jeda()


# Fungsi untuk mengeluarkan pengguna dari akun yang sedang digunakan.
def proses_logout():
    sesi["user_aktif"] = None
    print("Logout berhasil.")


# Fungsi untuk menampilkan daftar seluruh akun yang terdaftar.
def proses_lihat_akun():
    # Menyiapkan tempat untuk menampung data akun dalam bentuk baris tabel.
    baris = []

    # Mengambil username, nama, umur, dan peran dari setiap akun.
    for username, akun in data_user.items():
        baris.append([username, akun["nama"], akun["umur"], akun["role"]])

    # Menampilkan seluruh akun dalam bentuk tabel.
    buat_tabel(
        "DAFTAR AKUN TERDAFTAR",
        ["Username", "Nama", "Umur", "Peran"],
        baris
    )


# Fungsi untuk menampilkan informasi akun pengguna yang sedang login.
def proses_lihat_data_diri():
    # Mengambil username dan informasi akun pengguna yang sedang aktif.
    username = sesi["user_aktif"]["username"]
    akun = data_user[username]

    # Menyusun informasi akun yang akan ditampilkan.
    baris = [
        ["Username", username],
        ["Nama Lengkap", akun["nama"]],
        ["Umur", akun["umur"]],
        ["Peran", akun["role"]],
    ]

    # Menampilkan informasi akun dalam bentuk tabel.
    buat_tabel("DATA DIRI", ["Keterangan", "Isi"], baris)


# Fungsi untuk mengubah informasi akun pengguna yang sedang login.
def proses_ubah_data_diri():
    # Mengambil username dan data akun pengguna yang sedang aktif.
    username = sesi["user_aktif"]["username"]
    akun = data_user[username]

    # Menampilkan informasi akun sebelum dilakukan perubahan.
    proses_lihat_data_diri()

    print("(Kosongkan lalu tekan Enter jika tidak ingin mengubah)")
    nama_baru = input(f"Nama [{akun['nama']}]: ").strip()
    umur_baru = input(f"Umur [{akun['umur']}]: ").strip()

    # Menampilkan perubahan nama dan umur yang akan dilakukan.
    layar_baru("UBAH DATA DIRI", [
        f"Nama baru: {nama_baru or 'tidak diubah'}",
        f"Umur baru: {umur_baru or 'tidak diubah'}",
    ])

    # Meminta konfirmasi apakah pengguna ingin mengganti password.
    ganti_password = konfirmasi("Ganti password?")

    print()

    # Mengubah nama jika pengguna memasukkan nama baru yang valid.
    if nama_baru != "":
        try:
            akun["nama"] = validasi_nama(nama_baru)
        # Menampilkan pesan jika nama baru tidak memenuhi ketentuan.
        except ValueError as e:
            print(f"{e}, nama tidak diubah.")

    # Mengubah umur jika pengguna memasukkan umur baru yang valid.
    if umur_baru != "":
        try:
            akun["umur"] = validasi_angka(umur_baru, "Umur", 1, 120)
        # Menampilkan pesan jika umur baru tidak memenuhi ketentuan.
        except ValueError as e:
            print(f"{e}, umur tidak diubah.")

    # Mengganti password jika pengguna menyetujuinya.
    if ganti_password:
        akun["password"] = input_password_baru()
        print("Password berhasil diganti.")

    # Menyesuaikan nama dan umur pada seluruh data vaksinasi milik pengguna.
    for d in data_milik(username).values():
        d["nama"] = akun["nama"]
        d["umur"] = akun["umur"]

    # Menyimpan seluruh perubahan akun dan data vaksinasi.
    simpan_data()
    print("Proses ubah data diri selesai.")