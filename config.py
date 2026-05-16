import os

# ─── TOKENS (put in .env file) ────────────────────────────
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "YOUR_BOT_TOKEN")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "YOUR_ANTHROPIC_KEY")
OWNER_TELEGRAM_ID = os.getenv("OWNER_TELEGRAM_ID", "YOUR_TELEGRAM_ID")  # You — unlimited free

FREE_DAILY_LIMIT = 5  # Free users: 5 prompts/day

# ─── AI PLATFORMS ─────────────────────────────────────────
AI_PLATFORMS = [
    {"id": "chatgpt",    "name": "ChatGPT",    "emoji": "🟢", "tips": "Use clear role + task + format instructions."},
    {"id": "claude",     "name": "Claude",     "emoji": "🟠", "tips": "Claude loves detailed context and XML tags."},
    {"id": "gemini",     "name": "Gemini",     "emoji": "🔵", "tips": "Gemini works well with step-by-step breakdowns."},
    {"id": "grok",       "name": "Grok",       "emoji": "⚫", "tips": "Grok is great for real-time and technical topics."},
    {"id": "deepseek",   "name": "DeepSeek",   "emoji": "🔷", "tips": "DeepSeek excels at reasoning and math problems."},
    {"id": "perplexity", "name": "Perplexity", "emoji": "🟣", "tips": "Perplexity is best for research with sources."},
    {"id": "gemini",     "name": "Gemini",     "emoji": "🔵", "tips": "Great for multimodal tasks."},
    {"id": "qwen",       "name": "Qwen",       "emoji": "🟡", "tips": "Qwen handles multilingual tasks well."},
    {"id": "mistral",    "name": "Mistral",    "emoji": "🌊", "tips": "Fast and efficient for coding tasks."},
    {"id": "llama",      "name": "Llama",      "emoji": "🦙", "tips": "Open source — good for local deployment prompts."},
]

# ─── PROMPT MODES ─────────────────────────────────────────
PROMPT_MODES = {
    "learn": {
        "questions": {
            "en": [
                "📊 What is your current level? (beginner / intermediate / advanced)",
                "⏰ How many hours per day can you study? (e.g. 1-2 hours)",
                "📅 What is your deadline or target date? (e.g. 3 months)",
                "🎯 What is your specific goal? (e.g. pass exam, get job, build project)",
            ],
            "ru": [
                "📊 Какой у вас уровень? (начинающий / средний / продвинутый)",
                "⏰ Сколько часов в день вы можете учиться? (например 1-2 часа)",
                "📅 Какой у вас дедлайн? (например 3 месяца)",
                "🎯 Какая конкретная цель? (сдать экзамен, найти работу, сделать проект)",
            ],
            "ky": [
                "📊 Деңгээлиң кандай? (баштоочу / орто / жогорку)",
                "⏰ Күнүнө канча саат үйрөнө аласың? (мис. 1-2 саат)",
                "📅 Мөөнөтүң канча? (мис. 3 ай)",
                "🎯 Конкреттүү максатың эмне? (экзамен тапшыруу, жумуш табуу, проект жасоо)",
            ],
        }
    },
    "code": {
        "questions": {
            "en": [
                "💻 What programming language or framework? (e.g. Python, Django, React)",
                "🔧 What exactly do you want to build? (describe the feature or app)",
                "📊 Your coding experience level? (beginner / intermediate / advanced)",
                "📐 Any specific requirements? (e.g. must use REST API, PostgreSQL, etc.)",
            ],
            "ru": [
                "💻 Какой язык или фреймворк? (например Python, Django, React)",
                "🔧 Что именно хотите создать? (опишите функцию или приложение)",
                "📊 Ваш уровень в программировании? (начинающий / средний / продвинутый)",
                "📐 Особые требования? (например REST API, PostgreSQL и т.д.)",
            ],
            "ky": [
                "💻 Кайсы тил же фреймворк? (мис. Python, Django, React)",
                "🔧 Так эмне жасагың келет? (функцияны же колдонмону сүрөттө)",
                "📊 Программалоодогу деңгээлиң? (баштоочу / орто / жогорку)",
                "📐 Атайын талаптар барбы? (мис. REST API, PostgreSQL ж.б.)",
            ],
        }
    },
    "create": {
        "questions": {
            "en": [
                "🎨 What do you want to create? (image, video, music, text, logo...)",
                "🖼️ Describe the style or mood (e.g. realistic, anime, dark, minimalist)",
                "📏 Any size or format requirements? (e.g. 16:9, square, portrait)",
                "✨ Key elements that MUST be in the result?",
            ],
            "ru": [
                "🎨 Что вы хотите создать? (изображение, видео, музыку, текст, логотип...)",
                "🖼️ Опишите стиль или настроение (реалистичный, аниме, тёмный, минималист)",
                "📏 Требования к размеру или формату? (16:9, квадрат, портрет)",
                "✨ Ключевые элементы которые ОБЯЗАТЕЛЬНО должны быть?",
            ],
            "ky": [
                "🎨 Эмне жаратгың келет? (сурет, видео, музыка, текст, логотип...)",
                "🖼️ Стилди же маанайды сүрөттө (реалдуу, аниме, кара, минималист)",
                "📏 Өлчөм же формат талаптары? (16:9, квадрат, портрет)",
                "✨ Милдеттүү болушу керек болгон элементтер?",
            ],
        }
    },
    "research": {
        "questions": {
            "en": [
                "🔬 What topic do you want to research deeply?",
                "📚 What sources do you prefer? (academic, news, technical docs, all)",
                "🎯 What specific question should be answered?",
                "📊 How detailed should the response be? (summary / detailed / exhaustive)",
            ],
            "ru": [
                "🔬 Какую тему хотите исследовать глубоко?",
                "📚 Какие источники предпочитаете? (академические, новости, техдоки, все)",
                "🎯 Какой конкретный вопрос нужно ответить?",
                "📊 Насколько детальным должен быть ответ? (краткий / детальный / исчерпывающий)",
            ],
            "ky": [
                "🔬 Кайсы теманы терең изилдегиң келет?",
                "📚 Кандай булактарды каалайсың? (академиялык, жаңылыктар, техдок, баары)",
                "🎯 Кандай конкреттүү суроого жооп берилиши керек?",
                "📊 Жооп канчалык деталдуу болсун? (кыскача / деталдуу / толук)",
            ],
        }
    },
    "business": {
        "questions": {
            "en": [
                "💼 What type of business content? (marketing copy, strategy, email, pitch...)",
                "👥 Who is your target audience?",
                "🎯 What is the goal of this content? (sell, inform, engage, convert)",
                "🏢 What industry or niche?",
            ],
            "ru": [
                "💼 Какой тип бизнес-контента? (маркетинг, стратегия, email, питч...)",
                "👥 Кто ваша целевая аудитория?",
                "🎯 Какая цель этого контента? (продать, информировать, вовлечь, конвертировать)",
                "🏢 Какая отрасль или ниша?",
            ],
            "ky": [
                "💼 Кандай бизнес контент? (маркетинг, стратегия, email, питч...)",
                "👥 Максаттуу аудиториең ким?",
                "🎯 Бул контенттин максаты эмне? (сатуу, маалымат берүү, тартуу, конверттөө)",
                "🏢 Кайсы тармак же ниша?",
            ],
        }
    },
    "roadmap": {
        "questions": {
            "en": [
                "🗺️ What skill or topic do you want a full roadmap for?",
                "⏰ How many hours per day can you dedicate?",
                "📅 How many weeks/months do you have?",
                "🏆 What is the end goal? (job, certificate, project, mastery)",
            ],
            "ru": [
                "🗺️ Для какого навыка или темы нужен полный роадмап?",
                "⏰ Сколько часов в день готовы уделять?",
                "📅 Сколько недель/месяцев у вас есть?",
                "🏆 Конечная цель? (работа, сертификат, проект, мастерство)",
            ],
            "ky": [
                "🗺️ Кайсы жөндөм же тема боюнча толук жол карта керек?",
                "⏰ Күнүнө канча саат коротуу мүмкүн?",
                "📅 Канча жума/ай бар?",
                "🏆 Акыркы максат? (жумуш, сертификат, проект, чеберчилик)",
            ],
        }
    },
}

# ─── UI TEXTS ─────────────────────────────────────────────
LANGUAGES = {
    "en": {
        "choose_mode": "Choose what you want to do:",
        "mode_learn": "Learn a Topic",
        "mode_code": "Build / Code",
        "mode_create": "Create (Image/Video/Art)",
        "mode_research": "Deep Research",
        "mode_business": "Business Content",
        "mode_roadmap": "Full Roadmap",
        "enter_topic": "What topic or subject?",
        "topic_example": "Example: OSCP certification, Django REST API, Photorealism portrait...",
        "choose_ai": "Which AI will you use this prompt with?",
        "generating": "Crafting your Pro+ prompt",
        "regenerate": "Regenerate",
        "save": "Save",
        "history": "History",
        "menu": "Menu",
        "your_history": "Your Prompt History",
        "no_history": "No prompts yet. Start with /start!",
        "your_stats": "Your Stats",
        "limit_reached": "Daily limit reached!",
        "limit_msg": "Free plan: {} prompts/day",
        "upgrade_msg": "Upgrade to Pro for unlimited prompts",
        "pro_title": "Pro Plan",
        "pro_features": "✅ Unlimited prompts\n✅ Full history\n✅ Roadmap mode\n✅ Priority generation",
        "contact_admin": "Contact",
        "no_data": "No recent prompt data. Please start again.",
        "regenerating": "Regenerating a fresh version",
    },
    "ru": {
        "choose_mode": "Что вы хотите сделать?",
        "mode_learn": "Изучить тему",
        "mode_code": "Создать / Код",
        "mode_create": "Создать (Фото/Видео/Арт)",
        "mode_research": "Глубокое исследование",
        "mode_business": "Бизнес контент",
        "mode_roadmap": "Полный роадмап",
        "enter_topic": "Какая тема или предмет?",
        "topic_example": "Пример: Сертификат OSCP, Django REST API, Фотореалистичный портрет...",
        "choose_ai": "Для какого ИИ создаём промт?",
        "generating": "Создаём ваш Pro+ промт",
        "regenerate": "Перегенерировать",
        "save": "Сохранить",
        "history": "История",
        "menu": "Меню",
        "your_history": "История ваших промтов",
        "no_history": "Промтов пока нет. Начните с /start!",
        "your_stats": "Ваша статистика",
        "limit_reached": "Дневной лимит исчерпан!",
        "limit_msg": "Бесплатный план: {} промтов в день",
        "upgrade_msg": "Обновитесь до Pro для безлимитных промтов",
        "pro_title": "Pro план",
        "pro_features": "✅ Безлимитные промты\n✅ Полная история\n✅ Режим роадмапа\n✅ Приоритетная генерация",
        "contact_admin": "Связаться",
        "no_data": "Нет данных. Пожалуйста, начните заново.",
        "regenerating": "Генерируем новую версию",
    },
    "ky": {
        "choose_mode": "Эмне кылгыңыз келет?",
        "mode_learn": "Тема үйрөнүү",
        "mode_code": "Жаратуу / Код",
        "mode_create": "Жаратуу (Сурет/Видео/Арт)",
        "mode_research": "Терең изилдөө",
        "mode_business": "Бизнес контент",
        "mode_roadmap": "Толук жол карта",
        "enter_topic": "Кандай тема же предмет?",
        "topic_example": "Мисал: OSCP сертификаты, Django REST API, Фотореалдуу портрет...",
        "choose_ai": "Кайсы AI үчүн промт жасайбыз?",
        "generating": "Pro+ промтуңузду жасап жатабыз",
        "regenerate": "Кайта жаз",
        "save": "Сакта",
        "history": "Тарых",
        "menu": "Меню",
        "your_history": "Промт тарыхыңыз",
        "no_history": "Промт жок. /start менен баштаңыз!",
        "your_stats": "Статистикаңыз",
        "limit_reached": "Күндүк лимит бүттү!",
        "limit_msg": "Бекер план: күнүнө {} промт",
        "upgrade_msg": "Чексиз промт үчүн Pro'го өтүңүз",
        "pro_title": "Pro план",
        "pro_features": "✅ Чексиз промттор\n✅ Толук тарых\n✅ Жол карта режими\n✅ Приоритеттүү генерация",
        "contact_admin": "Байланыш",
        "no_data": "Маалымат жок. Кайрадан баштаңыз.",
        "regenerating": "Жаңы версия жасап жатабыз",
    },
}
