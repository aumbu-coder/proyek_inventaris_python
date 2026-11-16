"""Module pemrosesan, pembersihan, filtering, dan rekapitulasi data."""

from .validator import validasi_baris


def bersihkan_data(data_mentah: list[dict]) -> tuple[list[dict], list[str]]:
    """
    Memvalidasi setiap baris dan menghapus data duplikat berdasarkan id_barang.

    Parameter:
        data_mentah (list[dict]): Daftar baris mentah dari CSV.

    Return:
        tuple: (list data bersih unik, list catatan error/duplikat).
    """
    data_bersih: list[dict] = []
    seen_ids: set[str] = set()
    log_peringatan: list[str] = []

    for idx, baris in enumerate(data_mentah, start=2):
        record, error = validasi_baris(baris, idx)
        if error:
            log_peringatan.append(error)
            continue

        if record["id_barang"] in seen_ids:
            log_peringatan.append(
                f"Baris {idx}: Duplikat ID '{record['id_barang']}' diabaikan."
            )
            continue

        seen_ids.add(record["id_barang"])
        data_bersih.append(record)

    return data_bersih, log_peringatan


def filter_stok_kritis(data_bersih: list[dict], batas_stok: int = 10) -> list[dict]:
    """
    Menyaring barang dengan jumlah stok di bawah batas tertentu.

    Parameter:
        data_bersih (list[dict]): Data inventaris valid.
        batas_stok (int): Ambang batas minimum stok aman.

    Return:
        list[dict]: Daftar barang yang perlu restock.
    """
    return [item for item in data_bersih if item["stok"] < batas_stok]


def cari_barang(data_bersih: list[dict], kata_kunci: str) -> list[dict]:
    """
    Mencari barang berdasarkan potongan nama, ID, atau kategori.

    Parameter:
        data_bersih (list[dict]): Data inventaris valid.
        kata_kunci (str): Teks pencarian.

    Return:
        list[dict]: Daftar barang yang cocok dengan kata kunci.
    """
    kunci = kata_kunci.strip().lower()
    if not kunci:
        return []

    return [
        item
        for item in data_bersih
        if kunci in item["nama_barang"].lower()
        or kunci in item["id_barang"].lower()
        or kunci in item["kategori"].lower()
    ]


def rekap_per_kategori(data_bersih: list[dict]) -> dict:
    """
    Mengelompokkan dan menghitung total unit serta total nilai aset per kategori.

    Parameter:
        data_bersih (list[dict]): Data inventaris valid.

    Return:
        dict: Rekapitulasi per kategori beserta ringkasan keseluruhan.
    """
    kategori_unik: set[str] = {item["kategori"] for item in data_bersih}
    rekap: dict[str, dict] = {
        kat: {"jumlah_item": 0, "total_unit": 0, "total_nilai_aset": 0.0}
        for kat in sorted(kategori_unik)
    }

    for item in data_bersih:
        kat = item["kategori"]
        rekap[kat]["jumlah_item"] += 1
        rekap[kat]["total_unit"] += item["stok"]
        rekap[kat]["total_nilai_aset"] = round(
            rekap[kat]["total_nilai_aset"] + item["total_nilai"], 2
        )

    return rekap
