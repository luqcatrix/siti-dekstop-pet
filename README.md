<div align="center">
  <h1>🐱 Siti: The Anti-Doomscrolling Desktop Pet</h1>
  <p><i>Asisten virtual galak yang siap mencakar layarmu dan menutup tab jika kamu keseringan doomscrolling!</i></p>
</div>

---

## 📖 Tentang Proyek
**Siti** adalah *Desktop Pet* interaktif berbasis Python yang terhubung langsung dengan *browser*-mu. Dibuat khusus untuk memerangi kebiasaan *doomscrolling* (scroll video pendek tanpa henti). 

Jika kamu terlalu lama atau terlalu banyak *scroll* di situs pembuang waktu (seperti YouTube Shorts, TikTok, dll.), Siti akan mengamuk, melompat ke tengah layar, mencakar video yang sedang kamu tonton, dan **menutup tab tersebut secara otomatis!**

## ✨ Fitur Utama
- **🐾 State Machine Lengkap:** Siti memiliki berbagai siklus animasi (Nganggur, Meow, Tidur, Marah, Lari, Cakar, Jalan, Pasrah, hingga Pusing).
- **🎯 Dynamic Auto-Targeting:** Siti dapat mendeteksi posisi *browser* aktif dan secara dinamis melompat tepat ke tengah jendela *browser* di mana pun posisinya berada.
- **🦖 Enlarge Mode:** Saat marah dan menyerang, ukuran Siti akan membesar 2x lipat layaknya bos di *game*!
- **🌐 Real-Time Tracker:** Menggunakan *WebSocket* dan ekstensi *browser* kustom yang dilengkapi fitur *Auto-Reconnect* (sambung ulang otomatis).
- **🖱️ Interaktif:** Tarik dan lempar Siti (*Drag & Drop*) ke mana saja di layar. Goyang-goyangkan *mouse*-mu dengan cepat untuk membuat Siti pusing!

## 🛠️ Teknologi yang Digunakan
- **Backend:** Python 3.x
- **GUI & Animasi:** PyQt6
- **Window Control & Hotkey:** PyAutoGUI, PyGetWindow
- **Komunikasi Data:** WebSockets
- **Ekstensi Browser:** JavaScript, HTML, CSS (Chrome/Brave/Edge Extension API)

---

## 🚀 Cara Instalasi & Menjalankan (Super Praktis!)


### 1. Pemasangan Ekstensi Browser (Cukup Sekali di Awal)
1. Cukup **double-click** file **`run.bat`** untuk pertama kalinya. 
2. Folder `siti-ekstensi` akan terbuka otomatis di File Explorer, dan browser akan mengarah ke halaman manajemen ekstensi.
3. Di browser, aktifkan **"Developer Mode"** di pojok kanan atas.
4. **Seret (Drag and drop)** folder `siti-ekstensi` yang terbuka tadi ke dalam halaman ekstensi browser.
5. Tekan tombol **ENTER** di terminal hitam (`run.bat`), dan Siti akan langsung muncul di pojok kanan bawah layar!

### 2. Penggunaan Selanjutnya
Untuk hari-hari berikutnya, kamu cukup **double-click file `run.bat`** saja. Siti akan langsung berjalan otomatis tanpa perlu mengatur ekstensi lagi!

---

## 📂 Struktur Direktori
📁 siti-dekstop-pet/
├── 📁 asset/             # Kumpulan file GIF & PNG animasi Siti
├── 📁 siti-ekstensi/     # Source code untuk Ekstensi Browser pelacak scroll
│   ├── background.js     # Skrip WebSocket & sistem Auto-Reconnect
│   ├── content.js        # Sensor scroll & URL checker
│   └── manifest.json     # Konfigurasi ekstensi
├── config.py             # Pengaturan sensitivitas, ukuran, & daftar target web
├── main.py               # Inisialisasi aplikasi dan penghubung sinyal
├── pet.py                # Logika utama GUI, interaksi mouse, dan pergerakan
├── tracker.py            # WebSocket Server penerima laporan dari browser
├── requirements.txt      # Daftar dependensi Python
└── run.bat               # Skrip otomatisasi setup & peluncur aplikasi