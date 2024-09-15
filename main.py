# main_app.py
import streamlit as st
from src.data_store import transformer_models, sports_list, sport_function_map
from src.styles import load_custom_styles
from src.instructions import show_instructions
from src.about_us import show_about_us


# Set page configurations and custom styles
st.set_page_config(page_title='SportiNetAI', layout='wide')

st.markdown(load_custom_styles(), unsafe_allow_html=True)
# Main content
def main():
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<h1 style='text-align: center; margin-top: 0px'>SportiNetAI</h1>", unsafe_allow_html=True)
    st.markdown("<div style='margin-top: 80px;'></div>", unsafe_allow_html=True)

# Sidebar content
def sidebar():
    st.sidebar.header("Model:")
    selected_model = st.sidebar.selectbox("Select Transformer Model:", transformer_models, index=0)

    sports_list_full = ["None"] + sports_list
    sport_selected = st.sidebar.selectbox("Choose a Sport", sports_list_full, index=0)

    if sport_selected == "None":
        show_instructions()
        show_about_us()
    elif sport_selected in sport_function_map:
        # Call the function associated with the selected sport
        sport_function_map[sport_selected]()


    st.sidebar.header("Adjust Parameters")
    slider1 = st.sidebar.slider("Slider 1", 0, 100, 25)
    slider2 = st.sidebar.slider("Slider 2", 0, 200, 100)
    slider3 = st.sidebar.slider("Slider 3", 0, 300, 150)

# Call the main content and sidebar functions
main()
sidebar()
