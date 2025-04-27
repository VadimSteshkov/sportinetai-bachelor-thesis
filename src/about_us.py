import streamlit as st

# Function to display information about the project and the team
def show_about_us():
    with st.expander("About Us", expanded=False):
        st.markdown("""
                    **Our Mission**

                    We aim to develop cutting-edge sports analytics tools using advanced data science and machine learning techniques. This project strives to help sports teams and athletes make data-driven decisions and achieve outstanding results.

                    **About the Project**

                    This project is part of my bachelor's thesis at the Faculty of Computer Science. Our primary goal is to create and implement a sports data analysis model capable of predicting match outcomes and providing valuable insights. 

                    **Supervised by**  
                    - Prof. Markus Prossegger

                    **Our Team**

                    - Vadim Steshkov: Developer and researcher in the field of machine learning.
                    - Support provided by faculty members and our supervisor.

                    **Contact Us**

                    If you have any questions or collaboration proposals, feel free to reach out:  
                    - Email: Vadim.Steshkov@edu.fh-kaernten.ac.at 
                    - Phone: +43 676 4803483   

                    Thank you for your interest in our project!
                """)

