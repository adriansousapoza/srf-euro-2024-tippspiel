
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
Enter the URL: https://sports.tipico.de/de/alle/fussball/em-wetten/event/587999910?eventPanelMode=2&t=match
```

### Example Output

```bash
Teams playing: Tschechien vs Türkei

Tipp Odds DataFrame:
      Country  Odds  Probability  Expectation
0  Tschechien  2.45     0.408163     1.941748
1        Draw  3.50     0.285714     1.359223
2      Türkei  2.80     0.357143     1.699029

Goal Difference Probabilities DataFrame:
   Goal_Difference  Probability  Expectation
5                1     0.196932     1.611123
6                2     0.099493     0.813964
7                3     0.051498     0.421311
8                4     0.018775     0.153603
0               -4     0.018775     0.156194
1               -3     0.051498     0.428417
2               -2     0.094244     0.784032
3               -1     0.196097     1.631357
4                0     0.272688     3.000000

Ergebnis DataFrame:
   Result  Probability  Goal_Difference  Expectation  Total_Expectation
9     1:1     0.166667                0     0.250337           4.609560
10    2:2     0.083333                0     0.125168           4.484392
8     0:0     0.071429                0     0.107287           4.466510
11    3:3     0.033333                0     0.050067           4.409291
12    4:4     0.008333                0     0.012517           4.371740
0     1:0     0.111111                1     0.166891           3.719762
2     2:1     0.111111                1     0.166891           3.719762
5     3:2     0.040000                1     0.060081           3.612951
18    1:2     0.111111               -1     0.166891           3.497278
16    0:1     0.100000               -1     0.150202           3.480588
21    2:3     0.050000               -1     0.075101           3.405487
1     2:0     0.076923                2     0.115540           2.871251
4     3:1     0.055556                2     0.083446           2.839157
17    0:2     0.066667               -2     0.100135           2.583195
20    1:3     0.058824               -2     0.088354           2.571415
3     3:0     0.040000                3     0.060081           2.423139
7     4:1     0.028571                3     0.042915           2.405973
19    0:3     0.040000               -3     0.060081           2.187527
23    1:4     0.028571               -3     0.042915           2.170361
6     4:0     0.025000                4     0.037550           2.132901
22    0:4     0.025000               -4     0.037550           1.892773
```

## How it Works

1. **Web Scraping**: The script uses Selenium to navigate to the provided URL and fetch the page content.
2. **Data Extraction**: BeautifulSoup is used to parse the HTML and extract relevant data, including teams, odds, and probabilities.
3. **Calculations**: The script calculates expected values for various betting outcomes, such as correct winner, correct score, and goal differences.
4. **Output**: The results are printed in the terminal, showing the teams playing, betting odds, and calculated expected values.

## License

This project is licensed under the MIT License.
