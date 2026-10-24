import requests
import time
from datetime import datetime

# ================= AYARLAR =================
TELEGRAM_TOKEN = "8666323841:AAH_3dB8R22N58J4fZ1JyjhkLyb120.0.0.0"  # (Token'ını buraya eksiksiz koyduğundan emin ol)
TELEGRAM_CHAT_ID = "616891924"

TARGET_URL = "https://stuttgart.konsentas.de/form/3/?signup_new=1"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7"
}

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print("Telegram bildirimi gönderilemedi:", e)

def check_appointment():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        response = requests.get(TARGET_URL, headers=HEADERS, timeout=15)
        
        if response.status_code == 200:
            html = response.text.lower()
            
            # Konsentas sisteminde randevu açıldığında görünen ifadeler
            has_slots = ("step-2" in html) or ("termin auswählen" in html) or ("datum" in html and "uhrzeit" in html)
            
            if has_slots:
                msg = f"🎉 [STUTTGART RANDEVU] Boş randevu açıldı!\n\nHemen girip al:\n{TARGET_URL}"
                print(f"[{now}] GERÇEK BOŞ RANDEVU BULUNDU!")
                send_telegram(msg)
                return True
            else:
                print(f"[{now}] Kontrol edildi: Henüz boş randevu yok.")
        else:
            print(f"[{now}] Sayfa yanıt vermedi. Hata kodu: {response.status_code}")
            
    except Exception as e:
        print(f"[{now}] Bağlantı hatası oluştu: {e}")
        
    return False

if __name__ == "__main__":
    print("Stuttgart Randevu Takip Botu Bulutta Başlatıldı...")
    check_appointment()
