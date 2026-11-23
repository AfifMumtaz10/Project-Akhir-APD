# Mengimpor json untuk menyimpan data dalam bentuk JSON.
import json

# Mengimpor os untuk mengatur lokasi dan memeriksa file.
import os

# Mengimpor date untuk mengubah teks tanggal menjadi objek tanggal.
from datetime import date

# Mengambil data pengguna, data vaksinasi, jadwal, serta daftar vaksin dan status.
from data import (
    data_user, data_vaksin, jadwal_vaksin, daftar_vaksin, daftar_status
)

# Menentukan lokasi file data_vaksin.json di folder yang sama dengan program ini.
BERKAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_vaksin.json")


# Menyimpan seluruh data dari memori ke dalam file JSON.
def simpan_data():
    # Menyiapkan data yang akan disimpan dan mengubah tanggal menjadi teks.
    isi = {
        "jadwal_vaksin": jadwal_vaksin,
        "data_user": data_user,
        "data_vaksin": {
            str(id_vaksin): {**d, "tanggal": d["tanggal"].isoformat()}
            for id_vaksin, d in data_vaksin.items()
        },
    }

    try:
        # Membuka file dan menuliskan data dengan susunan yang rapi.
        with open(BERKAS, "w", encoding="utf-8") as f:
            json.dump(isi, f, indent=4, ensure_ascii=False)

    # Memberi peringatan jika data tidak berhasil disimpan.
    except OSError:
        print("Peringatan: data gagal disimpan ke berkas.")


# Membaca data dari file JSON agar dapat digunakan oleh program.
def muat_data():
    # Jika file belum tersedia, simpan data awal terlebih dahulu.
    if not os.path.exists(BERKAS):
        simpan_data()
        return

    try:
        # Membuka file dan membaca data yang tersimpan di dalamnya.
        with open(BERKAS, encoding="utf-8") as f:
            isi = json.load(f)

        # Mengambil informasi akun pengguna dari file.
        user = isi["data_user"]

        # Mengambil data vaksin, mengubah ID menjadi angka, dan mengembalikan tanggal ke format date.
        vaksin = {
            int(kunci): {
                "status": daftar_status[0],
                **d,
                "tanggal": date.fromisoformat(d["tanggal"]),
            }
            for kunci, d in isi["data_vaksin"].items()
        }

        # Membaca jadwal vaksin dan memastikan nilai dosis serta interval berupa angka.
        jadwal = {
            nama: {"maks": int(v["maks"]), "interval": int(v["interval"])}
            for nama, v in isi.get("jadwal_vaksin", jadwal_vaksin).items()
        }

    # Menghentikan pemuatan jika file bermasalah atau isinya tidak sesuai format.
    except (json.JSONDecodeError, KeyError, ValueError, TypeError, OSError):
        return

    # Memperbarui data dalam memori menggunakan data yang berhasil dibaca.
    data_user.clear()
    data_user.update(user)
    data_vaksin.clear()
    data_vaksin.update(vaksin)
    jadwal_vaksin.clear()
    jadwal_vaksin.update(jadwal)

    # Menyesuaikan daftar vaksin dengan jadwal vaksin yang tersedia.
    daftar_vaksin[:] = list(jadwal_vaksin)