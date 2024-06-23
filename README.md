
# SRF Euro 2024 Tippspiel

This project provides a tool to predict betting outcomes for Euro 2024 matches using data scraped from Tipico. The script calculates expected values for various betting scenarios and displays the results in the terminal.

## Requirements

- Python 3.x
- Selenium
- BeautifulSoup
- pandas
- requests
- webdriver_manager

You can install the necessary dependencies using:

```bash
pip install selenium beautifulsoup4 pandas requests webdriver_manager
```

## Usage

To run the script, execute the following command in your terminal:

```bash
python3 srf_euro_bet_predictor.py
```

You will be prompted to enter the URL of the Tipico page you want to scrape. For example:

```bash
(base) ➜  srf-euro-2024-tippspiel git:(main) python3 srf_euro_bet_predictor.py
Enter the URL: https://sports.tipico.de/de/alle/fussball/em-wetten/event/587999910?eventPanelMode=2&t=match
```

### Example Output

```bash
Teams playing: Tschechien vs Türkei

Tipp Odds DataFrame:
      Country  Odds  Probability  Expectation
0  Tschechien  2.45     0.388350     1.941748
1        Draw  3.50     0.271845     1.359223
2      Türkei  2.80     0.339806     1.699029

Goal Difference Probabilities DataFrame:
   Goal_Difference  Probability  Expectation
0               -4     0.018775     0.056326
1               -3     0.051498     0.154493
2               -2     0.094244     0.282733
3               -1     0.196097     0.588291
4                0     0.272688     0.818064
5                1     0.196932     0.590795
6                2     0.099493     0.298478
7                3     0.051498     0.154493
8                4     0.018775     0.056326

Ergebnis DataFrame:
   Result  Probability  Goal_Difference  Expectation  Total_Expectation
0     1:0     0.083446                1     0.166891           2.699433
2     2:1     0.083446                1     0.166891           2.699433
5     3:2     0.030040                1     0.060081           2.592623
18    1:2     0.083446               -1     0.166891           2.454211
16    0:1     0.075101               -1     0.150202           2.437522
9     1:1     0.125168                0     0.250337           2.427624
21    2:3     0.037550               -1     0.075101           2.362421
1     2:0     0.057770                2     0.115540           2.355766
4     3:1     0.041723                2     0.083446           2.323671
10    2:2     0.062584                0     0.125168           2.302456
8     0:0     0.053644                0     0.107287           2.284575
11    3:3     0.025034                0     0.050067           2.227355
12    4:4     0.006258                0     0.012517           2.189805
3     3:0     0.030040                3     0.060081           2.156322
7     4:1     0.021457                3     0.042915           2.139156
17    0:2     0.050067               -2     0.100135           2.081897
20    1:3     0.044177               -2     0.088354           2.070116
6     4:0     0.018775                4     0.037550           2.035624
19    0:3     0.030040               -3     0.060081           1.913603
23    1:4     0.021457               -3     0.042915           1.896437
22    0:4     0.018775               -4     0.037550           1.792905
(base) ➜  srf-euro-2024-tippspiel git:(main) ✗ 

```

## How it Works

1. **Web Scraping**: The script uses Selenium to navigate to the provided URL and fetch the page content.
2. **Data Extraction**: BeautifulSoup is used to parse the HTML and extract relevant data, including teams, odds, and probabilities.
3. **Calculations**: The script calculates expected values for various betting outcomes, such as correct winner, correct score, and goal differences.
4. **Output**: The results are printed in the terminal, showing the teams playing, betting odds, and calculated expected values.

## License

This project is licensed under the MIT License.
