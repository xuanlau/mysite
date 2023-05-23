import paramiko


class Collect:

    def __init__(self, serverinfo):

        self.ip = serverinfo[0]
        self.passwd = serverinfo[2]
        self.username = serverinfo[1]
        self.portset = serverinfo[3]

    def exec_collect(self) -> object:

        conn = paramiko.SSHClient()
        conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        args = ["lscpu | grep -w CPU\(s\): | head -1 | awk '{print $NF}'", "dmidecode  -t system | grep 'Serial Number' | awk '{print $NF}'"]
        try:
            conn.connect(self.ip, self.portset, self.username, self.passwd)
            # if outmsg.decode():
            #     info = outmsg.decode()
            # else:
            #     info = errmsg.decode()
        except:
            return "远程主机用户或者密码错误"
        else:
            info = []
            for i in args:
                stdin, stdout, stderr = conn.exec_command(i)
                outmsg, errmsg = stdout.read(), stderr.read()
                info.append(outmsg.decode())

            conn.close()
        return info


# if __name__ == '__main__':
#
#     addrinfo = ['211.93.22.166', 'stor123;', 'root', '22']
#     shouji = Collect(addrinfo)
#
#     shouji.exec_collect()
