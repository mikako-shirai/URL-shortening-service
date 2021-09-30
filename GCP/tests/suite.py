import tests.test_models
import tests.test_utils

import unittest

# -----------------------------------------------------------------------------------

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(tests.test_models.TestModels))
    test_suite.addTest(unittest.makeSuite(tests.test_utils.TestUtils))
    return test_suite

# -----------------------------------------------------------------------------------


mySuite = suite()
runner = unittest.TextTestRunner()
runner.run(mySuite)

