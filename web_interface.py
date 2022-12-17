import streamlit as st
from tika import parser
from model import DocClassifier
import pickle
from pathlib import Path
import json

with open("model3.pkl", 'rb') as f:
         cl = pickle.load(f)

@st.cache
def parse_doc(doc):
    parsed = parser.from_file(uploaded_file)
    return parsed["content"]        

def define_doc_state(doc):

    with open(doc.name,"wb") as f:
         f.write(doc.getbuffer())

    result = cl.get_dict(doc.name)
    cl.pdf_viz(doc.name)
    json_data = json.dumps(result)


    return json_data
    
st.markdown("<h1 style='text-align: center;'> Определение вида договора </h1>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Выберите файл", type=["doc", "docx", "pdf", "rtf"], accept_multiple_files=False)
if uploaded_file:
    result = """
            Такой результат получен из-за того, что Вы не нажали кнопку 'Определить'.
            Вернитесь на сайт и попробуйте снова
             """
    st.success("Файл успешно загружен", icon="✅")
    define_button_state = st.button("Определить")
    if define_button_state:
        short_result = define_doc_state(uploaded_file)
        st.success("Вид договора успешно определён", icon="✅")
        st.markdown("Краткие результаты")
        st.json(short_result)
        result="PREDICTED"
        download_button_state = st.download_button(label="Загрузить результаты", data=open("output.pdf", "rb"), file_name="output.pdf")
    


else:
     st.error("Вы ничего не вабрали", icon="🚨")

st.markdown("<h5 style='text-align: center; color: white;'> Навязчивые мысли </h5>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: white;'> 2022 </h5>", unsafe_allow_html=True)