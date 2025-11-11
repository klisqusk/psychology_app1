import streamlit as st
import base64
import random
from themes import THEMES
import streamlit.components.v1 as components


def get_weather_type(total_score, max_possible, test_key, test_data):
    """Определяет тип погоды на основе результата теста"""
    percentage = (total_score / max_possible) * 100 if max_possible > 0 else 0

    # Для теста стилей решений используем нейтральную погоду (облачно)
    if test_key == "decision_style_test":
        return "cloudy"

    # Определяем логику в зависимости от типа интерпретации теста
    if "interpretations" in test_data and "ranges" in test_data["interpretations"]:
        # Для тестов с диапазонами
        for range_info in test_data["interpretations"]["ranges"]:
            if range_info["min"] <= total_score <= range_info["max"]:
                if range_info["min"] == 0 and range_info["max"] <= 5:  # Хороший результат
                    return "sunny"
                elif range_info["min"] >= 11:  # Плохой результат
                    return "rainy"
                else:  # Средний результат
                    return "cloudy"

    elif "interpretation" in test_data and test_data["interpretation"]:
        # Для тестов с интерпретацией в виде словаря
        for (min_score, max_score), result_info in test_data["interpretation"].items():
            if min_score <= total_score <= max_score:
                level = result_info.get("level", "").lower()
                emoji = result_info.get("emoji", "")

                # Определяем по уровню результата
                if any(word in level for word in
                       ["высокий", "отличный", "хороший", "хорошая", "идеальная", "молниеносная", "глубокий"]):
                    return "sunny"
                elif any(word in level for word in
                         ["низкий", "критически", "выгорание", "потеря", "слабая", "медленная"]):
                    return "rainy"
                else:  # Средний, удовлетворительный, умеренный
                    return "cloudy"

    # Общая логика по проценту
    if percentage >= 70:
        return "sunny"  # Хороший результат - солнечно
    elif percentage >= 40:
        return "cloudy"  # Средний результат - облачно
    else:
        return "rainy"  # Низкий результат - дождливо


def show_sunny_animation(theme_key, test_key, score_text, description):
    """Анимация с солнечной погодой для хороших результатов"""
    plane_path = "assets/plane.png"
    box_path = "assets/box.png"
    with open(plane_path, "rb") as f:
        plane_base64 = base64.b64encode(f.read()).decode()
    with open(box_path, "rb") as f:
        box_base64 = base64.b64encode(f.read()).decode()

    html_animation = f"""
    <style>
    .sky {{
        position: relative;
        height: 700px;
        background: linear-gradient(to bottom, #4A90E2, #87CEEB);
        overflow: hidden;
        border-radius: 20px;
        margin-bottom: 30px;
    }}
    .plane {{
        position: absolute;
        top: 100px;
        left: -250px;
        width: 250px;
        transition: left 4s ease-out;
        z-index: 10;
    }}
    .box {{
        position: absolute;
        width: 160px;
        height: 160px;
        cursor: pointer;
        display: none;
        z-index: 5;
        transition: top 4s ease-in-out;
    }}
    .sun {{
        position: absolute;
        top: 50px;
        right: 80px;
        width: 120px;
        height: 120px;
        background: radial-gradient(circle, #FFD700, #FF8C00);
        border-radius: 50%;
        box-shadow: 0 0 60px #FFA500, 0 0 100px #FF4500;
        animation: pulse 3s ease-in-out infinite;
    }}
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); opacity: 0.9; }}
        50% {{ transform: scale(1.05); opacity: 1; }}
    }}
    .cloud {{
        position: absolute;
        opacity: 0.7;
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
        background: linear-gradient(to top, #32CD32, #90EE90);
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
        width: 8px;
        height: 8px;
        background: radial-gradient(circle, #FFD700, #FF8C00);
        border-radius: 50%;
        animation: floatUp 2s ease-out forwards;
        box-shadow: 0 0 10px #FFD700;
    }}
    @keyframes floatUp {{
        0% {{ transform: translateY(0) scale(1); opacity: 1; }}
        100% {{ transform: translateY(-250px) scale(0.2); opacity: 0; }}
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
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: #8B4513;
        text-align: center;
        border: 3px solid #FF8C00;
    }}
    .page.back {{
        background: linear-gradient(to bottom right, #FFFACD, #FFE4B5);
        transform: rotateY(180deg);
        border: 2px solid #DAA520;
        box-shadow: inset 0 0 25px rgba(255, 165, 0, 0.3);
    }}
    .flip-btn {{
        margin-top: 15px;
        background: linear-gradient(to bottom, #FF8C00, #FF6347);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 30px;
        cursor: pointer;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 8px rgba(255, 140, 0, 0.3);
    }}
    .flip-btn:hover {{
        background: linear-gradient(to bottom, #FFA500, #FF4500);
        transform: scale(1.08);
        box-shadow: 0 6px 12px rgba(255, 140, 0, 0.4);
    }}
    </style>

    <div class="sky">
        <div class="sun"></div>
        <img src="data:image/png;base64,{plane_base64}" class="plane" id="plane">
        <img src="data:image/png;base64,{box_base64}" class="box" id="dropBox">

        {"".join([
        f'<img src="https://cdn-icons-png.flaticon.com/512/414/414927.png" class="cloud" style="top:{y}px; left:{x}px; width:{w}px; animation-duration:{d}s;">'
        for (y, x, w, d) in [
            (180, random.randint(0, 300), 120, 60),
            (280, random.randint(400, 700), 100, 80)
        ]
    ])}

        <div class="ground"></div>
        <div id="particles" class="particles"></div>

        <div id="book" class="book">
            <div class="book-inner">
                <div class="page front">
                    <h2>☀️ {score_text}</h2>
                    <p style="font-size: 16px; margin-top: 10px; color: #8B4513;">Отличный результат!</p>
                    <button class="flip-btn" onclick="flipPage()">Перевернуть 📖</button>
                </div>
                <div class="page back">
                    <h3>🎯 Объяснение результата</h3>
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
        box.style.transition = 'opacity 0.5s, transform 0.5s';
        box.style.opacity = 0;
        box.style.transform = 'scale(1.2) rotate(180deg)';
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
        for (let i = 0; i < 50; i++) {{
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


def show_cloudy_animation(theme_key, test_key, score_text, description):
    """Анимация с облачной погодой для средних результатов"""
    plane_path = "assets/plane.png"
    box_path = "assets/box.png"
    with open(plane_path, "rb") as f:
        plane_base64 = base64.b64encode(f.read()).decode()
    with open(box_path, "rb") as f:
        box_base64 = base64.b64encode(f.read()).decode()

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
                    <h2>☁️ {score_text}</h2>
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


def show_rainy_animation(theme_key, test_key, score_text, description):
    """Анимация с дождливой погодой для низких результатов"""
    plane_path = "assets/plane.png"
    box_path = "assets/box.png"
    with open(plane_path, "rb") as f:
        plane_base64 = base64.b64encode(f.read()).decode()
    with open(box_path, "rb") as f:
        box_base64 = base64.b64encode(f.read()).decode()

    html_animation = f"""
    <style>
    .sky {{
        position: relative;
        height: 700px;
        background: linear-gradient(to bottom, #2F4F4F, #696969);
        overflow: hidden;
        border-radius: 20px;
        margin-bottom: 30px;
    }}
    .plane {{
        position: absolute;
        top: 100px;
        left: -250px;
        width: 250px;
        transition: left 5s ease-in-out;
        z-index: 10;
        filter: brightness(0.8);
    }}
    .box {{
        position: absolute;
        width: 160px;
        height: 160px;
        cursor: pointer;
        display: none;
        z-index: 5;
        transition: top 3s ease-in-out;
        filter: brightness(0.9);
    }}
    .cloud {{
        position: absolute;
        opacity: 0.9;
        animation: float linear infinite;
        filter: brightness(0.7);
    }}
    @keyframes float {{
        0% {{ transform: translateX(0); }}
        100% {{ transform: translateX(100vw); }}
    }}
    .rain-container {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 2;
    }}
    .rain {{
        position: absolute;
        width: 1.5px;
        height: 25px;
        background: linear-gradient(to bottom, transparent, #87CEEB 70%, #4682B4);
        animation: rainFall 1.5s linear infinite;
        opacity: 0.6;
    }}
    @keyframes rainFall {{
        0% {{ transform: translateY(-50px); opacity: 0; }}
        10% {{ opacity: 0.7; }}
        90% {{ opacity: 0.7; }}
        100% {{ transform: translateY(650px); opacity: 0; }}
    }}
    .ground {{
        position: absolute;
        bottom: 0;
        width: 100%;
        height: 150px;
        background: linear-gradient(to top, #556B2F, #6B8E23);
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
        background: rgba(173, 216, 230, 0.8);
        border-radius: 50%;
        animation: floatUp 2s ease-out forwards;
    }}
    @keyframes floatUp {{
        0% {{ transform: translateY(0) scale(1); opacity: 1; }}
        100% {{ transform: translateY(-150px) scale(0.2); opacity: 0; }}
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
        box-shadow: 0 0 35px rgba(0, 0, 0, 0.5);
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
        background: linear-gradient(135deg, #4682B4, #2F4F4F);
        color: #E6E6FA;
        text-align: center;
        border: 2px solid #5F9EA0;
    }}
    .page.back {{
        background: linear-gradient(to bottom right, #F0F8FF, #E6E6FA);
        transform: rotateY(180deg);
        border: 1px solid #B0C4DE;
        box-shadow: inset 0 0 25px rgba(70, 130, 180, 0.3);
    }}
    .flip-btn {{
        margin-top: 15px;
        background: linear-gradient(to bottom, #4682B4, #2F4F4F);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 25px;
        cursor: pointer;
        font-weight: bold;
        transition: all 0.3s ease;
    }}
    .flip-btn:hover {{
        background: linear-gradient(to bottom, #5F9EA0, #4682B4);
        transform: scale(1.05);
    }}
    </style>

    <div class="sky">
        <img src="data:image/png;base64,{plane_base64}" class="plane" id="plane">
        <img src="data:image/png;base64,{box_base64}" class="box" id="dropBox">

        {"".join([
        f'<img src="https://cdn-icons-png.flaticon.com/512/414/414927.png" class="cloud" style="top:{y}px; left:{x}px; width:{w}px; animation-duration:{d}s;">'
        for (y, x, w, d) in [
            (30, random.randint(0, 600), 200, 90),
            (120, random.randint(200, 800), 220, 110),
            (200, random.randint(100, 500), 180, 95),
            (280, random.randint(400, 900), 190, 105)
        ]
    ])}

        <div class="rain-container" id="rainContainer"></div>

        <div class="ground"></div>
        <div id="particles" class="particles"></div>

        <div id="book" class="book">
            <div class="book-inner">
                <div class="page front">
                    <h2>🌧️ {score_text}</h2>
                    <p style="font-size: 16px; margin-top: 10px; color: #E6E6FA;">Есть над чем поработать!</p>
                    <button class="flip-btn" onclick="flipPage()">Перевернуть 📖</button>
                </div>
                <div class="page back">
                    <h3>💡 Рекомендации</h3>
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
    const rainContainer = document.getElementById('rainContainer');

    // Функция для создания дождя с оптимизацией
    function createRain() {{
        const containerWidth = rainContainer.offsetWidth;
        const rainCount = 60; // Уменьшено количество капель

        for (let i = 0; i < rainCount; i++) {{
            const rain = document.createElement('div');
            rain.className = 'rain';
            rain.style.left = Math.random() * containerWidth + 'px';
            rain.style.animationDelay = (Math.random() * 2) + 's';
            rain.style.animationDuration = (1 + Math.random() * 0.5) + 's';
            rainContainer.appendChild(rain);
        }}
    }}

    // Запускаем дождь после загрузки
    setTimeout(createRain, 100);

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
        box.style.transition = 'opacity 0.5s, transform 0.5s';
        box.style.opacity = 0;
        box.style.transform = 'scale(0.8)';
        setTimeout(() => {{
            box.style.display = 'none';
            spawnParticles();
            setTimeout(() => {{
                book.style.display = 'block';
                book.classList.add('showing');
            }}, 1000);
        }}, 500);
    }};

    function spawnParticles() {{
        particles.style.display = 'block';
        const skyRect = document.querySelector('.sky').getBoundingClientRect();
        for (let i = 0; i < 25; i++) {{ // Уменьшено количество частиц
            const p = document.createElement('div');
            p.className = 'particle';
            p.style.left = Math.random() * skyRect.width + 'px';
            p.style.top = Math.random() * skyRect.height + 'px';
            p.style.animationDelay = (Math.random() * 0.3) + 's';
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


def show_results_animation(theme_key, test_key):
    """Основная функция для показа анимации результатов"""
    test = THEMES[theme_key]["tests"][test_key]
    total_questions = len(test["questions"])

    # === Расчет результатов ===
    if test_key == "decision_style_test":
        style_scores = {"R": 0, "I": 0, "A": 0, "D": 0, "S": 0}
        for i, q in enumerate(test["questions"]):
            score = st.session_state.scores[i]
            if "style" in q and q["style"] in style_scores:
                style_scores[q["style"]] += score
        dominant_style = max(style_scores, key=style_scores.get)
        total_score = style_scores[dominant_style]
        max_possible = 25
        score_text = f"🎯 Ваш стиль: {test.get('style_labels', {}).get(dominant_style, dominant_style)} ({total_score}/25)"
        description = test.get("style_descriptions", {}).get(dominant_style, "Описание отсутствует.")

    elif "interpretations" in test and "ranges" in test["interpretations"]:
        total_score = sum(st.session_state.scores)
        max_possible = total_questions * max(test["questions"][0]["scores"]) if test["questions"] else 0
        score_text = f"✨ Ваш результат: {total_score} из {max_possible} баллов"
        description = "Описание результата отсутствует."
        for range_info in test["interpretations"]["ranges"]:
            if range_info["min"] <= total_score <= range_info["max"]:
                description = range_info["text"]
                break

    elif "interpretation" in test and test["interpretation"]:
        total_score = sum(st.session_state.scores)
        max_possible = total_questions * max(test["questions"][0]["scores"]) if test["questions"] else 0
        score_text = f"✨ Ваш результат: {total_score} из {max_possible} баллов"
        description = "Описание результата отсутствует."
        for (min_score, max_score), result_info in test["interpretation"].items():
            if min_score <= total_score <= max_score:
                description = f"{result_info['emoji']} {result_info['level']}\n\n{result_info['advice']}"
                break

    else:
        total_score = sum(st.session_state.scores)
        max_possible = total_questions * max(test["questions"][0]["scores"]) if test["questions"] else 0
        score_text = f"✨ Ваш результат: {total_score} из {max_possible} баллов"
        description = test.get("result_description", "Описание результата отсутствует.")

    # === Определение типа погоды и показ соответствующей анимации ===
    weather_type = get_weather_type(total_score, max_possible, test_key, test)

    if weather_type == "sunny":
        show_sunny_animation(theme_key, test_key, score_text, description)
    elif weather_type == "rainy":
        show_rainy_animation(theme_key, test_key, score_text, description)
    else:  # cloudy по умолчанию
        show_cloudy_animation(theme_key, test_key, score_text, description)

    # Кнопка "Главное меню"
    if st.button("🏠 Главное меню"):
        for key in ['current_theme', 'current_test', 'current_question', 'answers', 'scores']:
            st.session_state.pop(key, None)
        st.session_state['show_main_menu'] = True