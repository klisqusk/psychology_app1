import streamlit as st
from themes import THEMES


def run_test():
    theme_key = st.session_state.current_theme
    test_key = st.session_state.current_test
    test = THEMES[theme_key]["tests"][test_key]
    total_questions = len(test["questions"])
    current_q = st.session_state.current_question

    if current_q < 0:
        st.session_state.current_question = 0
        st.rerun()
    elif current_q >= total_questions:
        st.session_state.current_question = total_questions - 1
        st.rerun()

    st.title(test["title"])
    st.progress(current_q / total_questions)

    question = test["questions"][current_q]

    st.markdown(f"### Вопрос {current_q + 1} из {total_questions}")
    st.markdown(f"**{question['text']}**")

    if len(st.session_state.answers) > current_q:
        prev_answer = st.session_state.answers[current_q]
        selected_index = question["options"].index(prev_answer)
    else:
        selected_index = 0

    answer = st.radio(
        "Выберите ответ:",
        question["options"],
        index=selected_index,
        key=f"q{current_q}"
    )

    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])

    if current_q > 0:
        with col1:
            if st.button("← Назад", key=f"btn_back_{current_q}", use_container_width=True):
                st.session_state.answers.pop()
                st.session_state.scores.pop()
                st.session_state.current_question -= 1
                st.rerun()

    with col2:
        if current_q == total_questions - 1:
            btn_text = "✅ Завершить тест"
        else:
            btn_text = "→ Следующий вопрос"

        if st.button(btn_text, key=f"btn_next_{current_q}", use_container_width=True):
            score_index = question["options"].index(answer)
            if len(st.session_state.answers) > current_q:
                st.session_state.answers[current_q] = answer
                st.session_state.scores[current_q] = question["scores"][score_index]
            else:
                st.session_state.answers.append(answer)
                st.session_state.scores.append(question["scores"][score_index])

            if current_q == total_questions - 1:
                st.session_state.current_question = total_questions
                st.rerun()
            else:
                st.session_state.current_question += 1
                st.rerun()