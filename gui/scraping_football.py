import pandas as pd
from selenium import webdriver


class FootballScrap:
    url = "https://www.flashscore.com/"
    driver = None
    options = None
    all_leagues = []
    all_matches_dict = []
    all_matches = []
    df = None

    # def __init__(self):
    #     self.df = pd.read_excel('mecze.xlsx')

    def run_selenium(self):
        self.options = webdriver.ChromeOptions();
        self.options.add_argument('headless');
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(self.url)
        self.all_matches = self.driver.find_elements_by_class_name("event__match")

        headers = self.driver.find_elements_by_class_name('event__titleBox')

        for head in headers:
            country = head.find_element_by_class_name('event__title--type').text
            league = head.find_element_by_class_name('event__title--name').text
            full_name = country + ' - ' + league
            self.all_leagues.append(full_name)

    def exit(self):
        print("Turning down selenium..")
        self.driver.quit()

    def is_last_match(self, element):
        classes = element.get_attribute("class")
        list_of_classes = classes.split(" ")
        for c in list_of_classes:
            if c == "event__match--last":
                return True
        return False

    def is_live_match(self, element):
        classes = element.get_attribute("class")
        list_of_classes = classes.split(" ")
        for c in list_of_classes:
            if c == "event__match--live":
                return True
        return False

    def is_scheduled_match(self, element):
        classes = element.get_attribute("class")
        list_of_classes = classes.split(" ")
        for c in list_of_classes:
            if c == "event__match--scheduled":
                return True
        return False

    def matches_to_list(self):
        list_of_matches = []
        df = self.df
        df['score'] = df['score'].fillna("-")

        numbers = df['#'].to_list()
        leagues = df['league'].to_list()
        times = df['time'].to_list()
        home_teams = df['home_team'].to_list()
        scores = df['score'].to_list()
        away_teams: list = df['away_team'].to_list()
        types = df['type'].to_list()

        for i in range(0, len(df.index)):
            match = str(numbers[i]) + " " + leagues[i] + " " + times[i] + " " + home_teams[i] + " " + scores[i] + " " + away_teams[i] + " " + types[i]
            list_of_matches.append(match)

        return list_of_matches

    def create_data_frame(self, how_many_matches):
        self.run_selenium()
        number_of_league = 0
        number = 1
        for match in self.all_matches:
            league = self.all_leagues[number_of_league]
            score_list = match.find_element_by_class_name("event__scores").text.split()
            score_correct = "".join(score_list)
            if self.is_live_match(match):

                match_items = {
                    '#': number,
                    'league': league,
                    'time': match.find_element_by_class_name('event__stage--block').text + ' min',
                    'home_team': match.find_element_by_class_name('event__participant--home').text,
                    'home_team_img': match.find_element_by_class_name('event__logo--home').get_attribute("src"),
                    'score': score_correct,
                    'away_team_img': match.find_element_by_class_name('event__logo--away').get_attribute("src"),
                    'away_team': match.find_element_by_class_name('event__participant--away').text,
                    'type': 'LIVE'
                }

                self.all_matches_dict.append(match_items)
            elif self.is_scheduled_match(match):

                match_items = {
                    '#': number,
                    'league': league,
                    'time': match.find_element_by_class_name('event__time').text,
                    'home_team': match.find_element_by_class_name('event__participant--home').text,
                    'home_team_img': match.find_element_by_class_name('event__logo--home').get_attribute("src"),
                    'score': score_correct,
                    'away_team_img': match.find_element_by_class_name('event__logo--away').get_attribute("src"),
                    'away_team': match.find_element_by_class_name('event__participant--away').text,
                    'type': 'SCHEDULED'
                }
                self.all_matches_dict.append(match_items)
            else:
                match_items = {
                    '#': number,
                    'league': league,
                    'time': match.find_element_by_class_name('event__stage--block').text,
                    'home_team': match.find_element_by_class_name('event__participant--home').text,
                    'home_team_img': match.find_element_by_class_name('event__logo--home').get_attribute("src"),
                    'score': score_correct,
                    'away_team_img': match.find_element_by_class_name('event__logo--away').get_attribute("src"),
                    'away_team': match.find_element_by_class_name('event__participant--away').text,
                    'type': 'ENDED'
                }
                self.all_matches_dict.append(match_items)
            print( (number*100)/how_many_matches)

            if self.is_last_match(match):
                number_of_league += 1

            number += 1

            if number == how_many_matches:
                break

        self.df = pd.DataFrame(self.all_matches_dict)
        self.df['score'] = self.df['score'].fillna("-")
        self.df.to_excel(r'mecze.xlsx')

if __name__ == "__main__":
    scrap = FootballScrap()
    scrap.create_data_frame(50)
    scrap.exit()
