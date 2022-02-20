import streamlit as st
from pathlib import Path

from utils import image_button_config
from prettybasicmaps.main import get_geometries
from prettybasicmaps.plotting import plot


# TODO: Empty container so that old content isnt shown while updating

EXAMPLES = {
    "Macau": "macao.png",
    "Palma Nova": "palmanova.png",
    "Barcelona": "barcelona.png",
    "Erbil": "erbil.png",
    "Cidadebaixa": "bomfim-farroupilha-cidadebaixa.png",
}

_location_ = Path(__file__).resolve().parent


st.markdown("# Pretty(basic)maps")
st.write("")


example_buttons = []
image_button_config()
example_cols = st.columns(5)
for example_name, example_col in zip(EXAMPLES.keys(), example_cols):
    # example_col.image(str(_location_ / "prints" / EXAMPLES[example_name]))
    example_buttons.append(example_col.button(example_name))


st.write("")
form = st.form(key="form_params")
form.markdown("**Or choose your own location & map style**")
col1, col2, col3 = form.columns([2, 1, 1])

address = col1.text_input(
    "Address or Location",
    "Praça Ferreira do Amaral, Macau",
)
radius = col2.slider("Radius Size", 1, 1500, 1100)

style = col3.selectbox("Map Style", ["1", "2", "3"])

expander = form.expander("More map style options")
col1style, col2style, col3style = expander.columns(3)


rectangular = col1style.checkbox("Rectangular map", False)
# = expander.checkbox("Location text")
description = False
background_color = col2style.color_picker("Background color")


submit_button = form.form_submit_button(label="Submit")

st.markdown("---")

if submit_button:
    # Activated exampled
    with st.spinner("Creating new map..."):
        result_container = st.container()
        df = get_geometries(
            address, radius=radius, rectangular=rectangular
        )  # show_description=description, background_color=background_color
        fig = plot(df, drawing_kwargs=DRAW_SETTINGS)
        result_container.pyplot(fig)
else:
    # Prerendered examples
    if not any(example_buttons):
        active_example_name = "Macau"
    else:
        active_example_name = list(EXAMPLES.keys())[example_buttons.index(True)]
    st.image(str(_location_ / "prints" / EXAMPLES[active_example_name]))
    st.write(active_example_name)
