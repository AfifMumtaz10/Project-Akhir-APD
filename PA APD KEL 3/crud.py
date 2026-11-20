# Mengimpor data vaksinasi, akun pengguna, jadwal vaksin, dan sesi program.
from data import data_vaksin, data_user, jadwal_vaksin, sesi
# Mengimpor fitur validasi data dan pencarian secara rekursif.
from validasi import validasi_nama, validasi_angka, validasi_tanggal, cari_rekursif
# Mengimpor fitur pengelolaan hak akses, data, ID, akun, dan saran dosis.
from logika import (
    adalah_admin, data_terlihat, buat_id_baru, akun_dari_nama, saran_dosis
)
# Mengimpor fitur untuk menerima dan memilih masukan pengguna.
from input import (
    TETAP, input_angka, input_nama, input_tanggal, pilih_vaksin, pilih_dosis,
    pilih_status, pilih_vaksin_ubah, pilih_dosis_ubah, pilih_status_ubah, pilih_data
)
# Mengimpor fitur untuk menampilkan daftar, penjelasan dosis, tabel, dan konfirmasi.
from tampilan import (
    tampilkan_daftar_vaksin, tampilkan_penjelasan_dosis, tampilkan_tabel_vaksin,
    tampilkan_tabel_jadwal, konfirmasi
)
# Mengimpor fitur untuk menyimpan perubahan data.
from penyimpanan import simpan_data

# Untuk menambahkan data vaksinasi baru.
def proses_tambah():
    print("TAMBAH DATA VAKSINASI")

    if adalah_admin():
        nama = input_nama("Nama Penerima Vaksin: ")
        umur = input_angka("Umur (1-120): ", "Umur", 1, 120)
        akun = akun_dari_nama(nama)
    else:
        akun = sesi["user_aktif"]["username"]
        nama = data_user[akun]["nama"]
        umur = data_user[akun]["umur"]
        print(f"Penerima vaksin: {nama} ({umur} tahun)")

    vaksin = pilih_vaksin()
    maks = jadwal_vaksin[vaksin]["maks"]
    tampilkan_penjelasan_dosis(vaksin, nama)
    dosis = pilih_dosis(maks, saran_dosis(nama, vaksin))
    status = pilih_status()
    tanggal = input_tanggal()

    data_vaksin[buat_id_baru()] = {
        "akun": akun,
        "nama": nama,
        "umur": umur,
        "vaksin": vaksin,
        "dosis": dosis,
        "status": status,
        "tanggal": tanggal,
    }

    simpan_data()
    print("Data berhasil ditambahkan!")


# Untuk menampilkan seluruh data vaksinasi yang dapat dilihat pengguna.
def proses_lihat():
    data = data_terlihat()

    if len(data) == 0:
        print("Belum ada data vaksinasi")
    else:
        tampilkan_tabel_vaksin("DAFTAR DATA VAKSINASI", data)
        print(f"Total data: {len(data)}")


# Untuk mencari data vaksinasi berdasarkan kata kunci.
def proses_cari():
    print("CARI DATA VAKSINASI")

    if adalah_admin():
        kolom, label = "nama", "nama penerima"
    else:
        kolom, label = "vaksin", "jenis vaksin"

    kata_kunci = input(f"Masukkan {label} yang dicari: ").strip().lower()

    if kata_kunci == "":
        print("Kata kunci tidak boleh kosong")
        return

    sumber = data_terlihat()
    daftar_id = list(sumber.keys())

    try:
        hasil_id = cari_rekursif(sumber, daftar_id, kata_kunci, kolom)
    except RecursionError:
        hasil_id = [i for i in daftar_id if kata_kunci in sumber[i][kolom].lower()]

    if len(hasil_id) == 0:
        print("Data tidak ditemukan.")
    else:
        hasil = {i: sumber[i] for i in hasil_id}
        tampilkan_tabel_vaksin("HASIL PENCARIAN", hasil)
        print(f"Ditemukan: {len(hasil)} data")


# Untuk mengubah informasi pada data vaksinasi yang dipilih.
def proses_ubah():
    print("UBAH DATA VAKSINASI")
    sumber = data_terlihat()

    if len(sumber) == 0:
        print("Belum ada data.")
        return

    tampilkan_tabel_vaksin("DAFTAR DATA VAKSINASI", sumber)
    id_ubah, data = pilih_data("Pilih data yang ingin diubah", sumber)

    if data is None:
        return

    print("(Kosongkan lalu tekan Enter jika tidak ingin mengubah)")
    nama_baru = umur_baru = ""

    if adalah_admin():
        nama_baru = input(f"Nama [{data['nama']}]: ").strip()
        umur_baru = input(f"Umur [{data['umur']}]: ").strip()

    tampilkan_daftar_vaksin()
    vaksin_baru = pilih_vaksin_ubah(data["vaksin"])
    vaksin_tujuan = data["vaksin"] if vaksin_baru == TETAP else vaksin_baru
    maks_tujuan = jadwal_vaksin[vaksin_tujuan]["maks"]
    tampilkan_penjelasan_dosis(vaksin_tujuan, data["nama"], id_ubah)
    dosis_baru = pilih_dosis_ubah(maks_tujuan, data["dosis"])
    status_baru = pilih_status_ubah(data["status"])
    tanggal_baru = input(f"Tanggal Vaksin [{data['tanggal'].strftime('%d-%m-%Y')}]: ").strip()

    print()

    if nama_baru != "":
        try:
            data["nama"] = validasi_nama(nama_baru)
        except ValueError as e:
            print(f"{e}, nama tidak diubah.")

    if umur_baru != "":
        try:
            data["umur"] = validasi_angka(umur_baru, "Umur", 1, 120)
        except ValueError as e:
            print(f"{e}, umur tidak diubah.")

    if vaksin_baru != TETAP:
        data["vaksin"] = vaksin_baru

    maks = jadwal_vaksin[data["vaksin"]]["maks"]

    if data["dosis"] > maks:
        data["dosis"] = maks
        print(f"Dosis disesuaikan menjadi {maks} sesuai jenis vaksin.")

    if dosis_baru != TETAP:
        data["dosis"] = dosis_baru

    if status_baru != TETAP:
        data["status"] = status_baru

    if tanggal_baru != "":
        try:
            data["tanggal"] = validasi_tanggal(tanggal_baru)
        except ValueError as e:
            print(f"{e}, tanggal tidak diubah.")

    simpan_data()
    print("Proses ubah data selesai.")


# Untuk menghapus data vaksinasi setelah pengguna mengonfirmasi penghapusan.
def proses_hapus():
    print("HAPUS DATA VAKSINASI")
    sumber = data_terlihat()

    if len(sumber) == 0:
        print("Belum ada data.")
        return

    tampilkan_tabel_vaksin("DAFTAR DATA VAKSINASI", sumber)
    id_hapus, data = pilih_data("Pilih data yang ingin dihapus", sumber)

    if data is None:
        return

    keterangan = f"{data['nama']} - {data['vaksin']} dosis {data['dosis']}"

    if konfirmasi(f"Yakin hapus data '{keterangan}'?"):
        del data_vaksin[id_hapus]
        simpan_data()
        print("Data berhasil dihapus!")
    else:
        print("Penghapusan dibatalkan.")


# Untuk menampilkan jadwal vaksinasi berdasarkan data dosis terakhir.
def proses_jadwal():
    data = data_terlihat()

    if len(data) == 0:
        print("Belum ada data vaksinasi")
        return

    tampilkan_tabel_jadwal(data)
    print("Jadwal dihitung dari dosis terakhir pada tiap jenis vaksin.")

# komentar dari cecil 1111