# Mengambil data sesi untuk mengetahui siapa yang sedang login dan apakah program masih berjalan.
from data import sesi
# Mengambil fungsi keluar_program untuk menangani proses keluar dari program.
from akun import keluar_program
# Mengambil fungsi jeda untuk menahan tampilan sejenak sebelum kembali ke menu.
from tampilan import jeda
# Mengambil menu_awal untuk pengguna yang belum login dan menu_pengguna untuk pengguna yang sudah login.
from menu import menu_awal, menu_pengguna
# Mengambil fungsi muat_data untuk memuat seluruh data yang tersimpan sebelum program dimulai.
from penyimpanan import muat_data

# Fungsi utama yang menjalankan alur program dari awal sampai selesai.
def main():
    # Memuat semua data yang tersimpan sebelum program mulai dijalankan.
    muat_data()

    # Selama program masih berjalan, tampilkan menu sesuai status login pengguna.
    while sesi["program_berjalan"]:
        try:
            if sesi["user_aktif"] is None:
                menu_awal()
            else:
                menu_pengguna()
        # Jika pengguna menekan Ctrl+C atau program dihentikan secara paksa, keluar dengan aman.
        except (KeyboardInterrupt, EOFError):
            print()
            keluar_program()
        # Jika terjadi error lain yang tidak terduga, tampilkan pesannya lalu kembali ke menu.
        except Exception as e:
            print(f"Terjadi kesalahan tidak terduga: {e}")
            jeda()

# Memastikan fungsi main hanya berjalan saat file ini dijalankan langsung, bukan saat diimpor.
if __name__ == "__main__":
    main()
