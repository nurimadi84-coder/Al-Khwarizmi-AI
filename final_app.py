import streamlit as st
import google.generativeai as genai
import json
import re

# ==========================================
# 1. AI ЖҮЙЕСІН БАПТАУ
# ==========================================
# ОСЫ ЖЕРГЕ ӨЗ API КІЛТІҢІЗДІ ҚОЙЫҢЫЗ:
API_KEY = " " 

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-3-flash-preview')

# ==========================================
# 2. ИНТЕРФЕЙС ЖӘНЕ СТИЛЬ (UI/UX)
# ==========================================
st.set_page_config(page_title="Al-Khwarizmi AI", page_icon="🕌", layout="wide")

# Кәсіби қараңғы стиль (Modern Dark Theme)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { 
        width: 100%; background-color: #ff4b4b; color: white; 
        font-weight: bold; border-radius: 10px; border: none; height: 3em;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px; background-color: #1e2129; border-radius: 8px;
        color: white; border: 1px solid #333;
    }
    .stTabs [aria-selected="true"] { background-color: #ff4b4b !important; }
    div[data-testid="stMetricValue"] { color: #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

st.title("🕌 Al-Khwarizmi AI: STEM Визуализаторы")
st.markdown("*LLM және Agentic Workflow негізіндегі адаптивті білім беру платформасы*")

# Сессияны сақтау (Слайдер деректері жоғалмауы үшін)
if 'cs_data' not in st.session_state:
    st.session_state['cs_data'] = None

# ==========================================
# 3. КӨМЕКШІ ФУНКЦИЯЛАР
# ==========================================
def clean_ai_json(text):
    """AI жауабынан тек JSON-ды тауып, тазалап алу"""
    try:
        json_str = re.search(r'\{.*\}', text, re.DOTALL).group()
        return json.loads(json_str)
    except:
        return None

# ==========================================
# 4. НЕГІЗГІ БӨЛІМДЕР (TABS)
# ==========================================
tab1, tab2, tab3 = st.tabs(["💻 Code Tracer", "📐 Math Animator", "🏆 Жоба концепциясы"])

# --- TAB 1: ИНФОРМАТИКА (CODE TRACER) ---
with tab1:
    st.header("💻 Алгоритмдердің қадамдық визуализациясы")
    st.write("Кодтың орындалу логикасын және жадыдағы (RAM) өзгерістерді бақылаңыз.")
    
    cs_query = st.text_input("Алгоритм тақырыбы:", placeholder="Мысалы: Тізімдегі сандарды сұрыптау (Bubble Sort)")

    if st.button("Талдауды бастау", key="tracer_btn"):
        if cs_query:
            with st.spinner("AI Agent алгоритмді есептеп жатыр..."):
                prompt = f"""
                Сен Python дебаггер-мұғалімісің. '{cs_query}' тақырыбына алгоритм жаз.
                Оны тек мына JSON форматында қайтар (басқа мәтін қоспа):
                {{
                  "code": "Python коды",
                  "steps": [
                    {{"line": "орындалып жатқан жол", "vars": {{"айнымалы": "мәні"}}, "desc": "қазақша түсіндірме"}}
                  ]
                }}
                Түсіндірмелерді тек қазақ тілінде жаз.
                """
                response = model.generate_content(prompt)
                st.session_state['cs_data'] = clean_ai_json(response.text)
        else:
            st.warning("Сұранысты толтырыңыз!")

    if st.session_state['cs_data']:
        data = st.session_state['cs_data']
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📝 Код")
            st.code(data["code"], language="python")
        
        with col2:
            st.subheader("🔍 Трассировка")
            steps = data["steps"]
            step_idx = st.slider("Орындалу қадамы:", 1, len(steps), 1) - 1
            curr = steps[step_idx]
            
            st.info(f"**Ағымдағы жол:** `{curr['line']}`")
            st.success(f"**Түсіндірме:** {curr['desc']}")
            st.warning("**Айнымалылар күйі (RAM):**")
            st.json(curr['vars'])

# --- TAB 2: МАТЕМАТИКА (MATH ANIMATOR) ---
with tab2:
    st.header("📐 AI Math Animator (Beta)")
    st.write("Математикалық концепцияларды Manim коды арқылы визуализациялау.")
    
    math_query = st.text_input("Математикалық сұрақ:", placeholder="Мысалы: Синус және косинус функцияларының байланысы")

    if st.button("Анимация кодын жасау", key="math_btn"):
        if math_query:
            with st.spinner("AI Manim моделін құрастыруда..."):
                math_prompt = f"Write Manim Python code for: {math_query}. Class GeneratedScene(Scene). Return ONLY the code. Use Kazakh labels."
                response = model.generate_content(math_prompt)
                
                st.subheader("🚀 Генерацияланған Manim коды")
                st.code(response.text.replace("```python", "").replace("```", ""), language="python")
                
                c1, c2 = st.columns(2)
                c1.metric("Статус", "Ready for Render")
                c2.metric("Тіл", "Қазақша")
                
                st.divider()
                st.info("💡 **MVP ескертуі:** Қазіргі сатыда AI анимация логикасын жасайды. Бұлтты рендеринг келесі кезеңде қосылады.")
                st.video("https://www.youtube.com/watch?v=ENMyFGmq5OA") # Демо видео

# --- TAB 3: КОНЦЕПЦИЯ (PITCH) ---
with tab3:
    st.header("🕌 Al-Khwarizmi AI: Инновациялық концепция")
    
    col_p1, col_p2 = st.columns([2, 1])
    with col_p1:
        st.markdown("""
        **Мәселе:** STEM пәндеріндегі абстракция кедергісі.
        **Шешім:** LLM арқылы мәтінді динамикалық логикаға айналдыру.
        
        **Негізгі инновациялар:**
        1. **Agentic Workflow:** AI кодты жазып қана қоймай, оның орындалу қадамдарын есептейді.
        2. **Real-time Tracing:** Оқушы алгоритмнің әр қадамын жады (RAM) деңгейінде көреді.
        3. **Generative Graphics:** Математикалық видеоларды қолмен емес, промпт арқылы жасау.
        """)
    
    with col_p2:
        # Сурет сілтемесі дұрысталды (raw URL)
        st.image("https://images.unsplash.com/photo-1509228468518-180dd48a5d5f?auto=format&fit=crop&q=80&w=1000", caption="Al-Khwarizmi AI Vision")


    st.success("🎯 **Мақсат:** Білім беруді статикалық бейнелерден интерактивті AI-ассистентке көшіру.")
