# Mengimpor date untuk menyimpan tanggal vaksinasi.
from datetime import date

# Menentukan batas minimal dan maksimal panjang nama.
NAMA_MIN = 3
NAMA_MAKS = 50
# Menentukan batas panjang nama vaksin.
VAKSIN_MIN = 2
VAKSIN_MAKS = 30
# Menentukan batas maksimal dosis dan interval vaksin.
DOSIS_VAKSIN_MAKS = 5
INTERVAL_MAKS = 365


# Menyimpan pilihan status vaksinasi yang tersedia.
daftar_status = ["Sudah Vaksin", "Belum Vaksin", "Ditunda"]

# Menyimpan informasi batas dosis dan jarak waktu setiap jenis vaksin.
jadwal_vaksin = {
    "Covid-19": {"maks": 3, "interval": 28},
    "Tetanus": {"maks": 3, "interval": 30},
    "Hepatitis B": {"maks": 3, "interval": 30},
    "Influenza": {"maks": 1, "interval": 0},
}

# Membuat daftar nama vaksin berdasarkan data jadwal vaksin.
daftar_vaksin = list(jadwal_vaksin)


# Menyimpan informasi akun pengguna, termasuk password, peran, nama, dan umur.
data_user = {
    "rendy": {"password": "rendy123", "role": "admin", "nama": "Rendy", "umur": 20},
    "afif": {"password": "afif123", "role": "user", "nama": "Muhammad Afif Mumtaz", "umur": 19},
    "abbie": {"password": "abbie123", "role": "user", "nama": "Abbie Mujahiddin Asmuransyah", "umur": 19},
    "salwa": {"password": "salwa123", "role": "user", "nama": "Salwa Salsabila", "umur": 19},
    "cecil": {"password": "cecil123", "role": "user", "nama": "Cecilia Marsya Pua", "umur": 19},
}


# Menyimpan data vaksinasi, seperti identitas penerima, jenis vaksin, dosis, status, dan tanggal.
data_vaksin = {
    1: {"akun": "abbie", "nama": "Abbie Mujahiddin Asmuransyah", "umur": 19,
        "vaksin": "Covid-19", "dosis": 1, "status": "Sudah Vaksin", "tanggal": date(2026, 10, 10)},
    2: {"akun": "abbie", "nama": "Abbie Mujahiddin Asmuransyah", "umur": 19,
        "vaksin": "Hepatitis B", "dosis": 1, "status": "Sudah Vaksin", "tanggal": date(2026, 10, 25)},
    3: {"akun": "afif", "nama": "Muhammad Afif Mumtaz", "umur": 19,
        "vaksin": "Hepatitis B", "dosis": 2, "status": "Sudah Vaksin", "tanggal": date(2026, 10, 15)},
    4: {"akun": "salwa", "nama": "Salwa Salsabila", "umur": 19,
        "vaksin": "Influenza", "dosis": 1, "status": "Ditunda", "tanggal": date(2026, 10, 20)},
    5: {"akun": "cecil", "nama": "Cecilia Marsya Pua", "umur": 19,
        "vaksin": "Tetanus", "dosis": 1, "status": "Belum Vaksin", "tanggal": date(2026, 10, 28)},
}


# Menyimpan informasi pengguna yang sedang login dan status jalannya program.
sesi = {
    "user_aktif": None,
    "program_berjalan": True,
}
