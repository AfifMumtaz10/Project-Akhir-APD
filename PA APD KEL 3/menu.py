# Mengambil sesi untuk mengetahui pengguna yang sedang login.
from data import sesi

# Mengambil fungsi untuk membersihkan layar, memberi jeda, dan menampilkan menu.
from tampilan import clear, jeda, pilih_menu

# Mengambil fungsi untuk mengecek apakah akun yang login memiliki peran admin.
from logika import adalah_admin

# Mengambil fungsi untuk login, membuat akun, logout, keluar program, dan mengelola akun.
from akun import (
    proses_login, proses_register, proses_logout, keluar_program,
    proses_lihat_akun, proses_lihat_data_diri, proses_ubah_data_diri
)

# Mengambil fungsi untuk menambah, melihat, mencari, mengubah, menghapus, dan melihat jadwal vaksin.
from crud import (
    proses_tambah, proses_lihat, proses_cari, proses_ubah, proses_hapus, proses_jadwal
)


# Menyimpan nama menu, penjelasan, fungsi yang dijalankan, dan pengaturan jeda.
def buat_opsi(label, info, aksi, pakai_jeda=True):
    return {"label": label, "info": info, "aksi": aksi, "jeda": pakai_jeda}


# Menjalankan fungsi sesuai pilihan pengguna dan memberi jeda jika diperlukan.
def jalankan_opsi(opsi, pilihan):
    clear()
    opsi[pilihan]["aksi"]()

    if opsi[pilihan]["jeda"]:
        jeda("Tekan Enter untuk kembali ke menu...")


# Menampilkan submenu berulang kali hingga pengguna memilih kembali.
def jalankan_submenu(judul, opsi):
    while True:
        clear()
        pilihan = pilih_menu(judul, opsi, "Kembali")

        if pilihan == "0":
            return

        jalankan_opsi(opsi, pilihan)


# Menyediakan menu admin untuk mengelola data vaksinasi seluruh penerima.
def menu_data_vaksinasi():
    jalankan_submenu("DATA VAKSINASI", {
        "1": buat_opsi("Tambah Data", "Catat penerima vaksin baru", proses_tambah),
        "2": buat_opsi("Lihat Data", "Tampilkan seluruh data vaksinasi", proses_lihat),
        "3": buat_opsi("Cari Data", "Cari penerima vaksin berdasarkan nama", proses_cari),
        "4": buat_opsi("Ubah Data", "Perbarui data vaksinasi yang sudah ada", proses_ubah),
        "5": buat_opsi("Hapus Data", "Hapus data vaksinasi", proses_hapus),
    })


# Menyediakan menu bagi pengguna biasa untuk mengatur riwayat vaksinasinya sendiri.
def menu_riwayat_vaksinasi():
    jalankan_submenu("RIWAYAT VAKSINASI", {
        "1": buat_opsi("Tambah Riwayat", "Catat vaksinasi yang sudah kamu jalani", proses_tambah),
        "2": buat_opsi("Lihat Riwayat", "Tampilkan semua riwayat vaksinasimu", proses_lihat),
        "3": buat_opsi("Cari Riwayat", "Cari riwayat berdasarkan jenis vaksin", proses_cari),
        "4": buat_opsi("Ubah Riwayat", "Perbarui riwayat vaksinasimu", proses_ubah),
        "5": buat_opsi("Hapus Riwayat", "Hapus riwayat vaksinasimu", proses_hapus),
    })


# Menyediakan pilihan untuk melihat dan memperbarui informasi pribadi pengguna.
def menu_data_diri():
    jalankan_submenu("DATA DIRI", {
        "1": buat_opsi("Lihat Data Diri", "Username, nama, umur, dan peran", proses_lihat_data_diri),
        "2": buat_opsi("Ubah Data Diri", "Ubah nama, umur, atau password", proses_ubah_data_diri),
    })


# Menentukan pilihan menu utama sesuai peran akun yang sedang login.
def opsi_menu_utama():
    if adalah_admin():
        return {
            "1": buat_opsi("Data Vaksinasi", "Tambah, lihat, cari, ubah, hapus data penerima vaksin",
                           menu_data_vaksinasi, False),
            "2": buat_opsi("Jadwal Dosis Berikutnya", "Pantau jadwal dosis lanjutan semua penerima",
                           proses_jadwal),
            "3": buat_opsi("Data Akun", "Lihat daftar akun yang terdaftar", proses_lihat_akun),
        }

    return {
        "1": buat_opsi("Data Diri", "Lihat dan ubah data pribadi serta password", menu_data_diri, False),
        "2": buat_opsi("Riwayat Vaksinasi", "Tambah, lihat, cari, ubah, hapus riwayat vaksinasi",
                       menu_riwayat_vaksinasi, False),
        "3": buat_opsi("Jadwal Dosis Berikutnya", "Lihat kapan dosis lanjutanmu dijadwalkan", proses_jadwal),
    }


# Menampilkan pilihan login, pendaftaran akun baru, atau keluar dari program.
def menu_awal():
    opsi = {
        "1": buat_opsi("Login", "Masuk dengan akun yang sudah terdaftar", proses_login, False),
        "2": buat_opsi("Register", "Buat akun baru", proses_register, False),
    }

    clear()
    pilihan = pilih_menu("SISTEM DATA VAKSIN", opsi, "Keluar")

    if pilihan == "0":
        keluar_program()
    else:
        jalankan_opsi(opsi, pilihan)


# Menampilkan menu utama berdasarkan akun yang sedang aktif.
def menu_pengguna():
    opsi = opsi_menu_utama()
    akun = sesi["user_aktif"]

    clear()
    print(f"Login sebagai: {akun['username']} ({akun['role']})")
    pilihan = pilih_menu("SISTEM DATA VAKSIN", opsi, "Logout")

    if pilihan == "0":
        clear()
        proses_logout()
        jeda()
    else:
        jalankan_opsi(opsi, pilihan)