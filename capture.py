from selenium import webdriver

def get_coordinates(browser):
    x = browser.find_element_by_id('x-range').find_element_by_css_selector('div').text
    y = browser.find_element_by_id('y-range').find_element_by_css_selector('div').text
    z = browser.find_element_by_id('z-range').find_element_by_css_selector('div').text

    if x and y and z:
        x = x[:-2]
        y = y[:-2]
        z = z[:-2]

        return (float(x), float(y), float(z))

    return None

def get_metric(metric, browser):
    error = browser.find_element_by_id(metric).find_element_by_css_selector('.error').text
    rate = browser.find_element_by_id(metric).find_element_by_css_selector('.rate').text

    if error and rate:
        error = error[:-1]
        rate = rate[:-4]

        return (float(error), float(rate))

    return None

