import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL for UFC athlete profiles
BASE_URL = 'https://www.ufc.com/athlete'
# Path to the processed UFC dataset
DATA_PATH = 'data/processed/ufc_data_final.csv'

# Function to load the UFC dataset from a CSV file
def load_ufc_dataset():
    """
    Loads the UFC dataset.
    """
    try:
        dataset = pd.read_csv(DATA_PATH)
        return dataset
    except FileNotFoundError:
        raise Exception(f"Dataset not found at {DATA_PATH}. Please ensure the file exists.")
    except Exception as e:
        raise Exception(f"An error occurred while loading the dataset: {e}")

# Function to fetch and parse fighter statistics from the UFC website
def get_fighter_stats_with_styles(fighter_name):
    fighter_url = f"{BASE_URL}/{fighter_name.replace(' ', '-').lower()}"

    response = requests.get(fighter_url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data for fighter {fighter_name}. Status code: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')
    fighter_data = {}

    # Include fighter's name in the dictionary
    fighter_data['name'] = fighter_name.title()

    # Extract profile info
    profile_info = soup.find('div', class_='hero-profile__info')
    fighter_data['profile_info'] = profile_info.text.strip() if profile_info else "No information available."

    # Extract SVG Diagram for Significant Strikes by Target
    svg_section = soup.find('div', class_='c-stat-body__diagram')
    if svg_section:
        svg_element = svg_section.find('svg')
        fighter_data['strikes_by_target_svg'] = str(svg_element) if svg_element else "No SVG available."
    else:
        fighter_data['strikes_by_target_svg'] = "No SVG section found."

    # Extract image URL
    image_wrap = soup.find('div', class_='hero-profile__image-wrap')
    fighter_data['image_url'] = image_wrap.find('img')['src'] if image_wrap else None

    # Extract general stats (wins by KO, submission, first round finishes)
    stats_section = soup.find('div', class_='stats-records-inner')
    if stats_section:
        stats_items = stats_section.find_all('div', class_='athlete-stats__stat')
        fighter_data['wins_ko'] = stats_items[0].find('p', class_='athlete-stats__stat-numb').text.strip() if len(
            stats_items) > 0 else "N/A"
        fighter_data['wins_sub'] = stats_items[1].find('p', class_='athlete-stats__stat-numb').text.strip() if len(
            stats_items) > 1 else "N/A"
        fighter_data['first_round_finishes'] = stats_items[2].find('p',
                                                                   class_='athlete-stats__stat-numb').text.strip() if len(
            stats_items) > 2 else "N/A"
    else:
        fighter_data['wins_ko'] = "N/A"
        fighter_data['wins_sub'] = "N/A"
        fighter_data['first_round_finishes'] = "N/A"

    # Extract striking and takedown stats
    overlap_section = soup.find('div', class_='overlap-athlete-content--horizontal')
    if overlap_section:
        # Striking Accuracy
        striking_section = overlap_section.find('div', class_='c-overlap__chart')
        if striking_section:
            striking_accuracy_circle = striking_section.find('text', class_='e-chart-circle__percent')
            fighter_data['striking_accuracy'] = striking_accuracy_circle.text.strip() if striking_accuracy_circle else "N/A"

            stats_section = overlap_section.find('div', class_='c-overlap__stats-wrap')
            if stats_section:
                stats = stats_section.find_all('dl', class_='c-overlap__stats')
                if len(stats) >= 2:
                    fighter_data['strikes_landed'] = stats[0].find('dd', class_='c-overlap__stats-value').text.strip()
                    fighter_data['strikes_attempted'] = stats[1].find('dd', class_='c-overlap__stats-value').text.strip()

        # Takedown Accuracy
        stats_blocks = soup.find_all('div', class_='stats-records-inner')
        takedown_block = None
        for block in stats_blocks:
            title = block.find('h2', class_='e-t3')
            if title and "Takedown Accuracy" in title.text:
                takedown_block = block
                break

        if takedown_block:
            accuracy_circle = takedown_block.find('text', class_='e-chart-circle__percent')
            fighter_data['takedown_accuracy'] = accuracy_circle.text.strip() if accuracy_circle else "N/A"

            takedown_stats = takedown_block.find('div', class_='c-overlap__stats-wrap')
            if takedown_stats:
                stats = takedown_stats.find_all('dl', class_='c-overlap__stats')
                if len(stats) > 0:
                    takedowns_landed = stats[0].find('dd', class_='c-overlap__stats-value')
                    fighter_data['takedowns_landed'] = takedowns_landed.text.strip() if takedowns_landed else "N/A"
                if len(stats) > 1:
                    takedowns_attempted = stats[1].find('dd', class_='c-overlap__stats-value')
                    fighter_data['takedowns_attempted'] = takedowns_attempted.text.strip() if takedowns_attempted else "N/A"

    # Extract Significant Strikes by Position
    position_block = soup.find('div', class_='c-stat-3bar', text=lambda x: x and "Sig. Str. By Position" in x)
    if position_block:
        position_data = position_block.find_all('div', class_='c-stat-3bar__group')
        fighter_data['strikes_by_position'] = {
            group.find('div', class_='c-stat-3bar__label').text.strip(): group.find('div', class_='c-stat-3bar__value').text.strip()
            for group in position_data
        }
    else:
        fighter_data['strikes_by_position'] = {}

    # Extract Significant Strikes by Target
    target_block = soup.find('div', class_='c-stat-body')
    if target_block:
        target_groups = target_block.find_all('g', id=lambda x: x and x.startswith("e-stat-body_x5F"))
        fighter_data['strikes_by_target'] = {}
        for group in target_groups:
            label = group.find('text', transform=lambda x: x and x.startswith("matrix"))
            value = group.find('text', fill="#D20A0A")
            if label and value:
                fighter_data['strikes_by_target'][label.text.strip()] = value.text.strip()
    else:
        fighter_data['strikes_by_target'] = {}

    # Extract Win by Method
    method_block = soup.find('div', class_='c-stat-3bar', text=lambda x: x and "Win by Method" in x)
    if method_block:
        method_data = method_block.find_all('div', class_='c-stat-3bar__group')
        fighter_data['win_by_method'] = {
            group.find('div', class_='c-stat-3bar__label').text.strip(): group.find('div', class_='c-stat-3bar__value').text.strip()
            for group in method_data
        }
    else:
        fighter_data['win_by_method'] = {}

    return fighter_data




