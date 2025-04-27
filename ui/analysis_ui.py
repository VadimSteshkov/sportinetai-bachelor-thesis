from app import st, display_fighter_profile

# def show_analysis_ui():
#     """
#     UFC Analysis tab: Show fighter data and analysis options.
#     """
#     st.subheader("Fight Analysis")
#     # Check if fighter data exists in session state
#     if "fighter1_profile" not in st.session_state or "fighter2_profile" not in st.session_state:
#         st.error("Fighter data not found. Please go back to the main page and enter fighter data.")
#         return
#
#     # Retrieve fighter data from session state
#     fighter1 = st.session_state.fighter1_profile
#     fighter2 = st.session_state.fighter2_profile
#
#     # Analysis options
#     st.markdown("### Analysis Options")
#     analysis_col1, analysis_col2 = st.columns([1, 1])  # Equal width for the analysis components
#
#     with analysis_col1:
#         # Round selection
#         round_number = st.slider("Select Round", min_value=1, max_value=5, value=1)
#
#         # Method of Victory
#         method_of_victory = st.radio(
#             "Method of Victory",
#             ["Knockout", "Submission", "Decision"],
#             horizontal=True
#         )
#
#         # Rematch checkbox
#         is_rematch = st.checkbox("Is this a rematch?")
#
#     with analysis_col2:
#         # Weight class selection
#         weight_class = st.selectbox(
#             "Weight Class",
#             ["Lightweight", "Middleweight", "Welterweight", "Heavyweight"]
#         )
#
#     # Display fighter profiles in two columns
#     col1, col2 = st.columns([1, 1])  # Equal width columns
#     with col1:
#         display_fighter_profile(fighter1, fighter1.get('name', 'Unknown'))
#     with col2:
#         display_fighter_profile(fighter2, fighter2.get('name', 'Unknown'))
#     # # Display selected options in a compact way
#     # st.markdown("### Selected Options")
#     # selected_col1, selected_col2 = st.columns([1, 1])  # Compact columns for displaying options
#     #
#     # with selected_col1:
#     #     st.write(f"**Round:** {round_number}")
#     #     st.write(f"**Method of Victory:** {method_of_victory}")
#     # with selected_col2:
#     #     st.write(f"**Is a Rematch:** {'Yes' if is_rematch else 'No'}")
#     #     st.write(f"**Weight Class:** {weight_class}")

from app import st, display_fighter_profile
import pandas as pd
import streamlit as st
import joblib


# Function to extract fighter data
def get_fighter_data(fighter_name, dataset, corner_prefix):
    fighter_data = dataset.query(f"{corner_prefix}fighter.str.lower() == '{fighter_name.lower()}'")
    if fighter_data.empty:
        return None
    # Map corner-specific columns to generic keys for easier access
    data = fighter_data.iloc[0].to_dict()
    return {
        "age": data.get(f"{corner_prefix}age"),
        "height": data.get(f"{corner_prefix}height"),
        "weight": data.get(f"{corner_prefix}weight"),
        "reach": data.get(f"{corner_prefix}reach"),
        "wins_total": data.get(f"{corner_prefix}wins_total"),
        "losses_total": data.get(f"{corner_prefix}losses_total"),
        "SLpM_total": data.get(f"{corner_prefix}SLpM_total"),
        "SApM_total": data.get(f"{corner_prefix}SApM_total"),
        "sig_str_acc_total": data.get(f"{corner_prefix}sig_str_acc_total"),
        "td_acc_total": data.get(f"{corner_prefix}td_acc_total"),
        "td_def_total": data.get(f"{corner_prefix}td_def_total"),
        "sub_avg": data.get(f"{corner_prefix}sub_avg"),
        "td_avg": data.get(f"{corner_prefix}td_avg"),
        "str_def_total": data.get(f"{corner_prefix}str_def_total"),
    }


# Function to display fighter profile
def display_fighter_metrics(fighter, name):
    st.markdown(f"### {name}")
    st.table(pd.DataFrame(fighter.items(), columns=["Metric", "Value"]))

# Function to predict the round
def predict_round(fighter1_data, fighter2_data, model, is_title_bout):
    try:
        # Prepare input features
        input_features = {
            'age_diff': fighter1_data['age'] - fighter2_data['age'],
            'height_diff': fighter1_data['height'] - fighter2_data['height'],
            'weight_diff': fighter1_data['weight'] - fighter2_data['weight'],
            'reach_diff': fighter1_data['reach'] - fighter2_data['reach'],
            'wins_total_diff': fighter1_data['wins_total'] - fighter2_data['wins_total'],
            'losses_total_diff': fighter1_data['losses_total'] - fighter2_data['losses_total'],
            'SLpM_total_diff': fighter1_data['SLpM_total'] - fighter2_data['SLpM_total'],
            'SApM_total_diff': fighter1_data['SApM_total'] - fighter2_data['SApM_total'],
            'sig_str_acc_total_diff': fighter1_data['sig_str_acc_total'] - fighter2_data['sig_str_acc_total'],
            'td_acc_total_diff': fighter1_data['td_acc_total'] - fighter2_data['td_acc_total'],
            'td_def_total_diff': fighter1_data['td_def_total'] - fighter2_data['td_def_total'],
            'sub_avg_diff': fighter1_data['sub_avg'] - fighter2_data['sub_avg'],
            'td_diff': fighter1_data['td_avg'] - fighter2_data['td_avg'],
            'activity_rate_diff': fighter1_data.get('activity_rate', 0) - fighter2_data.get('activity_rate', 0),
            'str_success_rate_diff': fighter1_data.get('str_success_rate', 0) - fighter2_data.get('str_success_rate', 0),
            'recent_wins_diff': fighter1_data.get('recent_wins', 0) - fighter2_data.get('recent_wins', 0),
            'avg_fight_duration_diff': fighter1_data.get('avg_fight_duration', 0) - fighter2_data.get('avg_fight_duration', 0),
            'strike_rate_diff': fighter1_data.get('strike_rate', 0) - fighter2_data.get('strike_rate', 0),
            'is_title_bout': int(is_title_bout)
        }

        # Ensure all additional features are added
        # additional_features = [
        #     'rev_diff', 'td_acc_diff', 'sig_str_acc_diff', 'td_total_diff',
        #     'str_def_diff', 'td_def_diff', 'td_avg_diff'
        # ]
        # for feature in additional_features:
        #     input_features[feature] = fighter1_data.get(feature, 0) - fighter2_data.get(feature, 0)

        # Convert to DataFrame for prediction
        input_data = pd.DataFrame([input_features])

        # Predict round outcome
        predicted_round = model.predict(input_data)[0] + 1
        predicted_proba = model.predict_proba(input_data)[0]

        return predicted_round, predicted_proba
    except Exception as e:
        st.error(f"Error during prediction: {e}")
        return None, None

# Main analysis UI
# Main analysis UI with external model input
def show_analysis_ui(ufc_dataset, loaded_model):
    """
    UFC Analysis tab: Show fighter data and analysis options with a preloaded model.
    """
    st.subheader("Fight Analysis")
    # Initialize session state variables if not already set
    if "fighter1_profile" not in st.session_state:
        st.session_state.fighter1_profile = None  # or default data if applicable
    if "fighter2_profile" not in st.session_state:
        st.session_state.fighter2_profile = None  # or default data if applicable

    # Retrieve fighter names from session state
    fighter1_name = st.session_state.get("fighter1", "").strip()
    fighter2_name = st.session_state.get("fighter2", "").strip()
    fighter1 = st.session_state.fighter1_profile
    fighter2 = st.session_state.fighter2_profile
    # Validate fighter names
    if not fighter1_name or not fighter2_name:
        st.error("Please enter valid fighter names in the input section.")
        return

    # Retrieve fighter data
    fighter1_data = get_fighter_data(fighter1_name, ufc_dataset, "r_")
    fighter2_data = get_fighter_data(fighter2_name, ufc_dataset, "b_")

    if not fighter1_data:
        st.error(f"Fighter '{fighter1_name}' not found in the dataset.")
        return
    if not fighter2_data:
        st.error(f"Fighter '{fighter2_name}' not found in the dataset.")
        return

    # Display fighter profiles in two columns
    col1, col2 = st.columns([1, 1])  # Equal width columns
    with col1:
        display_fighter_profile(fighter1, fighter1.get('name', 'Unknown'))
    with col2:
        display_fighter_profile(fighter2, fighter2.get('name', 'Unknown'))

    # Display fighter metrics
    st.markdown("### Fighter Metrics")
    col1, col2 = st.columns([1, 1])  # Equal width columns
    with col1:
        display_fighter_metrics(fighter1_data, fighter1_name)
    with col2:
        display_fighter_metrics(fighter2_data, fighter2_name)

    # Analysis options
    st.markdown("### Analysis Options")
    analysis_col1, analysis_col2 = st.columns([1, 1])

    with analysis_col1:
        # Round selection
        round_number = st.slider("Select Round", min_value=1, max_value=5, value=1)

        # Method of Victory
        method_of_victory = st.radio(
            "Method of Victory",
            ["Knockout", "Submission", "Decision"],
            horizontal=True
        )

        # Rematch checkbox
        is_rematch = st.checkbox("Is this a rematch?")

    with analysis_col2:
        # Weight class selection
        weight_class = st.selectbox(
            "Weight Class",
            ["Lightweight", "Middleweight", "Welterweight", "Heavyweight"]
        )

    # Fight type selection
    st.markdown("### Fight Type")
    is_title_bout = st.radio("Is this a title bout?", ["Yes", "No"]) == "Yes"

    # Use the preloaded model for predictions
    if st.button("Predict Outcome", key="predict_outcome"):
        predicted_round, predicted_proba = predict_round(fighter1_data, fighter2_data, loaded_model, is_title_bout)

        if predicted_round is not None:
            st.markdown("### Prediction Results")
            st.write(f"**Predicted Round:** {predicted_round}")
            st.write("**Probability of Each Round:**")
            for i, prob in enumerate(predicted_proba, start=1):
                st.write(f"Round {i}: {prob * 100:.2f}%")
