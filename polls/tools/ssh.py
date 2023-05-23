import os.path
import paramiko
import stat
# import os


class lx_ssh:
    def __init__(self, **dict_args):
        # self.sftp = None
        self.hostname = dict_args["hostname"]
        self.user = dict_args["user"]
        self.password = dict_args["password"]
        self.key = dict_args["key"]
        self.port = 22
        # self.remote_dir = remote_dir
        # self.local_dir = local_dir

    def lx_ssh_client(self, command):
        client = paramiko.SSHClient()
        # 自动添加策略，保存服务器的主机名和密钥信息，如果不添加，那么不再本地know_hosts文件中记录的主机将无法连接
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        client.connect(hostname=self.hostname, username=self.user, port=self.port, password=self.password, timeout=1)
        stdin, stdout, stderr = client.exec_command(command)
        # print(stdout.read().decode('utf-8'))
        res = stdout.read().decode('utf-8')
        # sdrr = stdout.read().decode('utf-8')
        client.close()  # 关闭客户端
        return res

    def lx_ssh_transport(self, command):
        # 创建一个通道
        transport = paramiko.Transport((self.hostname, self.port))
        transport.connect(username=self.user, password=self.password)
        # 实例化SSHClient
        ssh = paramiko.SSHClient()
        ssh._transport = transport
        stdin, stdout, stderr = ssh.exec_command(command)
        # print(stdout.read().decode('utf-8'))
        if stdout:
            res = stdout.read().decode('utf-8')
        else:
            res = stderr.read()
        res = res
        transport.close()  # 关闭通道
        return res

    def chu_shi_hua_sftp(self):
        # 获取Transport实例
        tran = paramiko.Transport((self.hostname, self.port))
        if self.key:
            private = paramiko.RSAKey.from_private_key_file(self.key)  # 配置密钥位置
            # 连接SSH服务端，使用password
            tran.connect(username=self.user, password=self.password, pkey=private)
        else:
            tran.connect(username=self.user, password=self.password)
        self.sftp = paramiko.SFTPClient.from_transport(tran)   # 实例化一个sftp客户端对象

    def lx_sftp_client(self, remote_dir):
        dic = []
        file = []
        file_list = (self.sftp.listdir_attr(path=remote_dir))  # 获取目录下的文件列表
        for f in file_list:
            if stat.S_ISDIR(f.st_mode):
                dic.append(f)
            else:
                file.append(f)

        # tran.close() # 文件服务器退出时触发
        return dic, file, remote_dir, self.hostname

    # def download(self):
    #     self.sftp.get(self.remote_dir)
    #     self.chushihua_sftp().

    def close(self):
        self.sftp.close()


# if __name__ == "__main__":
    # 开启本地端口映射
    # rest = os.popen("ssh -t -t -L 88:10.50.50.10:22 -o ServerAliveInterval=60 root@211.93.22.166 -i ~/.ssh/pfsrsa")
    # lx_ssh = lx_ssh("127.0.0.1", "root", "stor123;", 88)  # 实例化lx_ssh
    # port = 22
    # vs_pt = lx_ssh({"hostname": "192.168.2.149", "user": "root", "password": "123..com", "key": None, "port": port})
    # print(vs_pt.lx_ssh_transport("bash /root/scripts/ping.sh"))
    # lx_ssh.lx_ssh_client()
    # lx_ssh.lx_ssh_transport()
    # lx_ssh.lx_sftp_client()
