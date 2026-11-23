# Mengimpor datetime untuk memeriksa dan mengolah data tanggal.
from datetime import datetime

# Mengambil data akun serta batas minimal dan maksimal panjang nama dan nama vaksin.
from data import data_user, NAMA_MIN, NAMA_MAKS, VAKSIN_MIN, VAKSIN_MAKS


# Memeriksa nama agar tidak kosong, hanya berisi huruf dan spasi,
# serta memenuhi batas jumlah karakter yang ditentukan.
def validasi_nama(teks):
    nama = teks.strip()

    if nama == "":
        raise ValueError("Nama tidak boleh kosong")

    if not nama.replace(" ", "").isalpha():
        raise ValueError("Nama hanya boleh berisi huruf")

    if len(nama) < NAMA_MIN or len(nama) > NAMA_MAKS:
        raise ValueError(f"Nama harus antara {NAMA_MIN}-{NAMA_MAKS} karakter")

    return nama


# Memeriksa nama vaksin, merapikan spasi, dan memastikan karakter
# serta panjang namanya sesuai dengan ketentuan.
def validasi_vaksin(teks):
    nama = " ".join(teks.split())

    if nama == "":
        raise ValueError("Nama vaksin tidak boleh kosong")

    if not all(huruf.isalnum() or huruf in " -" for huruf in nama):
        raise ValueError("Nama vaksin hanya boleh berisi huruf, angka, spasi, dan tanda hubung")

    if len(nama) < VAKSIN_MIN or len(nama) > VAKSIN_MAKS:
        raise ValueError(f"Nama vaksin harus antara {VAKSIN_MIN}-{VAKSIN_MAKS} karakter")

    return nama


# Mengubah masukan menjadi angka bulat dan memastikan nilainya
# tidak kurang dari batas minimum atau melebihi batas maksimum.
def validasi_angka(teks, label, minimum, maksimum):
    try:
        angka = int(teks)
    except ValueError:
        raise ValueError(f"{label} harus berupa angka") from None

    if angka < minimum or angka > maksimum:
        raise ValueError(f"{label} harus antara {minimum}-{maksimum}")

    return angka


# Memeriksa apakah tanggal sesuai dengan format DD-MM-YYYY
# kemudian mengubahnya menjadi bentuk tanggal.
def validasi_tanggal(teks):
    try:
        return datetime.strptime(teks.strip(), "%d-%m-%Y").date()
    except ValueError:
        raise ValueError("Format tanggal harus DD-MM-YYYY") from None


# Memeriksa username dan password berdasarkan data akun,
# lalu mengembalikan peran akun jika keduanya sesuai.
def cek_login(username, password):
    password_dikenal = any(akun["password"] == password for akun in data_user.values())

    if username not in data_user:
        if password_dikenal:
            raise ValueError("Username salah")

        raise ValueError("Username dan password salah")

    if data_user[username]["password"] != password:
        raise ValueError("Password salah")

    return data_user[username]["role"]


# Mencari data berdasarkan kata kunci pada kolom tertentu
# dengan memanggil fungsi ini kembali sampai seluruh ID diperiksa.
def cari_rekursif(data, daftar_id, kata_kunci, kolom, indeks=0):
    if indeks >= len(daftar_id):
        return []

    id_sekarang = daftar_id[indeks]
    cocok = []

    if kata_kunci in data[id_sekarang][kolom].lower():
        cocok = [id_sekarang]

    return cocok + cari_rekursif(data, daftar_id, kata_kunci, kolom, indeks + 1)


# Mengubah tanggal menjadi teks dengan susunan hari-bulan-tahun.
def format_tanggal(tanggal):
    return tanggal.strftime("%d-%m-%Y")