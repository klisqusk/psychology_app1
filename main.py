import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ===== НАСТРОЙКА СТРАНИЦЫ =====
st.set_page_config(
    page_title="PsychoTest Pro",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== СТИЛИ ДЛЯ КРАСОТЫ =====
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #6a5acd;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .test-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        margin: 1rem 0;
        transition: transform 0.3s ease;
    }
    .test-card:hover {
        transform: translateY(-5px);
    }
    .stButton>button {
        background: linear-gradient(45deg, #FF4B4B, #FF6B6B);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 12px 25px;
        font-size: 1.1rem;
        font-weight: bold;
    }
    .result-box {
        background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ===== ДАННЫЕ ТЕСТОВ =====
TESTS = {
    "depression": {
        "title": "📊 Тест на депрессию",
        "description": "Оценка эмоционального состояния",
        "questions": [
            {
                "text": "Чувствуете ли вы подавленность?",
                "options": ["Никогда", "Редко", "Иногда", "Часто", "Постоянно"],
                "scores": [0, 1, 2, 3, 4]
            },
            {
                "text": "Есть ли у вас проблемы со сном?",
                "options": ["Никогда", "Редко", "Иногда", "Часто", "Постоянно"],
                "scores": [0, 1, 2, 3, 4]
            },
            {
                "text": "Испытываете ли вы усталость?",
                "options": ["Никогда", "Редко", "Иногда", "Часто", "Постоянно"],
                "scores": [0, 1, 2, 3, 4]
            }
        ],
        "interpretation": {
            (0, 4): {"level": "Норма", "emoji": "😊", "advice": "Отличное состояние!"},
            (5, 8): {"level": "Легкая", "emoji": "😐", "advice": "Возможен стресс"},
            (9, 12): {"level": "Умеренная", "emoji": "😔", "advice": "Рекомендуем отдых"},
            (13, 20): {"level": "Высокая", "emoji": "😢", "advice": "Обратитесь к специалисту"}
        }
    },
    "anxiety": {
        "title": "😰 Тест на тревожность",
        "description": "Оценка уровня тревоги",
        "questions": [
            {
                "text": "Беспокоитесь ли вы без причины?",
                "options": ["Никогда", "Редко", "Иногда", "Часто", "Постоянно"],
                "scores": [0, 1, 2, 3, 4]
            },
            {
                "text": "Чувствуете ли вы напряжение?",
                "options": ["Никогда", "Редко", "Иногда", "Часто", "Постоянно"],
                "scores": [0, 1, 2, 3, 4]
            }
        ],
        "interpretation": {
            (0, 3): {"level": "Норма", "emoji": "😊", "advice": "Все отлично!"},
            (4, 6): {"level": "Легкая", "emoji": "😐", "advice": "Небольшое волнение"},
            (7, 8): {"level": "Умеренная", "emoji": "😔", "advice": "Нужно расслабиться"},
            (9, 20): {"level": "Высокая", "emoji": "😢", "advice": "Рекомендуем консультацию"}
        }
    }
}


# ===== ФУНКЦИИ =====
def show_main_menu():
    st.markdown('<h1 class="main-header">🧠 PsychoTest Pro</h1>', unsafe_allow_html=True)
    st.write("Выберите тест для прохождения:")

    for test_key, test_data in TESTS.items():
        with st.container():
            st.markdown(f"""
                <div class="test-card">
                    <h3>{test_data['title']}</h3>
                    <p>{test_data['description']}</p>
                </div>
            """, unsafe_allow_html=True)

            if st.button("Начать тест", key=f"btn_{test_key}"):
                st.session_state.current_test = test_key
                st.session_state.current_question = 0
                st.session_state.answers = []
                st.session_state.scores = []
                st.rerun()


def run_test():
    test_key = st.session_state.current_test
    test = TESTS[test_key]

    st.title(test["title"])
    st.progress(st.session_state.current_question / len(test["questions"]))

    if st.session_state.current_question < len(test["questions"]):
        question = test["questions"][st.session_state.current_question]

        st.markdown(f"### Вопрос {st.session_state.current_question + 1} из {len(test['questions'])}")
        st.markdown(f"{question['text']}")

        answer = st.radio("Выберите ответ:", question["options"], key=f"q{st.session_state.current_question}")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Следующий вопрос →" if st.session_state.current_question < len(
                    test["questions"]) - 1 else "Завершить тест ✅"):
                score_index = question["options"].index(answer)
                st.session_state.answers.append(answer)
                st.session_state.scores.append(question["scores"][score_index])
                st.session_state.current_question += 1
                st.rerun()
    else:
        show_results(test)


def show_results(test):
    total_score = sum(st.session_state.scores)

    # Находим результат
    result = None
    for score_range, interpretation in test["interpretation"].items():
        if score_range[0] <= total_score <= score_range[1]:
            result = interpretation
            break

    # Показываем красивые результаты
    st.balloons()
    st.markdown(f"""
        <div class="result-box">
            <h2>{result['emoji']} Ваш результат: {total_score} баллов</h2>
            <h3>{result['level']} уровень</h3>
            <p>{result['advice']}</p>
        </div>
    """, unsafe_allow_html=True)

    # График
    df = pd.DataFrame({
        'Вопрос': [f"Вопр. {i + 1}" for i in range(len(st.session_state.scores))],
        'Баллы': st.session_state.scores
    })

    fig = px.bar(df, x='Вопрос', y='Баллы', title='Результаты по вопросам')
    st.plotly_chart(fig)

    # Таблица ответов
    st.write("### Ваши ответы:")
    results_df = pd.DataFrame({
        'Вопрос': [q['text'] for q in test['questions']],
        'Ответ': st.session_state.answers,
        'Баллы': st.session_state.scores
    })
    st.dataframe(results_df, use_container_width=True)

    if st.button("🔄 Выбрать другой тест"):
        for key in ['current_test', 'current_question', 'answers', 'scores']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

# ===== ЗАПУСК ПРИЛОЖЕНИЯ =====
def main():
    if 'current_test' not in st.session_state:
        show_main_menu()
    else:
        run_test()


if __name__ == "__main__":
    main()