import streamlit as st
from themes import THEMES
import random
import base64

def show_results_animation(theme_key, test_key):
    test = THEMES[theme_key]["tests"][test_key]
    total_questions = len(test["questions"])

    # === Plane image ===
    plane_path = "assets/plane.png"
    with open(plane_path, "rb") as f:
        plane_base64 = base64.b64encode(f.read()).decode()

    # === Box image ===
    box_path = "assets/box.png"
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
        style_label = test.get('style_labels', {}).get(dominant_style, dominant_style)
        style_description = test.get('style_descriptions', {}).get(dominant_style, '')
        result_text = f"🎯 Ваш стиль принятия решений: {style_label}\n\n{style_description}"
    else:
        total_score = sum(st.session_state.scores)

        # Поиск подходящей интерпретации
        interpretation = "Результат теста обрабатывается..."
        if "interpretations" in test and "ranges" in test["interpretations"]:
            for range_info in test["interpretations"]["ranges"]:
                if range_info["min"] <= total_score <= range_info["max"]:
                    interpretation = range_info["text"]
                    break

        result_text = f"{interpretation}"

    # === HTML анимация (остальной код остается без изменений) ===
    html_animation = f"""
    <style>
    .sky {{
        position: relative;
        height: 700px;
        width: 100%;
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
        width: 180px;
        height: 180px;
        cursor: pointer;
        display: none;
        z-index: 5;
        transition: top 5s ease;
    }}
    .cloud {{
        position: absolute;
        opacity: 0.8;
        animation: moveClouds linear infinite;
    }}
    @keyframes moveClouds {{
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
    .result-box {{
        display: none;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 320px;
        background: rgba(255,255,255,0.95);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 0 15px rgba(0,0,0,0.3);
        animation: fadeIn 1s ease forwards;
    }}
    @keyframes fadeIn {{
        0% {{ opacity: 0; transform: translate(-50%, -100%); }}
        100% {{ opacity: 1; transform: translate(-50%, -50%); }}
    }}
    </style>

    <div class="sky">
        <img src="data:image/png;base64,{plane_base64}" class="plane" id="plane">
        <img src="data:image/png;base64,{box_base64}" class="box" id="dropBox">
        <img src="https://cdn-icons-png.flaticon.com/512/414/414927.png" class="cloud" style="top: 50px; width:150px; left:{random.randint(0, 800)}px; animation-duration: 60s;">
        <img src="https://cdn-icons-png.flaticon.com/512/414/414927.png" class="cloud" style="top: 150px; width:200px; left:{random.randint(0, 800)}px; animation-duration: 80s;">
        <img src="https://cdn-icons-png.flaticon.com/512/414/414927.png" class="cloud" style="top: 250px; width:180px; left:{random.randint(0, 800)}px; animation-duration: 100s;">
        <div class="ground"></div>
        <div id="resultContainer" class="result-box">
            <h2>{result_text}</h2>
        </div>
    </div>

    <script>
    const plane = document.getElementById('plane');
    const box = document.getElementById('dropBox');
    const result = document.getElementById('resultContainer');

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
            box.style.top = planeRect.top + "px";
            box.style.left = planeRect.left + planeRect.width/2 - box.width/2 + "px";
            box.style.transition = "top 5s ease";
            box.style.top = planeRect.top + 400 + "px";
            clearInterval(checkInterval);
        }}
    }}, 50);

    box.onclick = () => {{
        box.style.display = 'none';
        result.style.display = 'block';
    }};
    </script>
    """

    st.components.v1.html(html_animation, height=750)

    if st.button("🔄 Выбрать другой тест"):
        for key in ['current_theme', 'current_test', 'current_question', 'answers', 'scores']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()