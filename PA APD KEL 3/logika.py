# Mengimpor date untuk mengambil tanggal saat ini dan timedelta untuk menghitung selisih hari.
from datetime import date, timedelta

# Mengambil data akun, vaksinasi, jadwal vaksin, daftar vaksin, status, dan sesi pengguna.
from data import (
    data_user, data_vaksin, jadwal_vaksin, daftar_vaksin, daftar_status, sesi
)

# Mengambil fungsi untuk mengubah tanggal menjadi format yang mudah dibaca.
from validasi import format_tanggal


# Fungsi untuk memeriksa apakah pengguna yang sedang login memiliki peran admin.
def adalah_admin():
    return sesi["user_aktif"]["role"] == "admin"


# Fungsi untuk mengambil seluruh data vaksinasi milik pengguna berdasarkan username.
def data_milik(username):
    return {i: d for i, d in data_vaksin.items() if d["akun"] == username}


# Fungsi untuk menampilkan data vaksinasi sesuai dengan hak akses pengguna.
def data_terlihat():
    # Admin dapat melihat seluruh data vaksinasi.
    if adalah_admin():
        return data_vaksin

    # Pengguna biasa hanya dapat melihat data miliknya sendiri.
    return data_milik(sesi["user_aktif"]["username"])


# Fungsi untuk membuat ID baru berdasarkan ID terbesar yang sudah digunakan.
def buat_id_baru():
    return max(data_vaksin, default=0) + 1


# Fungsi untuk mencari username berdasarkan nama lengkap pengguna.
def akun_dari_nama(nama):
    for username, akun in data_user.items():
        # Membandingkan nama tanpa membedakan huruf besar dan kecil.
        if akun["nama"].lower() == nama.lower():
            return username

    # Mengembalikan None jika nama tidak ditemukan.
    return None


# Fungsi untuk menghubungkan data vaksinasi lama dengan akun pengguna yang baru dibuat.
def hubungkan_data_ke_akun(username):
    nama = data_user[username]["nama"].lower()
    jumlah = 0

    # Memeriksa data vaksinasi yang belum terhubung dengan akun.
    for d in data_vaksin.values():
        if d["akun"] is None and d["nama"].lower() == nama:
            d["akun"] = username
            jumlah += 1

    # Mengembalikan jumlah data yang berhasil dihubungkan.
    return jumlah


# Fungsi untuk mencari nama vaksin yang sudah tersedia dalam daftar.
def cari_nama_vaksin(nama):
    for nama_vaksin in daftar_vaksin:
        # Membandingkan nama vaksin tanpa membedakan huruf besar dan kecil.
        if nama_vaksin.lower() == nama.lower():
            return nama_vaksin

    # Mengembalikan None jika nama vaksin tidak ditemukan.
    return None


# Fungsi untuk menambahkan jenis vaksin beserta aturan dosis dan jarak waktunya.
def daftarkan_vaksin(nama, maks, interval):
    jadwal_vaksin[nama] = {"maks": maks, "interval": interval}
    daftar_vaksin.append(nama)


# Fungsi untuk memberikan keterangan berdasarkan nomor dosis vaksin.
def keterangan_dosis(vaksin, nomor):
    # Mengambil informasi dosis dan interval dari jenis vaksin yang dipilih.
    info = jadwal_vaksin[vaksin]

    # Memberikan keterangan jika vaksin hanya memiliki satu dosis.
    if info["maks"] == 1:
        return "Dosis tunggal (hanya 1 dosis)"

    # Memberikan keterangan untuk dosis pertama.
    if nomor == 1:
        return "Dosis pertama (dosis awal)"

    # Menentukan jarak waktu dari dosis sebelumnya.
    jarak = f"{info['interval']} hari setelah dosis sebelumnya"

    # Memberikan keterangan jika dosis yang dipilih merupakan dosis terakhir.
    if nomor == info["maks"]:
        return f"Dosis ke-{nomor} (dosis terakhir, {jarak})"

    # Memberikan keterangan untuk dosis lanjutan.
    return f"Dosis ke-{nomor} (dosis lanjutan, {jarak})"


# Fungsi untuk mengambil riwayat vaksinasi seseorang berdasarkan nama dan jenis vaksin.
def riwayat_orang(nama, vaksin, kecuali_id=None):
    return [
        d
        for id_vaksin, d in data_vaksin.items()
        # Mengabaikan ID tertentu jika sedang melakukan proses pengubahan data.
        if id_vaksin != kecuali_id
        and d["nama"].lower() == nama.lower()
        and d["vaksin"] == vaksin
    ]


# Fungsi untuk mengumpulkan nomor dosis yang sudah tercatat telah diterima.
def dosis_tercatat(nama, vaksin, kecuali_id=None):
    return {
        d["dosis"]
        for d in riwayat_orang(nama, vaksin, kecuali_id)
        if d["status"] == daftar_status[0]
    }


# Fungsi untuk menentukan dosis berikutnya berdasarkan riwayat vaksinasi.
def saran_dosis(nama, vaksin, kecuali_id=None):
    # Mengambil nomor dosis yang sudah tercatat sebagai vaksinasi yang diterima.
    tercatat = dosis_tercatat(nama, vaksin, kecuali_id)
    berikutnya = max(tercatat, default=0) + 1

    # Tidak memberikan saran jika jumlah dosis sudah mencapai batas maksimal.
    if berikutnya > jadwal_vaksin[vaksin]["maks"]:
        return None

    # Mengembalikan nomor dosis yang disarankan.
    return berikutnya


# Fungsi untuk menjelaskan alasan pemberian saran dosis berdasarkan riwayat vaksinasi.
def alasan_saran(nama, vaksin, kecuali_id=None):
    # Mengambil aturan vaksin dan seluruh riwayat yang sesuai.
    info = jadwal_vaksin[vaksin]
    semua = riwayat_orang(nama, vaksin, kecuali_id)
    sudah = [d for d in semua if d["status"] == daftar_status[0]]
    belum = len(semua) - len(sudah)
    alasan = []

    # Memberikan alasan jika belum ada riwayat vaksinasi yang berstatus sudah vaksin.
    if not sudah:
        alasan.append(
            f"Belum ada riwayat {vaksin} berstatus {daftar_status[0]} atas nama {nama}, "
            f"sehingga dimulai dari Dosis 1."
        )
    else:
        # Mengambil data dosis tertinggi yang sudah tercatat telah diterima.
        terakhir = max(sudah, key=lambda d: d["dosis"])

        # Menjelaskan bahwa seluruh dosis sudah lengkap jika batas maksimal tercapai.
        if terakhir["dosis"] >= info["maks"]:
            alasan.append(
                f"Dosis {terakhir['dosis']} (dosis terakhir {vaksin}) sudah tercatat "
                f"{daftar_status[0]}, jadi seluruh dosis sudah lengkap."
            )
        else:
            # Menentukan nomor dosis berikutnya dan perkiraan tanggal pelaksanaannya.
            berikutnya = terakhir["dosis"] + 1
            jadwal = terakhir["tanggal"] + timedelta(days=info["interval"])
            alasan.append(
                f"Dosis {terakhir['dosis']} sudah tercatat {daftar_status[0]} pada "
                f"{format_tanggal(terakhir['tanggal'])}, sehingga berikutnya Dosis {berikutnya}."
            )
            alasan.append(
                f"Jarak {vaksin} adalah {info['interval']} hari, jadi Dosis {berikutnya} "
                f"dianjurkan mulai {format_tanggal(jadwal)}."
            )

    # Menjelaskan bahwa data yang belum berstatus sudah vaksin tidak dihitung sebagai dosis yang diterima.
    if belum > 0:
        alasan.append(
            f"{belum} data berstatus selain {daftar_status[0]} tidak dihitung "
            f"sebagai dosis yang sudah diterima."
        )

    # Mengembalikan seluruh alasan dalam bentuk daftar.
    return alasan


# Fungsi untuk menghitung jadwal dosis berikutnya berdasarkan dosis dan tanggal sebelumnya.
def hitung_jadwal(vaksin, dosis, tanggal):
    # Mengambil batas dosis dan interval dari jenis vaksin yang dipilih.
    info = jadwal_vaksin[vaksin]

    # Menghentikan perhitungan jika seluruh dosis sudah lengkap.
    if dosis >= info["maks"]:
        return "-", "-", "Dosis lengkap"

    # Menghitung tanggal dosis berikutnya dan selisihnya dengan tanggal hari ini.
    jadwal = tanggal + timedelta(days=info["interval"])
    selisih = (jadwal - date.today()).days

    # Menentukan keterangan jadwal berdasarkan selisih hari.
    if selisih < 0:
        status = f"Terlambat {-selisih} hari"
    elif selisih == 0:
        status = "Hari ini"
    else:
        status = f"{selisih} hari lagi"

    # Mengembalikan nomor dosis berikutnya, tanggal jadwal, dan status waktunya.
    return dosis + 1, format_tanggal(jadwal), status


# Fungsi untuk mengambil data dosis terakhir dari setiap orang pada masing-masing jenis vaksin.
def dosis_terakhir(data):
    terakhir = {}

    # Memeriksa setiap data vaksinasi untuk menentukan dosis tertinggi.
    for id_vaksin, d in data.items():
        # Mengelompokkan data berdasarkan nama penerima dan jenis vaksin.
        kunci = (d["nama"].lower(), d["vaksin"])

        # Menyimpan ID data jika belum ada atau dosisnya lebih tinggi dari data sebelumnya.
        if kunci not in terakhir or d["dosis"] > data[terakhir[kunci]]["dosis"]:
            terakhir[kunci] = id_vaksin

    # Mengembalikan daftar ID yang mewakili dosis terakhir setiap kelompok.
    return list(terakhir.values())