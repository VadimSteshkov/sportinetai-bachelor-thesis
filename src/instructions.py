import streamlit as st

def show_instructions():
    with st.expander("Instructions and Tips", expanded=True):
        st.markdown("""
            **Instructions:**

            1. Upload a crawl file from your favorite website crawler.
            2. Select the column that contains the URL.
            3. Select the column that contains the content to match on (best results are typically on the page heading rather than the page content).
            4. Wait for the clustering to complete and download your file!

            **Notes and Tips:**

            - You can adjust the similarity cut-off threshold in real time to see how the connections are impacted, helping you find the sweet spot before exporting.
            - Choice of graph visualization and full display customization.
            - This Web app is limited to 1000 rows. If you have a bigger project, please get in touch.
        """)
