from app import st, pd


# def predict_winner(fighter1_name, fighter2_name, loaded_model, ufc_dataset):
#     """
#     Predicts the winner between two fighters using the model.
#     Returns the winner's name, probabilities, and fighter data.
#     """
#     try:
#         if not loaded_model:
#             st.warning("Please load the prediction model.")
#             return None, None, None, None
#
#
#         # Очистка и приведение имен бойцов
#         fighter1_name_clean = fighter1_name.strip().lower()
#         fighter2_name_clean = fighter2_name.strip().lower()
#
#         def find_fighter_data(fighter_name, ufc_dataset):
#             """
#             Находит данные бойца в наборе данных для обоих углов.
#             Если данные отсутствуют в противоположном углу, копирует из доступного.
#             """
#             fighter_name_clean = fighter_name.strip().lower()
#             red_fighters = ufc_dataset['r_fighter'].str.strip().str.lower()
#             blue_fighters = ufc_dataset['b_fighter'].str.strip().str.lower()
#
#             if fighter_name_clean in red_fighters.values:
#                 data = ufc_dataset[red_fighters == fighter_name_clean].iloc[0].to_dict()
#                 # Если данных для синего угла нет, копируем из красного
#                 if not any(data.get(key, None) for key in ['b_age', 'b_height', 'b_weight', 'b_reach']):
#                     for key in data.keys():
#                         if key.startswith('r_'):
#                             data[key.replace('r_', 'b_')] = data[key]
#                 return pd.DataFrame([data]), 'r_'
#             elif fighter_name_clean in blue_fighters.values:
#                 data = ufc_dataset[blue_fighters == fighter_name_clean].iloc[0].to_dict()
#                 # Если данных для красного угла нет, копируем из синего
#                 if not any(data.get(key, None) for key in ['r_age', 'r_height', 'r_weight', 'r_reach']):
#                     for key in data.keys():
#                         if key.startswith('b_'):
#                             data[key.replace('b_', 'r_')] = data[key]
#                 return pd.DataFrame([data]), 'b_'
#             else:
#                 return None, None
#
#         # Найти данные для бойцов
#         fighter1_data, _ = find_fighter_data(fighter1_name_clean, ufc_dataset)
#         fighter2_data, _ = find_fighter_data(fighter2_name_clean, ufc_dataset)
#
#         # Проверка, нашли ли бойцов
#         if fighter1_data is None or fighter1_data.empty:
#             st.error(f"Fighter '{fighter1_name}' not found in the dataset.")
#             return None, None, None, None
#         if fighter2_data is None or fighter2_data.empty:
#             st.error(f"Fighter '{fighter2_name}' not found in the dataset.")
#             return None, None, None, None
#
#         # Извлечение значений для первого бойца (проверка нормализации)
#         if "r_age" in fighter1_data.columns:  # Если нормализовано под красный угол
#             fighter1_values = [
#                 fighter1_data.iloc[0]['r_age'],
#                 fighter1_data.iloc[0]['r_height'],
#                 fighter1_data.iloc[0]['r_weight'],
#                 fighter1_data.iloc[0]['r_reach'],
#                 fighter1_data.iloc[0]['r_wins_total'],
#                 fighter1_data.iloc[0]['r_losses_total'],
#                 fighter1_data.iloc[0]['r_SLpM_total'],
#                 fighter1_data.iloc[0]['r_SApM_total'],
#                 fighter1_data.iloc[0]['r_sig_str_acc_total'],
#                 fighter1_data.iloc[0]['r_td_acc_total'],
#                 fighter1_data.iloc[0]['r_td_def_total'],
#                 fighter1_data.iloc[0]['r_sub_avg'],
#                 fighter1_data.iloc[0]['r_td_avg'],
#                 fighter1_data.iloc[0]['r_str_def_total']
#             ]
#         else:  # Если данные из синего угла
#             fighter1_values = [
#                 fighter1_data.iloc[0]['b_age'],
#                 fighter1_data.iloc[0]['b_height'],
#                 fighter1_data.iloc[0]['b_weight'],
#                 fighter1_data.iloc[0]['b_reach'],
#                 fighter1_data.iloc[0]['b_wins_total'],
#                 fighter1_data.iloc[0]['b_losses_total'],
#                 fighter1_data.iloc[0]['b_SLpM_total'],
#                 fighter1_data.iloc[0]['b_SApM_total'],
#                 fighter1_data.iloc[0]['b_sig_str_acc_total'],
#                 fighter1_data.iloc[0]['b_td_acc_total'],
#                 fighter1_data.iloc[0]['b_td_def_total'],
#                 fighter1_data.iloc[0]['b_sub_avg'],
#                 fighter1_data.iloc[0]['b_td_avg'],
#                 fighter1_data.iloc[0]['b_str_def_total']
#             ]
#
#         # Извлечение значений для второго бойца (аналогично)
#         if "r_age" in fighter2_data.columns:  # Если нормализовано под красный угол
#             fighter2_values = [
#                 fighter2_data.iloc[0]['r_age'],
#                 fighter2_data.iloc[0]['r_height'],
#                 fighter2_data.iloc[0]['r_weight'],
#                 fighter2_data.iloc[0]['r_reach'],
#                 fighter2_data.iloc[0]['r_wins_total'],
#                 fighter2_data.iloc[0]['r_losses_total'],
#                 fighter2_data.iloc[0]['r_SLpM_total'],
#                 fighter2_data.iloc[0]['r_SApM_total'],
#                 fighter2_data.iloc[0]['r_sig_str_acc_total'],
#                 fighter2_data.iloc[0]['r_td_acc_total'],
#                 fighter2_data.iloc[0]['r_td_def_total'],
#                 fighter2_data.iloc[0]['r_sub_avg'],
#                 fighter2_data.iloc[0]['r_td_avg'],
#                 fighter2_data.iloc[0]['r_str_def_total']
#             ]
#         else:  # Если данные из синего угла
#             fighter2_values = [
#                 fighter2_data.iloc[0]['b_age'],
#                 fighter2_data.iloc[0]['b_height'],
#                 fighter2_data.iloc[0]['b_weight'],
#                 fighter2_data.iloc[0]['b_reach'],
#                 fighter2_data.iloc[0]['b_wins_total'],
#                 fighter2_data.iloc[0]['b_losses_total'],
#                 fighter2_data.iloc[0]['b_SLpM_total'],
#                 fighter2_data.iloc[0]['b_SApM_total'],
#                 fighter2_data.iloc[0]['b_sig_str_acc_total'],
#                 fighter2_data.iloc[0]['b_td_acc_total'],
#                 fighter2_data.iloc[0]['b_td_def_total'],
#                 fighter2_data.iloc[0]['b_sub_avg'],
#                 fighter2_data.iloc[0]['b_td_avg'],
#                 fighter2_data.iloc[0]['b_str_def_total']
#             ]
#
#         shared_features = [
#             fighter1_data.iloc[0]['age_diff'],
#             fighter1_data.iloc[0]['wins_total_diff']
#         ]
#         # Формирование входных данных в DataFrame с именами признаков
#         input_data = pd.DataFrame([fighter1_values + fighter2_values + shared_features], columns=[
#         "r_age", "r_height", "r_weight", "r_reach", "r_wins_total", "r_losses_total",
#         "r_SLpM_total", "r_SApM_total", "r_sig_str_acc_total", "r_td_acc_total",
#         "r_td_def_total", "r_sub_avg", "r_td_avg","r_str_def_total",
#         "b_age", "b_height", "b_weight", "b_reach", "b_wins_total", "b_losses_total",
#         "b_SLpM_total", "b_SApM_total", "b_sig_str_acc_total", "b_td_acc_total",
#         "b_td_def_total", "b_sub_avg", "b_td_avg","b_str_def_total", "age_diff", "wins_total_diff"
#     ])
#     #     input_data = pd.DataFrame([fighter1_values + fighter2_values], columns=[
#     #         "r_age", "r_height", "r_weight", "r_reach", "r_wins_total", "r_losses_total",
#     #         "r_SLpM_total", "r_SApM_total", "r_sig_str_acc_total", "r_td_acc_total",
#     #         "r_td_def_total", "r_sub_avg", "r_td_avg",
#     #         "b_age", "b_height", "b_weight", "b_reach", "b_wins_total", "b_losses_total",
#     #         "b_SLpM_total", "b_SApM_total", "b_sig_str_acc_total", "b_td_acc_total",
#     #         "b_td_def_total", "b_sub_avg", "b_td_avg",
#     #     ])
#
#         # Перестановка признаков в соответствии с обучением модели
#         if hasattr(loaded_model, "feature_names_in_"):
#             input_data = input_data[loaded_model.feature_names_in_]
#
#         # Прогноз модели
#         prediction = loaded_model.predict(input_data)
#         probabilities = loaded_model.predict_proba(input_data)
#
#         # Отображение используемых признаков
#         feature_names = [
#             "Age", "Height", "Weight", "Reach", "Wins Total", "Losses Total",
#             "SLpM Total", "SApM Total", "Sig. Strike Accuracy", "TD Accuracy",
#             "TD Defense", "Sub Avg", "TD Avg","Str. Def:"
#         ]
#         features_df = pd.DataFrame({
#             "Feature": feature_names,
#             "Fighter 1": fighter1_values,
#             "Fighter 2": fighter2_values
#         })
#
#         st.markdown("### Features Used for Prediction")
#         st.table(features_df)
#
#         # Определение победителя
#         winner = fighter1_name if prediction[0] == 1 else fighter2_name
#         winner_probability = probabilities[0][1] * 100 if prediction[0] == 1 else probabilities[0][0] * 100
#
#
#         return winner, winner_probability, fighter1_data, fighter2_data
#
#     except Exception as e:
#         st.error(f"Error during prediction: {e}")
#         return None, None, None, None
#
def find_fighter_data(fighter_name, ufc_dataset):
    """
    Finds fighter's data in the dataset for both corners.
    If data is missing in the opposite corner, it copies from the available corner.
    """
    fighter_name_clean = fighter_name.strip().lower()
    red_fighters = ufc_dataset['r_fighter'].str.strip().str.lower()
    blue_fighters = ufc_dataset['b_fighter'].str.strip().str.lower()

    if fighter_name_clean in red_fighters.values:
        data = ufc_dataset[red_fighters == fighter_name_clean].iloc[0].to_dict()
        if not any(data.get(key, None) for key in ['b_age', 'b_height', 'b_weight', 'b_reach']):
            for key in data.keys():
                if key.startswith('r_'):
                    data[key.replace('r_', 'b_')] = data[key]
        return pd.DataFrame([data]), 'r_'
    elif fighter_name_clean in blue_fighters.values:
        data = ufc_dataset[blue_fighters == fighter_name_clean].iloc[0].to_dict()
        if not any(data.get(key, None) for key in ['r_age', 'r_height', 'r_weight', 'r_reach']):
            for key in data.keys():
                if key.startswith('b_'):
                    data[key.replace('b_', 'r_')] = data[key]
        return pd.DataFrame([data]), 'b_'
    else:
        return None, None

def extract_metrics(fighter_data, prefix):
    """
    Extracts metrics dynamically based on the prefix.
    """
    if fighter_data is None:
        return [None] * 14

    return [
        fighter_data.iloc[0][f'{prefix}age'],
        fighter_data.iloc[0][f'{prefix}height'],
        fighter_data.iloc[0][f'{prefix}weight'],
        fighter_data.iloc[0][f'{prefix}reach'],
        fighter_data.iloc[0][f'{prefix}wins_total'],
        fighter_data.iloc[0][f'{prefix}losses_total'],
        fighter_data.iloc[0][f'{prefix}SLpM_total'],
        fighter_data.iloc[0][f'{prefix}SApM_total'],
        fighter_data.iloc[0][f'{prefix}sig_str_acc_total'],
        fighter_data.iloc[0][f'{prefix}td_acc_total'],
        fighter_data.iloc[0][f'{prefix}td_def_total'],
        fighter_data.iloc[0][f'{prefix}sub_avg'],
        fighter_data.iloc[0][f'{prefix}td_avg'],
        fighter_data.iloc[0][f'{prefix}str_def_total']
    ]

def predict_winner(fighter1_name, fighter2_name, loaded_model, ufc_dataset):
    """
    Predicts the winner between two fighters using the model.
    Returns the winner's name, probabilities, and fighter data.
    """
    try:
        if not loaded_model:
            st.warning("Please load the prediction model.")
            return None, None, None, None

        # Сортируем имена бойцов по алфавиту для консистентности
        if fighter1_name.lower() > fighter2_name.lower():
            fighter1_name, fighter2_name = fighter2_name, fighter1_name

        # Find data for both fighters
        fighter1_data, fighter1_prefix = find_fighter_data(fighter1_name, ufc_dataset)
        fighter2_data, fighter2_prefix = find_fighter_data(fighter2_name, ufc_dataset)

        if fighter1_data is None or fighter1_data.empty:
            st.error(f"Fighter '{fighter1_name}' not found in the dataset.")
            return None, None, None, None
        if fighter2_data is None or fighter2_data.empty:
            st.error(f"Fighter '{fighter2_name}' not found in the dataset.")
            return None, None, None, None

        # Extract metrics for both fighters
        fighter1_values = extract_metrics(fighter1_data, fighter1_prefix)
        fighter2_values = extract_metrics(fighter2_data, fighter2_prefix)

        # Calculate shared features
        age_diff = abs(fighter1_values[0] - fighter2_values[0])
        wins_total_diff = abs(fighter1_values[4] - fighter2_values[4])
        shared_features = [wins_total_diff, age_diff]

        # Prepare input data for prediction
        input_data = pd.DataFrame([fighter1_values + fighter2_values + shared_features], columns=[
            "r_age", "r_height", "r_weight", "r_reach", "r_wins_total", "r_losses_total",
            "r_SLpM_total", "r_SApM_total", "r_sig_str_acc_total", "r_td_acc_total",
            "r_td_def_total", "r_sub_avg", "r_td_avg", "r_str_def_total",
            "b_age", "b_height", "b_weight", "b_reach", "b_wins_total", "b_losses_total",
            "b_SLpM_total", "b_SApM_total", "b_sig_str_acc_total", "b_td_acc_total",
            "b_td_def_total", "b_sub_avg", "b_td_avg", "b_str_def_total", "age_diff", "wins_total_diff"
        ])

        # Align input data with model features
        if hasattr(loaded_model, "feature_names_in_"):
            input_data = input_data[loaded_model.feature_names_in_]

        # Make prediction
        prediction = loaded_model.predict(input_data)
        probabilities = loaded_model.predict_proba(input_data)

        # Display features used for prediction
        feature_names = [
            "Age", "Height", "Weight", "Reach", "Wins Total", "Losses Total",
            "SLpM Total", "SApM Total", "Sig. Strike Accuracy", "TD Accuracy",
            "TD Defense", "Sub Avg", "TD Avg", "Str. Def:"
        ]
        features_df = pd.DataFrame({
            "Feature": feature_names,
            "Fighter 1": fighter1_values,
            "Fighter 2": fighter2_values
        })

        st.markdown("### Features Used for Prediction")
        st.table(features_df)

        # Determine winner
        winner = fighter1_name if prediction[0] == 1 else fighter2_name
        winner_probability = probabilities[0][1] * 100 if prediction[0] == 1 else probabilities[0][0] * 100

        return winner, winner_probability, fighter1_data, fighter2_data

    except Exception as e:
        st.error(f"Error during prediction: {e}")
        return None, None, None, None

