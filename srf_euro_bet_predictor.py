import pandas as pd
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def fetch_page_content(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    
    # Wait for the page to load and accept cookies if necessary
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    
    try:
        consent_button = driver.find_element(By.ID, '_evidon-accept-button')
        if consent_button:
            consent_button.click()
    except:
        pass  # If there's no consent button, continue

    time.sleep(3)  # Wait for the content to load
    html_content = driver.page_source
    driver.quit()
    return html_content

def process_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract country names
    teams_section = soup.find('section', class_='SoccerPreLive-styles-module-content')
    teams = teams_section.find_all('div', class_='SoccerPreLive-styles-module-team-data')
    country_names = [team.find('div', class_='SoccerPreLive-styles-module-team-name').text.strip() for team in teams]

    # Extract match odds for "Tipp"
    tipp_section = soup.find('div', class_='Category-styles-module-market-group')
    tipp_odds_data = []

    if tipp_section:
        odds_buttons = tipp_section.find_all('button', class_='OddResult-styles-module-odd-button')
        labels = ['1', 'X', '2']
        for button, label in zip(odds_buttons, labels):
            odds = button.find('div', class_='OddResult-styles-module-value-cell').text.strip()
            country = None
            if label == '1':
                country = country_names[0]  # Home team
            elif label == 'X':
                country = 'Draw'
            elif label == '2':
                country = country_names[1]  # Away team
            tipp_odds_data.append({'Country': country, 'Odds': odds})

    # Convert the list of dictionaries to a DataFrame
    tipp_odds_df = pd.DataFrame(tipp_odds_data)

    # Extract match results and probabilities for "Ergebnis"
    ergebnis_section = soup.find_all('div', class_='OddsDivided-styles-module-odds-divided')
    ergebnis_data = []

    for section in ergebnis_section:
        buttons = section.find_all('button', class_='OddResult-styles-module-odd-button')
        for button in buttons:
            label = button.find('div', class_='OddResult-styles-module-label-cell').text.strip()
            probability = button.find('div', class_='OddResult-styles-module-value-cell').text.strip()
            ergebnis_data.append({'Result': label, 'Probability': probability})

    # Convert the list of dictionaries to a DataFrame
    ergebnis_df = pd.DataFrame(ergebnis_data)

    # Convert Odds to Probabilities (handle comma as decimal separator)
    tipp_odds_df['Odds'] = tipp_odds_df['Odds'].str.replace(',', '.').astype(float)
    tipp_odds_df['Probability'] = 1 / tipp_odds_df['Odds']
    tipp_odds_df['Normalized_Probability'] = tipp_odds_df['Probability'] / tipp_odds_df['Probability'].sum()

    # Convert result odds to probabilities (handle comma as decimal separator)
    ergebnis_df['Probability'] = ergebnis_df['Probability'].str.replace(',', '.').astype(float)
    ergebnis_df = ergebnis_df[ergebnis_df['Probability'] != 250]  # Exclude rows with odds of 250
    ergebnis_df = ergebnis_df[ergebnis_df['Result'] != 'X:X']  # Exclude 'X:X' result
    ergebnis_df['Probability'] = 1 / ergebnis_df['Probability']
    ergebnis_df['Normalized_Probability'] = ergebnis_df['Probability'] / ergebnis_df['Probability'].sum()

    # Extract country names
    home_team = tipp_odds_df.loc[tipp_odds_df['Country'] != 'Draw', 'Country'].values[0]
    away_team = tipp_odds_df.loc[tipp_odds_df['Country'] != 'Draw', 'Country'].values[1]

    # Calculate expected goal differences
    def calculate_goal_difference(result):
        home_goals, away_goals = map(int, result.split(':'))
        return home_goals - away_goals

    ergebnis_df['Goal_Difference'] = ergebnis_df['Result'].apply(calculate_goal_difference)

    # Create a table showing the probability of each goal difference
    goal_difference_probabilities = ergebnis_df.groupby('Goal_Difference')['Normalized_Probability'].sum().reset_index()
    goal_difference_probabilities = goal_difference_probabilities.rename(columns={'Normalized_Probability': 'Probability'})

    # Calculate the expected points for guessing the outcome correctly
    tipp_odds_df['Expectation'] = tipp_odds_df['Normalized_Probability'] * 5

    # Normalize probabilities within each group
    home_win_probabilities = goal_difference_probabilities[goal_difference_probabilities['Goal_Difference'] > 0].copy()
    away_win_probabilities = goal_difference_probabilities[goal_difference_probabilities['Goal_Difference'] < 0].copy()
    draw_probabilities = goal_difference_probabilities[goal_difference_probabilities['Goal_Difference'] == 0].copy()

    home_win_probabilities['Normalized_Probability'] = home_win_probabilities['Probability'] / home_win_probabilities['Probability'].sum()
    away_win_probabilities['Normalized_Probability'] = away_win_probabilities['Probability'] / away_win_probabilities['Probability'].sum()
    draw_probabilities['Normalized_Probability'] = draw_probabilities['Probability'] / draw_probabilities['Probability'].sum()

    # Calculate the expected points for guessing the goal difference correctly within each group
    home_win_probabilities['Expectation'] = home_win_probabilities['Normalized_Probability'] * 3
    away_win_probabilities['Expectation'] = away_win_probabilities['Normalized_Probability'] * 3
    draw_probabilities['Expectation'] = draw_probabilities['Normalized_Probability'] * 3

    # Merge the normalized probabilities back into the goal_difference_probabilities DataFrame
    goal_difference_probabilities = pd.concat([home_win_probabilities, away_win_probabilities, draw_probabilities])

    # Calculate the total expected points for each goal difference
    goal_difference_probabilities['Expectation_sum'] = goal_difference_probabilities.apply(
        lambda row: tipp_odds_df.loc[tipp_odds_df['Country'] == home_team, 'Expectation'].values[0] + row['Expectation'] if row['Goal_Difference'] > 0 else
                    tipp_odds_df.loc[tipp_odds_df['Country'] == away_team, 'Expectation'].values[0] + row['Expectation'] if row['Goal_Difference'] < 0 else
                    tipp_odds_df.loc[tipp_odds_df['Country'] == 'Draw', 'Expectation'].values[0] + row['Expectation'],
        axis=1
    )

    # Multiply ergebnis_df probabilities with 2
    ergebnis_df['Expectation'] = ergebnis_df['Normalized_Probability'] * 2

    # Add the expectation_sum to the score expectation
    def add_goal_difference_expectation(row):
        goal_diff = row['Goal_Difference']
        goal_diff_expectation = goal_difference_probabilities.loc[goal_difference_probabilities['Goal_Difference'] == goal_diff, 'Expectation_sum'].values[0]
        return row['Expectation'] + goal_diff_expectation

    ergebnis_df['Total_Expectation'] = ergebnis_df.apply(add_goal_difference_expectation, axis=1)

    # Sort the results by Total_Expectation
    ergebnis_df = ergebnis_df.sort_values(by='Total_Expectation', ascending=False)

    return country_names, tipp_odds_df, goal_difference_probabilities, ergebnis_df

def main(url):
    html_content = fetch_page_content(url)
    country_names, tipp_odds_df, goal_difference_probabilities, ergebnis_df = process_data(html_content)
    
    # Print the results
    print(f"Teams playing: {country_names[0]} vs {country_names[1]}")
    print("\nTipp Odds DataFrame:")
    print(tipp_odds_df[['Country', 'Odds', 'Probability', 'Expectation']])
    print("\nGoal Difference Probabilities DataFrame:")
    print(goal_difference_probabilities[['Goal_Difference', 'Probability', 'Expectation']])
    print("\nErgebnis DataFrame:")
    print(ergebnis_df[['Result', 'Probability', 'Goal_Difference', 'Expectation', 'Total_Expectation']])

if __name__ == "__main__":
    url = input("Enter the URL: ")
    main(url)
