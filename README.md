# Analisis Pengikut Instagram

![Versi Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)

Sebuah skrip Python sederhana untuk menganalisis data ekspor Instagram (`followers` dan `following`) dan menampilkan laporan tentang siapa yang tidak Anda ikuti kembali dan siapa yang tidak mengikuti Anda kembali.

## Deskripsi

Instagram tidak menyediakan fitur bawaan untuk melihat dengan mudah siapa saja yang tidak mengikuti Anda kembali (unfollowers). Skrip ini hadir untuk mengatasi masalah tersebut dengan cara yang aman dan privat, karena semua proses analisis dilakukan secara lokal di komputer Anda tanpa perlu memberikan akses akun Anda ke layanan pihak ketiga.

Skrip ini membaca file data yang Anda unduh langsung dari Instagram, membandingkannya, dan menghasilkan tiga daftar yang jelas:
1.  **Mutuals**: Akun yang saling mengikuti dengan Anda.
2.  **Not Following Back**: Akun yang Anda ikuti, tetapi tidak mengikuti Anda kembali.
3.  **Fans**: Akun yang mengikuti Anda, tetapi tidak Anda ikuti kembali.

## Fitur

-   ✅ **Analisis Cepat**: Memproses ratusan hingga ribuan data dalam hitungan detik.
-   ✅ **100% Aman & Privat**: Tidak memerlukan login dan tidak mengirim data Anda ke mana pun.
-   ✅ **Tanpa Instalasi**: Tidak memerlukan instalasi library eksternal, hanya Python standar.
-   ✅ **Informatif**: Laporan yang mudah dibaca langsung di terminal Anda.
-   ✅ **Penanganan Error**: Memberikan pesan yang jelas jika file tidak ditemukan atau rusak.

## Memulai

Untuk menjalankan skrip ini, Anda hanya memerlukan Python dan data ekspor dari Instagram.

### Prasyarat

1.  **Python 3.7 atau lebih baru** terinstal di komputer Anda. Anda bisa memeriksanya dengan menjalankan `python --version` di terminal.
2.  **File data Instagram**. Anda perlu mengunduh data Anda dari Instagram.
    -   Buka Instagram > Profil Anda > Menu (ikon tiga garis) > "Aktivitas Anda" > "Unduh informasi Anda".
    -   Minta unduhan dalam format **JSON**.
    -   Setelah unduhan siap (biasanya dalam beberapa menit hingga jam), ekstrak file ZIP tersebut. Anda akan memerlukan file `followers_1.json` dan `following.json`.

### Instalasi & Konfigurasi

1.  **Clone atau Unduh Proyek**
    ```sh
    git clone https://url_proyek_anda.git
    # ATAU unduh file ZIP dan ekstrak.
    ```
2.  **Pindahkan File Data**
    Salin file `followers_1.json` dan `following.json` yang telah Anda unduh ke dalam direktori proyek ini, di lokasi yang sama dengan file skrip (`cek_followers_ig.py`).

## Penggunaan

Setelah semua file berada di tempat yang benar, jalankan skrip melalui terminal atau command prompt:

```sh
python cek_followers_ig.py
```

Anda akan melihat output yang mirip seperti ini:

```
Memulai analisis pengikut Instagram...
Berhasil memuat 82 akun 'following' dan 78 akun 'followers'.
Melakukan perbandingan...

=============================================
      HASIL ANALISIS PENGIKUT INSTAGRAM
=============================================

Saling Mengikuti (Mutuals): 62 akun
---------------------------------------------
- user_a
- user_b
...

Anda Follow Tapi Tidak di-Follback (Not Following Back): 20 akun
---------------------------------------------
- user_c
- user_d
...

Follow Anda Tapi Tidak Anda Follback (Fans): 16 akun
---------------------------------------------
- user_e
- user_f
...

Analisis selesai.
```

## Struktur File

Struktur direktori proyek Anda harus terlihat seperti ini agar skrip dapat berjalan dengan benar:
```
.
├── cek_followers_ig.py    # Skrip utama yang akan Anda jalankan
├── followers_1.json       # <-- File data pengikut Anda
├── following.json         # <-- File data yang Anda ikuti
└── README.md              # File dokumentasi yang sedang Anda baca
```
