# -*- coding: utf-8 -*-
'''
(c) Copyright 2014 Telefonica, I+D. Printed in Spain (Europe). All Rights
Reserved.

The copyright to the software program(s) is property of Telefonica I+D.
The program(s) may be used and or copied only with the express written
consent of Telefonica I+D or in accordance with the terms and conditions
stipulated in the agreement/contract under which the program(s) have
been supplied.
'''
import unittest
import logging
import sys
from seleniumtid import selenium_driver
from seleniumtid.utils import Utils


class SeleniumTestCase(unittest.TestCase):
    driver = None
    utils = None

    def get_subclassmethod_name(self):
        return self.__class__.__name__ + "." + self._testMethodName

    @classmethod
    def tearDownClass(cls):
        if SeleniumTestCase.driver:
            SeleniumTestCase.driver.quit()
            SeleniumTestCase.driver = None

    def setUp(self):
        # Configure logger
        self.logger = logging.getLogger(__name__)
        # Create driver
        if not SeleniumTestCase.driver:
            SeleniumTestCase.driver = selenium_driver.connect()
            SeleniumTestCase.utils = Utils(SeleniumTestCase.driver)
        # Get common configuration of reusing driver
        self.reuse_driver = selenium_driver.config.getboolean_optional('Common', 'reuse_driver')
        # Set implicitly wait
        self.utils.set_implicit_wait()
        # Maximize browser
        if selenium_driver.is_maximizable():
            SeleniumTestCase.driver.maximize_window()
        self.logger.info("Running new test: {0}".format(self.get_subclassmethod_name()))

    def tearDown(self):
        # Check test result
        result = sys.exc_info()
        if result == (None, None, None):
            self.logger.info("The test '{0}' has passed".format(self.get_subclassmethod_name()))
        else:
            self.logger.error("The test '{0}' has failed: {1}".format(self.get_subclassmethod_name(), result[1]))
            test_name = self.get_subclassmethod_name().replace('.', '_')
            self.utils.capture_screenshot(test_name)

        # Close browser and stop driver
        if not self.reuse_driver:
            SeleniumTestCase.driver.quit()
            SeleniumTestCase.driver = None