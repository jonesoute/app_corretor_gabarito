import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import io

st.set_page_config(page_title="Gabarito Oficial", layout="wide")

st.title("📄 Enviando Gabarito Oficial")
st.write("Envie uma imagem ou tire uma foto do gabarito em branco e clique sobre os círculos corretos.")

# --- Opção de envio da imagem ---
upload_option = st.radio("Escolha como enviar a imagem:", ("📁 Fazer upload", "📷 Usar câmera"))

image_data = None

if upload_option == "📁 Fazer upload":
    uploaded_file = st.file_uploader("Envie o gabarito em branco", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image_data = uploaded_file.read()

elif upload_option == "📷 Usar câmera":
    if st.button("Ativar câmera"):
        camera_photo = st.camera_input("Tire uma foto do gabarito")
        if camera_photo:
            image_data = camera_photo.getvalue()

# --- Se imagem disponível, mostrar e permitir seleção interativa ---
if image_data:
    image = Image.open(io.BytesIO(image_data))

    st.markdown("### 🖍️ Clique nos círculos corretos do gabarito")

    canvas_result = st_canvas(
        fill_color="rgba(0, 255, 0, 0.3)",
        stroke_width=2,
        stroke_color="green",
        background_image=image,
        update_streamlit=True,
        height=image.height,
        width=image.width,
        drawing_mode="point",
        key="canvas",
    )

    if canvas_result.json_data:
        st.success("Você selecionou as posições corretas do gabarito.")
        st.json(canvas_result.json_data)
