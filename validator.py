"""Module validasi data input untuk menerapkan defensive programming."""


def validasi_baris(baris: dict, nomor_baris: int) -> tuple[dict | None, str | None]:
    """
    Memvalidasi dan mengonversi tipe data satu baris record inventaris.

    Parameter:
        baris (dict): Data mentah satu baris dari csv.DictReader.
        nomor_baris (int): Nomor urut baris pada file CSV.

    Return:
        tuple: (data_bersih, None) jika valid, atau (None, pesan_error) jika tidak valid.
    """
    kolom_wajib = {"id_barang", "nama_barang", "kategori", "stok", "harga_satuan"}
    if not baris or not kolom_wajib.issubset(baris.keys()):
        return None, f"Baris {nomor_baris}: Struktur kolom tidak lengkap."

    id_barang = (baris.get("id_barang") or "").strip().upper()
    nama_barang = (baris.get("nama_barang") or "").strip()
    kategori = (baris.get("kategori") or "").strip().title()

    if not id_barang or not nama_barang or not kategori:
        return None, f"Baris {nomor_baris}: ID, nama, atau kategori kosong."

    try:
        stok = int((baris.get("stok") or "").strip())
        harga = float((baris.get("harga_satuan") or "").strip())
    except ValueError:
        return None, f"Baris {nomor_baris} ({id_barang}): Stok atau harga bukan angka valid."

    if stok < 0 or harga < 0:
        return None, f"Baris {nomor_baris} ({id_barang}): Stok atau harga tidak boleh negatif."

    return {
        "id_barang": id_barang,
        "nama_barang": nama_barang,
        "kategori": kategori,
        "stok": stok,
        "harga_satuan": harga,
        "total_nilai": round(stok * harga, 2),
    }, None
