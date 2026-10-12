let scrollCount = 0;
let lastUrl = location.href;
const DOOMSCROLL_LIMIT = 10; // Batas tepat 10 video/scroll

// Cek apakah URL saat ini adalah area doomscrolling
function isDoomscrollingSite(url) {
    const lower = url.toLowerCase();
    return lower.includes("/shorts/") || 
           lower.includes("tiktok.com") || 
           lower.includes("/reels/") ||
           lower.includes("/reel/");
}

// Fungsi aman kirim pesan ke background.js
function safeSendMessage(message) {
    try {
        chrome.runtime.sendMessage(message, () => {
            if (chrome.runtime.lastError) {
                // Mengabaikan error koneksi sementara
            }
        });
    } catch (e) {
        // Abaikan jika ekstensi di-reload
    }
}

// Fungsi untuk mencatat dan menambah hitungan doomscroll
function incrementScrollCount() {
    if (!isDoomscrollingSite(location.href)) return;

    scrollCount++;
    console.log(`[Siti] Doomscroll terdeteksi: Video ke-${scrollCount} dari ${DOOMSCROLL_LIMIT}`);

    if (scrollCount >= DOOMSCROLL_LIMIT) {
        safeSendMessage({ action: "ATTACK" });
        scrollCount = 0; // Reset setelah diserang
    } else {
        safeSendMessage({ action: "ALERT" });
    }
}

// 1. Lapor "ALERT" saat pertama kali buka web doomscrolling
if (isDoomscrollingSite(lastUrl)) {
    safeSendMessage({ action: "ALERT" });
}

// 2. Deteksi pergantian URL (Untuk Shorts / Reels)
setInterval(() => {
    let currentUrl = location.href;
    if (currentUrl !== lastUrl) {
        lastUrl = currentUrl;
        if (isDoomscrollingSite(currentUrl)) {
            incrementScrollCount();
        }
    }
}, 500);

// 3. Deteksi Wheel Scroll (Khusus TikTok saat URL tidak berubah)
let lastScrollTime = 0;
window.addEventListener("wheel", (e) => {
    // Hanya tangkap scroll ke bawah dengan throttle 800ms
    if (e.deltaY > 0 && isDoomscrollingSite(location.href)) {
        const now = Date.now();
        if (now - lastScrollTime > 800) {
            lastScrollTime = now;
            // Jika di TikTok dan URL-nya tidak berubah-ubah, hitung via wheel
            if (location.href.includes("tiktok.com")) {
                incrementScrollCount();
            }
        }
    }
}, { passive: true });

// 4. Deteksi Navigasi Tombol Panah Bawah / KeyDown (Untuk TikTok)
window.addEventListener("keydown", (e) => {
    if ((e.key === "ArrowDown" || e.key === "PageDown") && isDoomscrollingSite(location.href)) {
        const now = Date.now();
        if (now - lastScrollTime > 800) {
            lastScrollTime = now;
            if (location.href.includes("tiktok.com")) {
                incrementScrollCount();
            }
        }
    }
});