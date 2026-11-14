# Menggunakan pustaka pwinput agar karakter kata sandi tersembunyi ketika dimasukkan.
import pwinput
# Mengimpor data akun, daftar vaksin, daftar status, serta batas nilai masukan yang diizinkan.
from data import (
    data_user, daftar_vaksin, daftar_status, NAMA_MIN, NAMA_MAKS,
    VAKSIN_MIN, VAKSIN_MAKS, DOSIS_VAKSIN_MAKS, INTERVAL_MAKS
)
# Mengimpor fungsi untuk memvalidasi nama, vaksin, angka, dan tanggal.
from validasi import (
    validasi_nama, validasi_vaksin, validasi_angka, validasi_tanggal, format_tanggal
)
# Mengimpor fungsi untuk mengelola pemilihan menu dan menampilkan daftar vaksin.
from tampilan import pilih_opsi, tampilkan_daftar_vaksin
# Mengimpor fungsi untuk memeriksa hak akses admin, mencari vaksin, dan mendaftarkan vaksin.
from logika import adalah_admin, cari_nama_vaksin, daftarkan_vaksin

# Penanda untuk pilihan tidak mengubah data lama saat proses pengubahan berlangsung.
TETAP = "__tetap__"
# Penanda untuk membatalkan proses pemilihan data yang sedang dilakukan.
BATAL = "__batal__"
# Penanda untuk memilih opsi memasukkan data baru secara manual di luar daftar yang tersedia.
LAINNYA = "__lainnya__"

# Meminta kata sandi dengan karakter yang ditampilkan dalam bentuk tersembunyi.
def input_password(pesan):
    return pwinput.pwinput(pesan, mask="*")

# Meminta masukan angka secara berulang hingga nilainya berada dalam rentang yang ditentukan.
def input_angka(pesan, label, minimum, maksimum):
    while True:
        try:
            return validasi_angka(input(pesan), label, minimum, maksimum)
        except ValueError as e:
            print(e)

# Meminta nama pengguna dan memastikan panjangnya memenuhi ketentuan yang berlaku.
def input_nama(pesan):
    label = pesan.rstrip(": ")

    while True:
        try:
            return validasi_nama(input(f"{label} ({NAMA_MIN}-{NAMA_MAKS} karakter): "))
        except ValueError as e:
            print(e)

# Meminta tanggal vaksinasi dan memeriksa kesesuaian format yang digunakan.
def input_tanggal():
    while True:
        try:
            return validasi_tanggal(input("Tanggal Vaksin (DD-MM-YYYY): "))
        except ValueError as e:
            print(e)

# Menambahkan nama vaksin baru beserta jumlah dosis dan interval antar dosisnya.
def input_vaksin_baru():
    while True:
        try:
            nama = validasi_vaksin(
                input(f"Nama Vaksin ({VAKSIN_MIN}-{VAKSIN_MAKS} karakter): ")
            )
            break
        except ValueError as e:
            print(e)

    sudah_ada = cari_nama_vaksin(nama)

    if sudah_ada is not None:
        print(f"Vaksin {sudah_ada} sudah tersedia, memakai data yang ada.")
        return sudah_ada

    maks = input_angka(
        f"Jumlah dosis (1-{DOSIS_VAKSIN_MAKS}): ", "Jumlah dosis", 1, DOSIS_VAKSIN_MAKS
    )
    interval = 0

    if maks > 1:
        interval = input_angka(
            f"Jarak antar dosis dalam hari (1-{INTERVAL_MAKS}): ",
            "Jarak antar dosis", 1, INTERVAL_MAKS
        )

    daftarkan_vaksin(nama, maks, interval)
    print(f"Vaksin {nama} berhasil ditambahkan ke daftar vaksin.")
    return nama

# Mewajibkan pengguna untuk memilih salah satu opsi yang telah disediakan.
def pilih_wajib(pertanyaan, daftar_pilihan, default=None):
    while True:
        hasil = pilih_opsi(pertanyaan, daftar_pilihan, default)

        if hasil is not None:
            return hasil

# Menampilkan daftar vaksin agar pengguna dapat memilih jenis vaksin yang diperlukan.
def pilih_vaksin():
    tampilkan_daftar_vaksin()
    pilihan = [(nama, nama) for nama in daftar_vaksin]
    pilihan.append(("Lainnya (input sendiri)", LAINNYA))
    hasil = pilih_wajib("Pilih Jenis Vaksin", pilihan)

    if hasil == LAINNYA:
        return input_vaksin_baru()

    return hasil

# Menyediakan daftar pilihan dosis sesuai batas maksimal vaksin dan menandai dosis yang direkomendasikan.
def pilih_dosis(maks, saran=None):
    pilihan = []

    for nomor in range(1, maks + 1):
        label = f"Dosis {nomor}"

        if nomor == saran:
            label += " (disarankan)"

        pilihan.append((label, nomor))

    return pilih_wajib("Pilih Dosis", pilihan, saran)

# Menampilkan pilihan status yang tersedia untuk vaksinasi.
def pilih_status():
    return pilih_wajib("Pilih Status Vaksin", [(nama, nama) for nama in daftar_status])

# Menentukan vaksin pengganti atau tetap menggunakan vaksin yang telah dipilih sebelumnya.
def pilih_vaksin_ubah(sekarang):
    pilihan = [(f"Tidak diubah ({sekarang})", TETAP)]
    pilihan += [(nama, nama) for nama in daftar_vaksin]
    pilihan.append(("Lainnya (input sendiri)", LAINNYA))
    hasil = pilih_wajib("Jenis Vaksin", pilihan)

    if hasil == LAINNYA:
        return input_vaksin_baru()

    return hasil

# Menentukan dosis pengganti atau mempertahankan dosis yang digunakan sebelumnya.
def pilih_dosis_ubah(maks, sekarang):
    pilihan = [(f"Tidak diubah ({sekarang})", TETAP)]
    pilihan += [(f"Dosis {n}", n) for n in range(1, maks + 1)]
    return pilih_wajib("Dosis", pilihan)

# Memilih status vaksinasi yang baru atau tetap menggunakan status sebelumnya.
def pilih_status_ubah(sekarang):
    pilihan = [(f"Tidak diubah ({sekarang})", TETAP)]
    pilihan += [(nama, nama) for nama in daftar_status]
    return pilih_wajib("Status Vaksin", pilihan)

# Menyusun daftar data vaksinasi yang dapat dipilih atau dibatalkan oleh pengguna.
def pilih_data(pesan, sumber):
    pilihan = []

    for nomor, (id_vaksin, d) in enumerate(sumber.items(), start=1):
        tanggal = format_tanggal(d["tanggal"])

        if adalah_admin():
            label = f"No {nomor} | {d['nama']} | {d['vaksin']} dosis {d['dosis']} | {tanggal}"
        else:
            label = f"No {nomor} | {d['vaksin']} dosis {d['dosis']} | {tanggal}"

        pilihan.append((label, id_vaksin))

    pilihan.append(("Batal", BATAL))
    hasil = pilih_opsi(pesan, pilihan)

    if hasil is None or hasil == BATAL:
        print("Pemilihan dibatalkan.")
        return None, None

    return hasil, sumber[hasil]

# Membuat nama pengguna baru dengan memeriksa panjang, spasi, dan ketersediaannya.
def input_username_baru():
    while True:
        username = input("Username: ").strip().lower()

        if username == "0":
            return None

        try:
            if len(username) < 4:
                raise ValueError("Username minimal 4 karakter")
            if " " in username:
                raise ValueError("Username tidak boleh mengandung spasi")
            if username in data_user:
                raise ValueError("Username sudah digunakan, buat yang lain")
            return username
        except ValueError as e:
            print(e)

# Membuat kata sandi baru dan memeriksa kesesuaiannya dengan konfirmasi kata sandi.
def input_password_baru():
    while True:
        password = input_password("Password: ")

        try:
            if len(password) < 6:
                raise ValueError("Password minimal 6 karakter")
        except ValueError as e:
            print(e)
            continue

        if input_password("Konfirmasi Password: ") == password:
            return password

        print("Password tidak sama, coba lagi")