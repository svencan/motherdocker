class Control:
    
    browser = None

    ctrl_pitch_up = None
    ctrl_pitch_done = None

    ctrl_roll_right = None
    ctrl_roll_left = None
    ctrl_yaw_left = None
    ctrl_yaw_right = None

    ctrl_translate_left = None
    ctrl_translate_right = None
    ctrl_translate_up = None
    ctrl_translate_down = None
    ctrl_translate_forward = None
    ctrl_translate_backward = None
    

    def identify_controls(self, browser):
        self.browser = browser

        self.ctrl_pitch_up = browser.find_element_by_id('pitch-up-button')
        self.ctrl_pitch_down = browser.find_element_by_id('pitch-down-button')

        self.ctrl_roll_left = browser.find_element_by_id('roll-left-button')
        self.ctrl_roll_right = browser.find_element_by_id('roll-right-button')

        self.ctrl_yaw_left = browser.find_element_by_id('yaw-left-button')
        self.ctrl_yaw_right = browser.find_element_by_id('yaw-right-button')

        self.ctrl_translate_left = browser.find_element_by_id('translate-left-button')
        self.ctrl_translate_right = browser.find_element_by_id('translate-right-button')

        self.ctrl_translate_up = browser.find_element_by_id('translate-up-button')
        self.ctrl_translate_down = browser.find_element_by_id('translate-down-button')

        self.ctrl_translate_forward = browser.find_element_by_id('translate-forward-button')
        self.ctrl_translate_backward = browser.find_element_by_id('translate-backward-button')

    
    def pitch_up(self):
        self.ctrl_pitch_up.click()

    def pitch_down(self):
        self.ctrl_pitch_down.click()

    def yaw_left(self):
        self.ctrl_yaw_left.click()

    def yaw_right(self):
        self.ctrl_yaw_right.click()
