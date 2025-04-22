import streamlit as st
from PIL import Image
import numpy as np
import cv2
from utils.align_image import detect_and_align

st.set_page_config(page_title="Enviando Gabarito Oficial", layout="centered")

st.title("📄 Enviando Gabarito Oficial")

st.markdown("### Etapa 1: Envie ou capture a imagem do gabarito")
st.markdown("Você pode **tirar uma foto** ou **enviar uma imagem existente** do gabarito.")

# Opções de envio
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("📁 Enviar imagem", type=["jpg", "jpeg", "png"])

with col2:
    camera_image = st.camera_input("📷 Tirar foto")

image_np = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    image_np = np.array(image)
elif camera_image is not None:
    image = Image.open(camera_image)
    image_np = np.array(image)

if image_np is not None:
    st.markdown("### Etapa 2: Alinhando a imagem do gabarito...")
    try:
        aligned_image = detect_and_align(image_np)
        st.image(aligned_image, caption="Imagem Alinhada", use_column_width=True)
        st.success("✅ Imagem alinhada com sucesso!")
        # Aqui você pode adicionar a próxima etapa, como a marcação do gabarito
    except Exception as e:
        st.error(f"❌ Erro ao alinhar a imagem: {e}")

