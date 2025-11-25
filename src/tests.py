import streamlit as st
from themes import THEMES


def show_theme_tests():
    theme_key = st.session_state.current_theme
    theme = THEMES[theme_key]

    # ⚙️ Светло-бежевый фон и тёмно-серый текст на страницах с тестами
    st.markdown("""
        <style>
        .stApp {
            background-color: #F7F3ED; /* очень светлый бежевый */
        }

        /* Основные надписи на страницах тестов */
        h1, h2, h3, h4, p {
            color: #333333;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title(theme["name"])
    st.subheader(theme["description"])
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    tests_list = list(theme["tests"].items())

    for idx, (test_key, test_data) in enumerate(tests_list):
        with [col1, col2, col3][idx % 3]:
            st.markdown(f"""
                <div class="test-card">
                    <h4>{test_data['title']}</h4>
                    <p>{test_data['description']}</p>
                </div>
            """, unsafe_allow_html=True)

            if st.button("👉 Пройти тест", key=f"btn_test_{theme_key}_{test_key}"):
                st.session_state.current_test = test_key
                st.session_state.current_question = 0
                st.session_state.answers = []
                st.session_state.scores = []
                st.rerun()

    if st.button("← Вернуться к темам"):
        del st.session_state.current_theme
        st.rerun()
