import streamlit as st
from qa_system import get_answer

st.set_page_config(page_title="Банк Аналитик", layout="wide")

st.title("📊 Анализ отчетов Национального банка")
st.markdown("Задайте вопрос по загруженным документам, и система найдет наиболее подходящие фрагменты.")

question = st.text_input("Введите ваш вопрос:", placeholder="Например: Какова инфляция в 2023 году?")

if question:
    with st.spinner('Поиск информации...'):
        try:
            answer = get_answer(question)
            st.subheader("Найденная информация:")
            st.info(answer)
        except Exception as e:
            st.error(f"Произошла ошибка: {e}")

