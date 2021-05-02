from selenium import webdriver

class Capture:

    position_x = None
    position_y = None
    position_z = None

    yaw = None
    pitch = None
    roll = None

    def initiate(self, browser):
        self.position_x = browser.find_element_by_id('x-range').find_element_by_css_selector('div')
        self.position_y = browser.find_element_by_id('y-range').find_element_by_css_selector('div')
        self.position_z = browser.find_element_by_id('z-range').find_element_by_css_selector('div')

        self.yaw = browser.find_element_by_id('yaw')
        self.pitch = browser.find_element_by_id('pitch')
        self.roll = browser.find_element_by_id('roll')

    def get_coordinates(self, browser):
        x = self.position_x.text
        y = self.position_y.text
        z = self.position_z.text

        if x and y and z:
            x = x[:-2]
            y = y[:-2]
            z = z[:-2]

            return (float(x), float(y), float(z))

        return None

    def get_metric(self, metric, browser):
        element = None
        if metric == 'yaw':
            element = self.yaw
        elif metric == 'pitch':
            element = self.pitch
        elif metric == 'roll':
            element = self.roll

        error = element.find_element_by_css_selector('.error').text
        rate = element.find_element_by_css_selector('.rate').text

        if error and rate:
            error = error[:-1]
            rate = rate[:-4]

            return (float(error), float(rate))

        return None

