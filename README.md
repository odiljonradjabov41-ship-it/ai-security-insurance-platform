# 🛡️ AI Security & Insurance Platform (MVP)

> **Real-Time Machine Learning Guardrail & Threat Intelligence Engine for Enterprise AI Applications.**

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML%20Engine-F7931E?style=flat&logo=scikit-learn)
![Telegram Bot](https://img.shields.io/badge/Telegram--Bot-Active-26A5E4?style=flat&logo=telegram)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 📌 Loyiha Haqida

Ushbu platforma Sun'iy Intellekt (LLM) ilovalarini kiberxavfsizlik tahdidlaridan (Prompt Injection, Jailbreak attacks, Data Leakage) real-vaqt rejimida himoya qilish uchun mo'ljallangan **gibrid AI Guardrail mikroxizmati**dir. 

Tizim ikki bosqichli tekshiruv va maxfiy ma'lumotlarni maskirovka qilish (DLP) orqali AI ilovalariga yuborilayotgan so'rovlar xavfsizligini 99% aniqlikda ta'minlaydi.

---

## 🌟 Asosiy Imkoniyatlar

- ⚔️ **Hybrid Threat Detection Engine:**
  - **1-Daraja (Statik Pattern Matcher):** Regex orqali tezkor va ma'lum xakerlik kalit so'zlarini tutib qolish.
  - **2-Daraja (Dinamik ML Classifier):** `Scikit-Learn (TF-IDF + Naive Bayes)` modelidan foydalanib, matn niyatini (*semantic intent*) tushunish va murakkab Jailbreak hujumlarini bloklash.
- 🔐 **Data Loss Prevention (DLP):** Kredit karta raqamlari hamda Email manzillarini AI modeliga ketishidan oldin avtomatik yashirish (Data Masking).
- 🤖 **Telegram Bot Interface (`aiogram`):** Foydalanuvchilar va testerlar uchun qulay interaktiv test platformasi.
- 📊 **Real-Time Web Analytics Dashboard:** Tizimga qilingan hujumlar, qabul qilingan so'rovlar va xavf ballarini (`risk_score`) real vaqt rejimida kuzatib borish uchun visual panel (`/dashboard`).

---

## 📐 Tizim Arxitekturasi