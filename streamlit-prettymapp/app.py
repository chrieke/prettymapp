import copy

import streamlit as st
from streamlit_profiler import Profiler
from geopandas import GeoDataFrame
from pandas.util import hash_pandas_object

from examples import EXAMPLES
from utils import image_button_config, plt_to_svg, svg_to_html, slugify
from prettymapp.main import get_geometries
from prettymapp.plotting import Plot
from prettymapp.settings import STYLES

p = Profiler()
p.start()

# Wrappers for streamlit caching
get_geometries = st.experimental_memo(show_spinner=False)(get_geometries)


# pylint: disable=unused-argument
@st.experimental_memo(show_spinner=False)
def st_plot_all(_df: GeoDataFrame, df_hash: int, **kwargs):
    """
    Wrapper to enable streamlit caching. Unused argument df_hash required to have unique value that avoids using cache
    as streamlit is not able to hash the geodataframe.
    """
    fig = Plot(_df, **kwargs).plot_all()
    return fig


if "run_id" not in st.session_state:
    st.session_state.run_id = 0
    st.session_state.settings = EXAMPLES["Macau"]
    st.session_state.settings["draw_settings"] = STYLES["Peach"]  # type: ignore

st.set_page_config(
    page_title="prettymapp", page_icon="🚀", initial_sidebar_state="collapsed"
)
st.markdown("# Prettymapp")
st.write("")

example_buttons = []
image_button_config()
example_cols = st.columns(5)
for example_name, example_col in zip(EXAMPLES.keys(), example_cols):
    example_buttons.append(example_col.button(example_name))
selected_example = None
if any(example_buttons):
    # Reset settings for new example
    name_selected_example = list(EXAMPLES.keys())[example_buttons.index(True)]
    settings: dict = EXAMPLES[name_selected_example]  # type: ignore
    st.session_state.settings = settings.copy()
    st.session_state.settings["draw_settings"] = STYLES[settings["style"]].copy()

st.write("")
form = st.form(key="form_params")
form.markdown("**Or choose your own location & map style**")
col1, col2, col3 = form.columns([3, 1, 1])

address = col1.text_input("Address or Location", st.session_state.settings["address"])
radius = col2.slider("Radius Size", 1, 1500, st.session_state.settings["radius"])
style = col3.selectbox(
    "Color theme",
    list(STYLES.keys()),
    list(STYLES.keys()).index(st.session_state.settings["style"]),
)

expander = form.expander("More map style options")
col1style, col2style, _, col3style = expander.columns([2, 2, 0.1, 1])

shape_options = ["circle", "rectangle"]
shape = col1style.radio(
    "Map Shape",
    options=shape_options,
    index=shape_options.index(st.session_state.settings["shape"]),
)
contour_width = col1style.slider(
    "Map contour width",
    0,
    20,
    st.session_state.settings["contour_width"],
    help="Thickness of contour line sourrounding the map.",
    key=f"contour_{st.session_state.run_id}",
)
contour_color = col1style.color_picker(
    "Map contour color", st.session_state.settings["contour_color"]
)
col1style.markdown("---")

bg_shape_options = ["rectangle", "circle", None]
bg_shape = col1style.radio(
    "Background Shape",
    options=bg_shape_options,
    index=bg_shape_options.index(st.session_state.settings["bg_shape"]),
)
bg_color = col1style.color_picker(
    "Background Color", st.session_state.settings["bg_color"]
)
bg_buffer = col1style.slider(
    "Background Size",
    0,
    50,
    st.session_state.settings["bg_buffer"],
    help="How much the background extends beyond the figure.",
)

name_on = col2style.checkbox(
    "Add Location Name",
    st.session_state.settings["name_on"],
    help="If checked, adds the "
    "selected address as the title. "
    "Can be customized below.",
)
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

col3style.write("Custom Colors")
if style != st.session_state.settings["style"]:
    # Ignore & reset custom colors if style changes
    desired_drawing_settings = copy.deepcopy(STYLES[style])
else:
    desired_drawing_settings = copy.deepcopy(st.session_state.settings["draw_settings"])
for lc_class, class_style in desired_drawing_settings.items():
    if "cmap" in class_style:
        for idx, color in enumerate(class_style["cmap"]):  # type: ignore
            picked_color = col3style.color_picker(f"{lc_class} {idx+1}", color)
            st.session_state.settings["draw_settings"][lc_class]["cmap"][
                idx
            ] = picked_color
    else:
        picked_color = col3style.color_picker(f"{lc_class}", class_style.get("fc"))
        st.session_state.settings["draw_settings"][lc_class]["fc"] = picked_color

variables = [
    address,
    radius,
    style,
    shape,
    contour_width,
    contour_color,
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

if st.button("Reset"):
    st.session_state.run_id += 1

submit_button = form.form_submit_button(label="Submit")
if submit_button:
    # Submit saves to session state from where the values are used.
    for var in variables:
        var_name = f"{var=}".split("=")[0]
        st.session_state.settings[var_name] = var

result_container = st.empty()
with st.spinner("Creating new map...(may take up to a minute)"):
    rectangular = shape != "circle"
    df = get_geometries(address=address, radius=radius, rectangular=rectangular)
    fig = st_plot_all(
        _df=df,
        df_hash=hash_pandas_object(df).sum(),
        draw_settings=st.session_state.settings["draw_settings"],
        name_on=name_on,
        name=address if custom_title == "" else custom_title,
        font_size=font_size,
        font_color=font_color,
        text_x=text_x,
        text_y=text_y,
        text_rotation=text_rotation,
        shape=shape,
        contour_width=contour_width,
        contour_color=contour_color,
        bg_shape=bg_shape,
        bg_buffer=bg_buffer,
        bg_color=bg_color,
    )

    svg_string = plt_to_svg(fig)
    html = svg_to_html(svg_string)
    result_container.write(html, unsafe_allow_html=True)
    # st.pyplot(fig, pad_inches=0, bbox_inches="tight", transparent=True)

st.write("")
download_expander = st.expander("Download")
if download_expander:
    st.download_button(
        label="SVG", data=svg_string, file_name=f"{slugify(address)}.svg"
    )
    # resolution = st.selectbox("Resolution", ["720", "1080"])
    # a = plt_to_href(fig, resolution, f"{slugify(address)}.svg", "PNG")
    # print(a)
    # st.markdown(a, unsafe_allow_html=True)

st.markdown("Share your map on social media!")

p.stop()
