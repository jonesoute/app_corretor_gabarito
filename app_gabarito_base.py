import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import json

st.set_page_config(page_title="Criar Gabarito Base", layout="centered")

st.title("📸 Criar Gabarito Base por Clique")

# Etapa 1: Upload ou captura de imagem do gabarito em branco
st.subheader("1. Envie uma imagem do gabarito em branco")

uploaded_file = st.file_uploader("Escolha uma imagem do gabarito (sem marcações)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Gabarito enviado", use_column_width=True)

    # Etapa 2: Área clicável sobre a imagem
    st.subheader("2. Clique nas alternativas corretas da imagem")

    canvas_result = st_canvas(
        fill_color="rgba(0, 255, 0, 0.3)",  # verde transparente
        stroke_width=2,
        background_image=image,
        update_streamlit=True,
        height=image.height,
        width=image.width,
        drawing_mode="point",
        point_display_radius=10,
        key="canvas",
    )

    # Etapa 3: Mostrar pontos clicados
    if canvas_result.json_data is not None:
        objects = canvas_result.json_data["objects"]
        pontos = [(int(obj["left"]), int(obj["top"])) for obj in objects]
        st.success(f"{len(pontos)} alternativas corretas marcadas.")
        st.write("Coordenadas:", pontos)

        if st.button("Salvar gabarito"):
            with open("gabarito_base.json", "w") as f:
                json.dump(pontos, f)
            st.success("Gabarito salvo com sucesso!")
