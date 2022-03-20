import base64
from io import StringIO, BytesIO
import unicodedata
import re

import streamlit as st


def plt_to_svg(fig):
    imgdata = StringIO()
    fig.savefig(
        imgdata, format="svg", pad_inches=0, bbox_inches="tight", transparent=True
    )
    imgdata.seek(0)
    svg_string = imgdata.getvalue()
    return svg_string


def svg_to_html(svg_string):
    b64 = base64.b64encode(svg_string.encode("utf-8")).decode("utf-8")
    # Add some CSS on top
    css_justify = "center"
    css = '<p style="text-align:center; display: flex; flex-direction: column; justify-content: {};">'.format(
        css_justify
    )
    html = r'{}<img src="data:image/svg+xml;base64,{}"/>'.format(css, b64)
    return html


def plt_to_href(fig, filename):
    buf = BytesIO()
    fig.savefig(buf, format="png", pad_inches=0, bbox_inches="tight", transparent=True)
    img_str = base64.b64encode(buf.getvalue()).decode()
    href = f'<a href="data:file/txt;base64,{img_str}" download="{filename}"></a>'
    return href


def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


def image_button_config():
    st.write(
        """
		<style>
			[data-testid="stHorizontalBlock"] button {
				width: 130px !important;
				height: 130px;
				padding: 0.1rem;
				font-weight: 600;
				font-size: 1.2rem;
				background-color: transparent;
				color: black;
				flex-grow:1;
				padding-top:102px;
			}
			[data-testid="stHorizontalBlock"] button:before {
				width: 130px;
				height: 130px;
				content: "";
				position: absolute;
				left: 0;
				top: 0;
				padding: 0.1rem;
				background-position: center; /* Center the image */
				background-repeat: no-repeat; /* Do not repeat the image */
				background-size: cover; /* Resize the background image to cover the entire container */
				background-origin: content-box;
				z-index: -1;
			}
			[data-testid="stHorizontalBlock"] button:hover:before {
				filter: blur(3px) brightness(1.05) saturate(0.3);
				-webkit-filter: blur(3px) brightness(1.05) saturate(0.3);
			}
			/* Required to create new stacking context in column, so that z-index on the before element works */
			[data-testid="stVerticalBlock"] {
				z-index: 0;
			}
			/* 1st button inside columns */
			[data-testid="stHorizontalBlock"] > div:nth-child(1) button:before {
				/*
				- Image URL must be a web address, not a local filepath(Streamlit doesn't serve local images on a static URL).
				- Must start with https:// or http://, otherwise it points to localhost.
				*/
				background-image: url("https://bit.ly/3pMzNIy");
			}
			/* 2nd button inside columns */
			[data-testid="stHorizontalBlock"] > div:nth-child(2) button:before  {
				background-image: url("https://bit.ly/3zhLfyH");
			}
		</style>
		""",
        unsafe_allow_html=True,
    )
