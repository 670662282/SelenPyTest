
import unittest
from SelenPyTest.pyselenium.models.ssh import Tl_ssh

class BackgroudTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #cls.logger = Log().get_logger()
        cls.ssh = Tl_ssh()
        cls.ssh.connect()
        cls.ssh.set_transport()

    @classmethod
    def tearDownClass(cls):
        cls.ssh.close()
