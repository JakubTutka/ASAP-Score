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

    def __init__(self):

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

    def is_last_match(self,element):
        classes = element.get_attribute("class")
        list_of_classes = classes.split(" ")
        for c in list_of_classes:
            if c == "event__match--last":
                return True
        return False

    def is_live_match(self,element):
        classes = element.get_attribute("class")
        list_of_classes = classes.split(" ")
        for c in list_of_classes:
            if c == "event__match--live":
                return True
        return False

    def is_scheduled_match(self,element):
        classes = element.get_attribute("class")
        list_of_classes = classes.split(" ")
        for c in list_of_classes:
            if c == "event__match--scheduled":
                return True
        return False

    def create_data_frame(self):
        i = 0
        for match in self.all_matches:
            league = self.all_leagues[i]
            score_list = match.find_element_by_class_name("event__scores").text.split()
            score_correct = "".join(score_list)
            if self.is_live_match(match):

                match_items = {
                    'league': league,
                    'time': match.find_element_by_class_name('event__stage--block').text,
                    'home_team': match.find_element_by_class_name('event__participant--home').text,
                    'home_team_img': match.find_element_by_class_name('event__logo--home').get_attribute("src"),
                    'score': score_correct,
                    'away_team': match.find_element_by_class_name('event__participant--away').text,
                    'away_team_img': match.find_element_by_class_name('event__logo--away').get_attribute("src"),
                    'type': 'LIVE'
                }

                self.all_matches_dict.append(match_items)
            elif self.is_scheduled_match(match):

                match_items = {
                    'league': league,
                    'time': match.find_element_by_class_name('event__time').text,
                    'home_team': match.find_element_by_class_name('event__participant--home').text,
                    'home_team_img': match.find_element_by_class_name('event__logo--home').get_attribute("src"),
                    'score': score_correct,
                    'away_team': match.find_element_by_class_name('event__participant--away').text,
                    'away_team_img': match.find_element_by_class_name('event__logo--away').get_attribute("src"),
                    'type': 'SCHEDULED'
                }
                self.all_matches_dict.append(match_items)
            else:
                match_items = {
                    'league': league,
                    'time': match.find_element_by_class_name('event__stage--block').text,
                    'home_team': match.find_element_by_class_name('event__participant--home').text,
                    'home_team_img': match.find_element_by_class_name('event__logo--home').get_attribute("src"),
                    'score': score_correct,
                    'away_team': match.find_element_by_class_name('event__participant--away').text,
                    'away_team_img': match.find_element_by_class_name('event__logo--away').get_attribute("src"),
                    'type': 'ENDED'
                }
                self.all_matches_dict.append(match_items)
            print(i)
            if self.is_last_match(match):
                i += 1
        self.df = pd.DataFrame(self.all_matches_dict)

scrap = FootballScrap()

scrap.create_data_frame()
scrap.df.to_excel(r'mecze.xlsx')
scrap.exit()