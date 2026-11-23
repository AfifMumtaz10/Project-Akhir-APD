# Mengimpor os untuk membantu membersihkan tampilan terminal.
import os

# Mengimpor questionary untuk membuat pilihan menu interaktif.
import questionary

# Mengimpor PrettyTable untuk menampilkan data dalam bentuk tabel.
from prettytable import PrettyTable

# Mengambil informasi jadwal dan daftar jenis vaksin.
from data import jadwal_vaksin, daftar_vaksin

# Mengambil fungsi untuk mengubah tanggal menjadi format yang mudah dibaca.
from validasi import format_tanggal

# Mengambil fungsi untuk memeriksa peran akun, menghitung jadwal,
# menentukan dosis terakhir, dan memberikan informasi dosis vaksin.
from logika import (
    adalah_admin, hitung_jadwal, dosis_terakhir,
    keterangan_dosis, dosis_tercatat, saran_dosis, alasan_saran
)


# Mengatur warna tulisan dan penanda pada pilihan menu.
GAYA_PILIHAN = questionary.Style([
    ("pointer", "fg:#00ffff bold"),
    ("highlighted", "fg:#00ffff bold"),
    ("answer", "fg:#00ffff bold"),
])


# Membersihkan tampilan terminal agar layar lebih rapi.
def clear():
    os.system("cls" if os.name == "nt" else "clear")


# Memberi jeda agar pengguna bisa membaca informasi sebelum melanjutkan.
def jeda(pesan="Tekan Enter untuk melanjutkan..."):
    try:
        input(pesan)
    except EOFError:
        pass


# Menampilkan judul beserta informasi tambahan setelah membersihkan layar.
def layar_baru(judul, ringkasan=()):
    clear()
    print(judul)

    for baris in ringkasan:
        print(baris)

    if ringkasan:
        print()


# Menampilkan judul dengan garis pembatas agar terlihat lebih jelas.
def tampilkan_judul(teks):
    garis = "=" * (len(teks) + 10)
    print(garis)
    print(teks.center(len(garis)))
    print(garis)


# Menyusun dan menampilkan data dalam tabel berdasarkan judul, kolom, dan isinya.
def buat_tabel(judul, kolom, baris):
    tabel = PrettyTable()
    tabel.title = judul
    tabel.field_names = kolom
    tabel.align = "l"

    for isi in baris:
        tabel.add_row(isi)

    print(tabel)


# Menampilkan daftar vaksin beserta jumlah dosis dan jarak antar dosisnya.
def tampilkan_daftar_vaksin():
    baris = []

    for nomor, nama in enumerate(daftar_vaksin, start=1):
        info = jadwal_vaksin[nama]
        jarak = f"{info['interval']} hari" if info["maks"] > 1 else "-"
        baris.append([nomor, nama, info["maks"], jarak])

    buat_tabel(
        "JENIS VAKSIN TERSEDIA",
        ["No", "Jenis Vaksin", "Jumlah Dosis", "Jarak Antar Dosis"],
        baris
    )


# Menjelaskan tahapan dosis vaksin, mencatat dosis yang sudah diterima,
# serta memberikan saran dosis berikutnya berdasarkan riwayat vaksinasi.
def tampilkan_penjelasan_dosis(vaksin, nama, kecuali_id=None):
    maks = jadwal_vaksin[vaksin]["maks"]
    tercatat = dosis_tercatat(nama, vaksin, kecuali_id)
    saran = saran_dosis(nama, vaksin, kecuali_id)
    baris = []

    for nomor in range(1, maks + 1):
        if nomor in tercatat:
            catatan = "Sudah tercatat"
        elif nomor == saran:
            catatan = "Disarankan"
        else:
            catatan = "-"

        baris.append([nomor, keterangan_dosis(vaksin, nomor), catatan])

    buat_tabel(
        f"PENJELASAN DOSIS {vaksin.upper()}",
        ["Dosis", "Penjelasan", "Catatan"],
        baris
    )

    if saran is None:
        print(f"Saran: semua dosis {vaksin} atas nama {nama} sudah tercatat lengkap.")
    else:
        print(f"Saran: Dosis {saran} untuk vaksin {vaksin}.")

    print("Dasar saran:")

    for alasan in alasan_saran(nama, vaksin, kecuali_id):
        print(f"- {alasan}")


# Menampilkan data vaksinasi dalam tabel dengan kolom yang disesuaikan
# berdasarkan peran akun yang sedang login.
def tampilkan_tabel_vaksin(judul, data):
    if adalah_admin():
        kolom = [
            "No", "Nama", "Umur", "Jenis Vaksin", "Dosis",
            "Status", "Tanggal Vaksin", "Akun"
        ]
    else:
        kolom = ["No", "Jenis Vaksin", "Dosis", "Status", "Tanggal Vaksin"]

    baris = []

    for nomor, d in enumerate(data.values(), start=1):
        if adalah_admin():
            baris.append([
                nomor, d["nama"], d["umur"], d["vaksin"], d["dosis"],
                d["status"], format_tanggal(d["tanggal"]), d["akun"] or "-"
            ])
        else:
            baris.append([
                nomor, d["vaksin"], d["dosis"], d["status"],
                format_tanggal(d["tanggal"])
            ])

    buat_tabel(judul, kolom, baris)


# Menampilkan jadwal vaksinasi setiap orang berdasarkan dosis terakhir
# yang tercatat, termasuk jadwal lanjutan dan status waktunya.
def tampilkan_tabel_jadwal(data):
    kolom = [
        "Nama", "Jenis Vaksin", "Dosis Terakhir", "Tanggal Terakhir",
        "Dosis Berikutnya", "Jadwal Berikutnya", "Status"
    ]
    baris = []

    for id_vaksin in dosis_terakhir(data):
        d = data[id_vaksin]
        dosis_next, jadwal, status = hitung_jadwal(d["vaksin"], d["dosis"], d["tanggal"])
        maks = jadwal_vaksin[d["vaksin"]]["maks"]
        baris.append([
            d["nama"], d["vaksin"], f"{d['dosis']} dari {maks}",
            format_tanggal(d["tanggal"]), dosis_next, jadwal, status
        ])

    buat_tabel("JADWAL DOSIS BERIKUTNYA", kolom, baris)


# Menampilkan pilihan interaktif dan mengembalikan nilai dari pilihan pengguna.
# Jika terjadi ValueError, pilihan ditampilkan kembali tanpa pilihan awal.
def pilih_opsi(pertanyaan, daftar_pilihan, default=None):
    pilihan = [
        questionary.Choice(title=label, value=nilai)
        for label, nilai in daftar_pilihan
    ]

    def tanya(awal):
        return questionary.select(
            pertanyaan,
            choices=pilihan,
            qmark="",
            pointer="»",
            instruction=" ",
            style=GAYA_PILIHAN,
            default=awal,
        ).ask()

    try:
        return tanya(default)
    except ValueError:
        return tanya(None)


# Meminta pengguna menentukan pilihan Ya atau Tidak dan mengembalikan hasilnya.
def konfirmasi(pertanyaan):
    hasil = pilih_opsi(pertanyaan, [("Tidak", False), ("Ya", True)])
    return hasil is True


# Menampilkan menu lengkap dengan keterangan setiap pilihan
# serta menyediakan pilihan tambahan untuk kembali atau keluar.
def pilih_menu(judul, opsi, label_nol):
    tampilkan_judul(judul)

    lebar = max(len(o["label"]) for o in opsi.values())
    pilihan = [
        (o["label"].ljust(lebar) + "  " + o["info"], kode)
        for kode, o in opsi.items()
    ]
    pilihan.append((label_nol, "0"))

    hasil = pilih_opsi("", pilihan)
    return hasil if hasil is not None else "0"