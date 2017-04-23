import argparse
parser = argparse.ArgumentParser()
parser.add_argument('day', choices=['today', 'tomorrow'], help='day to check the weather forcast')
args = parser.parse_args()

API_KEY_FILE = '~/home_agent/owm_key.txt'

def get_credential():
    import os
    try:
        file_path = os.path.expanduser(API_KEY_FILE)
        api_key_file = open(file_path, 'r')
    except IOError:
        print('Please create {0}'.format(file_path))
        quit()
    with api_key_file:
        return api_key_file.readline().strip()

def get_weather():
    import pyowm
    owm = pyowm.OWM(get_credential())
    forecasts = owm.daily_forecast("Fujisawa,jp", limit=2).get_forecast()
    days = {'today': 0, 'tomorrow': 1}
    forecast = forecasts.get(days[args.day])
    detailed_status = forecast.get_detailed_status()
    #reference_time = forecast.get_reference_time(timeformat='date')
    temperature = forecast.get_temperature(unit='celsius')
    days = {'morn': 'morning', 'eve': 'evening'}
    temperatures = {}
    for day in days.keys():
        temperatures[days[day]] = str(int(round(temperature[day])))
    return args.day, detailed_status, temperatures

if __name__ == '__main__':
    day, detailed_status, temperatures = get_weather()
    print(day + '\'s weather forcast')
    print(detailed_status)
    for t in temperatures.keys():
        print(temperatures[t] + ' degrees in the ' + t)
