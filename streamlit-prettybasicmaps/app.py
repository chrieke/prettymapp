import streamlit as st
from matplotlib.figure import Figure
from examples import EXAMPLES
from utils import image_button_config
from prettybasicmaps.main import get_geometries
from prettybasicmaps.plotting import Plot
from prettybasicmaps.settings import DRAW_SETTINGS


# Enabling streamlit caching for imports
get_geometries = st.experimental_memo(show_spinner=False)(get_geometries)
# todo: effect?
st.experimental_memo(show_spinner=False)


def st_plot_all(**kwargs):
    fig = Plot(**kwargs).plot_all()
    return fig


if "settings" not in st.session_state:
    st.session_state.settings = EXAMPLES["Macau"]

st.set_page_config(
    page_title="prettybasicmaps", page_icon="🚀", initial_sidebar_state="collapsed"
)
st.markdown("# Pretty(basic)maps")
st.write("")

example_buttons = []
image_button_config()
example_cols = st.columns(5)
for example_name, example_col in zip(EXAMPLES.keys(), example_cols):
    example_buttons.append(example_col.button(example_name))
if any(example_buttons):
    selected_example = list(EXAMPLES.keys())[example_buttons.index(True)]
    st.session_state.settings = EXAMPLES[selected_example]
st.write("")

form = st.form(key="form_params")
form.markdown("**Or choose your own location & map style**")
col1, col2, col3 = form.columns([3, 1, 1])

address = col1.text_input("Address or Location", st.session_state.settings["address"])

style = col2.selectbox(
    "Map Style",
    list(DRAW_SETTINGS.keys()),
    list(DRAW_SETTINGS.keys()).index(st.session_state.settings["style"]),
)
radius = col3.slider("Radius Size", 1, 1500, st.session_state.settings["radius"])


expander = form.expander("More map style options")
col1style, col2style, col3style = expander.columns(3)
shape_options = ["circle", "rectangle"]
shape = col1style.radio(
    "Map Shape",
    options=shape_options,
    index=shape_options.index(st.session_state.settings["shape"]),
)
bg_shape_options = ["rectangle", "circle", None]
bg_shape = col1style.radio(
    "Background",
    options=bg_shape_options,
    index=bg_shape_options.index(st.session_state.settings["bg_shape"]),
)
bg_buffer = col1style.slider(
    "Background Buffer", 0, 50, st.session_state.settings["bg_buffer"]
)
bg_color = col1style.color_picker(
    "Background Color", st.session_state.settings["bg_color"]
)

name_on = col2style.checkbox("Add Location Name", st.session_state.settings["name_on"])
custom_title = col2style.text_input(
    "Use custom title instead", st.session_state.settings["custom_title"], max_chars=30
)
font_size = col2style.slider("Font Size", 1, 50, st.session_state.settings["font_size"])
font_color = col2style.color_picker(
    "Font Color", st.session_state.settings["font_color"]
)
text_x = col2style.slider(
    "Text left/right", -100, 100, st.session_state.settings["text_x"]
)
text_y = col2style.slider(
    "Text top/bottom", -100, 100, st.session_state.settings["text_y"]
)
text_rotation = col2style.slider(
    "Text rotation", -90, 90, st.session_state.settings["text_rotation"]
)

vars = [
    address,
    radius,
    style,
    shape,
    name_on,
    custom_title,
    font_size,
    font_color,
    text_x,
    text_y,
    text_rotation,
    bg_shape,
    bg_buffer,
    bg_color,
]

submit_button = form.form_submit_button(label="Submit")
if submit_button:
    # Submit saves to session state from where the values are used.
    # TODO: second submit button click does not update session state?
    for var in vars:
        var_name = f"{var=}".split("=")[0]
        st.session_state.settings[var_name] = var

result_container = st.empty()
with st.spinner("Creating new map...(may take up to a minute)"):
    rectangular = shape != "circle"
    df = get_geometries(address=address, radius=radius, rectangular=rectangular)

    fig = st_plot_all(
        df=df,
        drawing_kwargs=DRAW_SETTINGS[style],
        name_on=name_on,
        name=address if custom_title == "" else custom_title,
        font_size=font_size,
        font_color=font_color,
        text_x=text_x,
        text_y=text_y,
        text_rotation=text_rotation,
        bg_shape=bg_shape,
        bg_buffer=bg_buffer,
        bg_color=bg_color,
    )

    result_container.pyplot(fig, pad_inches=0, bbox_inches="tight", transparent=True)

st.write("")
st.markdown("Share your map on social media using the hashtag **#prettymaps**")
