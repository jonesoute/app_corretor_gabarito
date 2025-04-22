import streamlit as st
from PIL import Image
import numpy as np
from utils.align_image import detect_and_align&#8203;:contentReference[oaicite:0]{index=0}

:contentReference[oaicite:1]{index=1}&#8203;:contentReference[oaicite:2]{index=2}

st.title("📄 Enviando Gabarito Oficial")&#8203;:contentReference[oaicite:3]{index=3}

st.markdown("### Etapa 1: Envie ou capture a imagem do gabarito")&#8203;:contentReference[oaicite:4]{index=4}

:contentReference[oaicite:5]{index=5}&#8203;:contentReference[oaicite:6]{index=6}

# :contentReference[oaicite:7]{index=7}
:contentReference[oaicite:8]{index=8}&#8203;:contentReference[oaicite:9]{index=9}

:contentReference[oaicite:10]{index=10}
    uploaded_file = st.file_uploader("📁 Enviar imagem", type=["jpg", "jpeg", "png"])

:contentReference[oaicite:11]{index=11}
    camera_image = st.camera_input("📷 Tirar foto")

:contentReference[oaicite:12]{index=12}&#8203;:contentReference[oaicite:13]{index=13}

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
