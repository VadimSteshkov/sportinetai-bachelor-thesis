import os
import joblib
import streamlit as st
from src.data_store import transformer_models, sports_list, sport_function_map
from src.styles import load_custom_styles
from src.instructions import show_instructions
from src.about_us import show_about_us


# Set page configurations and custom styles
st.set_page_config(page_title='SportiNetAI', layout='wide')
st.markdown(load_custom_styles(), unsafe_allow_html=True)


# Function to load available models from the 'models' directory
def load_models_from_directory():
    models_dir = './models'
    if os.path.exists(models_dir):
        return [f for f in os.listdir(models_dir) if f.endswith('.pkl')]
    return []


# Function for model selection and loading via sidebar
# Stores the selected and loaded model in Streamlit session state
def model_selection():
    st.sidebar.header("Model Selection")

    # Load available models from directory
    available_models = load_models_from_directory()
    if not available_models:
        st.sidebar.warning("No models found in the 'models' directory.")
        return None

    # Store selected and loaded model in session state
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = None
    if "loaded_model" not in st.session_state:
        st.session_state.loaded_model = None

    selected_model = st.sidebar.selectbox("Select a Model:", available_models, index=0)

    # Reset state if model changes
    if st.session_state.selected_model != selected_model:
        st.session_state.loaded_model = None
        st.session_state.selected_model = selected_model

    # Load the model when the button is pressed
    if st.sidebar.button("Load Selected Model") and st.session_state.loaded_model is None:
        try:
            model_path = os.path.join('./models', selected_model)
            st.session_state.loaded_model = joblib.load(model_path)
            st.sidebar.success(f"Model '{selected_model}' loaded successfully!")
        except Exception as e:
            st.sidebar.error(f"Error loading model: {e}")

    return st.session_state.loaded_model


# Main content area of the app
# Displays the app title and spacing
def main():
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<h1 style='text-align: center; margin-top: 0px'>SportiNetAI</h1>", unsafe_allow_html=True)
    st.markdown("<div style='margin-top: 80px;'></div>", unsafe_allow_html=True)


# Sidebar content and logic
# Includes toggles, model selection, and sport selection
# Calls the appropriate UI function for the selected sport
# Also shows instructions/about if no sport is selected
def sidebar():
    # Toggle for enabling/disabling name suggestion
    st.sidebar.header("Settings")
    if "enable_name_suggestion" not in st.session_state:
        st.session_state.enable_name_suggestion = True  # Enabled by default

    st.session_state.enable_name_suggestion = st.sidebar.toggle(
        "Enable Name Suggestion (Helps with Incorrect Spelling)",
        value=st.session_state.enable_name_suggestion
    )

    # Show current state of the toggle
    if st.session_state.enable_name_suggestion:
        st.sidebar.success("Name Suggestion is ENABLED.")
    else:
        st.sidebar.warning("Name Suggestion is DISABLED.")
    # Load model selection UI
    loaded_model = model_selection()

    # Sport selection dropdown
    sports_list_full = ["None"] + sports_list
    if "sport_selected" not in st.session_state:
        st.session_state.sport_selected = "None"
    sport_selected = st.sidebar.selectbox(
        "Choose a Sport", sports_list_full, index=sports_list_full.index(st.session_state.sport_selected)
    )

    st.session_state.sport_selected = sport_selected

    # Show instructions/about or call the selected sport's UI
    if sport_selected == "None":
        show_instructions()
        show_about_us()
    elif sport_selected in sport_function_map:
        # Call the function for the selected sport, passing the loaded model
        sport_function_map[sport_selected](loaded_model)

    return loaded_model


# Run the main content and sidebar logic
main()
loaded_model = sidebar()
