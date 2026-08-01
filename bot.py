import os
import logging
import httpx
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = "http://127.0.0.1:8080/v1/chat/protected"

logging.basicConfig(level=logging.INFO)

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN topilmadi! .env faylini tekshiring.")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "👋 **InsurTech AI Security Botiga xush kelibsiz!**\n\n"
        "Menga sug'urta bo'yicha savollaringizni yoki ma'lumotlaringizni yuboring. "
        "Tizim har bir so'rovni kiberxavfsizlik va DLP süzgichidan o'tkazadi."
    )

@dp.message()
async def handle_message(message: types.Message):
    user_text = message.text

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.post(API_URL, json={"user_prompt": user_text})
            
            # JSON formatida javob kelganini tekshirish
            try:
                data = response.json()
            except Exception:
                await message.answer(f"⚠️ Serverdan kutilmagan javob keldi (Status: {response.status_code}). Server loglarini tekshiring.")
                return

            # Agar API 200 (Success) qaytarsa
            if response.status_code == 200:
                clean_prompt = data.get("clean_prompt_sent_to_ai", user_text)
                risk_score = data.get("ai_risk_score", 0.0)
                ai_resp = data.get("ai_response", "")
                
                await message.answer(
                    f"✅ **So'rov Xavfsiz deb Topildi**\n\n"
                    f"🛡️ **DLP Maskalangan matn:**\n`{clean_prompt}`\n\n"
                    f"📊 **Risk Score:** `{risk_score}`\n\n"
                    f"🤖 **AI Javobi:** {ai_resp}",
                    parse_mode="Markdown"
                )
            
            # Agar API 400 (BLOCKED) qaytarsa
            elif response.status_code == 400:
                detail = data.get("detail", {})
                reason = detail.get("reason", "Xavfsizlik siyosati buzildi")
                detection = detail.get("detection_type", "Guardrail Engine")
                risk = detail.get("risk_score", 1.0)
                
                await message.answer(
                    f"🚨 **SO'ROV BLOKLANDI! (THREAT DETECTED)**\n\n"
                    f"❌ **Sabab:** {reason}\n"
                    f"🔍 **Aniqladi:** {detection}\n"
                    f"⚠️ **Xavf Darajasi:** {risk}\n\n"
                    f"_Ushbu hodisa kiberxavfsizlik jurnaliga (Dashboard) qayd etildi._",
                    parse_mode="Markdown"
                )
            else:
                await message.answer(f"⚠️ Noma'lum server javobi: Status {response.status_code}")

        except httpx.RequestError:
            await message.answer("❌ **Xatolik:** Security API Serveriga (`main.py`) ulanib bo'lmadi. `main.py` ishlayotganini tekshiring!")
        except Exception as ex:
            await message.answer(f"❌ Kutilmagan xatolik: {str(ex)}")

if __name__ == "__main__":
    import asyncio
    print("🤖 InsurTech AI Guardrail Bot ishga tushdi...")
    asyncio.run(dp.start_polling(bot))