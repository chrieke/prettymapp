import streamlit as st

from utils import image_button_config, st_get_geometries, st_plot
from prettybasicmaps.settings import DRAW_SETTINGS

EXAMPLES = {
    "Macau": {
        "address": "Praça Ferreira do Amaral, Macau",
        "radius": 1500,
        "style": 1,
        "rectangular": False,
        "image": "macao.png",
    },
    "Palma Nova": {
        "address": "Keerkring 49, 1705 Heerhugowaard, Netherlands",
        "radius": 550,
        "style": 1,
        "rectangular": True,
        "image": "heerhugowaard.png",
    },
    "Barcelona": "barcelona.png",
    "Erbil": "erbil.png",
    "Cidadebaixa": "bomfim-farroupilha-cidadebaixa.png",
}
if "settings" not in st.session_state:
    st.session_state.settings = EXAMPLES["Macau"]

st.markdown("# Pretty(basic)maps")
st.write("")

example_buttons = []
image_button_config()
example_cols = st.columns(5)
for example_name, example_col in zip(EXAMPLES.keys(), example_cols):
    # example_col.image(str(_location_ / "prints" / EXAMPLES[example_name]))
    example_buttons.append(example_col.button(example_name))
if any(example_buttons):
    selected_example = EXAMPLES[list(EXAMPLES.keys())[example_buttons.index(True)]]
    st.session_state.settings = selected_example
st.write("")

form = st.form(key="form_params")
form.markdown("**Or choose your own location & map style**")
col1, col2, col3 = form.columns([3, 1, 1])

address = col1.text_input("Address or Location", st.session_state.settings["address"])
radius = col2.slider("Radius Size", 1, 1500, st.session_state.settings["radius"])
style = col3.selectbox("Map Style", [1, 2, 3], st.session_state.settings["style"])

expander = form.expander("More map style options")
col1style, col2style, col3style = expander.columns(3)
rectangular = col1style.checkbox(
    "Rectangular map", st.session_state.settings["rectangular"]
)
# = expander.checkbox("Location text")
description = False
background_color = col2style.color_picker("Background color")

submit_button = form.form_submit_button(label="Submit")
st.markdown("---")

if submit_button:
    st.session_state.settings["address"] = address
    st.session_state.settings["radius"] = radius
    st.session_state.settings["style"] = style
    st.session_state.settings["rectangular"] = rectangular

result_container = st.empty()
with st.spinner("Creating new map...(may take up to a minute)"):
    df = st_get_geometries(
        address=address, radius=radius, rectangular=rectangular
    )  # show_description=description, background_color=background_color
    fig = st_plot(df=df, drawing_kwargs=DRAW_SETTINGS)

    result_container.pyplot(fig)
