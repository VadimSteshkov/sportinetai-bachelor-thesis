import streamlit as st

# Function to display instructions and tips for using the app
def show_instructions():
    with st.expander("Instructions and Tips", expanded=True):
        st.markdown("""
                    **Instructions:**

                    1. Select the model you want to use for analysis.
                    2. Choose the sport (currently, only UFC is supported).
                    3. Select the features you are interested in for analytics.
                    4. Wait for the processing to complete and download your results!

                    **Notes and Recommendations:**

                    - The default model already contains all the necessary data for analysis.
                    - In the future, there will be an option to upload your own model.
                    - Various types of data visualization are available with full customization options.
                """)

