import streamlit as st
from PIL import Image
import numpy as np
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title="Corretor de Gabarito", layout="wide")
st.title("📌 Corretor de Gabarito")

st.markdown("## 👆 Clique em 'Enviando Gabarito Oficial'")

# Escolha entre tirar foto ou fazer upload
opcao = st.radio("Como deseja enviar a imagem do gabarito?", ["📸 Tirar Foto (Câmera)", "📁 Fazer Upload"], horizontal=True)

# Lê a imagem dependendo da opção
imagem = None
if opcao == "📁 Fazer Upload":
    uploaded_image = st.file_uploader("Faça o upload da imagem do gabarito oficial", type=["png", "jpg", "jpeg"])
    if uploaded_image is not None:
        imagem = Image.open(uploaded_image)
        st.image(imagem, caption="Imagem enviada", use_column_width=True)

elif opcao == "📸 Tirar Foto (Câmera)":
    camera_image = st.camera_input("Tire uma foto com o gabarito oficial")
    if camera_image is not None:
        imagem = Image.open(camera_image)
        st.image(imagem, caption="Foto tirada", use_column_width=True)

# Se a imagem estiver carregada, permite clicar nos círculos
if imagem is not None:
    st.markdown("## 🖱️ Clique sobre os círculos corretos para marcar as respostas do gabarito")
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=3,
        stroke_color="#FF0000",
        background_image=imagem,
        update_streamlit=True,
        height=imagem.height,
        width=imagem.width,
        drawing_mode="circle",
        key="canvas",
    )

    if st.button("Salvar Gabarito Base"):
        if canvas_result.json_data is not None:
            st.success("✔️ Gabarito base salvo com sucesso (simulação)!")
        else:
            st.warning("⚠️ Você ainda não marcou nenhuma resposta no gabarito.")
