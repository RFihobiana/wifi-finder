'''
Find the wifi near you

Before using this, make sure you have:
    - `iwlist` if you use Linux. For Windows user,
    - `netsh` must be in your machine (by default it is)
'''

import re
import sys
import subprocess

def get_wifi_networks() -> list[dict[str, int]]:
    '''
    Gets every wifi your computer can hear around you
    
    Return: wifi list
    '''

    # Getting the best argument depending on the current platform
    if sys.platform == 'win32':
        process_name = ['netsh', 'wlan', 'show', 'networks', 'mode=Bssid']
        essid_regex_string = r'SSID\s\d+\s:\s(.+)'
        signal_regex_string = r'Signal\s:\s(\d+)%'
    elif sys.platform == 'linux':
        process_name = ['iwlist', 'wlan0', 'scan']
        essid_regex_string = r'ESSID:"(.+)"'
        signal_regex_string = r'Signal level=(-?\d+) dBm'
    else:
        raise SystemError('This programs is intended to run on Windows and Linux only!')

    result = subprocess.run(process_name, capture_output=True, text=True)
    networks = result.stdout
    
    essid_regex = re.compile(essid_regex_string)
    signal_regex = re.compile(signal_regex_string)

    essids = essid_regex.findall(networks)
    signals = signal_regex.findall(networks)

    return [ {'ESSID': essid, 'signal': int(signal)} for (essid, signal) in zip(essids, signals) ] # Return wifi list

def find_strongest_wifi() -> dict[str, int]:
    '''
    Gets strongest wifi singal around

    Return: Strongest wifi (with its signal). None if there is no wifi
    '''
    networks = get_wifi_networks()
    if not networks: return
    return max(networks, key=lambda net: -net['signal']) # the most negative signal is the strongest network

if __name__ == '__main__':
    strongest_wifi = find_strongest_wifi()
    if strongest_wifi is not None:
        print(f'Strongest Wifi Network: {strongest_wifi["ESSID"]} ({strongest_wifi["signal"]})')
    else: print('No Wifi Network found.')

