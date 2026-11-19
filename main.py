import os
import requests

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
raw_chat_ids = os.environ.get("TELEGRAM_CHAT_ID") or ""
CHAT_IDS = [cid.strip() for cid in raw_chat_ids.split(",") if cid.strip()]

IMAGE_PATH = "491527.jpg"

CAPTION_TEXT = """🧭✨ สิทธิประโยชน์ที่สมาชิก COMPASS จะได้รับ

เพราะเราเชื่อว่าการเทรดที่ดี ต้องมีทั้งแนวทาง กลยุทธ์ และการบริหารความเสี่ยงที่เหมาะสม

📊 เลือกระดับ Signal Room ให้เหมาะกับพอร์ตของคุณ

🔹 COMPASS START — 100 USD
เทรด M5 เน้นการเทรดระยะสั้น

🔹 COMPASS PRO — 500 USD
จุดเข้าตามแผน เป้าหมาย 1,000 จุด

🔹 COMPASS ELITE — 1,000 USD
จุดเข้าตามโครงสร้างตลาด พร้อมแนวทางวางแผนการเทรด

👑 COMPASS — เข็มทิศเทรดเดอร์
เติบโตไปด้วยกัน เรียนรู้และพัฒนาทักษะอย่างเป็นระบบ

📩 สนใจเข้าร่วม ติดต่อสอบถามรายละเอียดเพิ่มเติมกับ Admin ได้เลย

⚠️ เงื่อนไขเป็นไปตามที่บริษัทกำหนด
การลงทุนมีความเสี่ยง ผู้ลงทุนควรศึกษาข้อมูลและทำความเข้าใจก่อนตัดสินใจ ผลกำไรไม่สามารถรับประกันได้"""


def send_telegram_photo():
  if not TELEGRAM_TOKEN or not CHAT_IDS:
    raise ValueError(
        "❌ ไม่พบค่า TELEGRAM_TOKEN หรือ TELEGRAM_CHAT_ID ใน GitHub Secrets"
    )

  if not os.path.exists(IMAGE_PATH):
    raise FileNotFoundError(f"❌ ไม่พบไฟล์รูปภาพ '{IMAGE_PATH}' ใน Repository")

  url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
  failed_chats = []

  for chat_id in CHAT_IDS:
    # เปิดไฟล์ใหม่ทุกรอบของลูป เพื่อให้ pointer เริ่มอ่านจากต้นไฟล์เสมอ
    with open(IMAGE_PATH, "rb") as image_file:
      files = {"photo": image_file}
      data = {"chat_id": chat_id, "caption": CAPTION_TEXT}

      response = requests.post(url, files=files, data=data)
      result = response.json()

      if result.get("ok"):
        print(f"✅ [{chat_id}] ส่งรูปภาพและข้อความสำเร็จ!")
      else:
        err_msg = result.get("description")
        print(f"❌ [{chat_id}] ส่งไม่สำเร็จ: {err_msg}")
        failed_chats.append(f"{chat_id} ({err_msg})")

  # ถ้ามีห้องไหนส่งไม่ผ่าน ให้แจ้ง Error ตอนจบเพื่อให้ GitHub Actions ขึ้นสีแดง
  if failed_chats:
    raise RuntimeError(
        f"❌ ส่งไม่สำเร็จ {len(failed_chats)} ห้อง: {', '.join(failed_chats)}"
    )


if __name__ == "__main__":
  send_telegram_photo()
