import streamlit as st
from pathlib import Path

from prettybasicmaps import main

# TODO: Empty container so that old content isnt shown while updating

EXAMPLES = {
    "Macau": "macao.png",
    "Palma Nova": "palmanova.png",
    "Barcelona": "barcelona.png",
    "Erbil": "erbil.png",
    "Cidadebaixa": "bomfim-farroupilha-cidadebaixa.png",
}

_location_ = Path(__file__).resolve().parent


st.title("🌆 Pretty(basic)maps")
st.write("")

example_buttons = []
example_cols = st.columns(5)
for example_name, example_col in zip(EXAMPLES.keys(), example_cols):
    example_col.image(str(_location_ / "prints" / EXAMPLES[example_name]))
    example_buttons.append(example_col.button(example_name))


st.write("")
form = st.form(key="form_params")
form.markdown("**Or select your own location & style**")
col1, col2, col3 = form.columns([1.5, 1, 0.5])

address = col1.text_input(
    "Enter address or location",
    "Praça Ferreira do Amaral, Macau",
)
radius = col1.slider("Select radius", 1, 1500, 1100)

style = col2.selectbox("Select style", ["1", "2", "3"])

expander = col2.expander("More styling options")
rectangular = expander.checkbox("Rectangular map", False)
#= expander.checkbox("Location text")
description=False
background_color = expander.color_picker("Background color")

submit_button = form.form_submit_button(label="Submit")

st.markdown("---")

if submit_button:
    # Activated exampled
    with st.spinner("Creating new map..."):
        result_container = st.container()
        fig = main.main(address, radius=radius, rectangular=rectangular) #show_description=description, background_color=background_color
        result_container.pyplot(fig)
else:
    # Prerendered examples
    if not any(example_buttons):
        active_example_name = "Macau"
    else:
        active_example_name = list(EXAMPLES.keys())[example_buttons.index(True)]
    st.image(str(_location_ / "prints" / EXAMPLES[active_example_name]))
    st.write(active_example_name)
