import streamlit as st
from PIL import Image
import numpy as np
from utils.align_image import detect_and_align

st.set_page_config(page_title="Corretor de Gabarito", layout="centered")
st.title("📝 Corretor de Gabarito")

st.markdown("### Etapa 1: Enviar ou capturar imagem do gabarito")

# Inicializa a variável da imagem
image_np = None

# Opção de envio de imagem
uploaded_file = st.file_uploader("📁 Enviar imagem", type=["jpg", "jpeg", "png"])

# Botão para ativar a câmera
if st.button("📷 Tirar foto"):
    camera_image = st.camera_input("Capturar imagem")

    if camera_image is not None:
        image = Image.open(camera_image)
        image_np = np.array(image)

# Se uma imagem foi enviada via upload
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    image_np = np.array(image)

# Se uma imagem foi capturada ou enviada
if image_np is not None:
    st.markdown("### Etapa 2: Alinhando a imagem do gabarito...")
    try:
        aligned_image = detect_and_align(image_np)
        st.image(aligned_image, caption="Imagem Alinhada", use_column_width=True)
        st.success("✅ Imagem alinhada com sucesso!")
        # Aqui você pode adicionar a próxima etapa, como a marcação do gabarito
    except Exception as e:
        st.error(f"❌ Erro ao alinhar a imagem: {e}")
