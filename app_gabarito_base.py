import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import json
import os

st.set_page_config(page_title="Enviar Gabarito Oficial", layout="wide")
st.title("📌 Enviando Gabarito Oficial")

# Armazena os pontos clicados
if "pontos_gabarito" not in st.session_state:
    st.session_state.pontos_gabarito = []

# Carregar imagem
input_option = st.radio("Selecione o modo de envio da imagem:", ["Upload da imagem", "Tirar uma foto"])
uploaded_file = None

if input_option == "Upload da imagem":
    uploaded_file = st.file_uploader("Envie o gabarito oficial", type=["png", "jpg", "jpeg"])
else:
    uploaded_file = st.camera_input("Tire uma foto do gabarito oficial")

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagem enviada", use_column_width=True)

    # Canvas para desenhar e registrar cliques
    canvas_result = st_canvas(
        fill_color="rgba(255, 0, 0, 0.5)",
        stroke_width=2,
        background_image=image,
        update_streamlit=True,
        height=image.height,
        width=image.width,
        drawing_mode="point",
        point_display_radius=8,
        key="canvas_gabarito"
    )

    # Botão para registrar clique
    if canvas_result.json_data is not None:
        objects = canvas_result.json_data.get("objects", [])
        st.session_state.pontos_gabarito = [{"x": obj["left"], "y": obj["top"]} for obj in objects if obj["type"] == "circle"]

    # Exibir pontos marcados
    st.markdown("### Questões marcadas:")
    for i, ponto in enumerate(st.session_state.pontos_gabarito):
        st.write(f"Questão {i + 1}: (x={int(ponto['x'])}, y={int(ponto['y'])})")

    # Botão para salvar gabarito
    if st.button("💾 Salvar Gabarito Oficial"):
        if len(st.session_state.pontos_gabarito) == 0:
            st.warning("Nenhum ponto foi marcado.")
        else:
            gabarito = {"questoes": st.session_state.pontos_gabarito}
            with open("gabarito_oficial.json", "w") as f:
                json.dump(gabarito, f, indent=4)
            st.success("✅ Gabarito oficial salvo com sucesso como 'gabarito_oficial.json'.")
