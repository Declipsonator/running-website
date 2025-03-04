import requests
import json
import purdy
import relays
from datetime import datetime

import save


def get_people(gender='M'):
    # Rotate through all pages of results
    page_number = 1
    page = json.loads(json.loads(get_page(page_number, gender=gender)))
    people = {}

    # Find what # to subtract from to get grade (ex. 2037 - 2025 = 12)
    now = datetime.now()
    subtract = (now.year + 12) if now.month < 8 else (now.year + 13)

    while True:
        for person in page['results']:

            # For each result in the page, extract the name, time, event, and grade
            name = person['athlete_fname'] + " " + person['athlete_lname']
            time = person['performance']
            event = person['event_name']
            grade = subtract -  int(person['graduate'])
            if grade < 0:
                continue


            if name not in people:
                people[name] = {'grade': grade}

            people[name][event] = time

        if not page['hasNext']:
            break
        page_number += 1
        page = json.loads(json.loads(get_page(page_number, gender=gender)))


    return people


def get_page(number, gender='M'):
    print(gender)
    link = f'https://www.yentiming.com/leaderboard/get?limit=49&sex={gender}&events%5B%5D=6&events%5B%5D=7&events%5B%5D=8&events%5B%5D=9&events%5B%5D=10&events%5B%5D=13&events%5B%5D=15&events%5B%5D=25&events%5B%5D=26&events%5B%5D=27&events%5B%5D=28&events%5B%5D=29&events%5B%5D=30&events%5B%5D=31&events%5B%5D=32&events%5B%5D=33&events%5B%5D=34&events%5B%5D=35&events%5B%5D=36&events%5B%5D=37&events%5B%5D=38&events%5B%5D=39&events%5B%5D=40&events%5B%5D=43&events%5B%5D=44&events%5B%5D=45&events%5B%5D=46&events%5B%5D=51&events%5B%5D=52&events%5B%5D=54&events%5B%5D=65&events%5B%5D=69&events%5B%5D=75&events%5B%5D=76&events%5B%5D=77&events%5B%5D=78&events%5B%5D=80&events%5B%5D=100&events%5B%5D=101&events%5B%5D=107&events%5B%5D=109&events%5B%5D=110&teams%5B%5D=85&season=indoor&year=2025&classs=&league=&name=&page={number}&sort_order=ASC&_=1739047933965'
    response = requests.get(link).text

    return response

def unformat_performance(time):
    if '-' in time:
        feet, inches = time.split('-')
        return int(feet) * 12 + float(inches)

    if ':' in time:
        minutes, seconds = time.split(':')
        return int(minutes) * 60 + float(seconds)
    else:
        return float(time)

def format_time(time):
    minutes = int(time // 60)
    seconds = time % 60
    return f'{minutes}:{("0" if seconds < 10 else "")}{round(seconds, 2)}'

def add_conversions(people):
    new_people = people
    for name in people:
        person = people[name]
        #1600m
        sixteen_time = 0
        if '1500m' in person.keys():
            sixteen_time = purdy.convert_distance(1500, unformat_performance(person['1500m']), 1609.34)

        if sixteen_time != 0:
            new_people[name]['1600m'] = format_time(sixteen_time)


        # 1200m
        twelve_time = 0
        if '1600m' in person.keys():
            twelve_time = purdy.convert_distance(1600, unformat_performance(person['1600m']), 1200)
        if '1000m' in person.keys():
            thoustwlve_time = purdy.convert_distance(1000, unformat_performance(person['1000m']), 1200)
            if thoustwlve_time < twelve_time or twelve_time == 0:
                twelve_time = thoustwlve_time
        if '1500m' in person.keys():
            fifteentwelve_time = purdy.convert_distance(1500, unformat_performance(person['1500m']), 1200)
            if fifteentwelve_time < twelve_time or twelve_time == 0:
                twelve_time = fifteentwelve_time


        if twelve_time != 0:
            new_people[name]['1200m'] = format_time(twelve_time)

        # 800
        eight_time = 0
        if '600m' in person.keys():
            eight_time = purdy.convert_distance(600, unformat_performance(person['600m']), 800)
        if '1000m' in person.keys():
            thouseight_time = purdy.convert_distance(1000, unformat_performance(person['1000m']), 800)
            if thouseight_time < eight_time or eight_time == 0:
                eight_time = thouseight_time

        if eight_time != 0:
            new_people[name]['800m'] = format_time(eight_time)

        # 400
        four_time = 0
        if '300m' in person.keys():
            four_time = purdy.convert_distance(300, unformat_performance(person['300m']), 400)
        if '600m' in person.keys():
            thouseight_time = purdy.convert_distance(600, unformat_performance(person['600m']), 400)
            if thouseight_time < four_time or four_time == 0:
                four_time = thouseight_time

        if four_time != 0:
            new_people[name]['400m'] = format_time(four_time)

        # 200
        two_time = 0
        if '300m' in person.keys():
            two_time = purdy.convert_distance(300, unformat_performance(person['300m']), 200)

        if two_time != 0:
            new_people[name]['200m'] = format_time(two_time)

        # Mile
        mile_time = 0
        if '1600m' in person.keys():
            mile_time = purdy.convert_distance(1600, unformat_performance(person['1600m']), 1609.34)
        if '1500m' in person.keys():
            fifteenmile_time = purdy.convert_distance(1500, unformat_performance(person['1500m']), 1609.34)
            if fifteenmile_time < mile_time or mile_time == 0:
                mile_time = fifteenmile_time



        if mile_time != 0:
            new_people[name]['1609m'] = format_time(mile_time)


    return people


def get_top_5_per_event(results):
    top_per_event = {}

    for name, data in results.items():
        for event, time in data.items():
            # Only events that have numbers in them
            if not any(char.isdigit() for char in event):
                continue

            if event == "grade":  # Skip grade field
                continue

            if event not in top_per_event:
                top_per_event[event] = []

            # Append current athlete's result
            top_per_event[event].append({"name": name, "time": time})

            # Sort the list by converted time and keep only top 5
            top_per_event[event] = sorted(
                top_per_event[event], key=lambda x: unformat_performance(x["time"])  # Sort by time in seconds
            )[:5]  # Keep only top 5

    return top_per_event



# bigdict = {'Frank D’Angelo': {'grade': 12, '55m': '00:06.68', '300m': '00:36.32', '600m': '01:32.06'}, 'Bailey Frank': {'grade': 12, '55m': '00:06.82', '300m': '00:38.94'}, 'Owen Andreatta': {'grade': 12, '55m': '00:06.83'}, 'Corey Roeser': {'grade': 11, '55m': '00:06.85', '300m': '00:40.02', '600m': '01:35.91'}, 'Brayden Schlicker': {'grade': 11, '55m': '00:06.91', '300m': '00:40.02'}, 'Sam Newburge': {'grade': 11, '55m': '00:07.03', '300m': '00:37.80', '600m': '01:33.80'}, 'CJ Wheaton': {'grade': 12, '55m': '00:07.04', '300m': '00:38.71'}, 'Austin Corwin': {'grade': 10, '55m': '00:07.05', '300m': '00:38.85'}, 'Nathan Supersad': {'grade': 9, '55m': '00:07.05', '300m': '00:41.93'}, 'Christian Stewart': {'grade': 11, '55m': '00:07.16', '300m': '00:40.90'}, 'Jared Mulley': {'grade': 10, '55m': '00:07.16', '300m': '00:38.74', '600m': '01:34.05'}, 'Leith Steele': {'grade': 10, '55m': '00:07.17', '55m Hurdles': '00:09.04', '300m': '00:40.46', 'High Jump': '05-06.00'}, 'Amare Bordley': {'grade': 9, '55m': '00:07.22', '300m': '00:44.02', 'High Jump': '04-09.00'}, 'Remington Kayser': {'grade': 9, '55m': '00:07.29', '300m': '00:41.36'}, 'Kaleb Casiano': {'grade': 11, '55m': '00:07.31', '300m': '00:45.69'}, 'Brandon Wildrick': {'grade': 11, '55m': '00:07.31', '300m': '00:41.80', 'High Jump': '04-06.00'}, 'Peter Huang': {'grade': 11, '55m': '00:07.33', '300m': '00:44.11'}, 'Aidan Caselli': {'grade': 10, '55m': '00:07.33', '300m': '00:44.11'}, 'Jayden Stafford': {'grade': 10, '55m': '00:07.36', '300m': '00:42.41'}, 'James Carter III': {'grade': 10, '55m': '00:07.37', '300m': '00:41.27'}, 'Anthony Bowen': {'grade': 10, '55m': '00:07.39', '300m': '00:39.07', '600m': '01:38.33'}, 'Jaki Huang': {'grade': 11, '55m': '00:07.44', '300m': '00:49.55', '600m': '02:07.51'}, 'Souksanh Sirimongkhoun': {'grade': 10, '55m': '00:07.48', '300m': '00:43.67'}, 'Ryan Mathis': {'grade': 12, '55m': '00:07.48', '300m': '00:42.11', 'High Jump': '06-02.00'}, 'Sam Shah': {'grade': 12, '55m': '00:07.50', 'Pole Vault': '10-03.00'}, 'Daryl Dutko': {'grade': 10, '55m': '00:07.60', '55m Hurdles': '00:10.81', '300m': '00:41.86', '600m': '01:39.81'}, 'Nico Zukaitis': {'grade': 9, '55m': '00:07.60', '300m': '00:42.84'}, 'Jaiden Balkum': {'grade': 9, '55m': '00:07.66', '300m': '00:45.98'}, 'Jayden Quinones': {'grade': 10, '55m': '00:07.73', '55m Hurdles': '00:11.74', '300m': '00:44.33'}, 'Ethan Betz': {'grade': 10, '55m': '00:07.83', '300m': '00:46.48'}, 'Teddy Carter': {'grade': 9, '55m': '00:08.00', '55m Hurdles': '00:11.35'}, 'Yaxiel Acosta': {'grade': 10, '55m': '00:08.14', '300m': '00:49.78'}, 'Michael Supersad': {'grade': 11, '55m': '00:08.19'}, 'Harun Abdulkadir': {'grade': 9, '55m': '00:08.33', '300m': '00:49.47'}, 'SaVon Bryant': {'grade': 11, '55m': '00:08.54', '300m': '00:53.39', 'Long Jump': '12-09.00'}, 'Carson Gould': {'grade': 10, '55m': '00:08.94'}, 'Kacey Ulrich': {'grade': 9, '55m': '00:09.03', '300m': '00:51.45', 'Long Jump': '11-03.75'}, 'Jackson Hickey': {'grade': 11, '300m': '00:39.66', '600m': '01:28.82', '1000m': '02:35.55', '1600m': '04:29.66', '3200m': '10:00.65'}, 'David Blodgett': {'grade': 11, '300m': '00:40.25', '600m': '01:30.51', '1000m': '02:49.49'}, 'Ethan Leombrone': {'grade': 11, '300m': '00:41.47', '600m': '01:33.22', '1000m': '02:43.82', '1600m': '04:36.62', '3200m': '10:25.92'}, 'Andrew Hain': {'grade': 11, '300m': '00:41.96', '600m': '01:39.30', '1000m': '02:59.16', '1600m': '04:48.60'}, 'Jacob Pacer': {'grade': 10, '300m': '00:42.35', '1000m': '02:59.42', '1600m': '05:05.68', '3200m': '10:26.75'}, 'T. J. Pasley': {'grade': 9, '300m': '00:42.41', '600m': '01:40.49', '1600m': '06:04.66'}, 'Ryan Balsamo': {'grade': 9, '300m': '00:43.15', '600m': '01:38.73', '1000m': '03:11.69'}, 'Evan Furciniti': {'grade': 11, '300m': '00:43.29', '600m': '01:36.38', '1000m': '02:58.12'}, 'Sean Gossin': {'grade': 11, '300m': '00:43.64', 'High Jump': '05-03.00'}, 'Daniel Oyesiku': {'grade': 11, '300m': '00:44.93', 'Pole Vault': '12-00.00'}, 'Brayden Vandeburg': {'grade': 11, '300m': '00:45.04', '1000m': '03:15.96', '1600m': '05:22.86', '3200m': '11:31.06'}, 'Liam Wilson': {'grade': 11, '300m': '00:45.21'}, 'Henry Wilson': {'grade': 11, '300m': '00:45.24', '600m': '01:50.71'}, 'Zach King': {'grade': 9, '300m': '00:45.38', '600m': '01:56.06', '1000m': '03:45.30', 'High Jump': '04-09.00'}, 'Colin McMahon': {'grade': 10, '300m': '00:45.55', '600m': '01:44.34', '1000m': '03:27.48'}, 'Ethan Burns': {'grade': 10, '300m': '00:45.88', '600m': '01:51.29', '1000m': '03:23.40', '1600m': '05:42.34'}, 'Henry Hill': {'grade': 11, '300m': '00:46.06', '600m': '01:37.77', '1600m': '04:35.82', '3200m': '09:48.42'}, 'Brandon Green': {'grade': 9, '300m': '00:48.69', '600m': '01:49.68', '1000m': '03:16.56', '1600m': '05:20.88', '3200m': '11:41.73'}, 'Liam Cass': {'grade': 12, '300m': '00:49.14', '1000m': '03:23.92', '1600m': '05:31.60'}, 'Alexander Morales Perdomo': {'grade': 10, '300m': '00:50.46', '600m': '02:02.54'}, 'Joseph Marafioti': {'grade': 10, '300m': '00:53.02', '1000m': '03:14.72', '1600m': '05:21.78'}, 'Andrew Green': {'grade': 11, '600m': '01:30.96', '1000m': '02:48.16', '1600m': '04:27.81', '3200m': '09:45.32'}, 'A Relay Team': {'grade': -7962, '4x200 Relay': '01:34.20', '4x400 Relay': '03:40.63', '4x800 Relay': '08:41.85'}, 'Andrew Kelly': {'grade': 12, '600m': '01:39.77', '1000m': '03:14.64', '1600m': '05:21.96'}, 'Dominick Tantalo': {'grade': 9, '600m': '01:40.33', '1000m': '03:10.84'}, 'Jacob Kolson': {'grade': 11, '600m': '01:40.52', '1000m': '03:19.91', 'Pole Vault': '12-00.00'}, 'Joshua Passalugo': {'grade': 10, '600m': '01:43.27', '1600m': '05:07.95', '3200m': '10:38.41'}, 'Tyler Ferri': {'grade': 12, '600m': '01:46.89', '1000m': '03:02.01', '1600m': '05:17.74'}, 'Andrew Osinski': {'grade': 9, '600m': '01:49.60', '1600m': '05:42.90'}, 'Jack Shafer': {'grade': 11, '600m': '01:54.34', '1000m': '03:34.26'}, 'Anthony Bracco': {'grade': 9, '600m': '01:56.14', '1000m': '03:29.39', '1600m': '05:40.69', '3200m': '12:10.92'}, 'Michael Gorman': {'grade': 9, '600m': '01:57.83', '1000m': '03:29.81', '1600m': '06:05.54'}, 'Ethan Osinski': {'grade': 9, '600m': '01:58.29', '1000m': '03:32.83', '1600m': '06:03.61'}, 'Sebastian Friedman': {'grade': 12, '600m': '01:59.16', '1000m': '03:23.47', '1600m': '05:51.79'}, 'Kaden Fuller': {'grade': 9, '600m': '02:00.71', '1000m': '03:20.45', '1600m': '05:55.72'}}
runners = add_conversions(get_people())
top_5 = get_top_5_per_event(runners)
save.save_people_json(runners)
save.save_top_5_json(top_5)

relay_types = [
    ['200m', '200m', '200m', '200m'],
    ['400m', '400m', '400m', '400m'],
    ['800m', '800m', '800m', '800m'],
    ['1609m', '1609m', '1609m', '1609m'],
    ['200m', '200m', '400m', '800m'],
    ['400m', '800m', '1200m', '1600m']
]

top_relay_combos = {}
for relay in relay_types:
    print(relay)
    result = relays.fastest_relays(runners, relay, num_relays=30)
    top_relay_combos[', '.join(relay)] = result

save.save_top_relays(top_relay_combos)

# Girls

runners = add_conversions(get_people(gender="F"))
top_5 = get_top_5_per_event(runners)
save.save_people_json(runners, suffix='-F')
save.save_top_5_json(top_5, suffix='-F')

relay_types = [
    ['200m', '200m', '200m', '200m'],
    ['400m', '400m', '400m', '400m'],
    ['800m', '800m', '800m', '800m'],
    ['1609m', '1609m', '1609m', '1609m'],
    ['200m', '200m', '400m', '800m'],
    ['400m', '800m', '1200m', '1600m']
]

top_relay_combos = {}
for relay in relay_types:
    print(relay)
    result = relays.fastest_relays(runners, relay, num_relays=30)
    top_relay_combos[', '.join(relay)] = result

save.save_top_relays(top_relay_combos, suffix='-F')