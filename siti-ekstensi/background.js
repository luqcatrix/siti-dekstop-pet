let ws = null;
let isConnecting = false;

function connectWebSocket() {
    // Kalau sudah konek atau sedang mencoba konek, batalkan
    if (isConnecting || (ws && ws.readyState === WebSocket.OPEN)) return;
    isConnecting = true;
    
    console.log("[Siti Ekstensi] Mencoba terhubung ke Python Siti...");
    ws = new WebSocket("ws://localhost:8765");

    ws.onopen = () => {
        console.log("[Siti Ekstensi] Berhasil terhubung ke Python Siti! 🐱");
        isConnecting = false;
    };

    ws.onclose = () => {
        console.log("[Siti Ekstensi] Koneksi terputus. Mencari Siti lagi dalam 3 detik...");
        isConnecting = false;
        ws = null;
        
        // Coba sambung ulang otomatis setelah 3 detik
        setTimeout(connectWebSocket, 3000);
    };

    ws.onerror = (error) => {
        console.log("[Siti Ekstensi] Error pada WebSocket. Menutup koneksi...");
        // Tutup paksa untuk memicu onclose agar bisa reconnect
        if (ws) ws.close(); 
    };
}

// Jalankan pencarian koneksi pertama kali
connectWebSocket();

// Mendengarkan ketukan/laporan dari content.js
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    // Hanya kirim sinyal JIKA Siti sedang aktif dan terhubung
    if (ws && ws.readyState === WebSocket.OPEN) {
        if (message.action === "ATTACK") {
            ws.send("ATTACK");
        } else if (message.action === "ALERT") {
            ws.send("ALERT");
        }
    } else {
        console.log("[Siti Ekstensi] Pesan ditahan: Siti sedang tidak aktif.");
    }
});