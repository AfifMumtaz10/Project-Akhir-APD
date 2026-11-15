# Mengambil sesi untuk mengetahui siapa yang sedang login.
from data import sesi
# Mengambil fungsi untuk membersihkan layar, memberi jeda, dan menampilkan pilihan menu.
from tampilan import clear, jeda, pilih_menu
# Mengambil fungsi untuk memeriksa apakah pengguna yang login adalah admin.
from logika import adalah_admin
# Mengambil fungsi-fungsi yang berhubungan dengan akun, seperti login, register, dan logout.
from akun import (
    proses_login, proses_register, proses_logout, keluar_program,
    proses_lihat_akun, proses_lihat_data_diri, proses_ubah_data_diri
)
# Mengambil fungsi-fungsi untuk mengolah data vaksinasi, seperti tambah, lihat, cari, ubah, dan hapus.
from crud import (
    proses_tambah, proses_lihat, proses_cari, proses_ubah, proses_hapus, proses_jadwal
)

# Membuat satu pilihan menu yang berisi label, keterangan, fungsi yang dijalankan, dan apakah perlu jeda setelahnya.
def buat_opsi(label, info, aksi, pakai_jeda=True):
    return {"label": label, "info": info, "aksi": aksi, "jeda": pakai_jeda}

# Membersihkan layar, menjalankan fungsi dari menu yang dipilih, lalu memberi jeda bila diperlukan.
def jalankan_opsi(opsi, pilihan):
    clear()
    opsi[pilihan]["aksi"]()

    if opsi[pilihan]["jeda"]:
        jeda("Tekan Enter untuk kembali ke menu...")

# Menampilkan submenu secara berulang sampai pengguna memilih untuk kembali.
def jalankan_submenu(judul, opsi):
    while True:
        clear()
        pilihan = pilih_menu(judul, opsi, "Kembali")

        if pilihan == "0":
            return

        jalankan_opsi(opsi, pilihan)

# Menampilkan submenu khusus admin untuk mengelola data vaksinasi semua penerima.
def menu_data_vaksinasi():
    jalankan_submenu("DATA VAKSINASI", {
        "1": buat_opsi("Tambah Data", "Catat penerima vaksin baru", proses_tambah),
        "2": buat_opsi("Lihat Data", "Tampilkan seluruh data vaksinasi", proses_lihat),
        "3": buat_opsi("Cari Data", "Cari penerima vaksin berdasarkan nama", proses_cari),
        "4": buat_opsi("Ubah Data", "Perbarui data vaksinasi yang sudah ada", proses_ubah),
        "5": buat_opsi("Hapus Data", "Hapus data vaksinasi", proses_hapus),
    })

# Menampilkan submenu khusus pengguna biasa untuk mengelola riwayat vaksinasinya sendiri.
def menu_riwayat_vaksinasi():
    jalankan_submenu("RIWAYAT VAKSINASI", {
        "1": buat_opsi("Tambah Riwayat", "Catat vaksinasi yang sudah kamu jalani", proses_tambah),
        "2": buat_opsi("Lihat Riwayat", "Tampilkan semua riwayat vaksinasimu", proses_lihat),
        "3": buat_opsi("Cari Riwayat", "Cari riwayat berdasarkan jenis vaksin", proses_cari),
        "4": buat_opsi("Ubah Riwayat", "Perbarui riwayat vaksinasimu", proses_ubah),
        "5": buat_opsi("Hapus Riwayat", "Hapus riwayat vaksinasimu", proses_hapus),
    })

# Menampilkan submenu untuk melihat dan mengubah data diri pengguna yang sedang login.
def menu_data_diri():
    jalankan_submenu("DATA DIRI", {
        "1": buat_opsi("Lihat Data Diri", "Username, nama, umur, dan peran", proses_lihat_data_diri),
        "2": buat_opsi("Ubah Data Diri", "Ubah nama, umur, atau password", proses_ubah_data_diri),
    })

# Menyusun daftar menu utama yang berbeda antara admin dan pengguna biasa.
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

# Menampilkan menu awal untuk pengguna yang belum login, yaitu login, register, atau keluar.
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

# Menampilkan menu utama untuk pengguna yang sudah login, lengkap dengan info akun yang aktif.
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
