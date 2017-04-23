from espeak import espeak
espeak.set_parameter(espeak.Parameter.Rate, 100)
espeak.set_parameter(espeak.Parameter.Volume, 500)

def speak_calendar():
    import google_calendar as gc
    day, events = gc.get_schedule_events()

    import time
    if events:
        espeak.synth('You have a plan ' + day + '. Get ready.')
        time.sleep(5)
        for event in events:
            espeak.synth(event['summary'])
            time.sleep(5)

def speak_weather():
    import open_weather_map as owm
    day, detailed_status, temperatures = owm.get_weather()

    import time
    espeak.synth(day + '\'s weather forcast')
    time.sleep(3)
    espeak.synth(detailed_status)
    time.sleep(2)
    for t in temperatures.keys():
        espeak.synth(temperatures[t] + ' degrees in the ' + t)
        time.sleep(4)
        
if __name__ == '__main__':
    speak_calendar()
    speak_weather()
