import pandas as pd
from selenium import webdriver


class Table:
    options = None
    driver = None

    def __init__(self):
        self.run_selenium()

    def run_selenium(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.driver = webdriver.Chrome(options=self.options)

    def exit(self):
        print("Turning down selenium..")
        self.driver.quit()

    def create_team_list(self, url):
        self.driver.get(url)

        all_teams = self.driver.find_elements_by_class_name("row___1rtP1QI")
        all_teams_list = []

        i = 1
        for team in all_teams:
            team_name = team.find_element_by_class_name("rowCellParticipantName___38vskiN").text
            numbers = team.find_elements_by_class_name("cell___4WLG6Yd")
            goals = team.find_element_by_class_name("cellScore___2A1RcrA").text

            numbers_list = [number.text for number in numbers]
            numbers_string = ' | '.join(numbers_list)
            full_name = str(i) + ". " + team_name + " " + numbers_string + " | " + goals
            all_teams_list.append(full_name)
            i += 1

        return all_teams_list


if __name__ == "__main__":
    t = Table()
    table = t.create_team_list("https://www.flashscore.com/football/germany/bundesliga/")
    print(table)
