import streamlit as st
from PIL import Image
import numpy as np
from utils.align_image import detect_and_align&#8203;:contentReference[oaicite:0]{index=0}

:contentReference[oaicite:1]{index=1}&#8203;:contentReference[oaicite:2]{index=2}

:contentReference[oaicite:3]{index=3}&#8203;:contentReference[oaicite:4]{index=4}

:contentReference[oaicite:5]{index=5}&#8203;:contentReference[oaicite:6]{index=6}

:contentReference[oaicite:7]{index=7}&#8203;:contentReference[oaicite:8]{index=8}

# :contentReference[oaicite:9]{index=9}
:contentReference[oaicite:10]{index=10}&#8203;:contentReference[oaicite:11]{index=11}

:contentReference[oaicite:12]{index=12}
    uploaded_file = st.file_uploader("📁 Enviar imagem", type=["jpg", "jpeg", "png"])

:contentReference[oaicite:13]{index=13}
    camera_image = st.camera_input("📷 Tirar foto")

:contentReference[oaicite:14]{index=14}&#8203;:contentReference[oaicite:15]{index=15}

:contentReference[oaicite:16]{index=16}
    image = Image.open(uploaded_file)
    image_np = np.array(image)
:contentReference[oaicite:17]{index=17}
    image = Image.open(camera_image)
    image_np = np.array(image)

:contentReference[oaicite:18]{index=18}
    st.markdown("### Etapa 2: Alinhando a imagem do gabarito...")
    try:
        aligned_image = detect_and_align(image_np)
        st.image(aligned_image, caption="Imagem Alinhada", use_column_width=True)
        st.success("✅ Imagem alinhada com sucesso!")
        # Aqui você pode adicionar a próxima etapa, como a marcação do gabarito
    except Exception as e:
        st.error(f"❌ Erro ao alinhar a imagem: {e}")
