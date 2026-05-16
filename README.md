# 🤖 PromptMaster Bot — Орнотуу Колдонмосу

## Файлдар структурасы
```
promptmaster/
├── bot.py              ← Негизги бот
├── config.py           ← Орнотуулар жана тилдер
├── prompt_generator.py ← Claude API менен промт жасоо
├── database.py         ← SQLite маалымат базасы
├── requirements.txt    ← Зарыл пакеттер
├── .env.example        ← Токен шаблону
└── README.md           ← Ушул файл
```

---

## 🚀 Баштоо — Кадам-кадам

### 1. Telegram Bot жаса
1. Telegramда **@BotFather** ач
2. `/newbot` жаз
3. Ботуңа ат бер: `PromptMaster`
4. Username бер: `mypromptmaster_bot`
5. **TOKEN** алдың → сакта!

### 2. Anthropic API ал
1. **https://console.anthropic.com** сайтына кир
2. "API Keys" → "Create Key"
3. **ANTHROPIC_API_KEY** алдың → сакта!

### 3. Өз Telegram ID алуу
1. Telegramда **@userinfobot** ач
2. `/start` жаз
3. **ID** санды сакта (мис: `123456789`)

### 4. Серверге орното (Linux/Mac)
```bash
# Репозиторий клондо же файлдарды жүктө
cd promptmaster

# Virtual environment жаса
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Пакеттерди орното
pip install -r requirements.txt

# .env файл жаса
cp .env.example .env
nano .env  # Токендерди жаз
```

### 5. .env файлды толтур
```
TELEGRAM_TOKEN=7234567890:AAF...
ANTHROPIC_API_KEY=sk-ant-...
OWNER_TELEGRAM_ID=123456789
```

### 6. Ботту иштет
```bash
python bot.py
```

---

## ☁️ Серверге Deploy (VPS)

### Systemd сервис катары (Ubuntu)
```bash
sudo nano /etc/systemd/system/promptmaster.service
```

```ini
[Unit]
Description=PromptMaster Telegram Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/promptmaster
Environment=PATH=/home/ubuntu/promptmaster/venv/bin
ExecStart=/home/ubuntu/promptmaster/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable promptmaster
sudo systemctl start promptmaster
sudo systemctl status promptmaster
```

---

## 📊 Функциялар

| Функция | Free | Pro | Owner |
|---------|------|-----|-------|
| Промт/күн | 5 | Чексиз | Чексиз |
| Тарых | ✅ | ✅ | ✅ |
| Жол карта режими | ✅ | ✅ | ✅ |
| Баары | ✅ | ✅ | ✅ |

---

## 🌐 Колдоого алынган AI платформалар
- 🟢 ChatGPT
- 🟠 Claude
- 🔵 Gemini
- ⚫ Grok
- 🔷 DeepSeek
- 🟣 Perplexity
- 🟡 Qwen
- 🌊 Mistral
- 🦙 Llama

## 🌍 Тилдер
- 🇬🇧 English
- 🇷🇺 Русский
- 🇰🇬 Кыргызча

---

## 💰 Монетизация
Pro план активдештирүү үчүн `database.py` ичинде:
```python
db.set_plan(user_id, "pro")
```
Stripe же Telegram Stars менен интеграция кошсо болот.

---

*PromptMaster Bot — Claude AI менен иштейт*
