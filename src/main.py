import streamlit as st
import pandas as pd

from themes import THEMES
from menu import show_main_menu
from tests import show_theme_tests
from runner import run_test
from results import show_results, show_results1
from config import setup_page, load_styles   # импортируем функции

# Настройка страницы и стилей
setup_page()
load_styles()



def main():
    if 'current_theme' not in st.session_state:
        show_main_menu()
    elif 'current_test' not in st.session_state:
        show_theme_tests()
    else:
        # Получаем текущий тест
        theme_key = st.session_state.current_theme
        test_key = st.session_state.current_test
        test = THEMES[theme_key]["tests"][test_key]
        total_questions = len(test["questions"])

        # Проверяем, завершен ли тест
        if 'current_question' not in st.session_state or st.session_state.current_question >= total_questions:
            # ✅ ВЫБОР ФУНКЦИИ РЕЗУЛЬТАТОВ В ЗАВИСИМОСТИ ОТ ТЕСТА
            if test_key == "decision_style_test":
                show_results1(theme_key, test_key)
            else:
                show_results(theme_key, test_key)
        else:
            run_test()


if __name__ == "__main__":
    main()