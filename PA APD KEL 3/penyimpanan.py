# Mengimpor json untuk mengubah data menjadi format JSON agar bisa disimpan di file.
import json
# Mengimpor os untuk mengelola lokasi dan keberadaan file penyimpanan.
import os
# Mengimpor date untuk mengubah kembali tanggal dari teks menjadi bentuk tanggal.
from datetime import date
# Mengambil data pengguna, data vaksin, jadwal vaksin, daftar vaksin, dan daftar status yang ada di memori.
from data import (
    data_user, data_vaksin, jadwal_vaksin, daftar_vaksin, daftar_status
)

# Menentukan lokasi file penyimpanan, yaitu file data_vaksin.json yang berada satu folder dengan file ini.
BERKAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_vaksin.json")

# Menyimpan seluruh data yang ada di memori ke dalam file JSON agar tidak hilang saat program ditutup.
def simpan_data():
    # Menyiapkan data yang akan disimpan, dengan mengubah tanggal menjadi teks agar bisa ditulis ke JSON.
    isi = {
        "jadwal_vaksin": jadwal_vaksin,
        "data_user": data_user,
        "data_vaksin": {
            str(id_vaksin): {**d, "tanggal": d["tanggal"].isoformat()}
            for id_vaksin, d in data_vaksin.items()
        },
    }

    try:
        # Menulis data ke file JSON dengan format yang rapi dan mudah dibaca.
        with open(BERKAS, "w", encoding="utf-8") as f:
            json.dump(isi, f, indent=4, ensure_ascii=False)
    # Jika file gagal ditulis, tampilkan peringatan tanpa menghentikan program.
    except OSError:
        print("Peringatan: data gagal disimpan ke berkas.")

# Memuat data dari file JSON ke dalam memori saat program pertama kali dijalankan.
def muat_data():
    # Jika file belum ada, buat file baru dari data awal lalu selesai.
    if not os.path.exists(BERKAS):
        simpan_data()
        return

    try:
        # Membaca isi file JSON.
        with open(BERKAS, encoding="utf-8") as f:
            isi = json.load(f)

        # Mengambil data pengguna dari file.
        user = isi["data_user"]

        # Mengambil data vaksin dan mengubah kembali tanggal dari teks menjadi tanggal, serta mengatur status awalnya.
        vaksin = {
            int(kunci): {
                "status": daftar_status[0],
                **d,
                "tanggal": date.fromisoformat(d["tanggal"]),
            }
            for kunci, d in isi["data_vaksin"].items()
        }

        # Mengambil jadwal vaksin dan memastikan jumlah dosis dan intervalnya berbentuk angka.
        jadwal = {
            nama: {"maks": int(v["maks"]), "interval": int(v["interval"])}
            for nama, v in isi.get("jadwal_vaksin", jadwal_vaksin).items()
        }
    # Jika file rusak atau formatnya tidak sesuai, batalkan proses pemuatan agar data lama tetap aman.
    except (json.JSONDecodeError, KeyError, ValueError, TypeError, OSError):
        return

    # Mengganti data lama di memori dengan data yang baru saja dibaca dari file.
    data_user.clear()
    data_user.update(user)
    data_vaksin.clear()
    data_vaksin.update(vaksin)
    jadwal_vaksin.clear()
    jadwal_vaksin.update(jadwal)
    daftar_vaksin[:] = list(jadwal_vaksin)
