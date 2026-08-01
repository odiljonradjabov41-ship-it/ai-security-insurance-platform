import asyncio
import logging
import httpx
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# --- CONFIG ---
BOT_TOKEN = "8941016368:AAF51yhu-i9p64Z6Vo4pvFhLmBx96RzvTGM"  # @BotFather'dan olingan token
API_URL = "http://127.0.0.1:8080/v1/chat/protected"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "🛡 **AI Security & Insurance Platform Botiga xush kelibsiz!**\n\n"
        "Menga har qanday matn yoki prompt yuboring. Men uni real-vaqt rejimida "
        "AI Guardrail (Scikit-Learn ML) dvigateli orqali xavfsizlikka tekshirib beraman."
    )

@dp.message()
async def analyze_prompt(message: types.Message):
    await message.answer_chat_action("typing")
    user_prompt = message.text

    payload = {
        "user_prompt": user_prompt,
        "api_key": "telegram-user-key"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(API_URL, json=payload, timeout=10.0)
            
            if response.status_code == 200:
                data = response.json()
                text = (
                    "✅ **STATUS: ALLOWED (RUXSAT BERILDI)**\n\n"
                    f"🔹 **AI Risk Score:** `{data['ai_risk_score']}`\n"
                    f"🔹 **Tozalangan Prompt (DLP):** `{data['clean_prompt_sent_to_ai']}`\n\n"
                    f"🤖 **AI Javobi:** {data['ai_response']}"
                )
                await message.answer(text, parse_mode="Markdown")
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 400:
                err_detail = e.response.json().get("detail", {})
                text = (
                    "🛑 **STATUS: BLOCKED (TO'SILDI!)**\n\n"
                    f"⚠️ **Sabab:** {err_detail.get('reason')}\n"
                    f"🎯 **Aniqlash Turi:** {err_detail.get('detection_type')}\n"
                    f"📊 **Xavf Darajasi (Risk Score):** `{err_detail.get('risk_score')}`"
                )
                await message.answer(text, parse_mode="Markdown")
            else:
                await message.answer("⚠️ Tizimda kutilmagan xatolik yuz berdi.")
        except Exception as ex:
            await message.answer("❌ Backend API bilan aloqa o'rnatib bo'lmadi. `main.py` ishlayotganini tekshiring.")

async def main():
    print("🤖 Telegram Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())