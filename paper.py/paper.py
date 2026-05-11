import json
from PIL import Image
import math
import os

# 1. Konfigurasi Warna Dasar & Inisial untuk Instruksi
DAFTAR_WARNA = {
    "MERAH": {"rgb": (255, 0, 0), "kode": "M"},
    "HIJAU": {"rgb": (0, 104, 71), "kode": "H"},
    "BIRU": {"rgb": (0, 0, 255), "kode": "B"},
    "KUNING": {"rgb": (255, 255, 0), "kode": "K"},
    "PUTIH": {"rgb": (255, 255, 255), "kode": "P"},
    "HITAM": {"rgb": (0, 0, 0), "kode": "HTM"}
}

def hitung_jarak_warna(rgb1, rgb2):
    """Menghitung kemiripan warna (Euclidean Distance)"""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(rgb1, rgb2)))

def cari_warna_terdekat(pixel_asli):
    """Mencari nama warna terdekat dari palet"""
    nama_warna = min(
        DAFTAR_WARNA.keys(),
        key=lambda nama: hitung_jarak_warna(pixel_asli, DAFTAR_WARNA[nama]["rgb"])
    )
    return nama_warna

def main():
    print("=== WELCOME TO PAPERMOB GENERATOR (by @lalala_habib) ===")

    # Input Ukuran Formasi
    try:
        kolom = int(input("Masukkan jumlah KOLOM (Lebar): "))
        baris = int(input("Masukkan jumlah BARIS (Tinggi): "))
    except ValueError:
        print("❌ Input harus berupa angka!")
        return

    print(f"\nTotal peserta: {kolom * baris} orang.")
    print("-" * 40)

    kumpulan_gambar = []
    while True:
        nama_file = input(f"Masukkan nama file gambar ke-{len(kumpulan_gambar)+1} (atau ketik 'DONE'): ")
        if nama_file.lower() == 'done':
            break
        if os.path.exists(nama_file):
            kumpulan_gambar.append(nama_file)
            print(f"✅ {nama_file} ditambahkan.")
        else:
            print("❌ File tidak ditemukan!")

    if not kumpulan_gambar:
        print("Tidak ada gambar untuk diproses.")
        return

    # Inisialisasi database untuk instruksi per orang {nomor_kursi: [list_kode_warna]}
    database_instruksi = {i: [] for i in range(1, (kolom * baris) + 1)}

    print("\n--- Memproses Gambar & Membuat Preview ---")

    for idx, img_path in enumerate(kumpulan_gambar, 1):
        try:
            img = Image.open(img_path).convert('RGB')
            img = img.resize((kolom, baris), Image.Resampling.LANCZOS)

            # Buat kanvas untuk preview visual
            preview_img = Image.new('RGB', (kolom, baris))

            nomor_urut = 1
            for y in range(baris):
                for x in range(kolom):
                    pixel_asli = img.getpixel((x, y))
                    nama_warna = cari_warna_terdekat(pixel_asli)

                    # Tambahkan kode warna ke database instruksi peserta
                    kode_warna = DAFTAR_WARNA[nama_warna]["kode"]
                    database_instruksi[nomor_urut].append(kode_warna)

                    # Update preview visual
                    preview_img.putpixel((x, y), DAFTAR_WARNA[nama_warna]["rgb"])
                    nomor_urut += 1

            # Simpan Preview PNG
            nama_preview = f"preview_formasi_{idx}.png"
            preview_img.resize((kolom*10, baris*10), Image.NEAREST).save(nama_preview)
            print(f"[{idx}/{len(kumpulan_gambar)}] ✅ {img_path} -> Preview: {nama_preview}")

        except Exception as e:
            print(f"❌ Gagal memproses {img_path}: {e}")

    # --- GENERATE OUTPUT TXT (CUE CARD) ---
    output_txt = "INSTRUKSI_PESERTA_FINAL.txt"
    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write(f"=== DAFTAR INSTRUKSI PAPERMOB ({kolom}x{baris}) ===\n\n")

        for kursi, daftar_kode in database_instruksi.items():
            # Hitung posisi baris dan kolom riil
            b_riil = math.ceil(kursi / kolom)
            k_riil = kursi % kolom if kursi % kolom != 0 else kolom

            f.write(f"PESERTA NO: {kursi} (Baris: {b_riil}, Kolom: {k_riil})\n")
            f.write("-" * 25 + "\n")

            for i, kode in enumerate(daftar_kode, 1):
                f.write(f"{i}. {kode}\n")

            f.write(f"{len(daftar_kode)+1}. TURUN (SELESAI)\n")
            f.write("\n" + "="*30 + "\n\n")

    print("\n" + "="*40)
    print(f"✨ SEMUA PROSES SELESAI!")
    print(f"Terimakasih Telah menggunakan program dari @lalala_habib")
    print(f"1. Lihat file PNG untuk preview visual tiap formasi.")
    print(f"2. Buka '{output_txt}' untuk daftar instruksi per orang.")
    print("="*40)

if __name__ == "__main__":
    main()