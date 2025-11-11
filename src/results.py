import streamlit as st
import base64
import random
from themes import THEMES
import streamlit.components.v1 as components


def show_results_animation(theme_key, test_key):
    test = THEMES[theme_key]["tests"][test_key]
    total_questions = len(test["questions"])

    # === Изображения ===
    plane_path = "assets/plane.png"
    box_path = "assets/box.png"
    with open(plane_path, "rb") as f:
        plane_base64 = base64.b64encode(f.read()).decode()
    with open(box_path, "rb") as f:
        box_base64 = base64.b64encode(f.read()).decode()

    # === Результаты ===
    if test_key == "decision_style_test":
        # Обработка теста на стили принятия решений
        style_scores = {"R": 0, "I": 0, "A": 0, "D": 0, "S": 0}
        for i, q in enumerate(test["questions"]):
            score = st.session_state.scores[i]
            if "style" in q and q["style"] in style_scores:
                style_scores[q["style"]] += score
        dominant_style = max(style_scores, key=style_scores.get)
        score_text = f"🎯 Ваш стиль: {test.get('style_labels', {}).get(dominant_style, dominant_style)} ({style_scores[dominant_style]}/25)"
        description = test.get("style_descriptions", {}).get(dominant_style, "Описание отсутствует.")

    elif "interpretations" in test and "ranges" in test["interpretations"]:
        # Обработка теста делегирования с диапазонами
        total_score = sum(st.session_state.scores)
        max_possible = total_questions * max(test["questions"][0]["scores"]) if test["questions"] else 0
        score_text = f"✨ Ваш результат: {total_score} из {max_possible} баллов"

        # Поиск подходящего диапазона
        description = "Описание результата отсутствует."
        for range_info in test["interpretations"]["ranges"]:
            if range_info["min"] <= total_score <= range_info["max"]:
                description = range_info["text"]
                break

    elif "interpretation" in test and test["interpretation"]:
        # Обработка тестов с интерпретацией в виде словаря
        total_score = sum(st.session_state.scores)
        max_possible = total_questions * max(test["questions"][0]["scores"]) if test["questions"] else 0
        score_text = f"✨ Ваш результат: {total_score} из {max_possible} баллов"

        # Поиск в интерпретации
        description = "Описание результата отсутствует."
        for (min_score, max_score), result_info in test["interpretation"].items():
            if min_score <= total_score <= max_score:
                description = f"{result_info['emoji']} {result_info['level']}\n\n{result_info['advice']}"
                break

    else:
        # Общий случай для остальных тестов
        total_score = sum(st.session_state.scores)
        max_possible = total_questions * max(test["questions"][0]["scores"]) if test["questions"] else 0
        score_text = f"✨ Ваш результат: {total_score} из {max_possible} баллов"
        description = test.get("result_description", "Описание результата отсутствует.")

    # === ОСТАЛЬНАЯ ЧАСТЬ ФУНКЦИИ ОСТАЕТСЯ БЕЗ ИЗМЕНЕНИЙ ===
    # (HTML, CSS, JS код)

    html_animation = f"""
    <style>
    .sky {{
        position: relative;
        height: 700px;
        background: linear-gradient(to bottom, #87CEEB, #e0c3fc);
        overflow: hidden;
        border-radius: 20px;
        margin-bottom: 30px;
    }}
    .plane {{
        position: absolute;
        top: 100px;
        left: -250px;
        width: 250px;
        transition: left 5s linear;
        z-index: 10;
    }}
    .box {{
        position: absolute;
        width: 160px;
        height: 160px;
        cursor: pointer;
        display: none;
        z-index: 5;
        transition: top 5s ease;
    }}
    .cloud {{
        position: absolute;
        opacity: 0.85;
        animation: float linear infinite;
    }}
    @keyframes float {{
        0% {{ transform: translateX(0); }}
        100% {{ transform: translateX(100vw); }}
    }}
    .ground {{
        position: absolute;
        bottom: 0;
        width: 100%;
        height: 150px;
        background: linear-gradient(to top, #2E8B57, #3CB371);
        z-index: 1;
    }}
    .particles {{
        position: absolute;
        display: none;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        overflow: visible;
        pointer-events: none;
        z-index: 15;
    }}
    .particle {{
        position: absolute;
        width: 6px;
        height: 6px;
        background: rgba(255, 255, 200, 0.9);
        border-radius: 50%;
        animation: floatUp 2s ease-out forwards;
    }}
    @keyframes floatUp {{
        0% {{ transform: translateY(0) scale(1); opacity: 1; }}
        100% {{ transform: translateY(-200px) scale(0.2); opacity: 0; }}
    }}
    .book {{
        display: none;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 500px;
        height: 320px;
        perspective: 1800px;
        z-index: 20;
    }}
    .book-inner {{
        position: relative;
        width: 100%;
        height: 100%;
        transform-style: preserve-3d;
        transition: transform 1.2s cubic-bezier(0.4, 0.2, 0.2, 1);
    }}
    .book.flipped .book-inner {{
        transform: rotateY(180deg);
    }}
    .page {{
        position: absolute;
        width: 100%;
        height: 100%;
        backface-visibility: hidden;
        border-radius: 18px;
        box-shadow: 0 0 35px rgba(0, 0, 0, 0.4);
        overflow: hidden;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 35px;
        box-sizing: border-box;
        font-family: 'Georgia', serif;
        font-size: 18px;
        color: #3b2a1a;
    }}
    .page.front {{
        background: radial-gradient(circle at 30% 30%, #5c4033, #3a2a22 90%);
        color: #f3e9d2;
        text-align: center;
    }}
    .page.back {{
        background: linear-gradient(to bottom right, #fff8e6, #f6e9c9);
        transform: rotateY(180deg);
        border: 1px solid #d9c29c;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.2);
    }}
    .flip-btn {{
        margin-top: 15px;
        background: linear-gradient(to bottom, #d4a373, #b07b4e);
        color: #fff;
        border: none;
        border-radius: 10px;
        padding: 10px 25px;
        cursor: pointer;
        font-weight: bold;
        transition: all 0.3s ease;
    }}
    .flip-btn:hover {{
        background: linear-gradient(to bottom, #e0b182, #c89263);
        transform: scale(1.05);
    }}
    </style>

    <div class="sky">
        <img src="data:image/png;base64,{plane_base64}" class="plane" id="plane">
        <img src="data:image/png;base64,{box_base64}" class="box" id="dropBox">

        {"".join([
        f'<img src="https://cdn-icons-png.flaticon.com/512/414/414927.png" class="cloud" style="top:{y}px; left:{x}px; width:{w}px; animation-duration:{d}s;">'
        for (y, x, w, d) in [
            (50, random.randint(0, 800), 150, 80),
            (150, random.randint(0, 800), 200, 100),
            (250, random.randint(0, 800), 180, 120)
        ]
    ])}

        <div class="ground"></div>
        <div id="particles" class="particles"></div>

        <div id="book" class="book">
            <div class="book-inner">
                <div class="page front">
                    <h2>{score_text}</h2>
                    <button class="flip-btn" onclick="flipPage()">Перевернуть 📖</button>
                </div>
                <div class="page back">
                    <h3>🪶 Объяснение результата</h3>
                    <p>{description}</p>
                    <button class="flip-btn" onclick="flipPage()">⬅ Назад</button>
                </div>
            </div>
        </div>
    </div>

    <script>
    const plane = document.getElementById('plane');
    const box = document.getElementById('dropBox');
    const book = document.getElementById('book');
    const particles = document.getElementById('particles');

    setTimeout(() => {{ plane.style.left = "100%"; }}, 100);

    let checkInterval = setInterval(() => {{
        const planeRect = plane.getBoundingClientRect();
        const skyRect = plane.parentElement.getBoundingClientRect();
        const planeCenter = planeRect.left + planeRect.width / 2;
        const skyCenter = skyRect.left + skyRect.width / 2;

        if (planeCenter >= skyCenter - 10 && planeCenter <= skyCenter + 10) {{
            box.style.display = 'block';
            box.style.left = (planeRect.left + planeRect.width / 2 - 80) + 'px';
            box.style.top = planeRect.top + 'px';
            setTimeout(() => {{ box.style.top = '520px'; }}, 100);
            clearInterval(checkInterval);
        }}
    }}, 50);

    box.onclick = () => {{
        box.style.transition = 'opacity 0.5s';
        box.style.opacity = 0;
        setTimeout(() => {{
            box.style.display = 'none';
            spawnParticles();
            setTimeout(() => {{
                book.style.display = 'block';
                book.classList.add('showing');
            }}, 1500);
        }}, 500);
    }};

    function spawnParticles() {{
        particles.style.display = 'block';
        const skyRect = document.querySelector('.sky').getBoundingClientRect();
        for (let i = 0; i < 40; i++) {{
            const p = document.createElement('div');
            p.className = 'particle';
            p.style.left = Math.random() * skyRect.width + 'px';
            p.style.top = Math.random() * skyRect.height + 'px';
            p.style.animationDelay = (Math.random() * 0.5) + 's';
            particles.appendChild(p);
            setTimeout(() => p.remove(), 2000);
        }}
    }}

    function flipPage() {{
        book.classList.toggle('flipped');
    }}
    </script>
    """

    components.html(html_animation, height=750, scrolling=False)

    # Кнопка "Главное меню" вне карточки
    if st.button("🏠 Главное меню"):
        for key in ['current_theme', 'current_test', 'current_question', 'answers', 'scores']:
            st.session_state.pop(key, None)
        st.session_state['show_main_menu'] = True