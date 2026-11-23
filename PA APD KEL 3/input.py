# Menggunakan pwinput agar kata sandi yang dimasukkan tidak terlihat secara langsung.
import pwinput

# Mengambil data akun, daftar vaksin, daftar status, dan batas nilai yang diperbolehkan.
from data import (
    data_user, daftar_vaksin, daftar_status, NAMA_MIN, NAMA_MAKS,
    VAKSIN_MIN, VAKSIN_MAKS, DOSIS_VAKSIN_MAKS, INTERVAL_MAKS
)

# Mengambil fungsi untuk memeriksa nama, jenis vaksin, angka, tanggal, dan format tanggal.
from validasi import (
    validasi_nama, validasi_vaksin, validasi_angka, validasi_tanggal, format_tanggal
)

# Mengambil fungsi untuk menampilkan pilihan menu dan daftar vaksin.
from tampilan import pilih_opsi, tampilkan_daftar_vaksin

# Mengambil fungsi untuk memeriksa hak akses admin, mencari vaksin, dan menambahkan vaksin.
from logika import adalah_admin, cari_nama_vaksin, daftarkan_vaksin

# Penanda untuk mempertahankan nilai lama ketika data tidak ingin diubah.
TETAP = "__tetap__"
# Penanda untuk membatalkan proses pemilihan.
BATAL = "__batal__"
# Penanda untuk memasukkan jenis vaksin secara manual.
LAINNYA = "__lainnya__"

# Fungsi untuk menerima kata sandi dengan karakter yang disembunyikan.
def input_password(pesan):
    return pwinput.pwinput(pesan, mask="*")

# Fungsi untuk meminta angka dan mengulang input jika nilainya tidak sesuai ketentuan.
def input_angka(pesan, label, minimum, maksimum):
    while True:
        try:
            return validasi_angka(input(pesan), label, minimum, maksimum)
        except ValueError as e:
            print(e)

# Fungsi untuk menerima nama dan memeriksa jumlah karakternya.
def input_nama(pesan):
    label = pesan.rstrip(": ")

    while True:
        try:
            return validasi_nama(input(f"{label} ({NAMA_MIN}-{NAMA_MAKS} karakter): "))
        except ValueError as e:
            print(e)

# Fungsi untuk meminta tanggal vaksinasi dengan format yang sesuai.
def input_tanggal():
    while True:
        try:
            return validasi_tanggal(input("Tanggal Vaksin (DD-MM-YYYY): "))
        except ValueError as e:
            print(e)

# Fungsi untuk memasukkan vaksin baru beserta jumlah dosis dan jarak antar dosis.
def input_vaksin_baru():
    while True:
        try:
            nama = validasi_vaksin(
                input(f"Nama Vaksin ({VAKSIN_MIN}-{VAKSIN_MAKS} karakter): ")
            )
            break
        except ValueError as e:
            print(e)

    # Memeriksa apakah nama vaksin sudah tersedia dalam daftar.
    sudah_ada = cari_nama_vaksin(nama)

    # Menggunakan data yang sudah ada jika vaksin tersebut ditemukan.
    if sudah_ada is not None:
        print(f"Vaksin {sudah_ada} sudah tersedia, memakai data yang ada.")
        return sudah_ada

    # Meminta jumlah dosis sesuai batas yang telah ditentukan.
    maks = input_angka(
        f"Jumlah dosis (1-{DOSIS_VAKSIN_MAKS}): ", "Jumlah dosis", 1, DOSIS_VAKSIN_MAKS
    )
    interval = 0

    # Meminta jarak antar dosis jika vaksin memiliki lebih dari satu dosis.
    if maks > 1:
        interval = input_angka(
            f"Jarak antar dosis dalam hari (1-{INTERVAL_MAKS}): ",
            "Jarak antar dosis", 1, INTERVAL_MAKS
        )

    # Menambahkan vaksin baru beserta aturan dosis dan intervalnya.
    daftarkan_vaksin(nama, maks, interval)
    print(f"Vaksin {nama} berhasil ditambahkan ke daftar vaksin.")
    return nama

# Fungsi untuk memastikan pengguna memilih salah satu pilihan yang tersedia.
def pilih_wajib(pertanyaan, daftar_pilihan, default=None):
    while True:
        hasil = pilih_opsi(pertanyaan, daftar_pilihan, default)

        # Mengembalikan pilihan jika pengguna sudah memilih opsi yang valid.
        if hasil is not None:
            return hasil

# Fungsi untuk memilih jenis vaksin dari daftar atau memasukkan vaksin baru.
def pilih_vaksin():
    # Menampilkan seluruh jenis vaksin yang tersedia.
    tampilkan_daftar_vaksin()
    pilihan = [(nama, nama) for nama in daftar_vaksin]
    pilihan.append(("Lainnya (input sendiri)", LAINNYA))
    hasil = pilih_wajib("Pilih Jenis Vaksin", pilihan)

    # Meminta data vaksin baru jika pengguna memilih opsi lainnya.
    if hasil == LAINNYA:
        return input_vaksin_baru()

    return hasil

# Fungsi untuk memilih dosis berdasarkan batas maksimal dan saran dosis.
def pilih_dosis(maks, saran=None):
    pilihan = []

    # Membuat pilihan dosis dari nomor satu hingga batas maksimal.
    for nomor in range(1, maks + 1):
        label = f"Dosis {nomor}"

        # Memberi tanda pada dosis yang disarankan.
        if nomor == saran:
            label += " (disarankan)"

        pilihan.append((label, nomor))

    return pilih_wajib("Pilih Dosis", pilihan, saran)

# Fungsi untuk memilih status vaksinasi yang tersedia.
def pilih_status():
    return pilih_wajib("Pilih Status Vaksin", [(nama, nama) for nama in daftar_status])

# Fungsi untuk memilih jenis vaksin baru atau mempertahankan pilihan sebelumnya.
def pilih_vaksin_ubah(sekarang):
    pilihan = [(f"Tidak diubah ({sekarang})", TETAP)]
    pilihan += [(nama, nama) for nama in daftar_vaksin]
    pilihan.append(("Lainnya (input sendiri)", LAINNYA))
    hasil = pilih_wajib("Jenis Vaksin", pilihan)

    # Meminta jenis vaksin baru jika pengguna memilih opsi lainnya.
    if hasil == LAINNYA:
        return input_vaksin_baru()

    return hasil

# Fungsi untuk memilih dosis baru atau tetap menggunakan dosis sebelumnya.
def pilih_dosis_ubah(maks, sekarang):
    pilihan = [(f"Tidak diubah ({sekarang})", TETAP)]
    pilihan += [(f"Dosis {n}", n) for n in range(1, maks + 1)]
    return pilih_wajib("Dosis", pilihan)

# Fungsi untuk memilih status baru atau mempertahankan status sebelumnya.
def pilih_status_ubah(sekarang):
    pilihan = [(f"Tidak diubah ({sekarang})", TETAP)]
    pilihan += [(nama, nama) for nama in daftar_status]
    return pilih_wajib("Status Vaksin", pilihan)

# Fungsi untuk menampilkan daftar data vaksinasi yang dapat dipilih atau dibatalkan.
def pilih_data(pesan, sumber):
    pilihan = []

    # Menyusun pilihan data dengan nomor, jenis vaksin, dosis, dan tanggal.
    for nomor, (id_vaksin, d) in enumerate(sumber.items(), start=1):
        tanggal = format_tanggal(d["tanggal"])

        # Menampilkan nama penerima jika pengguna yang mengakses adalah admin.
        if adalah_admin():
            label = f"No {nomor} | {d['nama']} | {d['vaksin']} dosis {d['dosis']} | {tanggal}"
        else:
            label = f"No {nomor} | {d['vaksin']} dosis {d['dosis']} | {tanggal}"

        pilihan.append((label, id_vaksin))

    # Menambahkan pilihan untuk membatalkan proses.
    pilihan.append(("Batal", BATAL))
    hasil = pilih_opsi(pesan, pilihan)

    # Menghentikan proses jika pengguna membatalkan atau belum memilih data.
    if hasil is None or hasil == BATAL:
        print("Pemilihan dibatalkan.")
        return None, None

    # Mengembalikan ID dan isi data yang telah dipilih.
    return hasil, sumber[hasil]

# Fungsi untuk membuat username baru dan memeriksa apakah username dapat digunakan.
def input_username_baru():
    while True:
        username = input("Username: ").strip().lower()

        # Membatalkan pembuatan username jika pengguna memasukkan angka nol.
        if username == "0":
            return None

        try:
            # Memeriksa apakah username memenuhi ketentuan yang berlaku.
            if len(username) < 4:
                raise ValueError("Username minimal 4 karakter")
            if " " in username:
                raise ValueError("Username tidak boleh mengandung spasi")
            if username in data_user:
                raise ValueError("Username sudah digunakan, buat yang lain")
            return username
        except ValueError as e:
            print(e)

# Fungsi untuk membuat password baru dan memastikan konfirmasi password sesuai.
def input_password_baru():
    while True:
        password = input_password("Password: ")

        try:
            # Memeriksa apakah password memiliki minimal enam karakter.
            if len(password) < 6:
                raise ValueError("Password minimal 6 karakter")
        except ValueError as e:
            print(e)
            continue

        # Memastikan password yang dikonfirmasi sama dengan password awal.
        if input_password("Konfirmasi Password: ") == password:
            return password

        print("Password tidak sama, coba lagi")