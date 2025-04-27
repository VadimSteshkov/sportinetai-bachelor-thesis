import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import difflib

# Все ваши модули и функции
from src.fighter_data_fetcher import load_ufc_dataset, get_fighter_stats_with_styles
from app.fighter_data import (
    process_fighter_data,
    display_fighter_profile,
    display_stats_block,
    display_features_with_corner_stats,
)
from app.prediction import predict_winner
