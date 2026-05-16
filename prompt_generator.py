import anthropic
from config import ANTHROPIC_API_KEY, AI_PLATFORMS

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

AI_TIPS = {ai["id"]: ai["tips"] for ai in AI_PLATFORMS}

GENERATOR_SYSTEM = """You are an elite prompt engineer with deep expertise in crafting 
high-performance prompts for every major AI platform. 

Your prompts are:
- Specific, detailed, and structured
- Tailored to the exact AI platform's strengths
- Include role, context, task, format, and constraints
- Use the best techniques: chain-of-thought, few-shot, role-play when appropriate
- Written in the same language the user is using

NEVER write generic prompts. Every prompt must be a professional, production-ready 
masterpiece that extracts the absolute best output from the target AI."""


class PromptGenerator:

    async def generate(
        self,
        topic: str,
        mode: str,
        answers: list,
        questions: list,
        ai_platform: str,
        lang: str,
        variation: bool = False
    ) -> str:

        ai_tip = AI_TIPS.get(ai_platform, "")
        qa_pairs = "\n".join([f"Q: {q}\nA: {a}" for q, a in zip(questions, answers)])
        variation_note = "Create a DIFFERENT variation from before — use a different angle or structure." if variation else ""

        lang_instruction = {
            "en": "Write the prompt in English.",
            "ru": "Напиши промт на русском языке.",
            "ky": "Промтту кыргыз тилинде жаз.",
        }.get(lang, "Write the prompt in English.")

        mode_context = {
            "learn": "learning / studying / mastering a topic",
            "code": "software development / coding / building an app",
            "create": "creative generation (image, video, art, music)",
            "research": "deep research / analysis / fact-finding",
            "business": "business content / marketing / strategy",
            "roadmap": "creating a complete structured learning roadmap",
        }.get(mode, "general task")

        user_message = f"""Create a Pro+ prompt for {ai_platform.upper()} AI.

TOPIC: {topic}
MODE: {mode_context}
TARGET AI: {ai_platform}
AI TIP: {ai_tip}

USER'S DETAILS:
{qa_pairs if qa_pairs else "No additional details provided."}

{variation_note}

REQUIREMENTS:
1. Start with a clear ROLE assignment for the AI
2. Include full CONTEXT about the user's situation
3. Give a precise TASK with all necessary details
4. Specify the OUTPUT FORMAT (structure, length, style)
5. Add CONSTRAINTS and quality standards
6. If relevant, add EXAMPLES or few-shot demonstrations
7. For learning/roadmap modes: include schedule structure
8. For creative modes: include technical specifications
9. Make it feel like it was written by a $500/hour prompt engineer
10. {lang_instruction}

Output ONLY the ready-to-use prompt — no explanations, no meta-commentary."""

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            system=GENERATOR_SYSTEM,
            messages=[{"role": "user", "content": user_message}]
        )

        return response.content[0].text.strip()
