# Mengimpor date untuk mengolah tanggal dan timedelta untuk menghitung jarak hari antar dosis.
from datetime import date, timedelta
# Mengimpor data pengguna, data vaksin, jadwal vaksin, daftar vaksin, daftar status, dan sesi yang sedang aktif.
from data import (
    data_user, data_vaksin, jadwal_vaksin, daftar_vaksin, daftar_status, sesi
)
# Mengimpor fungsi format_tanggal untuk menampilkan tanggal dalam format DD-MM-YYYY.
from validasi import format_tanggal

# Memeriksa apakah pengguna yang sedang login berperan sebagai admin.
def adalah_admin():
    return sesi["user_aktif"]["role"] == "admin"

# Mengambil semua data vaksinasi yang dimiliki oleh satu akun pengguna.
def data_milik(username):
    return {i: d for i, d in data_vaksin.items() if d["akun"] == username}

# Menentukan data vaksinasi yang boleh dilihat berdasarkan peran pengguna yang sedang login.
def data_terlihat():
    if adalah_admin():
        return data_vaksin

    return data_milik(sesi["user_aktif"]["username"])

# Membuat ID baru dengan cara menambahkan satu pada ID terbesar yang sudah ada.
def buat_id_baru():
    return max(data_vaksin, default=0) + 1

# Mencari username berdasarkan nama lengkap yang tersimpan di data pengguna.
def akun_dari_nama(nama):
    for username, akun in data_user.items():
        if akun["nama"].lower() == nama.lower():
            return username

    return None

# Menghubungkan data vaksinasi yang belum memiliki akun ke akun pengguna yang namanya sama.
def hubungkan_data_ke_akun(username):
    nama = data_user[username]["nama"].lower()
    jumlah = 0

    for d in data_vaksin.values():
        if d["akun"] is None and d["nama"].lower() == nama:
            d["akun"] = username
            jumlah += 1

    return jumlah

# Mencari nama vaksin di daftar vaksin tanpa membedakan huruf besar dan huruf kecil.
def cari_nama_vaksin(nama):
    for nama_vaksin in daftar_vaksin:
        if nama_vaksin.lower() == nama.lower():
            return nama_vaksin

    return None

# Menambahkan vaksin baru ke jadwal dan daftar vaksin beserta jumlah dosis dan jarak antar dosisnya.
def daftarkan_vaksin(nama, maks, interval):
    jadwal_vaksin[nama] = {"maks": maks, "interval": interval}
    daftar_vaksin.append(nama)

# Membuat keterangan yang menjelaskan posisi dosis, apakah dosis awal, lanjutan, atau terakhir.
def keterangan_dosis(vaksin, nomor):
    info = jadwal_vaksin[vaksin]

    if info["maks"] == 1:
        return "Dosis tunggal (hanya 1 dosis)"

    if nomor == 1:
        return "Dosis pertama (dosis awal)"

    jarak = f"{info['interval']} hari setelah dosis sebelumnya"

    if nomor == info["maks"]:
        return f"Dosis ke-{nomor} (dosis terakhir, {jarak})"

    return f"Dosis ke-{nomor} (dosis lanjutan, {jarak})"

# Mengumpulkan nomor dosis yang sudah tercatat untuk satu nama dan satu jenis vaksin.
def dosis_tercatat(nama, vaksin, kecuali_id=None):
    return {
        d["dosis"]
        for id_vaksin, d in data_vaksin.items()
        if id_vaksin != kecuali_id
        and d["nama"].lower() == nama.lower()
        and d["vaksin"] == vaksin
        and d["status"] == daftar_status[0]
    }

# Menentukan dosis berikutnya yang disarankan berdasarkan dosis yang sudah tercatat sebelumnya.
def saran_dosis(nama, vaksin, kecuali_id=None):
    tercatat = dosis_tercatat(nama, vaksin, kecuali_id)
    berikutnya = max(tercatat, default=0) + 1

    if berikutnya > jadwal_vaksin[vaksin]["maks"]:
        return None

    return berikutnya

# Menghitung tanggal dan status jadwal dosis berikutnya berdasarkan tanggal vaksinasi terakhir.
def hitung_jadwal(vaksin, dosis, tanggal):
    info = jadwal_vaksin[vaksin]

    if dosis >= info["maks"]:
        return "-", "-", "Dosis lengkap"

    jadwal = tanggal + timedelta(days=info["interval"])
    selisih = (jadwal - date.today()).days

    if selisih < 0:
        status = f"Terlambat {-selisih} hari"
    elif selisih == 0:
        status = "Hari ini"
    else:
        status = f"{selisih} hari lagi"

    return dosis + 1, format_tanggal(jadwal), status

# Mengambil data dengan dosis paling tinggi untuk setiap kombinasi nama dan jenis vaksin.
def dosis_terakhir(data):
    terakhir = {}

    for id_vaksin, d in data.items():
        kunci = (d["nama"].lower(), d["vaksin"])

        if kunci not in terakhir or d["dosis"] > data[terakhir[kunci]]["dosis"]:
            terakhir[kunci] = id_vaksin

    return list(terakhir.values())