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
        if (ws) ws.close(); 
    };
}

// Jalankan pencarian koneksi pertama kali
connectWebSocket();

// Mendengarkan ketukan/laporan dari content.js
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (ws && ws.readyState === WebSocket.OPEN) {
        if (message.action === "ATTACK" || message.action === "ALERT") {
            // Gunakan sender.tab agar indeks tab yang dikirim 100% akurat
            if (sender && sender.tab) {
                chrome.tabs.query({ windowId: sender.tab.windowId }, (tabs) => {
                    const totalTabs = tabs ? tabs.length : 1;
                    const activeTabIndex = sender.tab.index; // Indeks tab persis tempat user scroll

                    const payload = JSON.stringify({
                        action: message.action,
                        totalTabs: totalTabs,
                        activeTabIndex: activeTabIndex
                    });

                    ws.send(payload);
                });
            } else {
                // Fallback jika pesan dikirim bukan dari konteks tab biasa
                chrome.tabs.query({ active: true, lastFocusedWindow: true }, (tabs) => {
                    if (tabs && tabs.length > 0) {
                        const payload = JSON.stringify({
                            action: message.action,
                            totalTabs: tabs.length,
                            activeTabIndex: tabs[0].index
                        });
                        ws.send(payload);
                    }
                });
            }
        }
    } else {
        console.log("[Siti Ekstensi] Pesan ditahan: Siti sedang tidak aktif.");
    }
});