# Mengambil data vaksinasi, data pengguna, jadwal vaksin, dan informasi sesi yang sedang berjalan.
from data import data_vaksin, data_user, jadwal_vaksin, sesi

# Mengambil fungsi untuk memeriksa nama, angka, tanggal, dan mencari data secara rekursif.
from validasi import validasi_nama, validasi_angka, validasi_tanggal, cari_rekursif

# Mengambil fungsi untuk memeriksa admin, menampilkan data, membuat ID baru, mencari akun, dan memberi saran dosis.
from logika import (
    adalah_admin, data_terlihat, buat_id_baru, akun_dari_nama, saran_dosis
)

# Mengambil fungsi untuk menerima input dan memilih data vaksinasi yang dibutuhkan.
from input import (
    TETAP, input_angka, input_nama, input_tanggal, pilih_vaksin, pilih_dosis,
    pilih_status, pilih_vaksin_ubah, pilih_dosis_ubah, pilih_status_ubah, pilih_data
)

# Mengambil fungsi untuk membersihkan tampilan dan menampilkan informasi vaksinasi.
from tampilan import (
    layar_baru, tampilkan_daftar_vaksin, tampilkan_penjelasan_dosis,
    tampilkan_tabel_vaksin, tampilkan_tabel_jadwal, konfirmasi
)

# Mengambil fungsi untuk menyimpan perubahan data.
from penyimpanan import simpan_data


# Fungsi untuk menambahkan data vaksinasi baru.
def proses_tambah():
    judul = "TAMBAH DATA VAKSINASI"
    print(judul)

    # Meminta nama dan umur penerima jika pengguna yang login adalah admin.
    if adalah_admin():
        nama = input_nama("Nama Penerima Vaksin: ")
        umur = input_angka("Umur (1-120): ", "Umur", 1, 120)
        akun = akun_dari_nama(nama)
    # Mengambil nama dan umur dari akun jika pengguna bukan admin.
    else:
        akun = sesi["user_aktif"]["username"]
        nama = data_user[akun]["nama"]
        umur = data_user[akun]["umur"]

    # Menyiapkan informasi penerima vaksin untuk ditampilkan.
    penerima = f"Penerima vaksin: {nama} ({umur} tahun)"

    layar_baru(judul, [penerima])
    # Meminta pengguna memilih jenis vaksin yang akan ditambahkan.
    vaksin = pilih_vaksin()
    # Mengambil batas dosis berdasarkan jenis vaksin yang dipilih.
    maks = jadwal_vaksin[vaksin]["maks"]

    layar_baru(judul, [penerima, f"Jenis vaksin: {vaksin}"])
    # Menampilkan penjelasan dosis sebelum pengguna memilih dosis vaksin.
    tampilkan_penjelasan_dosis(vaksin, nama)
    dosis = pilih_dosis(maks, saran_dosis(nama, vaksin))

    layar_baru(judul, [penerima, f"Jenis vaksin: {vaksin}", f"Dosis: {dosis}"])
    # Meminta status dan tanggal pelaksanaan vaksinasi.
    status = pilih_status()
    tanggal = input_tanggal()

    # Menyimpan data vaksinasi baru dengan ID yang dibuat secara otomatis.
    data_vaksin[buat_id_baru()] = {
        "akun": akun,
        "nama": nama,
        "umur": umur,
        "vaksin": vaksin,
        "dosis": dosis,
        "status": status,
        "tanggal": tanggal,
    }

    # Menyimpan data vaksinasi yang baru ditambahkan.
    simpan_data()
    print("Data berhasil ditambahkan!")


# Fungsi untuk menampilkan seluruh data vaksinasi yang dapat dilihat pengguna.
def proses_lihat():
    # Mengambil data vaksinasi sesuai hak akses pengguna.
    data = data_terlihat()

    # Menampilkan pesan jika belum ada data vaksinasi.
    if len(data) == 0:
        print("Belum ada data vaksinasi")
    # Menampilkan daftar vaksinasi beserta jumlah datanya jika tersedia.
    else:
        tampilkan_tabel_vaksin("DAFTAR DATA VAKSINASI", data)
        print(f"Total data: {len(data)}")


# Fungsi untuk mencari data vaksinasi berdasarkan kata kunci.
def proses_cari():
    print("CARI DATA VAKSINASI")

    # Admin mencari berdasarkan nama penerima, sedangkan pengguna biasa berdasarkan jenis vaksin.
    if adalah_admin():
        kolom, label = "nama", "nama penerima"
    else:
        kolom, label = "vaksin", "jenis vaksin"

    # Meminta kata kunci pencarian dan mengubahnya menjadi huruf kecil.
    kata_kunci = input(f"Masukkan {label} yang dicari: ").strip().lower()

    # Menghentikan pencarian jika kata kunci tidak diisi.
    if kata_kunci == "":
        print("Kata kunci tidak boleh kosong")
        return

    # Mengambil data yang dapat dilihat dan menyusun daftar ID-nya.
    sumber = data_terlihat()
    daftar_id = list(sumber.keys())

    try:
        # Mencari data yang cocok menggunakan fungsi rekursif.
        hasil_id = cari_rekursif(sumber, daftar_id, kata_kunci, kolom)
    # Menggunakan pencarian biasa jika proses rekursif mencapai batas pemanggilan.
    except RecursionError:
        hasil_id = [i for i in daftar_id if kata_kunci in sumber[i][kolom].lower()]

    # Menampilkan pesan jika tidak ada data yang cocok.
    if len(hasil_id) == 0:
        print("Data tidak ditemukan.")
    # Menampilkan data yang sesuai dengan kata kunci pencarian.
    else:
        hasil = {i: sumber[i] for i in hasil_id}
        tampilkan_tabel_vaksin("HASIL PENCARIAN", hasil)
        print(f"Ditemukan: {len(hasil)} data")


# Fungsi untuk mengubah informasi pada data vaksinasi yang sudah tersimpan.
def proses_ubah():
    judul = "UBAH DATA VAKSINASI"
    print(judul)
    # Mengambil data vaksinasi yang dapat diakses oleh pengguna.
    sumber = data_terlihat()

    # Menghentikan proses jika tidak ada data yang tersedia.
    if len(sumber) == 0:
        print("Belum ada data.")
        return

    # Menampilkan daftar vaksinasi dan meminta pengguna memilih data yang akan diubah.
    tampilkan_tabel_vaksin("DAFTAR DATA VAKSINASI", sumber)
    id_ubah, data = pilih_data("Pilih data yang ingin diubah", sumber)

    # Menghentikan proses jika pengguna tidak memilih data.
    if data is None:
        return

    # Menyiapkan keterangan data yang dipilih untuk ditampilkan.
    dipilih = [
        f"Data dipilih: {data['nama']} | {data['vaksin']} dosis {data['dosis']} | {data['status']}"
    ]
    nama_baru = umur_baru = ""

    # Admin dapat mengubah nama dan umur penerima vaksinasi.
    if adalah_admin():
        layar_baru(judul, dipilih)
        print("(Kosongkan lalu tekan Enter jika tidak ingin mengubah)")
        nama_baru = input(f"Nama [{data['nama']}]: ").strip()
        umur_baru = input(f"Umur [{data['umur']}]: ").strip()

    # Menampilkan pilihan jenis vaksin yang tersedia.
    layar_baru(judul, dipilih)
    tampilkan_daftar_vaksin()
    vaksin_baru = pilih_vaksin_ubah(data["vaksin"])

    # Menggunakan jenis vaksin lama jika pengguna memilih untuk tidak mengubahnya.
    vaksin_tujuan = data["vaksin"] if vaksin_baru == TETAP else vaksin_baru
    # Mengambil batas dosis sesuai jenis vaksin yang akan digunakan.
    maks_tujuan = jadwal_vaksin[vaksin_tujuan]["maks"]

    # Menampilkan penjelasan dosis dan meminta perubahan dosis serta status vaksinasi.
    layar_baru(judul, dipilih + [f"Jenis vaksin: {vaksin_tujuan}"])
    tampilkan_penjelasan_dosis(vaksin_tujuan, data["nama"], id_ubah)
    dosis_baru = pilih_dosis_ubah(maks_tujuan, data["dosis"])
    status_baru = pilih_status_ubah(data["status"])

    # Meminta tanggal baru jika tanggal vaksinasi ingin diubah.
    print("(Kosongkan lalu tekan Enter jika tidak ingin mengubah)")
    tanggal_baru = input(f"Tanggal Vaksin [{data['tanggal'].strftime('%d-%m-%Y')}]: ").strip()

    print()

    # Memeriksa dan memperbarui nama jika pengguna memasukkan nama baru.
    if nama_baru != "":
        try:
            data["nama"] = validasi_nama(nama_baru)
        # Menampilkan pesan jika nama tidak valid dan mempertahankan nama sebelumnya.
        except ValueError as e:
            print(f"{e}, nama tidak diubah.")

    # Memeriksa dan memperbarui umur jika pengguna memasukkan umur baru.
    if umur_baru != "":
        try:
            data["umur"] = validasi_angka(umur_baru, "Umur", 1, 120)
        # Menampilkan pesan jika umur tidak valid dan mempertahankan umur sebelumnya.
        except ValueError as e:
            print(f"{e}, umur tidak diubah.")

    # Mengganti jenis vaksin jika pengguna memilih jenis yang berbeda.
    if vaksin_baru != TETAP:
        data["vaksin"] = vaksin_baru

    # Mengambil batas dosis berdasarkan jenis vaksin yang tersimpan.
    maks = jadwal_vaksin[data["vaksin"]]["maks"]

    # Menyesuaikan dosis jika melebihi batas jenis vaksin yang baru.
    if data["dosis"] > maks:
        data["dosis"] = maks
        print(f"Dosis disesuaikan menjadi {maks} sesuai jenis vaksin.")

    # Memperbarui dosis jika pengguna memilih dosis baru.
    if dosis_baru != TETAP:
        data["dosis"] = dosis_baru

    # Memperbarui status jika pengguna memilih status baru.
    if status_baru != TETAP:
        data["status"] = status_baru

    # Memeriksa dan memperbarui tanggal jika tanggal baru diisi.
    if tanggal_baru != "":
        try:
            data["tanggal"] = validasi_tanggal(tanggal_baru)
        # Menampilkan pesan jika tanggal tidak valid dan mempertahankan tanggal sebelumnya.
        except ValueError as e:
            print(f"{e}, tanggal tidak diubah.")

    # Menyimpan perubahan data vaksinasi.
    simpan_data()
    print("Proses ubah data selesai.")


# Fungsi untuk menghapus data vaksinasi yang dipilih pengguna.
def proses_hapus():
    judul = "HAPUS DATA VAKSINASI"
    print(judul)
    # Mengambil data vaksinasi yang dapat diakses oleh pengguna.
    sumber = data_terlihat()

    # Menghentikan proses jika tidak ada data yang bisa dihapus.
    if len(sumber) == 0:
        print("Belum ada data.")
        return

    # Menampilkan daftar vaksinasi dan meminta pengguna memilih data yang akan dihapus.
    tampilkan_tabel_vaksin("DAFTAR DATA VAKSINASI", sumber)
    id_hapus, data = pilih_data("Pilih data yang ingin dihapus", sumber)

    # Menghentikan proses jika pengguna tidak memilih data.
    if data is None:
        return

    # Menyiapkan keterangan data yang akan dihapus.
    keterangan = f"{data['nama']} - {data['vaksin']} dosis {data['dosis']}"
    layar_baru(judul, [f"Data dipilih: {keterangan}"])

    # Meminta konfirmasi sebelum menghapus data secara permanen dari penyimpanan program.
    if konfirmasi("Yakin hapus data ini?"):
        del data_vaksin[id_hapus]
        # Menyimpan perubahan setelah data berhasil dihapus.
        simpan_data()
        print("Data berhasil dihapus!")
    # Membatalkan penghapusan jika pengguna tidak menyetujuinya.
    else:
        print("Penghapusan dibatalkan.")


# Fungsi untuk menampilkan jadwal vaksinasi berdasarkan data yang tersedia.
def proses_jadwal():
    # Mengambil data vaksinasi yang dapat dilihat oleh pengguna.
    data = data_terlihat()

    # Menampilkan pesan jika belum ada data vaksinasi.
    if len(data) == 0:
        print("Belum ada data vaksinasi")
        return

    # Menampilkan jadwal vaksinasi berdasarkan data yang tersimpan.
    tampilkan_tabel_jadwal(data)
    print("Jadwal dihitung dari dosis terakhir pada tiap jenis vaksin.")