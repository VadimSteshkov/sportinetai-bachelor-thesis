import os
import pandas as pd
import streamlit as st
from ui.ufc_ui_new import show_ufc_ui
from ui.analysis_ui import show_analysis_ui

# Import separate modules for each tab
# from UFC_UI_predictions import show_predictions_tab
# from UFC_UI_analysis import show_analysis_tab
# from UFC_UI_manual import show_manual_input_tab

# Function to load the UFC dataset
def load_ufc_dataset():
    try:
        return pd.read_csv('data/processed/ufc_data_final.csv')
    except FileNotFoundError:
        st.error("Dataset file not found.")
        return None

# Main UFC UI function
def show_ufc_main(loaded_model):
    """
    Main function to display the UFC prediction UI.
    """
    st.title("UFC Fight Outcome Prediction")

    # Load the UFC dataset
    ufc_dataset = load_ufc_dataset()
    if ufc_dataset is None:
        return


    # Create a tabbed menu
    tabs = st.tabs(["Predictions", "Analysis", "Manual Input"])

    with tabs[0]:  # Для первой вкладки
        show_ufc_ui(loaded_model)
    with tabs[1]:
        show_analysis_ui(ufc_dataset,loaded_model)  # Retrieves data from st.session_state
    #
    # with selected_tab[2]:
        # show_manual_input_tab(ufc_dataset)

# Run the application
if __name__ == "__main__":
    show_ufc_main()
