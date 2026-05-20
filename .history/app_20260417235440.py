import streamlit as st
from qa_system import get_answer

st.title("📊 Анализ отчетов Национального банка")

question = st.text_input("Задайте вопрос:")

if question:
    answer = get_answer(question)
    st.subheader("Ответ:")
    st.write(answer)