# ==========================================
# KONFIGURASI TARGET & SENSITIVITAS SITI
# ==========================================

TARGET_SITES = [
    "YouTube", "TikTok", "Instagram", "Twitter", 
    "X", "Reddit", "Facebook", "Shopee", "Tokopedia"
]

SCROLL_THRESHOLD = 8     # Minimal jumlah scroll
SCROLL_RESET_TIME = 3.0  # Waktu reset (detik)

# ==========================================
# PENGATURAN VISUAL & GERAKAN SITI
# ==========================================
PET_SIZE = 128           # Ukuran normal (128x128 pixel)
ENLARGED_SIZE = 256      # Ukuran membesar saat ngamuk & nyakar (256x256 pixel)
WALK_SPEED = 8           # Kecepatan lari Siti

# ==========================================
# KONFIGURASI ANIMASI & INTERAKSI
# ==========================================
SCRATCH_DELAY = 2500     # Jeda mencakar sebelum tab ditutup (ms)
IDLE_TIMEOUT = 120000    # Waktu idle sebelum tidur (2 menit)
SHAKE_THRESHOLD = 1500   # Sensitivitas goyangan mouse