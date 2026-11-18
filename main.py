import os
import time
import requests

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
raw_chat_ids = (
    os.environ.get("TELEGRAM_CHAT_ID") or ""
)  # ป้องกัน Error กรณีค่าเป็น None
CHAT_IDS = [cid.strip() for cid in raw_chat_ids.split(",") if cid.strip()]

IMAGE_PATH = "images/491529.jpg"

MESSAGE_TEXT = """📢 ประกาศแจ้งสมาชิก COMPASS ทุกท่าน

ขณะนี้ทาง COMPASS ได้เปิดห้อง Signal ใหม่ เพื่อยกระดับการให้บริการและจัดระบบสัญญาณเทรดให้เป็นสัดส่วนตามระดับสมาชิก

สมาชิกทุกท่านที่ประสงค์จะเข้าร่วมห้อง Signal ใหม่ สามารถแจ้งความประสงค์กับทาง Admin พร้อมแจ้ง เลข CID ของบัญชีโบรกเกอร์ OTG เพื่อดำเนินการตรวจสอบและเพิ่มสิทธิ์เข้าห้องได้เลยครับ

📊 ระดับห้อง Signal ใหม่
🔹 COMPASS START — 100 USD
🔹 COMPASS PRO — 500 USD
🔹 COMPASS ELITE — 1,000 USD

สิทธิ์การเข้าถึงห้อง Signal
✅ สมาชิกระดับ ELITE (1,000 USD) เข้าถึงได้ครบทุกห้อง (START, PRO และ ELITE)
✅ สมาชิกระดับ PRO (500 USD) เข้าถึงได้ 2 ห้อง (START และ PRO)
✅ สมาชิกระดับ START (100 USD) เข้าถึงห้อง START ได้

📌 ข้อควรทราบและกำหนดการสำคัญ
1. ห้อง Signal ใหม่จะเริ่มส่งสัญญาณตั้งแต่วันที่ 1 ธันวาคม 2569 (1/12/69) เป็นต้นไป
2. ห้อง Signal เดิมจะยุติการส่งสัญญาณตั้งแต่วันที่เริ่มใช้งานห้องใหม่เป็นต้นไป
3. สำหรับสมาชิกที่ยังไม่มีบัญชีโบรกเกอร์ OTG สามารถติดต่อ Admin เพื่อขอรายละเอียดและคำแนะนำในการเปิดบัญชีได้

📩 วิธีเข้าร่วมห้อง Signal ใหม่
เพียงแจ้งความประสงค์กับทาง Admin พร้อมส่งเลข CID ของบัญชี OTG เพื่อดำเนินการตรวจสอบสิทธิ์และเพิ่มเข้าห้องตามระดับสมาชิก

ขอบคุณสมาชิก COMPASS ทุกท่านที่ไว้วางใจและเติบโตไปด้วยกัน

COMPASS — เติบโตอย่างมีระบบ ก้าวไปด้วยกันอย่างยั่งยืน"""


def send_telegram_announcement():
  if not TELEGRAM_TOKEN or not CHAT_IDS:
    print("❌ ไม่พบค่า TELEGRAM_TOKEN หรือ TELEGRAM_CHAT_ID ใน Secrets")
    return

  if not os.path.exists(IMAGE_PATH):
    print(f"❌ ไม่พบไฟล์รูปภาพที่ '{IMAGE_PATH}'")
    return

  base_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

  for chat_id in CHAT_IDS:
    print(f"⏳ กำลังส่งประกาศไปยังห้อง: {chat_id} ...")
    try:
      # 1. ส่งรูปภาพ
      with open(IMAGE_PATH, "rb") as image_file:
        photo_res = requests.post(
            f"{base_url}/sendPhoto",
            files={"photo": image_file},
            data={"chat_id": chat_id},
        ).json()

      if not photo_res.get("ok"):
        print(f"❌ [{chat_id}] ส่งรูปไม่สำเร็จ: {photo_res.get('description')}")
        continue  # ข้ามไปส่งห้องถัดไปทันที ไม่หยุดทำงานทั้งระบบ

      # 2. ส่งข้อความ
      msg_res = requests.post(
          f"{base_url}/sendMessage",
          data={"chat_id": chat_id, "text": MESSAGE_TEXT},
      ).json()

      if msg_res.get("ok"):
        print(f"✅ [{chat_id}] ส่งรูปภาพและประกาศสำเร็จ!")
      else:
        print(
            f"❌ [{chat_id}] ส่งข้อความไม่สำเร็จ: {msg_res.get('description')}"
        )

      # หน่วงเวลา 1 วินาที ป้องกัน Telegram บล็อก Rate Limit กรณีมีหลายห้อง
      time.sleep(1)

    except Exception as e:
      print(f"❌ [{chat_id}] เกิดข้อผิดพลาด: {e}")


if __name__ == "__main__":
  send_telegram_announcement()
