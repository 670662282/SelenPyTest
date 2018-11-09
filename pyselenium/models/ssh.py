import paramiko


class Tl_ssh():

    def __init__(self, ip='10.10.50.7', passwd=''):
        self.host = (ip, 22)
        self.user = 'root'
        self.passwd = passwd
        self.ssh = paramiko.SSHClient()

    def connect(self):
        ts = paramiko.Transport(self.host)
        ts.connect(username=self.user, password=self.passwd)
        self.__ts = ts

    def set_transport(self):
        self.ssh._transport = self.__ts

    def exec_cmd(self, str):
        stdin, stdout, stderr = self.ssh.exec_command(str)
        result = stdout.read()
        if not result:
            result = stderr.read()
        return result.decode()

    def down(self, service_file_dir, local_dir):
        sftp = paramiko.SFTPClient.from_transport(self.__ts)
        sftp.get(service_file_dir, local_dir)

    def close(self):
        self.__ts.close()
