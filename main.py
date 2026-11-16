"""Aplikasi CLI Pengolahan Data Inventaris Gudang."""

from inventaris_pkg import (
    baca_csv,
    bersihkan_data,
    cari_barang,
    filter_stok_kritis,
    rekap_per_kategori,
    simpan_json,
)


def tampilkan_menu() -> None:
    """Menampilkan opsi menu utama CLI."""
    print("\n=== SISTEM PENGOLAHAN INVENTARIS GUDANG ===")
    print("1. Tampilkan Ringkasan Rekapitulasi per Kategori")
    print("2. Tampilkan Daftar Barang Stok Kritis (< 10 unit)")
    print("3. Cari Barang (ID / Nama / Kategori)")
    print("4. Simpan Laporan ke JSON & Keluar")


def jalankan_aplikasi() -> None:
    """Fungsi utama untuk menjalankan alur program CLI."""
    path_input = input("Masukkan path file CSV [default: data/inventaris_input.csv]: ").strip()
    if not path_input:
        path_input = "data/inventaris_input.csv"

    path_output = "data/laporan_inventaris.json"

    try:
        data_mentah = baca_csv(path_input)
    except (FileNotFoundError, ValueError, OSError) as err:
        print(f"[ERROR] Gagal membaca file: {err}")
        return

    data_bersih, log_peringatan = bersihkan_data(data_mentah)

    print(f"\nBerhasil memuat {len(data_bersih)} data valid dari {len(data_mentah)} baris.")
    if log_peringatan:
        print(f"Ditemukan {len(log_peringatan)} peringatan data (duplikat/tidak valid):")
        for catatan in log_peringatan:
            print(f"  - {catatan}")

    if not data_bersih:
        print("[INFO] Tidak ada data valid untuk diproses.")
        return

    while True:
        tampilkan_menu()
        pilihan = input("Pilih menu (1-4): ").strip()

        if pilihan == "1":
            rekap = rekap_per_kategori(data_bersih)
            print("\n--- REKAPITULASI PER KATEGORI ---")
            for kategori, info in rekap.items():
                print(
                    f"- {kategori}: {info['jumlah_item']} jenis | "
                    f"{info['total_unit']} unit | Aset: Rp{info['total_nilai_aset']:,.2f}"
                )

        elif pilihan == "2":
            kritis = filter_stok_kritis(data_bersih, batas_stok=10)
            print("\n--- BARANG STOK KRITIS (< 10) ---")
            if not kritis:
                print("Semua stok barang dalam kondisi aman.")
            for item in kritis:
                print(
                    f"- [{item['id_barang']}] {item['nama_barang']} "
                    f"({item['kategori']}) -> Sisa: {item['stok']} unit"
                )

        elif pilihan == "3":
            kata_kunci = input("Masukkan kata kunci pencarian: ")
            hasil = cari_barang(data_bersih, kata_kunci)
            print(f"\nDitemukan {len(hasil)} hasil:")
            for item in hasil:
                print(
                    f"- [{item['id_barang']}] {item['nama_barang']} | "
                    f"Stok: {item['stok']} | Harga: Rp{item['harga_satuan']:,.2f}"
                )

        elif pilihan == "4":
            laporan = {
                "ringkasan_umum": {
                    "total_jenis_barang_valid": len(data_bersih),
                    "total_baris_diabaikan": len(log_peringatan),
                    "total_nilai_seluruh_aset": round(
                        sum(item["total_nilai"] for item in data_bersih), 2
                    ),
                },
                "rekap_per_kategori": rekap_per_kategori(data_bersih),
                "peringatan_stok_kritis": filter_stok_kritis(data_bersih, batas_stok=10),
                "data_inventaris_bersih": data_bersih,
                "log_anomali_data": log_peringatan,
            }
            try:
                simpan_json(path_output, laporan)
                print(f"[SUKSES] Laporan berhasil disimpan ke '{path_output}'.")
            except OSError as err:
                print(f"[ERROR] Gagal menyimpan output: {err}")
            break

        else:
            print("[PERINGATAN] Pilihan tidak valid. Silakan masukkan angka 1 sampai 4.")


if __name__ == "__main__":
    try:
        jalankan_aplikasi()
    except KeyboardInterrupt:
        print("\nProgram dihentikan oleh pengguna.")
