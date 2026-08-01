import os
import asyncio
import httpx
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL", "http://127.0.0.1:8080/v1/chat/protected")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "👋 Xush kelibsiz! Men **AI Security Guardrail Bot**man.\n\n"
        "Menga ixtiyoriy matn yuboring, men uni AI Security Engine orqali tekshirib beraman."
    )

@dp.message()
async def process_prompt(message: types.Message):
    user_prompt = message.text
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(API_URL, json={"user_prompt": user_prompt}, timeout=10.0)
            if response.status_code == 200:
                data = response.json()
                await message.answer(
                    f"✅ **STATUS: ALLOWED**\n\n"
                    f"🟢 **Tozalangan Prompt:** `{data['clean_prompt_sent_to_ai']}`\n"
                    f"📊 **Risk Score:** `{data['ai_risk_score']}`\n\n"
                    f"🤖 **AI Javobi:** {data['ai_response']}",
                    parse_mode="Markdown"
                )
            else:
                err_data = response.json().get("detail", {})
                await message.answer(
                    f"🛑 **STATUS: BLOCKED**\n\n"
                    f"⚠️ **Sababi:** {err_data.get('reason')}\n"
                    f"🔍 **Aniqlash turi:** {err_data.get('detection_type')}\n"
                    f"📊 **Risk Score:** `{err_data.get('risk_score')}`",
                    parse_mode="Markdown"
                )
        except Exception as e:
            await message.answer(f"❌ Xatolik yuz berdi: {str(e)}")

async def main():
    print("🤖 Telegram Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())