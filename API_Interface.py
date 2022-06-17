import csv

import pandas as pd
import requests

base_url = 'http://cotaaustin.clubspeedtiming.com/api/index.php/'

with open('TokenKeys.csv', 'r') as file_in:
    token_file = csv.reader(file_in, delimiter=',')
    tokens = {}
    for token in token_file:
        tokens[token[0]] = token[1]


def findDriversID(driverName):
    request_url = base_url + 'racers/search.json?query=' + driverName.replace(' ', '%20') + '&' + tokens['main_key']
    possible_drivers = requests.get(request_url).json()

    for driver in possible_drivers['racers']:
        driver.update(driver.pop('name'))
    df = pd.DataFrame(possible_drivers['racers'])
    df.set_index('id', inplace=True)
    return df


def getDriversRaces(driverID):
    request_url = base_url + 'racers/' + str(driverID) + '/races.json?&' + tokens['main_key']
    races_by_driver = requests.get(request_url).json()

    df = pd.DataFrame(races_by_driver['heats'])
    df.set_index('id', inplace=True)
    return df


def getDriversInfo(driverID):
    request_url = base_url + 'racers/' + str(driverID) + '.json?' + tokens['main_key']
    driver_info = requests.get(request_url).json()

    driver_info['racer'].update(driver_info['racer'].pop('name'))
    df = pd.DataFrame(driver_info['racer'], index=[0])
    df.set_index('id', inplace=True)
    return df


def getRaceDriverData(raceID):
    request_url = base_url + 'races/' + str(raceID) + '.json?' + tokens['main_key']
    race_info = requests.get(request_url).json()

    race_driver_info = []
    for driver in race_info['race']['racers']:
        del driver['laps']
        race_driver_info.append(driver)
    df = pd.DataFrame(race_driver_info)
    df.set_index('id', inplace=True)
    return df


def getRaceLapData(raceID):
    request_url = base_url + 'races/' + str(raceID) + '.json?' + tokens['main_key']
    race_info = requests.get(request_url).json()

    driver_lap_dfs = []
    for driver in race_info['race']['racers']:
        df = pd.DataFrame(driver['laps'])
        df.set_index('lap_number', inplace=True)
        driver_lap_dfs.append(df)
    return driver_lap_dfs


def getRaceResults(raceID):
    request_url = base_url + 'races/' + str(raceID) + '.json?' + tokens['main_key']
    race_info = requests.get(request_url).json()

    df = pd.DataFrame(race_info['scoreboard'])
    df.set_index('racer_id', inplace=True)
    df.position = df.position.astype(int)
    df.sort_values(by='position', inplace=True)
    return df


def getRaceData(raceID):
    driver_data = getRaceDriverData(raceID)
    lap_data = getRaceLapData(raceID)
    results = getRaceResults(raceID)
    return driver_data, lap_data, results
