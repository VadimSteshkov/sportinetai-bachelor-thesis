# data_store.py
import streamlit as st
from ui.UFC_UI import show_ufc_ui
from ui.Football_UI import show_football_ui


# Ensure that all necessary UI modules are imported here

# Example of data storage
transformer_models = ["None", "Model A", "Model B", "Model C"]
sports_list = ["Football", "Basketball", "Tennis", "Hockey", "Volleyball", "UFC"]

# Mapping sports to their respective UI functions
sport_function_map = {
    "Football": show_football_ui,
    "Basketball": lambda: st.write("Basketball UI not implemented yet"),
    "Tennis": lambda: st.write("Tennis UI not implemented yet"),
    "Hockey": lambda: st.write("Hockey UI not implemented yet"),
    "Volleyball": lambda: st.write("Volleyball UI not implemented yet"),
    "UFC": show_ufc_ui,
}
