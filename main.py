from selenium import webdriver
import time

import capture
from control import Control

# Start web browser
browser=webdriver.Chrome("C:\chromedriver_win32\chromedriver.exe")
browser.get("https://iss-sim.spacex.com/")

# Wait for the "Begin" button
begin_button = None

while not begin_button:
    print('Wait for begin button...')
    time.sleep(5)
    begin_button = browser.find_element_by_id('begin-button')
    
print(begin_button)

while not (begin_button.is_displayed() and begin_button.is_enabled()):
    print('Still waiting for begin button')
    time.sleep(2)


print("Here we go.")
time.sleep(5)

begin_button.click()

time.sleep(5)
print("My spaceship!")
control = Control()
control.identify_controls(browser)

abort = False
while not abort:
    coordinates = capture.get_coordinates(browser)
    pitch = capture.get_metric('pitch', browser)
    roll = capture.get_metric('roll', browser)
    yaw = capture.get_metric('yaw', browser)

    print('Coordinates:', coordinates)
    print('Pitch:', pitch)
    print('Roll:', roll)
    print('Yaw:', yaw)

    ### Correct pitch, yaw and roll until we're below abs(0.2) for each
    # Pitch
    pitch_rate = pitch[1]
    pitch_error = pitch[0]

    pitch_direction = 0

    if pitch_error < -0.2:
        pitch_direction = -1
    elif pitch_error > 0.2:
        pitch_direction = 1
    
    pitch_rate_limit = pitch_error / 40  # initial pitch -20, limit would be 0.25

    print('Pitch error:', pitch_error, 'Pitch rate:', pitch_rate, 'Pitch limit:', pitch_rate_limit, 'Pitch direction:', pitch_direction)

    if abs(pitch_rate) > abs(pitch_rate_limit):
        # Slow down
        if pitch_direction == -1:
            control.pitch_down()
        elif pitch_direction == 1:
            control.pitch_up()
    elif abs(pitch_rate) < abs(pitch_rate_limit):
        # Speed up
        if pitch_direction == -1:
            control.pitch_up()
        elif pitch_direction == 1:
            control.pitch_down()

    # Translate until we're within abs(0.2) for Y and Z


    # POWER!

    time.sleep(0.01)


"""
<div id="begin-button" class="message-button animate" style="opacity: 1; visibility: inherit; transform: translate(0px, 0px);">BEGIN</div>
"""

# close web browser
browser.close()
