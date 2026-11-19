import os
import requests

# ดึงค่าจาก Environment Variables (GitHub Secrets)
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
IMAGE_PATH = '491529.jpg'  # อ้างอิงชื่อไฟล์ใน Repo โดยตรง

def send_telegram_photo():
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Error: ไม่พบค่า TELEGRAM_TOKEN หรือ TELEGRAM_CHAT_ID ใน Secrets")
        return

    if not os.path.exists(IMAGE_PATH):
        print(f"Error: ไม่พบไฟล์รูปภาพ {IMAGE_PATH} ใน Repository")
        return

    caption = """📢 *ประกาศแจ้งสมาชิก COMPASS ทุกท่าน*

ทาง COMPASS ได้เปิดห้อง Signal ใหม่ เพื่อยกระดับการให้บริการและจัดระบบสัญญาณเทรดตามระดับสมาชิก

สมาชิกที่ประสงค์เข้าร่วม สามารถแจ้งความประสงค์กับ Admin พร้อมส่ง *เลข CID บัญชีโบรกเกอร์ OTG* เพื่อตรวจสอบและเพิ่มสิทธิ์เข้าห้องได้เลยครับ

📊 *ระดับห้อง Signal ใหม่*
🔹 COMPASS START — 100 USD
🔹 COMPASS PRO — 500 USD
🔹 COMPASS ELITE — 1,000 USD

*สิทธิ์การเข้าถึงห้อง Signal*
✅ ELITE (1,000 USD) เข้าได้ทุกห้อง (START, PRO, ELITE)
✅ PRO (500 USD) เข้าได้ 2 ห้อง (START, PRO)
✅ START (100 USD) เข้าได้ห้อง START

📌 *ข้อควรทราบและกำหนดการ*
1. ห้อง Signal ใหม่ เริ่มส่งสัญญาณวันที่ 1 ธ.ค. 2569 (1/12/69) เป็นต้นไป
2. ห้อง Signal เดิม จะยุติการส่งสัญญาณตั้งแต่วันที่เริ่มใช้งานห้องใหม่
3. หากยังไม่มีบัญชี OTG สามารถติดต่อ Admin เพื่อขอคำแนะนำการเปิดบัญชีได้

📩 *วิธีเข้าร่วม:* แจ้ง Admin พร้อมส่งเลข CID บัญชี OTG เพื่อรับสิทธิ์ตามระดับสมาชิก

ขอบคุณทุกท่านที่ไว้วางใจและเติบโตไปด้วยกัน
*COMPASS — เติบโตอย่างมีระบบ ก้าวไปด้วยกันอย่างยั่งยืน*"""

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "caption": caption,
        "parse_mode": "Markdown"
    }

    try:
        with open(IMAGE_PATH, 'rb') as photo_file:
            response = requests.post(url, data=payload, files={'photo': photo_file})
            response.raise_for_status()
            print("ส่งรูปภาพและประกาศสำเร็จเรียบร้อย!")
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err} - รายละเอียด: {response.text}")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    send_telegram_photo()
