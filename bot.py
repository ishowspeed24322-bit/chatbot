import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters, ConversationHandler
)
from anthropic import Anthropic
from database import Database
from prompt_generator import PromptGenerator
from config import (
    TELEGRAM_TOKEN, FREE_DAILY_LIMIT, OWNER_TELEGRAM_ID,
    LANGUAGES, AI_PLATFORMS, PROMPT_MODES
)

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Conversation states
(
    CHOOSING_LANG, CHOOSING_MODE, ENTERING_TOPIC,
    ASKING_DETAILS, CHOOSING_AI, CONFIRMING
) = range(6)

db = Database()
generator = PromptGenerator()


# ─── /start ───────────────────────────────────────────────
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db.ensure_user(user.id, user.username or user.first_name)

    is_owner = str(user.id) == str(OWNER_TELEGRAM_ID)
    plan = "owner" if is_owner else db.get_plan(user.id)

    keyboard = [
        [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
         InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton("🇰🇬 Кыргызча", callback_data="lang_ky")],
    ]
    await update.message.reply_text(
        "👋 *PromptMaster Bot*\n\n"
        "Каалаган тема боюнча каалаган AI үчүн\n"
        "Pro+ промт жазып берем!\n\n"
        "Тилди тандаңыз / Choose language:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return CHOOSING_LANG


# ─── Language selection ────────────────────────────────────
async def choose_language(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.replace("lang_", "")
    ctx.user_data["lang"] = lang
    db.set_language(query.from_user.id, lang)
    await show_mode_menu(query, lang)
    return CHOOSING_MODE


async def show_mode_menu(query, lang):
    texts = LANGUAGES[lang]
    keyboard = [
        [InlineKeyboardButton(f"🎓 {texts['mode_learn']}", callback_data="mode_learn")],
        [InlineKeyboardButton(f"💻 {texts['mode_code']}", callback_data="mode_code")],
        [InlineKeyboardButton(f"🎨 {texts['mode_create']}", callback_data="mode_create")],
        [InlineKeyboardButton(f"🔬 {texts['mode_research']}", callback_data="mode_research")],
        [InlineKeyboardButton(f"💼 {texts['mode_business']}", callback_data="mode_business")],
        [InlineKeyboardButton(f"📦 {texts['mode_roadmap']}", callback_data="mode_roadmap")],
    ]
    await query.edit_message_text(
        f"*{texts['choose_mode']}*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ─── Mode selection ────────────────────────────────────────
async def choose_mode(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    mode = query.data.replace("mode_", "")
    ctx.user_data["mode"] = mode
    lang = ctx.user_data.get("lang", "en")
    texts = LANGUAGES[lang]

    await query.edit_message_text(
        f"*{texts['enter_topic']}*\n\n"
        f"_{texts['topic_example']}_",
        parse_mode="Markdown"
    )
    return ENTERING_TOPIC


# ─── Topic entered ─────────────────────────────────────────
async def enter_topic(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    topic = update.message.text.strip()
    ctx.user_data["topic"] = topic
    lang = ctx.user_data.get("lang", "en")
    texts = LANGUAGES[lang]
    mode = ctx.user_data.get("mode", "learn")

    # Ask clarifying questions based on mode
    questions = PROMPT_MODES[mode]["questions"][lang]
    ctx.user_data["questions"] = questions
    ctx.user_data["answers"] = []
    ctx.user_data["q_index"] = 0

    await update.message.reply_text(
        f"✅ *{topic}*\n\n{questions[0]}",
        parse_mode="Markdown"
    )
    return ASKING_DETAILS


# ─── Collecting answers ────────────────────────────────────
async def collect_answers(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    answer = update.message.text.strip()
    ctx.user_data["answers"].append(answer)
    idx = ctx.user_data["q_index"] + 1
    ctx.user_data["q_index"] = idx
    questions = ctx.user_data["questions"]

    if idx < len(questions):
        await update.message.reply_text(questions[idx], parse_mode="Markdown")
        return ASKING_DETAILS

    # All questions answered — choose AI
    lang = ctx.user_data.get("lang", "en")
    texts = LANGUAGES[lang]
    keyboard = []
    row = []
    for i, ai in enumerate(AI_PLATFORMS):
        row.append(InlineKeyboardButton(ai["emoji"] + " " + ai["name"], callback_data=f"ai_{ai['id']}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    await update.message.reply_text(
        f"*{texts['choose_ai']}*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return CHOOSING_AI


# ─── AI selected — generate prompt ────────────────────────
async def choose_ai(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    ai_id = query.data.replace("ai_", "")
    ctx.user_data["ai"] = ai_id
    user_id = query.from_user.id
    lang = ctx.user_data.get("lang", "en")
    texts = LANGUAGES[lang]

    # Check limits
    is_owner = str(user_id) == str(OWNER_TELEGRAM_ID)
    plan = db.get_plan(user_id)
    if not is_owner and plan == "free":
        used = db.get_daily_usage(user_id)
        if used >= FREE_DAILY_LIMIT:
            keyboard = [[InlineKeyboardButton("⭐ Upgrade to Pro", callback_data="upgrade")]]
            await query.edit_message_text(
                f"*{texts['limit_reached']}*\n\n"
                f"{texts['limit_msg'].format(FREE_DAILY_LIMIT)}\n\n"
                f"_{texts['upgrade_msg']}_",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return ConversationHandler.END

    await query.edit_message_text(f"⚡ {texts['generating']}...")

    # Generate prompt
    result = await generator.generate(
        topic=ctx.user_data["topic"],
        mode=ctx.user_data["mode"],
        answers=ctx.user_data["answers"],
        questions=ctx.user_data["questions"],
        ai_platform=ai_id,
        lang=lang
    )

    # Save to DB
    if not is_owner and plan == "free":
        db.increment_usage(user_id)
    db.save_prompt(user_id, ctx.user_data["topic"], ai_id, ctx.user_data["mode"], result)

    # Send result
    ai_name = next((a["name"] for a in AI_PLATFORMS if a["id"] == ai_id), ai_id)
    header = f"✅ *Pro+ Prompt for {ai_name}*\n{'─'*30}\n\n"

    keyboard = [
        [InlineKeyboardButton(f"🔄 {texts['regenerate']}", callback_data="regenerate"),
         InlineKeyboardButton(f"💾 {texts['save']}", callback_data="save_last")],
        [InlineKeyboardButton(f"📚 {texts['history']}", callback_data="history"),
         InlineKeyboardButton(f"🏠 {texts['menu']}", callback_data="main_menu")],
    ]

    # Telegram message limit — split if needed
    full_text = header + result
    if len(full_text) > 4000:
        await query.edit_message_text(header, parse_mode="Markdown")
        await query.message.reply_text(result, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await query.edit_message_text(full_text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    return ConversationHandler.END


# ─── Regenerate ────────────────────────────────────────────
async def regenerate(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = ctx.user_data.get("lang", "en")
    texts = LANGUAGES[lang]

    if not ctx.user_data.get("topic"):
        await query.edit_message_text(texts["no_data"])
        return

    await query.edit_message_text(f"🔄 {texts['regenerating']}...")
    result = await generator.generate(
        topic=ctx.user_data["topic"],
        mode=ctx.user_data.get("mode", "learn"),
        answers=ctx.user_data.get("answers", []),
        questions=ctx.user_data.get("questions", []),
        ai_platform=ctx.user_data.get("ai", "chatgpt"),
        lang=lang,
        variation=True
    )
    ai_name = next((a["name"] for a in AI_PLATFORMS if a["id"] == ctx.user_data.get("ai")), "AI")
    keyboard = [
        [InlineKeyboardButton(f"🔄 {texts['regenerate']}", callback_data="regenerate"),
         InlineKeyboardButton(f"🏠 {texts['menu']}", callback_data="main_menu")],
    ]
    await query.edit_message_text(
        f"✅ *Pro+ Prompt for {ai_name}* (v2)\n{'─'*30}\n\n{result}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ─── History ───────────────────────────────────────────────
async def show_history(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = ctx.user_data.get("lang", db.get_language(user_id) or "en")
    texts = LANGUAGES[lang]

    history = db.get_history(user_id, limit=5)
    if not history:
        await query.edit_message_text(
            texts["no_history"],
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"🏠 {texts['menu']}", callback_data="main_menu")]])
        )
        return

    msg = f"*📚 {texts['your_history']}*\n\n"
    for i, row in enumerate(history, 1):
        msg += f"{i}. *{row['topic']}* → {row['ai_platform']}\n"
        msg += f"   📅 {row['created_at'][:10]}\n\n"

    keyboard = [[InlineKeyboardButton(f"🏠 {texts['menu']}", callback_data="main_menu")]]
    await query.edit_message_text(msg, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))


# ─── Stats (/stats) ────────────────────────────────────────
async def stats(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = db.get_language(user_id) or "en"
    texts = LANGUAGES[lang]
    is_owner = str(user_id) == str(OWNER_TELEGRAM_ID)
    plan = "owner" if is_owner else db.get_plan(user_id)
    used = db.get_daily_usage(user_id)
    total = db.get_total_prompts(user_id)

    plan_label = "👑 Owner (Unlimited)" if is_owner else ("⭐ Pro" if plan == "pro" else f"Free ({FREE_DAILY_LIMIT - used} left today)")
    msg = (
        f"📊 *{texts['your_stats']}*\n\n"
        f"Plan: {plan_label}\n"
        f"Today: {used} prompts\n"
        f"Total: {total} prompts\n"
    )
    if is_owner:
        total_users = db.get_total_users()
        msg += f"\n👥 Total users: {total_users}"
    await update.message.reply_text(msg, parse_mode="Markdown")


# ─── Main menu callback ────────────────────────────────────
async def main_menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = ctx.user_data.get("lang", "en")
    await show_mode_menu(query, lang)
    return CHOOSING_MODE


# ─── Upgrade callback ──────────────────────────────────────
async def upgrade(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = ctx.user_data.get("lang", "en")
    texts = LANGUAGES[lang]
    await query.edit_message_text(
        f"⭐ *{texts['pro_title']}*\n\n"
        f"{texts['pro_features']}\n\n"
        f"💳 {texts['contact_admin']}: @YOUR_USERNAME",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"🏠 {texts['menu']}", callback_data="main_menu")]])
    )


# ─── /help ────────────────────────────────────────────────
async def help_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *PromptMaster Bot*\n\n"
        "Commands:\n"
        "/start — Start / Main menu\n"
        "/stats — Your stats\n"
        "/help — Help\n\n"
        "How it works:\n"
        "1. Choose mode (Learn/Code/Create...)\n"
        "2. Enter your topic\n"
        "3. Answer a few questions\n"
        "4. Choose AI platform\n"
        "5. Get your Pro+ Prompt! ✅",
        parse_mode="Markdown"
    )


# ─── Main ─────────────────────────────────────────────────
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CallbackQueryHandler(main_menu, pattern="^main_menu$"),
        ],
        states={
            CHOOSING_LANG: [CallbackQueryHandler(choose_language, pattern="^lang_")],
            CHOOSING_MODE: [CallbackQueryHandler(choose_mode, pattern="^mode_")],
            ENTERING_TOPIC: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_topic)],
            ASKING_DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, collect_answers)],
            CHOOSING_AI: [CallbackQueryHandler(choose_ai, pattern="^ai_")],
        },
        fallbacks=[CommandHandler("start", start)],
        allow_reentry=True,
    )

    app.add_handler(conv)
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CallbackQueryHandler(regenerate, pattern="^regenerate$"))
    app.add_handler(CallbackQueryHandler(show_history, pattern="^history$"))
    app.add_handler(CallbackQueryHandler(upgrade, pattern="^upgrade$"))

    logger.info("🚀 PromptMaster Bot started!")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
