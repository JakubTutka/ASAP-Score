import pandas as pd
from selenium import webdriver

url = "https://www.flashscore.com/"

options = webdriver.ChromeOptions();
options.add_argument('headless');
driver = webdriver.Chrome(options=options)

driver.get(url)

def is_last_match(element):
    classes = element.get_attribute("class")
    list_of_classes = classes.split(" ")
    for c in list_of_classes:
        if c == "event__match--last":
            return True
    return False

def is_live_match(element):
    classes = element.get_attribute("class")
    list_of_classes = classes.split(" ")
    for c in list_of_classes:
        if c == "event__match--live":
            return True
    return False

def is_scheduled_match(element):
    classes = element.get_attribute("class")
    list_of_classes = classes.split(" ")
    for c in list_of_classes:
        if c == "event__match--scheduled":
            return True
    return False


# JESZCZE NIE SKONZONE
#class="event__match event__match--oneLine event__match--scheduled "

# JESZCZE NIE SKONCZONE ostatnie
#class="event__match event__match--oneLine event__match--scheduled event__match--last "

#SKONZONE
#class="event__match event__match--oneLine "

#SKONCZONE ostatnie
#class="event__match event__match--oneLine event__match--last "

# W TRAKCIE
#class="event__match event__match--oneLine event__match--live "

# W TRAKCIE ostatnie
#class="event__match event__match--oneLine event__match--live event__match--last "

headers = driver.find_elements_by_class_name('event__titleBox')
all_leagues = []

for head in headers:
    country = head.find_element_by_class_name('event__title--type').text
    league = head.find_element_by_class_name('event__title--name').text
    full_name = country + ' - ' + league
    all_leagues.append(full_name)

# live_matches = driver.find_elements_by_class_name("event__match--live")
# # last_matches = driver.find_elements_by_class_name("event__match--last")
# # not_started_matches = driver.find_elements_by_class_name("event__match--scheduled")
all_matches = driver.find_elements_by_class_name("event__match")


all_matches_dict = []
i = 0
number = 1
for match in all_matches:
    league = all_leagues[i]
    score_list = match.find_element_by_class_name("event__scores").text.split()
    score_correct = "".join(score_list)
    if is_live_match(match):

        match_items = {
            '#': number,
            'league': league,
            'time': match.find_element_by_class_name('event__stage--block').text,
            'home_team': match.find_element_by_class_name('event__participant--home').text,
            'home_team_img': match.find_element_by_class_name('event__logo--home').get_attribute("src"),
            'score': score_correct,
            'away_team': match.find_element_by_class_name('event__participant--away').text,
            'away_team_img': match.find_element_by_class_name('event__logo--away').get_attribute("src"),
            'type': 'LIVE'
        }

        all_matches_dict.append(match_items)
    elif is_scheduled_match(match):

        match_items = {
            '#': number,
            'league': league,
            'time': match.find_element_by_class_name('event__time').text,
            'home_team': match.find_element_by_class_name('event__participant--home').text,
            'home_team_img': match.find_element_by_class_name('event__logo--home').get_attribute("src"),
            'score': score_correct,
            'away_team': match.find_element_by_class_name('event__participant--away').text,
            'away_team_img': match.find_element_by_class_name('event__logo--away').get_attribute("src"),
            'type': 'SCHEDULED'
        }
        all_matches_dict.append(match_items)
    else:
        match_items = {
            '#': number,
            'league': league,
            'time': match.find_element_by_class_name('event__stage--block').text,
            'home_team': match.find_element_by_class_name('event__participant--home').text,
            'home_team_img': match.find_element_by_class_name('event__logo--home').get_attribute("src"),
            'score': score_correct,
            'away_team': match.find_element_by_class_name('event__participant--away').text,
            'away_team_img': match.find_element_by_class_name('event__logo--away').get_attribute("src"),
            'type': 'ENDED'
        }
        all_matches_dict.append(match_items)

    if is_last_match(match):
        i += 1

    number += 1

print(str(len(all_leagues)) + 'dupa')
df = pd.DataFrame(all_matches_dict)
df.to_excel(r'mecze.xlsx')
driver.quit()



