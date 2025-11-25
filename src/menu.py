import streamlit as st
from themes import THEMES


def show_main_menu():
    # ⚙️ Стили только для главной страницы
    st.markdown("""
        <style>
        /* Заголовок PsychoTest Pro тёмно-серый */
        .main-header {
            color: #333333 !important;
        }

        /* Заголовки и описания карточек тем тоже тёмно-серые */
        .theme-card h3,
        .theme-card p {
            color: #333333 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="main-header">🧠 PsychoTest Pro</h1>', unsafe_allow_html=True)
    st.write("Выберите тему для прохождения теста:")

    for theme_key, theme_data in THEMES.items():
        with st.container():
            st.markdown(f"""
                <div class="theme-card">
                    <h3>{theme_data['name']}</h3>
                    <p>{theme_data['description']}</p>
                </div>
            """, unsafe_allow_html=True)

            if st.button("Выбрать тему", key=f"btn_theme_{theme_key}"):
                st.session_state.current_theme = theme_key
                if 'current_test' in st.session_state:
                    del st.session_state.current_test
                if 'current_question' in st.session_state:
                    del st.session_state.current_question
                if 'answers' in st.session_state:
                    del st.session_state.answers
                if 'scores' in st.session_state:
                    del st.session_state.scores
                st.rerun()
