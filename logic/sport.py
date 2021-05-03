# import http.client
# import json
#
# connection = http.client.HTTPConnection('api.football-data.org')
# headers = { 'X-Auth-Token': 'c2ea3671544c415496e76bedd214c651' }
# connection.request('GET', '/v2/competitions/DED', None, headers )
# response = json.loads(connection.getresponse().read().decode())
#
# print (response)

from selenium import webdriver

url = "https://www.flashscore.com/"

options = webdriver.ChromeOptions();
options.add_argument('headless');
driver = webdriver.Chrome(options=options)

driver.get(url)

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

all_matches = driver.find_elements_by_class_name('sportName soccer')

headers = driver.find_elements_by_class_name('event__titleBox')
all_leagues = []

for head in headers:
    country = head.find_element_by_class_name('event__title--type').text
    league = head.find_element_by_class_name('event__title--name').text
    full_name = country + ' - ' + league
    all_leagues.append(full_name)




