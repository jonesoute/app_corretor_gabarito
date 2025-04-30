import streamlit as st
from PIL import Image
import numpy as np
import cv2
import json
import os

st.set_page_config(page_title="Configurar Gabarito", layout="centered")
st.title("🛠️ Configurar Gabarito Base")

# Etapa 1: Upload da imagem do gabarito base
uploaded_file = st.file_uploader("📁 Envie a imagem do gabarito base", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)
    st.image(image, caption="Gabarito Base", use_column_width=True)

    # Etapa 2: Seleção das respostas corretas
    st.markdown("### 🖱️ Selecione as respostas corretas clicando na imagem abaixo.")
    coords = []

    if 'coords' not in st.session_state:
        st.session_state.coords = []

    def click_event(e):
        st.session_state.coords.append((e.x, e.y))

    st.image(image, caption="Clique nas respostas corretas", use_column_width=True)
    st.markdown("Clique na imagem para selecionar as respostas corretas.")

    # Etapa 3: Detecção dos marcadores para alinhamento
    st.markdown("### 🔍 Detecção dos marcadores para alinhamento")
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray, 2, 3, 0.04)

    # Dilate result to mark the corners
    dst = cv2.dilate(dst, None)

    # Threshold for an optimal value; it may vary depending on the image.
    image_np[dst > 0.01 * dst.max()] = [255, 0, 0]
    st.image(image_np, caption="Marcadores detectados", use_column_width=True)

    # Etapa 4: Salvar configurações
    if st.button("💾 Salvar configurações"):
        configuracao = {
            "respostas_certas": st.session_state.coords,
            "marcadores": dst.tolist()
        }
        with open("configuracao_gabarito.json", "w") as f:
            json.dump(configuracao, f)
        st.success("Configurações salvas com sucesso!")
