import streamlit as st

def show_ufc_ui():
    tabs = ["Preds ", "Data Viz", "PerfMetrics", "StratSim","Benchmarks"]
    selected_tab = st.tabs(tabs)
    with selected_tab[0]:  # Assuming 'txt2img' is selected by default
        # Main content area with input fields and buttons
        st.text_input("Home Team ", key="input_mermaid")

        # Generate button with additional style toggle options
        col1, col2 = st.columns([3, 1])
        with col1:
            st.text_input("Away Team:", key="input_negative_prompt")
        with col2:
            if st.button("Generate", key="generate_button"):
                # Logic for generate action
                st.success("Generated")

        # Style toggles
        col_style1, col_style2 = st.columns([1, 1])
        with col_style1:
            style1 = st.selectbox("Style 1", ["None", "Style A", "Style B"], key="select_style1")
        with col_style2:
            style2 = st.selectbox("Style 2", ["None", "Style A", "Style B"], key="select_style2")


    with st.expander("ControlNet Options", expanded=False):
        with st.container():
            # Set up columns for the form elements
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                # Preprocessor selectbox
                preprocessor_options = ['none', 'option1', 'option2']  # Example options
                preprocessor = st.selectbox("Preprocessor", preprocessor_options)

            with col2:
                # Control Weight slider
                control_weight = st.slider("Control Weight", min_value=0, max_value=100, value=1, step=1)

            with col3:
                # Starting Control Step slider
                starting_control_step = st.slider("Starting Control Step", min_value=0, max_value=100, value=0, step=1)

            with col4:
                # Model selectbox
                model_options = ['None', 'Model1', 'Model2']  # Example options
                model = st.selectbox("Model", model_options)

                # Ending Control Step slider
                ending_control_step = st.slider("Ending Control Step", min_value=0, max_value=100, value=1, step=1)
    # Sidebar with sliders
    with st.sidebar:
        # Define the transformer models assuming it's provided earlier in the code
        transformer_models = ["None", "Model A", "Model B", "Model C"]
