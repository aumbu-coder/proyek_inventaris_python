"""Module untuk membaca file CSV dan menulis hasil analisis ke file JSON."""

import csv
import json
from pathlib import Path


def baca_csv(path_file: str) -> list[dict]:
    """
    Membaca data mentah dari file CSV.

    Parameter:
        path_file (str): Lokasi file CSV input.

    Return:
        list[dict]: Daftar dictionary mentah hasil pembacaan CSV.
    """
    lokasi = Path(path_file)
    if not lokasi.exists() or not lokasi.is_file():
        raise FileNotFoundError(f"File input tidak ditemukan: {path_file}")

    with lokasi.open(mode="r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames is None:
            raise ValueError("File CSV kosong atau tidak memiliki header.")
        return list(reader)


def simpan_json(path_file: str, data_output: dict) -> None:
    """
    Menyimpan hasil rekapitulasi dan data bersih ke dalam file JSON.

    Parameter:
        path_file (str): Lokasi file JSON tujuan.
        data_output (dict): Struktur data laporan yang akan disimpan.
    """
    lokasi = Path(path_file)
    lokasi.parent.mkdir(parents=True, exist_ok=True)

    with lokasi.open(mode="w", encoding="utf-8") as file:
        json.dump(data_output, file, indent=4, ensure_ascii=False)
