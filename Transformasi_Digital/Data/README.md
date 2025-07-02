#Deskripsi
Program file 'script.py' ini digunakan untuk menggabungkan beberapa data indikator kesejahteraan daerah (seperti IPM, kemiskinan, PDRB, dan Gini Ratio) ke dalam satu file Excel utama berdasarkan provinsi dan tahun. Data sumber diambil dari beberapa file Excel, dibersihkan, dan diupdate ke file target.

#Jalankan
- Pastikan semua file Excel yang dibutuhkan ('data_kesejahteraan_daerah.xlsx', 'IPM.xlsx', 'Presentasi penduduk 'miskin.xlsx', 'PDRB.xlsx', 'Gini Ratio.xlsx') berada di folder yang sama dengan 'script.py'.
- Pastikan Python dan library pandas sudah terinstall. Jika belum, install dengan perintah:
```pip install pandas openpyxl```
- Jalankan script di terminal/command prompt dengan perintah:
```python script.py```
- Setelah proses selesai, file hasil akan bernama HASIL_GABUNGAN_KESEJAHTERAAN_v2.xlsx di folder yang sama.
