import streamlit as st
from themes import THEMES
import pandas as pd

def show_results(theme_key, test_key):
    test = THEMES[theme_key]["tests"][test_key]
    total_score = sum(st.session_state.scores)
    max_possible = len(test["questions"]) * max(test["questions"][0]["scores"])  # Максимальный балл

    # Находим интерпретацию
    result = None
    for score_range, interpretation in test["interpretation"].items():
        if score_range[0] <= total_score <= score_range[1]:
            result = interpretation
            break

    # Показываем красивые результаты
    st.balloons()
    st.markdown(f"""
        <div class="result-box">
            <h2>{result['emoji']} Ваш результат: {total_score} из {max_possible} баллов</h2>
            <h3>{result['level']}</h3>
            <p>{result['advice']}</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📊 Визуализация результата")

    # Определяем цвета по диапазонам
    if max_possible == 16:  # Для теста на делегирование
        low_end = 3
        medium_end = 7
    else:
        # Автоматически определяем границы на основе интерпретаций
        ranges = list(test["interpretation"].keys())
        low_end = ranges[0][1]  # Верхняя граница первого диапазона
        medium_end = ranges[1][1]  # Верхняя граница второго

    # Рассчитываем процент
    percentage = min(100, (total_score / max_possible) * 100)

    # Цветовая шкала: зелёный → жёлтый → красный
    if percentage <= (low_end / max_possible) * 100:
        color = "#4CAF50"  # Зелёный
    elif percentage <= (medium_end / max_possible) * 100:
        color = "#FFC107"  # Жёлтый
    else:
        color = "#F44336"  # Красный

    # Создаём HTML-шкалу
    st.markdown(f"""
        <div style="
            background-color: #e0e0e0;
            height: 30px;
            border-radius: 15px;
            position: relative;
            margin: 20px 0;
            overflow: hidden;
            width: 100%;
        ">
            <div style="
                background: linear-gradient(90deg, #4CAF50, #FFC107, #F44336);
                height: 100%;
                width: {percentage}%;
                border-radius: 15px;
                transition: width 1s ease-in-out;
            "></div>
            <div style="
                position: absolute;
                top: 50%;
                left: {percentage}%;
                transform: translateX(-50%) translateY(-50%);
                color: white;
                font-weight: bold;
                font-size: 14px;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.7);
                padding: 0 8px;
                background: rgba(0,0,0,0.3);
                border-radius: 15px;
            ">{total_score}/{max_possible}</div>
        </div>
    """, unsafe_allow_html=True)

    # Подпись под шкалой
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div style='text-align: center; color: #4CAF50;'>🔹 Низкий<br>({0}-{low_end})</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div style='text-align: center; color: #FFC107;'>🟡 Средний<br>({low_end+1}-{medium_end})</div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div style='text-align: center; color: #F44336;'>🔴 Высокий<br>({medium_end+1}-{max_possible})</div>", unsafe_allow_html=True)

    # Таблица ответов
    st.write("### 📝 Ваши ответы:")
    results_df = pd.DataFrame({
        'Вопрос': [q['text'] for q in test['questions']],
        'Ответ': st.session_state.answers,
        'Баллы': st.session_state.scores
    })
    st.dataframe(results_df, use_container_width=True)

    if st.button("🔄 Выбрать другой тест"):
        for key in ['current_theme', 'current_test', 'current_question', 'answers', 'scores']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

def show_results1(theme_key, test_key):
    test = THEMES[theme_key]["tests"][test_key]
    total_questions = len(test["questions"])

    # Считаем баллы по стилям — только если есть поле "style"
    style_scores = {"R": 0, "I": 0, "A": 0, "D": 0, "S": 0}
    has_style = False

    for i in range(total_questions):
        score = st.session_state.scores[i]
        question = test["questions"][i]
        if "style" in question:
            style = question["style"]
            if style in style_scores:
                style_scores[style] += score
            else:
                print(f"Неизвестный стиль: {style}")
        has_style = True  # Если хотя бы один вопрос имеет style — значит, это тест со стилями

    # Находим доминирующий стиль
    if has_style:
        dominant_style = max(style_scores, key=style_scores.get)
        max_score = style_scores[dominant_style]
        total_possible = 25  # Фиксировано: 25 вопросов × 1 балл максимум
        avg_score = sum(style_scores.values()) / len(style_scores)

        # Получаем описание доминирующего стиля
        style_name = test.get("style_labels", {}).get(dominant_style, "Неизвестный стиль")
        style_desc = test.get("style_descriptions", {}).get(dominant_style, "Описание отсутствует")

        # Показываем результаты
        st.balloons()
        st.markdown(f"""
            <div class="result-box">
                <h2>🎯 Ваш доминирующий стиль принятия решений</h2>
                <h3>{style_name} ({max_score}/{total_possible})</h3>
                <p><em>"{style_desc}"</em></p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📊 Распределение стилей (баллы из 25)")

        for style_code, score in style_scores.items():
            label = test.get("style_labels", {}).get(style_code, style_code)
            percentage = min(100, (score / total_possible) * 100)

            # Цветовая шкала: 0–8 = красный, 9–16 = жёлтый, 17–25 = зелёный
            if percentage <= 32:   # ≤ 8 баллов
                color = "#F44336"  # Красный
            elif percentage <= 64: # ≤ 16 баллов
                color = "#FFC107"  # Жёлтый
            else:                  # >16 баллов
                color = "#4CAF50"  # Зелёный

            # Создаём HTML-шкалу
            st.markdown(f"""
                <div style="
                    background-color: #e0e0e0;
                    height: 20px;
                    border-radius: 10px;
                    margin: 10px 0;
                    position: relative;
                    width: 100%;
                ">
                    <div style="
                        background: {color};
                        height: 100%;
                        width: {percentage}%;
                        border-radius: 10px;
                        transition: width 1s ease-in-out;
                    "></div>
                    <div style="
                        position: absolute;
                        top: 50%;
                        left: {percentage}%;
                        transform: translateX(-50%) translateY(-50%);
                        color: white;
                        font-weight: bold;
                        font-size: 14px;
                        text-shadow: 1px 1px 2px rgba(0,0,0,0.7);
                        padding: 0 8px;
                        background: rgba(0,0,0,0.3);
                        border-radius: 15px;
                    ">{score}/{total_possible}</div>
                </div>
                <p style="margin: 5px 0; font-weight: 500; color: white;">{label}</p>
            """, unsafe_allow_html=True)

        st.markdown("### 🔍 Подробная интерпретация")

        for style_code, score in style_scores.items():
            label = test.get("style_labels", {}).get(style_code, style_code)
            description = test.get("style_descriptions", {}).get(style_code, "Описание отсутствует")
            is_dominant = "✅ **ДОМИНИРУЮЩИЙ**" if style_code == dominant_style else ""
            st.markdown(f"""
                **{label}** — {score}/25<br>
                _"{description}"_ {is_dominant}
                """, unsafe_allow_html=True)

    else:
        total_score = sum(st.session_state.scores)
        max_possible = total_questions * max(test["questions"][0]["scores"]) if test["questions"] else 0

        # Найди интерпретацию
        result = None
        for score_range, interpretation in test["interpretation"].items():
            if score_range[0] <= total_score <= score_range[1]:
                result = interpretation
                break

        if not result:
            result = {"level": "Не определено", "emoji": "❓", "advice": "Результат не интерпретируется."}

        st.balloons()
        st.markdown(f"""
            <div class="result-box">
                <h2>{result['emoji']} Ваш результат: {total_score} из {max_possible} баллов</h2>
                <h3>{result['level']}</h3>
                <p>{result['advice']}</p>
            </div>
        """, unsafe_allow_html=True)

        percentage = min(100, (total_score / max_possible) * 100)
        st.markdown(f"""
            <div style="
                background-color: #e0e0e0;
                height: 30px;
                border-radius: 15px;
                position: relative;
                margin: 20px 0;
                overflow: hidden;
                width: 100%;
            ">
                <div style="
                    background: linear-gradient(90deg, #4CAF50, #FFC107, #F44336);
                    height: 100%;
                    width: {percentage}%;
                    border-radius: 15px;
                    transition: width 1s ease-in-out;
                "></div>
                <div style="
                    position: absolute;
                    top: 50%;
                    left: {percentage}%;
                    transform: translateX(-50%) translateY(-50%);
                    color: white;
                    font-weight: bold;
                    font-size: 14px;
                    text-shadow: 1px 1px 2px rgba(0,0,0,0.7);
                    padding: 0 8px;
                    background: rgba(0,0,0,0.3);
                    border-radius: 15px;
                ">{total_score}/{max_possible}</div>
            </div>
        """, unsafe_allow_html=True)

    # таблица ответов
    st.markdown("### 📝 Ваши ответы:")
    results_df = pd.DataFrame({
        'Вопрос': [q['text'] for q in test['questions']],
        'Ответ': st.session_state.answers,
        'Баллы': st.session_state.scores,
        'Стиль': [q.get('style', '—') for q in test['questions']]  # Безопасно получаем style
    })
    st.dataframe(results_df, use_container_width=True)

    if st.button("🔄 Выбрать другой тест"):
        for key in ['current_theme', 'current_test', 'current_question', 'answers', 'scores']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()