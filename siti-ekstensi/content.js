let scrollCount = 0;
let lastUrl = location.href;

// Cek apakah URL saat ini adalah tempat khusus doomscrolling
function isDoomscrollingSite(url) {
    return url.includes("/shorts/") || 
           url.includes("tiktok.com") || 
           url.includes("/reels/");
}

// 1. Lapor "ALERT" saat pertama kali buka web bahaya
if (isDoomscrollingSite(lastUrl)) {
    chrome.runtime.sendMessage({ action: "ALERT" });
}

// 2. Deteksi pergantian URL tanpa refresh (Khas YT/TikTok/IG)
setInterval(() => {
    let currentUrl = location.href;
    if (currentUrl !== lastUrl) {
        lastUrl = currentUrl;
        
        // Jika pindah ke halaman Shorts/Reels/TikTok, bangunkan Siti
        if (isDoomscrollingSite(currentUrl)) {
            chrome.runtime.sendMessage({ action: "ALERT" });
        }
    }
}, 1000); // Cek setiap 1 detik

// 3. Menghitung scroll brutal
window.addEventListener("wheel", (event) => {
    // Hanya hitung scroll JIKA user sedang berada di halaman doomscrolling
    if (isDoomscrollingSite(location.href)) {
        scrollCount++;
        
        if (scrollCount >= 15) {
            chrome.runtime.sendMessage({ action: "ATTACK" });
            scrollCount = 0; 
        }
    } else {
        scrollCount = 0; // Reset jika scroll di web biasa
    }
});