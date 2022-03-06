import streamlit as st


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
			[data-testid="stHorizontalBlock"] > div:nth-child(1) button:before  {
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
