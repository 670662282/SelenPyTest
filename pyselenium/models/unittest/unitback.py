
import unittest
from SelenPyTest.pyselenium.models.ssh import Tl_ssh

class BackgroudTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        #self.logger = Log().get_logger()
        self.ssh = Tl_ssh()
        self.ssh.connect()
        self.ssh.set_transport()

    @classmethod
    def tearDownClass(self):
        self.ssh.close()
