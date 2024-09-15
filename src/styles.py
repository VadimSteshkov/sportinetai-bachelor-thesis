# styles.py

# Streamlit custom CSS
def load_custom_styles():
    return """
    <style>
        .css-18e3th9, .css-1d391kg {
            background-color: #2C2C2C;
            color: white;
        }
        button {
            background-color: #FF6700;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            transition-duration: 0.4s;
            cursor: pointer;
        }
        button:hover {
            background-color: #FF5733;
        }
        .stTextInput > div > div > input {
            background-color: #333333;
            color: #ffffff;
        }
        header, footer {
            visibility: hidden;
        }
        .reportview-container .main .block-container {
            padding-top: 2rem;
        }
        .reportview-container .markdown-text-container {
            flex: 1;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        div.row-widget.stButton > button:first-child {
            margin-top: 28px;
        }
    </style>
    """

