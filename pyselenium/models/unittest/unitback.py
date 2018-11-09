import unittest
from .logs import Log
from . import myssh

class BackgroudTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.logger = Log().get_logger()
        self.ssh = myssh.Tl_ssh()
        self.ssh.connect()
        self.ssh.set_transport()

    @classmethod
    def tearDownClass(self):
        self.ssh.close()
