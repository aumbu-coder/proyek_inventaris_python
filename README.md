# Sistem Pengolahan Data Inventaris Gudang (CLI)

Aplikasi berbasis Command Line Interface (CLI) menggunakan Python untuk membersihkan data inventaris mentah (CSV), menghapus duplikat, mendeteksi stok kritis, merekapitulasi aset per kategori, dan mengekspor laporan ke format JSON.

## Struktur Program
- `main.py`: Titik masuk utama (*entry point*) aplikasi CLI.
- `inventaris_pkg/`: Package buatan sendiri yang berisi logika inti:
  - `__init__.py`: Antarmuka ekspor fungsi package.
  - `file_handler.py`: Modul pembacaan CSV dan penulisan JSON.
  - `validator.py`: Modul validasi tipe data dan *defensive programming*.
  - `processor.py`: Modul deduplikasi, pencarian, filter stok kritis, dan rekapitulasi kategori.
- `data/inventaris_input.csv`: Contoh dataset masukan.
- `data/laporan_inventaris.json`: Hasil keluaran analisis sistem.

## Dependency & Kebutuhan Sistem
- **Python**: Versi 3.10 atau lebih baru.
- **Library**: Hanya menggunakan *Python Standard Library* (`csv`, `json`, `pathlib`) tanpa dependensi eksternal tambahan.

## Cara Menjalankan Aplikasi
1. Buka terminal/command prompt dan arahkan ke direktori utama `proyek_inventaris/`.
2. Jalankan perintah berikut:
   ```bash
   python main.py
   ```
3. Tekan `Enter` saat diminta memasukkan path file CSV untuk menggunakan file bawaan (`data/inventaris_input.csv`), atau ketik path file CSV lain.
4. Pilih menu `1` hingga `4` sesuai kebutuhan. Pilih menu `4` untuk menyimpan laporan akhir ke `data/laporan_inventaris.json`.
