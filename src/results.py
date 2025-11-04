import streamlit as st
import base64
import random
from themes import THEMES


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
        style_scores = {"R": 0, "I": 0, "A": 0, "D": 0, "S": 0}
        for i, q in enumerate(test["questions"]):
            score = st.session_state.scores[i]
            if "style" in q and q["style"] in style_scores:
                style_scores[q["style"]] += score
        dominant_style = max(style_scores, key=style_scores.get)
        score_text = f"🎯 Ваш стиль: {test.get('style_labels', {}).get(dominant_style, dominant_style)} ({style_scores[dominant_style]}/25)"
        description = test.get("style_descriptions", {}).get(dominant_style, "Описание отсутствует.")
    else:
        total_score = sum(st.session_state.scores)
        max_possible = total_questions * max(test["questions"][0]["scores"]) if test["questions"] else 0
        score_text = f"🎉 Ваш результат: {total_score} из {max_possible} баллов"
        description = test.get("result_description", "Описание результата отсутствует.")

    # === HTML ===
    html_animation = f"""
    <style>
    .sky {{
        position: relative;
        height: 700px;
        background: linear-gradient(to bottom, #87CEEB, #c2e9fb);
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
    /* === Книга === */
    .book {{
        display: none;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 420px;
        height: 260px;
        perspective: 1500px;
        z-index: 15;
    }}
    .book-inner {{
        position: relative;
        width: 100%;
        height: 100%;
        transform-style: preserve-3d;
        transition: transform 1s ease;
    }}
    .book.flipped .book-inner {{
        transform: rotateY(180deg);
    }}
    .page {{
        position: absolute;
        width: 100%;
        height: 100%;
        backface-visibility: hidden;
        border-radius: 15px;
        box-shadow: 0 0 20px rgba(0,0,0,0.3);
        overflow: hidden;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 25px;
        box-sizing: border-box;
        font-size: 18px;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    .page.front {{
        background: #ffffff;
    }}
    .page.back {{
        background: #fff8e6;
        transform: rotateY(180deg);
    }}
    .flip-btn {{
        margin-top: 20px;
        background: #4caf50;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 8px 20px;
        cursor: pointer;
        font-weight: bold;
        transition: 0.3s;
    }}
    .flip-btn:hover {{
        background: #45a049;
    }}
    </style>

    <div class="sky">
        <img src="data:image/png;base64,{plane_base64}" class="plane" id="plane">
        <img src="data:image/png;base64,{box_base64}" class="box" id="dropBox">

        <!-- Облака -->
        {"".join([
        f'<img src="https://cdn-icons-png.flaticon.com/512/414/414927.png" class="cloud" style="top:{y}px; left:{x}px; width:{w}px; animation-duration:{d}s;">'
        for (y, x, w, d) in [
            (50, random.randint(0, 800), 150, 80),
            (150, random.randint(0, 800), 200, 100),
            (250, random.randint(0, 800), 180, 120)
        ]
    ])}

        <div class="ground"></div>

        <div id="book" class="book">
            <div class="book-inner">
                <div class="page front">
                    <h2>{score_text}</h2>
                    <button class="flip-btn" onclick="flipPage()">Перевернуть страницу 📖</button>
                </div>
                <div class="page back">
                    <h3>🪶 Объяснение результата</h3>
                    <p style="font-size:16px; line-height:1.4;">{description}</p>
                    <button class="flip-btn" onclick="flipPage()">⬅ Назад</button>
                </div>
            </div>
        </div>
    </div>

    <script>
    const plane = document.getElementById('plane');
    const box = document.getElementById('dropBox');
    const book = document.getElementById('book');
    const bookInner = book.querySelector('.book-inner');

    setTimeout(() => {{
        plane.style.left = "100%";
    }}, 100);

    let checkInterval = setInterval(() => {{
        const planeRect = plane.getBoundingClientRect();
        const skyRect = plane.parentElement.getBoundingClientRect();
        const planeCenter = planeRect.left + planeRect.width / 2;
        const skyCenter = skyRect.left + skyRect.width / 2;

        if (planeCenter >= skyCenter - 10 && planeCenter <= skyCenter + 10) {{
            box.style.display = 'block';
            box.style.left = (planeRect.left + planeRect.width / 2 - 80) + 'px';
            box.style.top = planeRect.top + 'px';
            setTimeout(() => {{
                box.style.top = '520px';
            }}, 100);
            clearInterval(checkInterval);
        }}
    }}, 50);

    box.onclick = () => {{
        box.style.display = 'none';
        book.style.display = 'block';
    }};

    function flipPage() {{
        book.classList.toggle('flipped');
    }}
    </script>
    """

    st.components.v1.html(html_animation, height=750)

    if st.button("🔄 Выбрать другой тест"):
        for key in ['current_theme', 'current_test', 'current_question', 'answers', 'scores']:
            st.session_state.pop(key, None)
        st.rerun()
