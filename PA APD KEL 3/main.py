# Mengambil data sesi untuk memeriksa siapa yang sedang login dan apakah program masih berjalan.
from data import sesi

# Mengambil fungsi keluar_program untuk mengatur proses keluar dari program.
from akun import keluar_program

# Mengambil fungsi jeda untuk memberi waktu sebelum program kembali ke menu.
from tampilan import jeda

# Mengambil menu_awal untuk pengguna yang belum login dan menu_pengguna untuk pengguna yang sudah login.
from menu import menu_awal, menu_pengguna

# Mengambil fungsi muat_data untuk memuat data yang tersimpan sebelum program dijalankan.
from penyimpanan import muat_data

# Fungsi utama yang mengatur jalannya program dari awal hingga selesai.
def main():
    # Memuat semua data yang dibutuhkan sebelum program mulai berjalan.
    muat_data()

    # Mengulang program selama status program masih aktif.
    while sesi["program_berjalan"]:
        try:
            # Jika pengguna belum login, tampilkan menu awal.
            if sesi["user_aktif"] is None:
                menu_awal()
            # Jika pengguna sudah login, tampilkan menu pengguna.
            else:
                menu_pengguna()
        # Menangani kondisi ketika program dihentikan menggunakan Ctrl+C atau input berakhir.
        except (KeyboardInterrupt, EOFError):
            print()
            keluar_program()
        # Menangani kesalahan lain yang terjadi selama program berjalan.
        except Exception as e:
            print(f"Terjadi kesalahan tidak terduga: {e}")
            # Memberi jeda sebelum program kembali ke menu.
            jeda()

# Memastikan fungsi main dijalankan ketika file ini dibuka secara langsung.
if __name__ == "__main__":
    main()