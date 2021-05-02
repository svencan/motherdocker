from selenium import webdriver
import time

from capture import Capture
from control import Control


def correction(error, rate, negative_correction, positive_correction):
    rate_limit = error / 40

    print('Error:', error, 'Rate:', rate, 'Limit:', rate_limit)

    if error <= -0.5:
        # Correct negatively (pitch_up) as fast as the limit allows
        if rate >= rate_limit:
            negative_correction()
        elif rate+0.1 <= rate_limit:
            positive_correction()
        return
    elif error >= 0.5:
        # Correct positively as fast as the limit allows
        if rate <= rate_limit:
            positive_correction()
        elif rate-0.1 >= rate_limit:
            negative_correction()
        return
    else:
        # Stop!
        print('! ! ! STOP ! ! !')
        if rate > 0:
            negative_correction()
        elif rate < 0:
            positive_correction()

    print("Micro-correcting")
    if error < 0:
        # Correct negatively (pitch_up) for a short time
        negative_correction()
        time.sleep(0.05)
        positive_correction()
    elif error > 0:
        # Correct positively (pitch_down) for a short time
        positive_correction()
        time.sleep(0.05)
        negative_correction()

def yz_correction(error, rate, negative_correction, positive_correction):
    print('Error:', error, 'Rate:', rate)

    if error > 5 and rate > -10:
        print('Normal correction left')
        negative_correction()
        return rate - 1
    elif error < -5 and rate < 10:
        print('Normal correction right')
        positive_correction()
        return rate + 1
    elif error <= 5 and rate < 0:
        positive_correction()
        return rate + 1
    elif error >= -5 and rate > 0:
        negative_correction()
        return rate - 1
    elif rate == 0:
        if error > 0:
            print('Micro-correction left')
            negative_correction()
            time.sleep(0.3)
            positive_correction()
            return rate
        if error < 0:
            print('Micro-correction right')
            positive_correction()
            time.sleep(0.3)
            negative_correction()
            return rate

    return rate


def x_correction(error, rate, negative_correction, positive_correction):
    print('Error:', error, 'Rate:', rate)

    if error > 50 and rate > -30:
        print('Normal correction left')
        negative_correction()
        return rate - 1
    elif error < -50 and rate < 30:
        print('Normal correction right')
        positive_correction()
        return rate + 1
    elif error <= 50 and rate < 0:
        positive_correction()
        return rate + 1
    elif error >= -50 and rate > 0:
        negative_correction()
        return rate - 1
    elif rate == 0:
        if error > 0:
            print('Micro-correction left')
            negative_correction()
            return rate + 1
        if error < 0:
            print('Micro-correction right')
            positive_correction()
            return rate - 1

    return rate


# Start web browser
browser=webdriver.Chrome("C:\chromedriver_win32\chromedriver.exe")
browser.get("https://iss-sim.spacex.com/")

# Wait for the "Begin" button
begin_button = None

while not begin_button:
    print('Wait for begin button...')
    time.sleep(5)
    begin_button = browser.find_element_by_id('begin-button')
    

while not (begin_button.is_displayed() and begin_button.is_enabled()):
    print('Still waiting for begin button')
    time.sleep(2)


print("Here we go.")
time.sleep(5)

begin_button.click()

time.sleep(10)
print("My spaceship!")
control = Control()
control.identify_controls(browser)
capture = Capture()
capture.initiate(browser)

# The interface does not give us Y and Z speed so we need to keep track
rate_y = 0
rate_z = 0
rate_x = 0

abort = False
allow_translations = False

while not abort:
    start_time = time.time() # start time of the loop

    coordinates = capture.get_coordinates(browser)
    pitch = capture.get_metric('pitch', browser)
    roll = capture.get_metric('roll', browser)
    yaw = capture.get_metric('yaw', browser)

    ### Correct pitch, yaw and roll until we're below abs(0.2) for each
    correction(pitch[0], pitch[1], control.pitch_up, control.pitch_down)
    correction(yaw[0], yaw[1], control.yaw_left, control.yaw_right)
    correction(roll[0], roll[1], control.roll_left, control.roll_right)

    allow_translations = allow_translations or (pitch[0] == yaw[0] == roll[0] == 0)
    
    if allow_translations:
        # Translate until we're within abs(0.2) for Y and Z
        # Y and Z translation must be ON or OFF as we only know the absolute rate
        y = coordinates[1]
        rate_y = yz_correction(y, rate_y, control.translate_left, control.translate_right)

        z = coordinates[2]
        rate_z = yz_correction(z, rate_z, control.translate_down, control.translate_up)

        x = coordinates[0]
        rate_x = x_correction(x, rate_x, control.translate_forward, control.translate_backward)
        
        

        # POWER!

    print("FPS: ", 1.0 / (time.time() - start_time)) # FPS = 1 / time to process loop
    time.sleep(0.05)


"""
<div id="begin-button" class="message-button animate" style="opacity: 1; visibility: inherit; transform: translate(0px, 0px);">BEGIN</div>
"""

# close web browser
browser.close()
