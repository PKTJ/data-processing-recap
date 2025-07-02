import pandas as pd
import os

# --- KONFIGURASI ---
TARGET_FILE = 'data_kesejahteraan_daerah.xlsx'
OUTPUT_FILE = 'HASIL_GABUNGAN_KESEJAHTERAAN_v2.xlsx'

SOURCE_FILES = {
    'IPM.xlsx': {'column': 'IPM', 'skip': 3},
    'Presentasi penduduk miskin.xlsx': {'column': 'Kemiskinan', 'skip': 3},
    'PDRB.xlsx': {'column': 'PDRB', 'skip': 3},
    'Gini Ratio.xlsx': {'column': 'Gini', 'skip': 3}
}

# --- ALUR UTAMA ---

def clean_province_name(series):
    """Membersihkan kolom provinsi agar seragam."""
    return series.str.strip().str.upper()

try:
    df_target = pd.read_excel(TARGET_FILE)
    df_target['Provinsi'] = clean_province_name(df_target['Provinsi'])
    print(f" WARNING: Kerangka utama dari '{TARGET_FILE}' berhasil dimuat.")
    df_target.set_index(['Provinsi', 'Tahun'], inplace=True)
except FileNotFoundError:
    print(f" WARNING: File target '{TARGET_FILE}' tidak ditemukan.")
    exit()

for filename, info in SOURCE_FILES.items():
    col_name = info['column']
    skip_rows = info['skip']
    
    print("-" * 40)
    print(f"WARNING: Memproses file '{filename}' untuk kolom '{col_name}'...")

    if not os.path.exists(filename):
        print(f"WARNING: File '{filename}' tidak ditemukan. Proses dilewati.")
        continue

    df_source_wide = pd.read_excel(filename, skiprows=skip_rows)
    df_source_wide.rename(columns={df_source_wide.columns[0]: 'Provinsi'}, inplace=True)
    df_source_wide['Provinsi'] = clean_province_name(df_source_wide['Provinsi'])
    
    df_source_long = pd.melt(
        df_source_wide,
        id_vars=['Provinsi'],
        var_name='Tahun',
        value_name=col_name
    )
    
    # --- Langkah Pembersihan yang Disempurnakan ---
    
    # 1. Konversi Tahun menjadi angka, paksa error menjadi kosong (NaT)
    df_source_long['Tahun'] = pd.to_numeric(df_source_long['Tahun'], errors='coerce')
    
    #    Konversi kolom NILAI (misal: 'PDRB per kapita') menjadi angka, paksa error menjadi kosong (NaN)
    df_source_long[col_name] = pd.to_numeric(df_source_long[col_name], errors='coerce')

    # 3. Hapus baris yang kolom kuncinya (Provinsi, Tahun, atau Nilai) kosong setelah konversi
    df_source_long.dropna(subset=['Provinsi', 'Tahun', col_name], inplace=True)
    
    # 4. Pastikan tipe data Tahun adalah integer
    if not df_source_long.empty:
        df_source_long['Tahun'] = df_source_long['Tahun'].astype(int)
        
        # Cek apakah masih ada data setelah dibersihkan
        if df_source_long.empty:
            print(f"    -> WARNING: Tidak ada data valid yang tersisa di '{filename}' setelah dibersihkan.")
        else:
            df_source_long.set_index(['Provinsi', 'Tahun'], inplace=True)
            df_target.update(df_source_long)
            print(f"    -> WARNING: Kolom '{col_name}' berhasil diupdate.")
    else:
        print(f"    -> WARNING: Tidak ada data valid yang ditemukan di '{filename}'.")


# --- Simpan Hasil Akhir ---
df_target.reset_index(inplace=True)
df_target.to_excel(OUTPUT_FILE, index=False, float_format='%.4f')

print("-" * 40)
print(f"WARNING: PROSES SELESAI! Hasil akhir disimpan di '{OUTPUT_FILE}'.")