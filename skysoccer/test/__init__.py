import unittest
import logging

from .index import IndexAppTest, IndexControllerTest, LoginControllerTest, LogoutControllerTest, GameControllerTest
from .admin import AdminControllerTest, RegisterControllerTest, DeleteControllerTest
from .game  import GamePageControllerTest

all_test_cases = [
    IndexAppTest,
    IndexControllerTest,
    LoginControllerTest,
    LogoutControllerTest,
    AdminControllerTest,
    RegisterControllerTest,
    DeleteControllerTest,
    GameControllerTest,
    GamePageControllerTest
]


def get_all_test_suite():
    logging.basicConfig(level=logging.INFO, format="%(asctime)-15s:%(message)s", filename='data/test.log')
    logging.getLogger('skysoccer').info('\n\t*** TESTING STARTED ***')
    suite = unittest.TestLoader()
    prepered_all_test_cases = []
    for test_case in all_test_cases:
        prepered_all_test_cases.append(
            suite.loadTestsFromTestCase(test_case)
        )
    return unittest.TestSuite(prepered_all_test_cases)


def run():
    suite = get_all_test_suite()
    unittest.TextTestRunner(verbosity=1).run(suite)
