import streamlit as st

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ClearCare · NHS Pre-Appointment",
    page_icon="🩺",
    layout="centered"
)

# ── Session state defaults ────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "language"   # start on page 1
if "selected_lang" not in st.session_state:
    st.session_state.selected_lang = None

# ══════════════════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════════════════

LANGUAGES = [
    {"code": "en", "flag": "🇬🇧", "name": "English",    "native": "English"},
    {"code": "fr", "flag": "🇫🇷", "name": "French",     "native": "Français"},
    {"code": "ar", "flag": "🇸🇦", "name": "Arabic",     "native": "العربية"},
    {"code": "ur", "flag": "🇵🇰", "name": "Urdu",       "native": "اردو"},
    {"code": "hi", "flag": "🇮🇳", "name": "Hindi",      "native": "हिन्दी"},
    {"code": "pl", "flag": "🇵🇱", "name": "Polish",     "native": "Polski"},
    {"code": "ro", "flag": "🇷🇴", "name": "Romanian",   "native": "Română"},
    {"code": "bn", "flag": "🇧🇩", "name": "Bengali",    "native": "বাংলা"},
    {"code": "zh", "flag": "🇨🇳", "name": "Chinese",    "native": "中文"},
    {"code": "sp", "flag": "🇪🇸", "name": "Spanish",    "native": "español"},
]

LANGUAGE_CONTENT = {
    "en": {
        "flag": "🇬🇧", "name": "English", "direction": "ltr",
        "greeting": "Hello! Welcome to ClearCare 👋",
        "subtitle": "Your NHS Pre-Appointment Assistant",
        "intro": "Before your appointment, I'd like to understand how you're feeling. This will help your GP prepare for your visit.",
        "what_to_expect": "What to expect:",
        "steps": [
            "💬 Answer a few simple questions about your symptoms",
            "📷 Optionally show us the affected area using your camera",
            "📋 Your GP will receive a clear summary before you arrive",
        ],
        "privacy": "Your responses are private and only shared with your GP.",
        "start_btn": "Start →",
        "back_btn": "← Change Language",
    },
    "fr": {
        "flag": "🇫🇷", "name": "Français", "direction": "ltr",
        "greeting": "Bonjour ! Bienvenue sur ClearCare 👋",
        "subtitle": "Votre assistant NHS avant votre rendez-vous",
        "intro": "Avant votre rendez-vous, j'aimerais comprendre comment vous vous sentez. Cela aidera votre médecin à se préparer pour votre visite.",
        "what_to_expect": "À quoi s'attendre :",
        "steps": [
            "💬 Répondez à quelques questions simples sur vos symptômes",
            "📷 Montrez éventuellement la zone affectée avec votre caméra",
            "📋 Votre médecin recevra un résumé clair avant votre arrivée",
        ],
        "privacy": "Vos réponses sont privées et partagées uniquement avec votre médecin.",
        "start_btn": "Commencer →",
        "back_btn": "← Changer de langue",
    },
    "ar": {
        "flag": "🇸🇦", "name": "العربية", "direction": "rtl",
        "greeting": "مرحباً! أهلاً بك في ClearCare 👋",
        "subtitle": "مساعدك قبل موعد الطبيب",
        "intro": "قبل موعدك، أود أن أفهم كيف تشعر. سيساعد هذا طبيبك على الاستعداد لزيارتك.",
        "what_to_expect": "ماذا تتوقع:",
        "steps": [
            "💬 أجب على بعض الأسئلة البسيطة حول أعراضك",
            "📷 يمكنك اختياريًا إظهار المنطقة المتأثرة بالكاميرا",
            "📋 سيتلقى طبيبك ملخصاً واضحاً قبل وصولك",
        ],
        "privacy": "ردودك خاصة ولا تُشارك إلا مع طبيبك.",
        "start_btn": "ابدأ →",
        "back_btn": "← تغيير اللغة",
    },
    "ur": {
        "flag": "🇵🇰", "name": "اردو", "direction": "rtl",
        "greeting": "!ClearCare میں خوش آمدید 👋",
        "subtitle": "آپ کا NHS پری اپوائنٹمنٹ اسسٹنٹ",
        "intro": "آپ کی ملاقات سے پہلے، میں سمجھنا چاہتا ہوں کہ آپ کیسا محسوس کر رہے ہیں۔",
        "what_to_expect": "کیا توقع کریں:",
        "steps": [
            "💬 اپنی علامات کے بارے میں چند سوالات کے جوابات دیں",
            "📷 اختیاری طور پر کیمرے سے متاثرہ جگہ دکھائیں",
            "📋 آپ کے پہنچنے سے پہلے آپ کے ڈاکٹر کو خلاصہ ملے گا",
        ],
        "privacy": "آپ کے جوابات نجی ہیں اور صرف آپ کے ڈاکٹر کے ساتھ شیئر کیے جائیں گے۔",
        "start_btn": "شروع کریں →",
        "back_btn": "← زبان تبدیل کریں",
    },
    "hi": {
        "flag": "🇮🇳", "name": "हिन्दी", "direction": "ltr",
        "greeting": "नमस्ते! ClearCare में आपका स्वागत है 👋",
        "subtitle": "आपका NHS प्री-अपॉइंटमेंट सहायक",
        "intro": "आपकी अपॉइंटमेंट से पहले, मैं समझना चाहता हूँ कि आप कैसा महसूस कर रहे हैं। इससे आपके डॉक्टर को तैयारी करने में मदद मिलेगी।",
        "what_to_expect": "क्या उम्मीद करें:",
        "steps": [
            "💬 अपने लक्षणों के बारे में कुछ सरल सवालों के जवाब दें",
            "📷 वैकल्पिक रूप से कैमरे से प्रभावित क्षेत्र दिखाएं",
            "📋 आपके पहुंचने से पहले आपके डॉक्टर को एक स्पष्ट सारांश मिलेगा",
        ],
        "privacy": "आपके उत्तर निजी हैं और केवल आपके डॉक्टर के साथ साझा किए जाते हैं।",
        "start_btn": "शुरू करें →",
        "back_btn": "← भाषा बदलें",
    },
    "pl": {
        "flag": "🇵🇱", "name": "Polski", "direction": "ltr",
        "greeting": "Cześć! Witamy w ClearCare 👋",
        "subtitle": "Twój asystent przed wizytą NHS",
        "intro": "Przed wizytą chciałbym zrozumieć, jak się czujesz. Pomoże to Twojemu lekarzowi przygotować się do wizyty.",
        "what_to_expect": "Czego się spodziewać:",
        "steps": [
            "💬 Odpowiedz na kilka prostych pytań o swoje objawy",
            "📷 Opcjonalnie pokaż nam dotknięty obszar za pomocą kamery",
            "📋 Twój lekarz otrzyma jasne podsumowanie przed Twoim przybyciem",
        ],
        "privacy": "Twoje odpowiedzi są prywatne i udostępniane tylko Twojemu lekarzowi.",
        "start_btn": "Rozpocznij →",
        "back_btn": "← Zmień język",
    },
    "ro": {
        "flag": "🇷🇴", "name": "Română", "direction": "ltr",
        "greeting": "Bună! Bine ai venit la ClearCare 👋",
        "subtitle": "Asistentul tău înainte de programare NHS",
        "intro": "Înainte de programare, aș dori să înțeleg cum te simți. Acest lucru îl va ajuta pe medicul tău să se pregătească pentru vizita ta.",
        "what_to_expect": "La ce să te aștepți:",
        "steps": [
            "💬 Răspunde la câteva întrebări simple despre simptomele tale",
            "📷 Opțional, arată-ne zona afectată folosind camera",
            "📋 Medicul tău va primi un rezumat clar înainte să ajungi",
        ],
        "privacy": "Răspunsurile tale sunt private și partajate doar cu medicul tău.",
        "start_btn": "Începe →",
        "back_btn": "← Schimbă limba",
    },
    "bn": {
        "flag": "🇧🇩", "name": "বাংলা", "direction": "ltr",
        "greeting": "হ্যালো! ClearCare-এ স্বাগতম 👋",
        "subtitle": "আপনার NHS প্রি-অ্যাপয়েন্টমেন্ট সহকারী",
        "intro": "আপনার অ্যাপয়েন্টমেন্টের আগে, আমি বুঝতে চাই আপনি কেমন অনুভব করছেন।",
        "what_to_expect": "কী আশা করবেন:",
        "steps": [
            "💬 আপনার লক্ষণ সম্পর্কে কয়েকটি সহজ প্রশ্নের উত্তর দিন",
            "📷 ঐচ্ছিকভাবে ক্যামেরা দিয়ে আক্রান্ত স্থান দেখান",
            "📋 আপনি আসার আগে আপনার ডাক্তার একটি স্পষ্ট সারসংক্ষেপ পাবেন",
        ],
        "privacy": "আপনার উত্তরগুলি ব্যক্তিগত এবং শুধুমাত্র আপনার ডাক্তারের সাথে শেয়ার করা হবে।",
        "start_btn": "শুরু করুন →",
        "back_btn": "← ভাষা পরিবর্তন করুন",
    },
    "zh": {
        "flag": "🇨🇳", "name": "中文", "direction": "ltr",
        "greeting": "您好！欢迎使用 ClearCare 👋",
        "subtitle": "您的 NHS 预约前助手",
        "intro": "在您预约之前，我想了解您的感受。这将帮助您的全科医生为您的就诊做好准备。",
        "what_to_expect": "您可以期待：",
        "steps": [
            "💬 回答几个关于您症状的简单问题",
            "📷 可选择使用摄像头展示受影响的部位",
            "📋 您的医生将在您到达之前收到清晰的摘要",
        ],
        "privacy": "您的回答是私密的，仅与您的医生共享。",
        "start_btn": "开始 →",
        "back_btn": "← 更改语言",
    },
    "sp": {"flag": "🇪🇸", "name": "Español", "direction": "ltr",
        "greeting": "¡Hola! Bienvenido a ClearCare 👋",
        "subtitle": "Tu asistente NHS antes de tu cita",
        "intro": "Antes de tu cita, me gustaría entender cómo te sientes. Esto ayudará a tu médico a prepararse para tu visita.",
        "what_to_expect": "Qué esperar:",
        "steps": [
            "💬 Responde algunas preguntas sencillas sobre tus síntomas",
            "📷 Opcionalmente muéstranos la zona afectada con tu cámara",
            "📋 Tu médico recibirá un resumen claro antes de que llegues",
        ],
        "privacy": "Tus respuestas son privadas y solo se comparten con tu médico.",
        "start_btn": "Comenzar →",
        "back_btn": "← Cambiar idioma",
    }
}

# ══════════════════════════════════════════════════════════════════════════════
# SHARED STYLES
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.main { background-color: #faf8f4; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 600px; }

.logo-bar {
    display: flex; align-items: center; gap: 10px; margin-bottom: 2rem;
}
.logo-dot {
    width: 10px; height: 10px; background: #2ea87e;
    border-radius: 50%; display: inline-block;
}
.logo-text {
    font-family: 'Lora', serif; font-size: 1.3rem;
    font-weight: 600; color: #1a7a5e;
}
.nhs-badge {
    display: flex; align-items: center; justify-content: center;
    gap: 0.5rem; margin-top: 2rem; color: #7a7a8a; font-size: 0.75rem;
}
.nhs-pill {
    background: #003087; color: white; font-size: 0.7rem;
    font-weight: 700; padding: 0.15rem 0.5rem;
    border-radius: 4px; letter-spacing: 0.05em;
}
.stButton > button {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important; font-weight: 500 !important;
    border-radius: 12px !important; transition: all 0.2s !important;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE ROUTER
# ══════════════════════════════════════════════════════════════════════════════

# ── PAGE 1: Language Selection ────────────────────────────────────────────────
if st.session_state.page == "language":

    st.markdown('<div class="logo-bar"><span class="logo-dot"></span><span class="logo-text">ClearCare</span></div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; margin-bottom: 2rem;">
        <p style="font-size:0.75rem; letter-spacing:0.15em; text-transform:uppercase; color:#7a7a8a; margin-bottom:0.6rem;">
            NHS · Pre-Appointment Assistant
        </p>
        <h1 style="font-family:'Lora',serif; font-size:2rem; font-weight:400; color:#1a1a24; line-height:1.3; margin-bottom:0.6rem;">
            Tell your GP how you feel<br><em style="font-style:italic; color:#1a7a5e;">in your language</em>
        </h1>
        <p style="color:#7a7a8a; font-size:0.9rem;">
            Choose your preferred language below.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='text-align:center; font-size:0.8rem; color:#7a7a8a; margin-bottom:0.75rem;'>Select your language · اختر لغتك · अपनी भाषा चुनें</p>", unsafe_allow_html=True)

    # Style buttons as single clean cards
    st.markdown("""
    <style>
    div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] > button {
        background: white !important;
        border: 1.5px solid #e2ddd6 !important;
        border-radius: 14px !important;
        padding: 1rem 1.1rem !important;
        text-align: left !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        color: #1a1a24 !important;
        height: 64px !important;
    }
    div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] > button:hover {
        border-color: #2ea87e !important;
        background: #e8f5f0 !important;
        color: #1a7a5e !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Language grid — 2 columns, ONE button per language
    for i in range(0, len(LANGUAGES), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j < len(LANGUAGES):
                lang = LANGUAGES[i + j]
                is_selected = st.session_state.selected_lang == lang["code"]
                with col:
                    prefix = "✓ " if is_selected else ""
                    label = f"{prefix}{lang['flag']}  {lang['name']}  ·  {lang['native']}"
                    if st.button(label, key=f"lang_{lang['code']}", use_container_width=True):
                        st.session_state.selected_lang = lang["code"]
                        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Continue button
    if st.session_state.selected_lang:
        lang_info = next(l for l in LANGUAGES if l["code"] == st.session_state.selected_lang)
        st.success(f"{lang_info['flag']} **{lang_info['name']}** selected")
        if st.button("Continue →", use_container_width=True, type="primary"):
            st.session_state.page = "welcome"   # ← goes to page 2
            st.rerun()
    else:
        st.button("Select a language to continue →", use_container_width=True, disabled=True)

    st.markdown("""
    <div class="nhs-badge">
        <span class="nhs-pill">NHS</span>
        Powered by ClearCare · Your data is private and secure
    </div>
    """, unsafe_allow_html=True)


# ── PAGE 2: Welcome in chosen language ───────────────────────────────────────
elif st.session_state.page == "welcome":

    lang_code = st.session_state.selected_lang or "en"
    c = LANGUAGE_CONTENT.get(lang_code, LANGUAGE_CONTENT["en"])
    is_rtl = c["direction"] == "rtl"
    text_align = "right" if is_rtl else "left"

    st.markdown(f"""
    <div class="logo-bar" style="justify-content:{'flex-end' if is_rtl else 'flex-start'};">
        <span class="logo-dot"></span>
        <span class="logo-text">ClearCare</span>
    </div>
    """, unsafe_allow_html=True)

    # Language pill
    st.markdown(f"""
    <div style="display:inline-flex; align-items:center; gap:0.4rem;
        background:#e8f5f0; color:#1a7a5e; padding:0.3rem 0.75rem;
        border-radius:20px; font-size:0.78rem; font-weight:500; margin-bottom:1rem;">
        {c["flag"]} {c["name"]}
    </div>
    """, unsafe_allow_html=True)

    # Welcome card
    st.markdown(f"""
    <div style="background:white; border-radius:20px; border:1px solid #e2ddd6;
        padding:2rem; margin-bottom:1.25rem; text-align:{text_align};
        direction:{c['direction']};">
        <div style="font-family:'Lora',serif; font-size:1.6rem; font-weight:400;
            color:#1a1a24; margin-bottom:0.3rem; line-height:1.3;">
            {c["greeting"]}
        </div>
        <div style="font-size:0.85rem; color:#7a7a8a; margin-bottom:1.25rem;">
            {c["subtitle"]}
        </div>
        <div style="font-size:0.95rem; color:#3a3a4a; line-height:1.7; padding:1rem;
            background:#f0faf6; border-radius:12px;
            border-{'right' if is_rtl else 'left'}:3px solid #2ea87e;">
            {c["intro"]}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Steps card
    steps_html = "".join([
        f'<div style="padding:0.65rem 0; border-bottom:1px solid #f0ede8; font-size:0.9rem; color:#2a2a3a; line-height:1.5; text-align:{text_align}; direction:{c["direction"]};">{step}</div>'
        for step in c["steps"]
    ])
    st.markdown(f"""
    <div style="background:white; border-radius:20px; border:1px solid #e2ddd6;
        padding:1.5rem 2rem; margin-bottom:1.25rem;">
        <div style="font-size:0.72rem; letter-spacing:0.12em; text-transform:uppercase;
            color:#7a7a8a; margin-bottom:1rem; font-weight:500; text-align:{text_align};">
            {c["what_to_expect"]}
        </div>
        {steps_html}
    </div>
    """, unsafe_allow_html=True)

    # Buttons
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button(c["back_btn"], use_container_width=True):
            st.session_state.page = "language"   # ← back to page 1
            st.rerun()
    with col2:
        if st.button(c["start_btn"], use_container_width=True, type="primary"):
            st.session_state.page = "chat"        # ← forward to chat
            st.rerun()

    st.markdown(f"""
    <div style="text-align:center; font-size:0.78rem; color:#7a7a8a; margin-top:1rem;">
        🔒 {c["privacy"]}
    </div>
    """, unsafe_allow_html=True)


# ── PAGE 3: Chat (your teammates' code goes here) ─────────────────────────────
elif st.session_state.page == "chat":
    lang_code = st.session_state.selected_lang or "en"
    c = LANGUAGE_CONTENT.get(lang_code, LANGUAGE_CONTENT["en"])

    st.markdown('<div class="logo-bar"><span class="logo-dot"></span><span class="logo-text">ClearCare</span></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="display:inline-flex; align-items:center; gap:0.4rem;
        background:#e8f5f0; color:#1a7a5e; padding:0.3rem 0.75rem;
        border-radius:20px; font-size:0.78rem; font-weight:500; margin-bottom:1.5rem;">
        {c["flag"]} {c["name"]}
    </div>
    """, unsafe_allow_html=True)

    # ── Your teammates paste their chatbox + motion sensing code below this line ──
    st.info("💬 Chat page — your teammates' chatbox and motion sensing code goes here!")

    if st.button("← Back", use_container_width=False):
        st.session_state.page = "welcome"
        st.rerun() 