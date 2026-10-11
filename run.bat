@echo off
cd /d "%~dp0"
title Siti Desktop Pet

echo [INFO] Memulai program...

:: Cek venv tanpa menggunakan blok kurung
if exist "venv" goto venv_aktif
echo [INFO] Membuat virtual environment...
python -m venv venv

:venv_aktif
call venv\Scripts\activate

echo [INFO] Menginstal dependensi...
python -m pip install -r requirements.txt --quiet

:: Cek apakah ekstensi sudah pernah dibuka
if exist "venv\.extension_opened" goto jalankan_siti

echo ========================================================
echo  PETUNJUK PASANG EKSTENSI (CUMA SEKALI):
echo  1. Buka browser dan masuk ke menu ekstensi
echo  2. Aktifkan 'Developer Mode' 
echo  3. Seret folder 'siti-ekstensi' yang terbuka ini ke browser!
echo ========================================================
explorer "%~dp0siti-ekstensi"
type nul > "venv\.extension_opened"
pause

:jalankan_siti
echo.
echo [INFO] Menjalankan Siti...
python main.py

:: GEMBOK TERMINAL - Mencegah jendela tertutup otomatis saat error
cmd /k