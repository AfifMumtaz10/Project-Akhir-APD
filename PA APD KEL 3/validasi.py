# Mengimpor datetime untuk mengubah teks tanggal menjadi bentuk tanggal yang bisa diolah.
from datetime import datetime
# Mengambil data pengguna serta batas minimal dan maksimal panjang nama dan nama vaksin.
from data import data_user, NAMA_MIN, NAMA_MAKS, VAKSIN_MIN, VAKSIN_MAKS
# Memeriksa apakah nama yang dimasukkan sudah sesuai aturan, lalu mengembalikan nama yang sudah dirapikan.
def validasi_nama(teks):
    nama = teks.strip()

    # Nama tidak boleh kosong.
    if nama == "":
        raise ValueError("Nama tidak boleh kosong")

    # Nama hanya boleh berisi huruf dan spasi, tidak boleh angka atau simbol.
    if not nama.replace(" ", "").isalpha():
        raise ValueError("Nama hanya boleh berisi huruf")

    # Panjang nama harus sesuai batas yang sudah ditentukan.
    if len(nama) < NAMA_MIN or len(nama) > NAMA_MAKS:
        raise ValueError(f"Nama harus antara {NAMA_MIN}-{NAMA_MAKS} karakter")

    return nama

# Memeriksa apakah nama vaksin yang dimasukkan sudah sesuai aturan, lalu mengembalikan nama yang sudah dirapikan.
def validasi_vaksin(teks):
    # Menggabungkan kembali teks agar spasi yang berlebih menjadi satu spasi.
    nama = " ".join(teks.split())

    # Nama vaksin tidak boleh kosong.
    if nama == "":
        raise ValueError("Nama vaksin tidak boleh kosong")

    # Nama vaksin hanya boleh berisi huruf, angka, spasi, dan tanda hubung.
    if not all(huruf.isalnum() or huruf in " -" for huruf in nama):
        raise ValueError("Nama vaksin hanya boleh berisi huruf, angka, spasi, dan tanda hubung")

    # Panjang nama vaksin harus sesuai batas yang sudah ditentukan.
    if len(nama) < VAKSIN_MIN or len(nama) > VAKSIN_MAKS:
        raise ValueError(f"Nama vaksin harus antara {VAKSIN_MIN}-{VAKSIN_MAKS} karakter")

    return nama

# Memeriksa apakah masukan berupa angka dan berada dalam rentang yang ditentukan.
def validasi_angka(teks, label, minimum, maksimum):
    try:
        angka = int(teks)
    # Jika masukan bukan angka, tampilkan pesan kesalahan sesuai labelnya.
    except ValueError:
        raise ValueError(f"{label} harus berupa angka") from None

    # Jika angka di luar rentang, tampilkan pesan kesalahan sesuai batasnya.
    if angka < minimum or angka > maksimum:
        raise ValueError(f"{label} harus antara {minimum}-{maksimum}")

    return angka

# Mengubah teks tanggal menjadi bentuk tanggal, dengan format yang harus DD-MM-YYYY.
def validasi_tanggal(teks):
    try:
        return datetime.strptime(teks.strip(), "%d-%m-%Y").date()
    # Jika formatnya salah, tampilkan pesan kesalahan tentang format tanggal.
    except ValueError:
        raise ValueError("Format tanggal harus DD-MM-YYYY") from None

# Memeriksa apakah username dan password cocok dengan data akun yang tersimpan.
def cek_login(username, password):
    try:
        akun = data_user[username]
    # Jika username tidak ditemukan, tampilkan pesan bahwa username salah.
    except KeyError:
        raise ValueError("Username salah") from None

    # Jika password tidak cocok, tampilkan pesan bahwa password salah.
    if akun["password"] != password:
        raise ValueError("Password salah")

    return akun["role"]

# Mencari data berdasarkan kata kunci dengan cara memeriksa satu per satu dari daftar ID secara berulang.
def cari_rekursif(data, daftar_id, kata_kunci, kolom, indeks=0):
    # Jika semua ID sudah diperiksa, berhenti dan kembalikan daftar kosong.
    if indeks >= len(daftar_id):
        return []

    id_sekarang = daftar_id[indeks]
    cocok = []

    # Jika kata kunci ditemukan di kolom yang dicari, simpan ID-nya sebagai hasil.
    if kata_kunci in data[id_sekarang][kolom].lower():
        cocok = [id_sekarang]

    # Lanjutkan pencarian ke ID berikutnya lalu gabungkan dengan hasil yang sudah ditemukan.
    return cocok + cari_rekursif(data, daftar_id, kata_kunci, kolom, indeks + 1)

# Mengubah tanggal menjadi teks dengan format DD-MM-YYYY agar mudah dibaca.
def format_tanggal(tanggal):
    return tanggal.strftime("%d-%m-%Y")
