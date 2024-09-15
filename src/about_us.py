import streamlit as st

def show_about_us():
    with st.expander("About Us", expanded=False):
        st.markdown("""
            **Our Mission**

            We aim to provide the most accurate and up-to-date sports analytics using advanced AI models, helping teams and individuals gain competitive advantages.

            **Our Team**

            - Jane Doe: Data Scientist and Machine Learning Expert.
            - John Smith: Sport Analyst and former professional football player.
            - Alex Brown: Software Developer with a passion for sports.

            **Contact Us**

            If you have any questions or would like to collaborate, please feel free to reach out at:
            - Email: contact@sportinet.ai
            - Phone: +123 456 7890
            - Address: 123 Sports Lane, Athletic City, 1010

            We love hearing from our users and partners!
        """)
