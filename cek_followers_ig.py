# -*- coding: utf-8 -*-
"""
Analisis Pengikut Instagram.

Script ini menganalisis data dari file ekspor Instagram untuk mengidentifikasi
hubungan antara akun yang diikuti (following) dan akun pengikut (followers).

Kebutuhan:
- Python 3.7+
- File `following.json` dan `followers_1.json` dari ekspor data Instagram
  harus berada di direktori yang sama dengan script ini.

Cara Menjalankan:
- Buka terminal atau command prompt.
- Arahkan ke direktori tempat script ini disimpan.
- Jalankan dengan perintah: python nama_file_ini.py
"""

# --- Tahap 1: Impor Modul yang Diperlukan ---
# Modul-modul ini menyediakan fungsionalitas yang kita butuhkan.
import json  # Untuk membaca dan mem-parsing data dari file format JSON.
from pathlib import Path  # Untuk mengelola path file secara modern dan lintas platform.
from typing import List, Set, Optional  # Untuk memberikan petunjuk tipe data (Type Hinting) demi kejelasan kode.

# --- Tahap 2: Definisi Konstanta ---
# Mendefinisikan path file sebagai konstanta di satu tempat.
# Keuntungannya: jika nama file perlu diubah, cukup ubah di sini.
# Ini adalah praktik "Single Source of Truth".
FOLLOWING_FILE_PATH = Path("following.json")
FOLLOWERS_FILE_PATH = Path("followers_1.json")


def _load_usernames_from_file(filepath: Path, data_key: str, list_key: str) -> Optional[Set[str]]:
    """
    Membaca file JSON dan mengekstrak daftar username.

    Fungsi ini dirancang untuk menangani struktur file JSON dari Instagram
    dan mengembalikan sebuah set berisi username. Tanda underscore (_) di awal nama
    fungsi menandakan ini adalah fungsi "internal" atau "helper".

    Args:
        filepath: Path object menuju file JSON yang akan dibaca.
        data_key: Kunci utama dalam JSON tempat daftar data berada (misal: 'relationships_following').
                  Jika tidak ada (data langsung berupa list), berikan string kosong.
        list_key: Kunci yang berisi daftar username (misal: 'string_list_data').

    Returns:
        Sebuah set berisi username jika berhasil, atau None jika terjadi error.
        Tipe kembalian `Optional[Set[str]]` secara eksplisit memberitahu bahwa
        kegagalan (None) adalah kemungkinan hasil.
    """
    # Langkah Validasi 1: Pastikan file ada sebelum mencoba membukanya.
    # Ini adalah pendekatan "fail-fast" (gagal lebih awal) untuk memberikan error yang jelas.
    if not filepath.exists():
        print(f"[ERROR] File tidak ditemukan di lokasi: {filepath}")
        return None

    try:
        # Langkah Membaca File: 'with' statement adalah cara standar dan aman
        # untuk membuka file di Python karena ia akan otomatis menutup file
        # bahkan jika terjadi error di tengah proses.
        with filepath.open('r', encoding='utf-8') as f:
            # json.load() mem-parsing seluruh file JSON menjadi objek Python (dict atau list).
            data = json.load(f)

        # Langkah Ekstraksi Data: Menangani dua kemungkinan struktur file dari Instagram.
        if data_key:
            # Jika ada kunci utama (seperti di following.json), kita ambil list dari sana.
            # .get() digunakan untuk keamanan; ia tidak akan error jika kunci tidak ada.
            data_list = data.get(data_key, [])
        else:
            # Jika tidak ada kunci utama (seperti di followers_1.json), data itu sendiri adalah list.
            data_list = data

        # Langkah Transformasi Data: Menggunakan 'set comprehension' untuk efisiensi.
        # Ini adalah cara ringkas untuk membuat sebuah set dari iterable lain.
        usernames = {
            # Ambil nilai dari kunci 'value', yang merupakan username.
            # .get(list_key, [{}])[0] adalah cara aman untuk mengakses elemen pertama
            # dari list yang mungkin tidak ada, menghindari IndexError.
            item.get(list_key, [{}])[0].get('value')
            # Ulangi untuk setiap 'item' dalam data_list...
            for item in data_list
            # ...tapi hanya jika item tersebut valid dan memiliki username.
            # Ini berfungsi sebagai filter untuk data yang rusak atau kosong.
            if item.get(list_key) and item.get(list_key)[0].get('value')
        }
        # Mengembalikan data dalam bentuk 'set' karena operasi perbandingan
        # (irisan, selisih) jauh lebih cepat pada set daripada pada list.
        return usernames

    # Langkah Penanganan Error: Menangkap jenis error yang spesifik.
    except json.JSONDecodeError:
        # Error ini terjadi jika file bukan format JSON yang valid.
        print(f"[ERROR] Gagal membaca file {filepath}. File mungkin rusak.")
        return None
    except (KeyError, IndexError) as e:
        # Error ini terjadi jika struktur JSON tidak seperti yang diharapkan.
        print(f"[ERROR] Struktur data pada file {filepath} tidak sesuai dugaan. Error: {e}")
        return None


def _display_results(title: str, accounts: List[str]) -> None:
    """
    Menampilkan hasil analisis dengan format yang rapi.

    Fungsi ini memisahkan logika presentasi (bagaimana data ditampilkan)
    dari logika analisis.

    Args:
        title: Judul untuk kategori yang akan ditampilkan.
        accounts: Daftar akun (username) yang akan ditampilkan.
    """
    # Mencetak judul dan jumlah akun dalam kategori tersebut.
    print(f"\n{title}: {len(accounts)} akun")
    # Mencetak garis bawah yang panjangnya dinamis, menyesuaikan panjang judul.
    print("-" * (len(title) + 12))
    # Jika daftar akun kosong, tampilkan pesan yang informatif.
    if not accounts:
        print("Tidak ada akun dalam kategori ini.")
        return  # Keluar dari fungsi lebih awal.

    # Ulangi setiap akun dalam daftar dan cetak dengan format.
    for account in accounts:
        print(f"- {account}")


def run_analysis() -> None:
    """
    Fungsi utama untuk menjalankan seluruh proses analisis.

    Fungsi ini bertindak sebagai "orkestrator" atau "manajer" yang memanggil
    fungsi-fungsi helper dalam urutan yang benar untuk menyelesaikan tugas.
    """
    print("Memulai analisis pengikut Instagram...")

    # --- Tahap 3: Pemuatan Data ---
    # Memanggil fungsi helper untuk memuat data 'following' dan 'followers'.
    following_usernames = _load_usernames_from_file(
        filepath=FOLLOWING_FILE_PATH,
        data_key='relationships_following',
        list_key='string_list_data'
    )

    followers_usernames = _load_usernames_from_file(
        filepath=FOLLOWERS_FILE_PATH,
        data_key='',  # Kosong karena file followers tidak punya kunci utama.
        list_key='string_list_data'
    )

    # --- Tahap 4: Validasi Pemuatan Data ---
    # Memeriksa apakah kedua fungsi pemuat data berhasil (tidak mengembalikan None).
    # Ini adalah "guard clause" untuk menghentikan eksekusi jika prasyarat tidak terpenuhi.
    if following_usernames is None or followers_usernames is None:
        print("\nAnalisis dihentikan karena gagal memuat data.")
        return

    print(f"\nBerhasil memuat {len(following_usernames)} akun 'following' dan {len(followers_usernames)} akun 'followers'.")
    print("Melakukan perbandingan...")

    # --- Tahap 5: Proses Analisis Inti ---
    # Inilah inti dari program: menggunakan operasi set yang sangat efisien.
    # .intersection() -> menemukan elemen yang ada di KEDUA set.
    mutuals = sorted(list(following_usernames.intersection(followers_usernames)))
    # .difference() -> menemukan elemen yang ada di set pertama TAPI TIDAK ADA di set kedua.
    not_following_back = sorted(list(following_usernames.difference(followers_usernames)))
    fans = sorted(list(followers_usernames.difference(following_usernames)))
    # `sorted(list(...))` mengubah hasil (yang berupa set) menjadi list yang terurut
    # menurut abjad agar outputnya rapi dan mudah dibaca.

    # --- Tahap 6: Presentasi Hasil ---
    # Menampilkan header utama untuk laporan hasil.
    print("\n" + "=" * 45)
    print("      HASIL ANALISIS PENGIKUT INSTAGRAM")
    print("=" * 45)

    # Memanggil fungsi helper untuk menampilkan setiap kategori hasil.
    _display_results("Saling Mengikuti (Mutuals)", mutuals)
    _display_results("Anda Follow Tapi Tidak di-Follback (Not Following Back)", not_following_back)
    _display_results("Follow Anda Tapi Tidak Anda Follback (Fans)", fans)

    print("\nAnalisis selesai.")


# --- Tahap 7: Titik Masuk Eksekusi (Entry Point) ---
# Ini adalah konvensi standar di Python.
# Blok kode di bawah ini HANYA akan berjalan jika file ini dieksekusi
# secara langsung (misal: `python analisis_ig.py`).
if __name__ == "__main__":
    # Jika script dijalankan langsung, panggil fungsi orkestrator utama.
    # Ini membuat kode dapat diimpor sebagai modul oleh skrip lain
    # tanpa menjalankan `run_analysis()` secara otomatis.
    run_analysis()