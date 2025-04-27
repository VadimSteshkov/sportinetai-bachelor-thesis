# data_store.py
import streamlit as st
import os
# from ui.UFC_UI import show_ufc_ui
from ui.Football_UI import show_football_ui
from ui.main_ufc_site import show_ufc_main

# Ensure that all necessary UI modules are imported here

# Example list of available transformer models (can be expanded)
transformer_models = ["None"]
# List of supported sports
sports_list = ["Football", "Basketball", "UFC"]

# Mapping sports to their respective UI functions
# Passes the loaded model to the corresponding UI function
sport_function_map = {
    "Football": lambda loaded_model: show_football_ui(),
    "Basketball": lambda loaded_model: st.write("Basketball UI not implemented yet"),
    # "UFC": show_ufc_ui,  # Passes the loaded model
    "UFC": show_ufc_main
}


# Function to load and display models in the sidebar
def load_model_ui():
    st.sidebar.header("Model Selection")

    # Specify the models directory
    models_dir = "models"

    # Check if the models directory exists
    if not os.path.exists(models_dir):
        st.sidebar.warning("No models directory found.")
        return None

    # Get the list of available models
    model_files = [file for file in os.listdir(models_dir) if file.endswith(".pkl")]

    # If no models found, display a message
    if not model_files:
        st.sidebar.warning("No models found in the 'models' directory.")
        return None

    # Allow the user to select a model
    selected_model = st.sidebar.selectbox("Select a model:", model_files)

    # Load the selected model when the user confirms
    if st.sidebar.button("Load Model"):
        st.success(f"Model '{selected_model}' loaded successfully.")
        return os.path.join(models_dir, selected_model)

    return None