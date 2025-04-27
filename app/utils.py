from app.fighter_data import calculate_fighter_stats

def format_fighter_name(name):
    """
    Format the fighter's name for URL or search:
    - Remove leading/trailing spaces
    - Convert to lowercase
    - Replace spaces with hyphens
    """
    return name.strip().lower().replace(" ", "-")


def normalize_fighter_name(name):
    """
    Normalize the fighter's name to a unified format:
    - Remove extra spaces
    - Convert to lowercase for searching
    - Capitalize the first letter of each word
    """
    return " ".join(word.capitalize() for word in name.strip().split())

# Example function for adjusting fighter probabilities (commented out)
# def adjust_fighter_probabilities(fighter1, fighter2, ufc_dataset):
#     """
#     Calculates normalized win probabilities for two fighters
#     using their stats from calculate_fighter_stats.
#     """
#     # Get stats for each fighter
#     fighter1_stats = calculate_fighter_stats(fighter1, ufc_dataset)
#     fighter2_stats = calculate_fighter_stats(fighter2, ufc_dataset)
#
#     # Use red corner win percentage
#     fighter1_red_win_rate = fighter1_stats['r_win_rate']
#     fighter2_red_win_rate = fighter2_stats['r_win_rate']
#
#     # Check if both fighters have data
#     if fighter1_red_win_rate == 0 and fighter2_red_win_rate == 0:
#         raise ValueError(f"Insufficient data for both fighters: {fighter1}, {fighter2}")
#
#     # Normalize probabilities
#     total = fighter1_red_win_rate + fighter2_red_win_rate
#     fighter1_normalized = (fighter1_red_win_rate / total) * 100 if total > 0 else 0
#     fighter2_normalized = (fighter2_red_win_rate / total) * 100 if total > 0 else 0
#
#     return fighter1_normalized, fighter2_normalized

def get_fighter_metrics(fighter_name, ufc_dataset):
    """
    Returns the fighter's metrics depending on the corner (red or blue).
    If the fighter is not found, returns an error message.
    """
    fighter_name_clean = fighter_name.strip().lower()
    red_fighters = ufc_dataset['r_fighter'].str.strip().str.lower()
    blue_fighters = ufc_dataset['b_fighter'].str.strip().str.lower()

    if fighter_name_clean in red_fighters.values:
        data = ufc_dataset[red_fighters == fighter_name_clean].iloc[0]
        metrics = {
            "Corner": "Red",
            "Age": data['r_age'],
            "Height": data['r_height'],
            "Weight": data['r_weight'],
            "Reach": data['r_reach'],
            "Wins": data['r_wins_total'],
            "Losses": data['r_losses_total'],
            "Strikes Landed per Minute (SLpM)": data['r_SLpM_total'],
            "Strikes Absorbed per Minute (SApM)": data['r_SApM_total'],
            "Significant Strike Accuracy (%)": data['r_sig_str_acc_total'],
            "Takedown Accuracy (%)": data['r_td_acc_total'],
            "Takedown Defense (%)": data['r_td_def_total'],
            "Submission Avg": data['r_sub_avg'],
            "Takedown Avg": data['r_td_avg'],
            "Striking Defense (%)": data['r_str_def_total'],
        }
        return metrics
    elif fighter_name_clean in blue_fighters.values:
        data = ufc_dataset[blue_fighters == fighter_name_clean].iloc[0]
        metrics = {
            "Corner": "Blue",
            "Age": data['b_age'],
            "Height": data['b_height'],
            "Weight": data['b_weight'],
            "Reach": data['b_reach'],
            "Wins": data['b_wins_total'],
            "Losses": data['b_losses_total'],
            "Strikes Landed per Minute (SLpM)": data['b_SLpM_total'],
            "Strikes Absorbed per Minute (SApM)": data['b_SApM_total'],
            "Significant Strike Accuracy (%)": data['b_sig_str_acc_total'],
            "Takedown Accuracy (%)": data['b_td_acc_total'],
            "Takedown Defense (%)": data['b_td_def_total'],
            "Submission Avg": data['b_sub_avg'],
            "Takedown Avg": data['b_td_avg'],
            "Striking Defense (%)": data['b_str_def_total'],
        }
        return metrics
    else:
        return {"Error": f"Fighter '{fighter_name}' not found in the dataset."}

# Example function for standardizing fighters by total stats (commented out)
# def standardize_fighters(fighter1_data, fighter2_data):
#     """
#     Standardizes fighters so that the one with higher total stats
#     is always in the red corner.
#     """
#     fighter1_total = fighter1_data[['r_height', 'r_weight', 'r_reach', 'r_wins_total', 'r_losses_total']].sum().sum()
#     fighter2_total = fighter2_data[['b_height', 'b_weight', 'b_reach', 'b_wins_total', 'b_losses_total']].sum().sum()
#
#     if fighter2_total > fighter1_total:
#         # Swap fighters' corners
#         fighter1_data, fighter2_data = fighter2_data, fighter1_data
#
#     return fighter1_data, fighter2_data
