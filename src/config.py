import streamlit as st

def setup_page():
    st.set_page_config(
        page_title="PsychoTest Pro",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def load_styles():

    st.markdown("""
    <style>
        .main-header {
            font-size: 3rem;
            color: #6a5acd;
            text-align: center;
            margin-bottom: 2rem;
            font-weight: bold;
        }
        .theme-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 20px;
            color: white;
            margin: 1.5rem 0;
            transition: transform 0.3s ease;
            text-align: center;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        }
        .theme-card:hover {
            transform: translateY(-8px);
        }
    .test-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        transition: transform 0.3s ease;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        height: 220px; /* 👈 ФИКСИРОВАННАЯ ВЫСОТА */
        display: flex;
        flex-direction: column;
        justify-content: space-between; /* Кнопка внизу, заголовок и описание сверху */
        overflow: hidden; /* Чтобы ничего не вылезало */
    }

    .test-card h4 {
        margin: 0 0 0.5rem 0;
        font-size: 1.2rem;
        font-weight: bold;
        line-height: 1.3;
    }

    .test-card p {
        margin: 0;
        font-size: 0.95rem;
        line-height: 1.5;
        flex-grow: 1; /* Занимает всё свободное пространство между заголовком и кнопкой */
        overflow-y: auto; /* 👈 ВКЛЮЧАЕМ СКРОЛЛ ПРИ ПЕРЕПОЛНЕНИИ */
        padding-right: 5px; /* Чтобы скролл не мешал тексту */
        scrollbar-width: thin; /* Для Firefox */
        scrollbar-color: rgba(255,255,255,0.5) transparent; /* Цвет скролла */
    }

    .test-card p::-webkit-scrollbar {
        width: 6px;
    }

    .test-card p::-webkit-scrollbar-track {
        background: transparent;
    }

    .test-card p::-webkit-scrollbar-thumb {
        background: rgba(255,255,255,0.4);
        border-radius: 3px;
    }

    .test-card button {
        margin-top: 1rem;
        width: 100%;
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
            margin: 2rem 0;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        }
    </style>
    """, unsafe_allow_html=True)