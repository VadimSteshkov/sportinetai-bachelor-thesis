from app import pd,st,process_fighter_data, predict_winner,load_ufc_dataset,display_fighter_profile,display_stats_block,get_fighter_stats_with_styles,go,display_features_with_corner_stats,make_subplots
from app.fighter_data import find_closest_fighter
# from app.utils import adjust_fighter_probabilities
from app.utils import get_fighter_metrics

def input_block():
    st.markdown("### Fighter Input")
    col1, col2, col3 = st.columns([3, 1, 3])

    if "fighter1" not in st.session_state:
        st.session_state.fighter1 = ""
    if "fighter2" not in st.session_state:
        st.session_state.fighter2 = ""

    with col1:
        st.session_state.fighter1 = st.text_input("Fighter 1", st.session_state.fighter1, key="fighter1_input")
    with col3:
        st.session_state.fighter2 = st.text_input("Fighter 2", st.session_state.fighter2, key="fighter2_input")

    with col2:
        if st.button("Swap Fighters"):
            st.session_state.fighter1, st.session_state.fighter2 = (
                st.session_state.fighter2,
                st.session_state.fighter1,
            )

    predict_button = st.button("Predict Outcome")
    return st.session_state.fighter1, st.session_state.fighter2, predict_button


def show_ufc_ui(loaded_model):
    """
    Main function to display the UFC prediction UI.
    """

    global winner
    # st.title("UFC Fight Outcome Prediction")

    # Load the UFC dataset
    try:
        ufc_dataset = load_ufc_dataset()
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return


    # Input block for fighter names
    fighter1_raw, fighter2_raw, predict_button = input_block()

    # Display fighter profiles and handle errors
    if fighter1_raw or fighter2_raw:
        try:
            st.markdown("### Fighter Profiles and Stats")
            col1, col2 = st.columns(2)

            # Initialize profiles in session state if not already present
            if "fighter1_profile" not in st.session_state:
                st.session_state.fighter1_profile = None
            if "fighter2_profile" not in st.session_state:
                st.session_state.fighter2_profile = None

            # Process Fighter 1
            if fighter1_raw:
                fighter1_processed = process_fighter_data(fighter1_raw, ufc_dataset,
                                                          st.session_state.get('enable_name_suggestion', False))
                if fighter1_processed:
                    # Check if the fighter is in the red corner
                    if fighter1_processed in ufc_dataset['r_fighter'].str.lower().tolist():
                        correct_name_1 = ufc_dataset.loc[
                            ufc_dataset['r_fighter'].str.lower() == fighter1_processed, 'r_fighter'
                        ].iloc[0]
                        fighter1_profile = get_fighter_stats_with_styles(fighter1_processed)
                        st.session_state.fighter1_profile = fighter1_profile  # Save to session state
                        with col1:
                            display_fighter_profile(fighter1_profile, correct_name_1)
                            display_stats_block(fighter1_profile, correct_name_1)

                    # Check if the fighter is in the blue corner
                    elif fighter1_processed in ufc_dataset['b_fighter'].str.lower().tolist():
                        correct_name_1 = ufc_dataset.loc[
                            ufc_dataset['b_fighter'].str.lower() == fighter1_processed, 'b_fighter'
                        ].iloc[0]
                        fighter1_profile = get_fighter_stats_with_styles(fighter1_processed)
                        st.session_state.fighter1_profile = fighter1_profile  # Save to session state
                        with col1:
                            display_fighter_profile(fighter1_profile, correct_name_1)
                            display_stats_block(fighter1_profile, correct_name_1)

                    # Fighter not found
                    else:
                        with col1:
                            st.error(f"Fighter '{fighter1_raw}' not found in the dataset.")
                else:
                    with col1:
                        st.error(f"Fighter '{fighter1_raw}' not found in the dataset.")
            # Show metrics for Fighter 1
            # if fighter1_raw:
            #     fighter1_metrics = get_fighter_metrics(fighter1_raw, ufc_dataset)
            #     st.markdown("### Metrics for Fighter 1")
            #     st.table(pd.DataFrame(fighter1_metrics.items(), columns=["Metric", "Value"]))
            #
            # # Show metrics for Fighter 2
            # if fighter2_raw:
            #     fighter2_metrics = get_fighter_metrics(fighter2_raw, ufc_dataset)
            #     st.markdown("### Metrics for Fighter 2")
            #     st.table(pd.DataFrame(fighter2_metrics.items(), columns=["Metric", "Value"]))

            # Process Fighter 2
            if fighter2_raw:
                fighter2_processed = process_fighter_data(fighter2_raw, ufc_dataset,
                                                          st.session_state.get('enable_name_suggestion', False))
                if fighter2_processed:
                    # Check if the fighter is in the red corner
                    if fighter2_processed in ufc_dataset['r_fighter'].str.lower().tolist():
                        correct_name_2 = ufc_dataset.loc[
                            ufc_dataset['r_fighter'].str.lower() == fighter2_processed, 'r_fighter'
                        ].iloc[0]
                        fighter2_profile = get_fighter_stats_with_styles(fighter2_processed)
                        st.session_state.fighter2_profile = fighter2_profile  # Save to session state
                        with col2:
                            display_fighter_profile(fighter2_profile, correct_name_2)
                            display_stats_block(fighter2_profile, correct_name_2)

                    # Check if the fighter is in the blue corner
                    elif fighter2_processed in ufc_dataset['b_fighter'].str.lower().tolist():
                        correct_name_2 = ufc_dataset.loc[
                            ufc_dataset['b_fighter'].str.lower() == fighter2_processed, 'b_fighter'
                        ].iloc[0]
                        fighter2_profile = get_fighter_stats_with_styles(fighter2_processed)
                        st.session_state.fighter2_profile = fighter2_profile  # Save to session state
                        with col2:
                            display_fighter_profile(fighter2_profile, correct_name_2)
                            display_stats_block(fighter2_profile, correct_name_2)

                    # Fighter not found
                    else:
                        with col2:
                            st.error(f"Fighter '{fighter2_raw}' not found in the dataset.")
                else:
                    with col2:
                        st.error(f"Fighter '{fighter2_raw}' not found in the dataset.")

        except Exception as e:
            st.error(f"Error loading fighter profiles: {e}")

    # try:
    #     display_features_with_corner_stats(fighter1_processed, fighter2_processed, ufc_dataset)
    # except Exception as e:
    #     st.error(f"Error displaying corner stats: {e}")

    # Handle prediction button click
    if predict_button:
        if not loaded_model:
            st.warning("Please load the prediction model.")
            return

        if not fighter1_raw or not fighter2_raw:
            st.error("Please enter both fighter names.")
            return

        try:
            # Определение окончательных имён для предсказания
            if st.session_state.get('enable_name_suggestion', False):
                # Используем исправленные имена из профилей, если они существуют
                fighter1_for_prediction = correct_name_1 if 'correct_name_1' in locals() else fighter1_raw
                fighter2_for_prediction = correct_name_2 if 'correct_name_2' in locals() else fighter2_raw
            else:
                # Используем введённые имена, если исправление отключено
                fighter1_for_prediction = fighter1_raw
                fighter2_for_prediction = fighter2_raw

            # try:
            #     fighter1_prob, fighter2_prob = adjust_fighter_probabilities(fighter1_for_prediction,
            #                                                                 fighter2_for_prediction, ufc_dataset)
            #     st.markdown(f"### Adjusted Probabilities (Assuming Both in Red Corner)")
            #     st.markdown(f"- {fighter1_for_prediction}: {fighter1_prob:.2f}%")
            #     st.markdown(f"- {fighter2_for_prediction}: {fighter2_prob:.2f}%")
            # except ValueError as e:
            #     st.error(f"Error adjusting probabilities: {e}")

            # Predict the winner and retrieve fighter data
            # winner, winner_probability, fighter1_data, fighter2_data = predict_winner(
            #     fighter1_for_prediction, fighter2_for_prediction, loaded_model, ufc_dataset
            # )

            if fighter1_for_prediction and fighter2_for_prediction:
                winner, winner_probability, fighter1_data, fighter2_data = predict_winner(
                    fighter1_for_prediction, fighter2_for_prediction, loaded_model, ufc_dataset)
            else:
                st.error("One or both fighters not found. Cannot make a prediction.")

            if winner:
                st.markdown("### Prediction Results")

                # Колонки для бойцов
                col1, col2 = st.columns(2)

                # Определение победителя и проигравшего
                loser = fighter1_raw if winner != fighter1_raw else fighter2_raw
                loser_probability = 100 - winner_probability  # Вероятность проигравшего

                # Fighter 1 (левый столбец)
                with col1:
                    is_winner_f1 = fighter1_for_prediction == winner
                    st.markdown(
                        f"""
                        <div style="background-color: #1a1a1a; padding: 20px; border-radius: 8px; text-align: center;">
                            <img src="{fighter1_profile.get('image_url')}"
                                alt="{fighter1_raw}" style="width: 150px; height: auto; border-radius: 10px; margin-bottom: 10px;">
                            <h2 style="color: {'green' if is_winner_f1 else 'red'}; margin: 0;">{'Winner' if is_winner_f1 else 'Loser'}</h2>
                            <h3 style="color: white; margin: 5px 0;">{fighter1_raw.title()}</h3>
                            <p style="color: white; font-size: 16px;">Probability: {winner_probability if is_winner_f1 else 100 - winner_probability:.2f}%</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                # Fighter 2 (правый столбец)
                with col2:
                    is_winner_f2 = fighter2_for_prediction == winner
                    st.markdown(
                        f"""
                        <div style="background-color: #1a1a1a; padding: 20px; border-radius: 8px; text-align: center;">
                            <img src="{fighter2_profile.get('image_url')}"
                                alt="{fighter2_raw}" style="width: 150px; height: auto; border-radius: 10px; margin-bottom: 10px;">
                            <h2 style="color: {'green' if is_winner_f2 else 'red'}; margin: 0;">{'Winner' if is_winner_f2 else 'Loser'}</h2>
                            <h3 style="color: white; margin: 5px 0;">{fighter2_raw.title()}</h3>
                            <p style="color: white; font-size: 16px;">Probability: {winner_probability if is_winner_f2 else 100 - winner_probability:.2f}%</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                # Use fighter1_data and fighter2_data for further visualization
                # Comparative Feature Differences
                st.markdown("### Comparative Feature Differences")
                features = ["height", "weight", "reach", "wins_total", "losses_total"]


                # Форматируем имена бойцов для поиска
                fighter1_formatted = find_closest_fighter(fighter1_raw, ufc_dataset) or fighter1_raw.strip().lower()
                fighter2_formatted = find_closest_fighter(fighter2_raw, ufc_dataset) or fighter2_raw.strip().lower()

                # Находим строки с данными бойцов
                fighter1_data_row = ufc_dataset[
                    (ufc_dataset['r_fighter'].str.strip().str.lower() == fighter1_formatted) |
                    (ufc_dataset['b_fighter'].str.strip().str.lower() == fighter1_formatted)
                    ]

                fighter2_data_row = ufc_dataset[
                    (ufc_dataset['r_fighter'].str.strip().str.lower() == fighter2_formatted) |
                    (ufc_dataset['b_fighter'].str.strip().str.lower() == fighter2_formatted)
                    ]

                # Проверяем, что данные для бойцов найдены
                if fighter1_data_row.empty:
                    st.error(f"Fighter '{fighter1_raw}' not found in the dataset. Closest match: {fighter1_formatted}")
                    return
                if fighter2_data_row.empty:
                    st.error(f"Fighter '{fighter2_raw}' not found in the dataset. Closest match: {fighter2_formatted}")
                    return

                # Берем первую строку для каждого бойца
                fighter1_data_row = fighter1_data_row.iloc[0]
                fighter2_data_row = fighter2_data_row.iloc[0]

                # Определяем префиксы для каждого бойца
                fighter1_prefix = 'r_' if fighter1_data_row['r_fighter'].strip().lower() == fighter1_formatted else 'b_'
                fighter2_prefix = 'r_' if fighter2_data_row['r_fighter'].strip().lower() == fighter2_formatted else 'b_'

                # Формируем значения динамически
                fighter1_values = [fighter1_data_row[f"{fighter1_prefix}{feature}"] for feature in features]
                fighter2_values = [fighter2_data_row[f"{fighter2_prefix}{feature}"] for feature in features]

                # Используем оригинальные имена, введённые пользователем, для графиков
                fighter1_display_name = fighter1_raw
                fighter2_display_name = fighter2_raw

                fig_features = go.Figure()
                fig_features.add_trace(go.Bar(
                    x=features,
                    y=fighter1_values,
                    name=fighter1_raw.title(),
                    marker_color='red'
                ))
                fig_features.add_trace(go.Bar(
                    x=features,
                    y=fighter2_values,
                    name=fighter2_raw.title(),
                    marker_color='blue'
                ))
                fig_features.update_layout(
                    title="Feature Comparison Between Fighters",
                    barmode='group',
                    xaxis_title="Features",
                    yaxis_title="Values"
                )
                st.plotly_chart(fig_features, use_container_width=True)

                # Polar charts for fighter strengths
                fighter1_polar_features = ["Strikes", "Takedowns", "Submissions", "Control"]
                fighter1_polar_values = [
                    fighter1_data.iloc[0]['r_SLpM_total'], fighter1_data.iloc[0]['r_td_avg'],
                    fighter1_data.iloc[0]['r_sub_avg'], fighter1_data.iloc[0]['r_td_def_total']
                ]

                fighter2_polar_features = ["Strikes", "Takedowns", "Submissions", "Control"]
                fighter2_polar_values = [
                    fighter2_data.iloc[0]['r_SLpM_total'], fighter2_data.iloc[0]['r_td_avg'],
                    fighter2_data.iloc[0]['r_sub_avg'], fighter2_data.iloc[0]['r_td_def_total']
                ]

                fig_polar = make_subplots(
                    rows=1, cols=2,
                    specs=[[{'type': 'polar'}, {'type': 'polar'}]],
                    subplot_titles=[f"{fighter1_raw.title()} Strengths", f"{fighter2_raw.title()} Strengths"]
                )

                fig_polar.add_trace(go.Scatterpolar(
                    r=fighter1_polar_values + [fighter1_polar_values[0]],
                    theta=fighter1_polar_features + [fighter1_polar_features[0]],
                    fill='toself',
                    marker_color='red',
                    name=fighter1_raw.title()
                ), row=1, col=1)

                fig_polar.add_trace(go.Scatterpolar(
                    r=fighter2_polar_values + [fighter2_polar_values[0]],
                    theta=fighter2_polar_features + [fighter2_polar_features[0]],
                    fill='toself',
                    marker_color='blue',
                    name=fighter2_raw.title()
                ), row=1, col=2)

                fig_polar.update_layout(
                    title="Categorical Polar Chart: Fighter Strengths",
                    template='plotly_dark',
                    showlegend=False
                )
                fig_polar.update_layout(
                    title="Categorical Polar Chart: Fighter Strengths",
                    template='plotly_dark',
                    showlegend=False,
                    polar=dict(
                        radialaxis=dict(visible=True,
                                        range=[0, max(max(fighter1_polar_values), max(fighter2_polar_values))]),
                        angularaxis=dict(tickfont=dict(size=10), rotation=45)  # Adjust category position
                    ),
                    polar2=dict(
                        radialaxis=dict(visible=True,
                                        range=[0, max(max(fighter1_polar_values), max(fighter2_polar_values))]),
                        angularaxis=dict(tickfont=dict(size=10), rotation=45)  # Adjust category position
                    )
                )
                st.plotly_chart(fig_polar, use_container_width=True)



        except Exception as e:
            st.error(f"Error making prediction: {e}")

