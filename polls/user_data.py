import sys
import yaml
import crypt

confile = "/var/www/html/ubuntu-uefi/20/20.04/user-data"
newconfile = "/var/www/html/ubuntu-uefi/20/20.04/scripts/user-data"
legacy_confile = "/var/www/html/ubuntu/20/20.04/user-data"
legacy_newconfile = "/var/www/html/ubuntu/20/20.04/scripts/user-data"

info = sys.argv[6:]  # 接收参数中的挂载信息


class MyDumper(yaml.Dumper):
    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break()

    def increase_indent(self, flow=False, *args, **kwargs):
        return super().increase_indent(flow=flow, indentless=False)


data = None
with open(confile, "r") as stream:
    try:
        data = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        sys.exit(exc)
passwd = data["autoinstall"]["identity"]["password"]
storages = (data["autoinstall"]["storage"]["config"])  # 挂载信息赋予对象
data["autoinstall"]["identity"]["password"] = crypt.crypt(sys.argv[1], crypt.mksalt(crypt.METHOD_SHA512))  # 修改密码
number = 0
# len_storages = len(storages)
for i in storages[:]:
    if "device" in i.keys():
        # print(i)
        if i["device"] == "disk-sda":
            number = number + 1
meter = 'G'
storage = []
device_number = None
# 根据传入参数修改挂载信息
if len(info) >= 1:
    print(len(info))
    for k, v in enumerate(info):
        vs = v.split(":")
        # size = int(vs[1])*1073741824
        size = str(vs[1]) + meter
        mount_path = vs[0]
        device_number = number + k + 1
        partition_number = device_number - 1
        storage.append({'device': 'disk-sda', 'size': size, 'wipe': 'superblock', 'flag': '', 'number': device_number,
                        'preserve': False, 'grub_device': False, 'type': 'partition',
                        'id': 'partition-' + str(partition_number)})
        storage.append(
            {'fstype': 'ext4', 'volume': 'partition-' + str(partition_number), 'preserve': False, 'type': 'format',
             'id': 'format-' + str(partition_number)})
        storage.append({'path': mount_path, 'device': 'format-' + str(partition_number), 'type': 'mount',
                    'id': 'mount-' + str(partition_number)})
# 判断是否增加swap分区
if int(sys.argv[4]) != 0:
    if len(info) >= 1:
        swap_device_number = device_number + 1
        swap_partition_number = swap_device_number - 1
    else:
        swap_device_number = number + 1
        swap_partition_number = swap_device_number - 1
    #part_str = 'partition-' + str(swap_partition_number)
    part_str = 'partition-swap'
    format_str = 'format-swap'
    mounnt_str = 'mount-swap'
    size_swap = str(sys.argv[4]) + meter
    storage.append(
        {'device': 'disk-sda', 'size': size_swap, 'wipe': 'superblock', 'flag': 'swap', 'number': swap_device_number,
         'preserve': False, 'grub_device': False, 'type': 'partition', 'id': part_str})
    storage.append({'fstype': 'swap', 'volume': part_str, 'preserve': False, 'type': 'format', 'id': format_str})
    storage.append({'path': '', 'device': format_str, 'type': 'mount', 'id': mounnt_str})

# 将传入参数提取数值并赋值
boot_size = int(sys.argv[2])
storages[1]['size'] = str(boot_size) + meter

# 判断根分区是否分配余下全部
if int(sys.argv[3]) == 1:
    # print(storages[3])
    storages[3]['size'] = -1

for info in storage[:]:
    storages.insert(len(storages) - 4, info)

# print(storages[3:len(storages) - 4])  # 输出增加的挂载信息
print("新增挂载信息:", storage)
# 将重新生成的data写入到新的文件中
if sys.argv[5] == "uefi":
    with open(newconfile, "w", encoding='utf-8') as outfile:
        yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True, sort_keys=False)
else:
    data_legacy = None
    with open(legacy_confile, "r") as stream:
        try:
            data_legacy = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            sys.exit(exc)
    passwd = data_legacy["autoinstall"]["identity"]["password"]
    legacy_storages = (data_legacy["autoinstall"]["storage"]["config"])  # 挂载信息赋予对象
    data["autoinstall"]["identity"]["password"] = crypt.crypt(sys.argv[1], crypt.mksalt(crypt.METHOD_SHA512))  # 修改密码
    boot_size = int(sys.argv[2])  # 修改boot分区大小
    legacy_storages[2]['size'] = str(boot_size) + meter
    # 判断根分区是否分配余下全部
    if int(sys.argv[3]) == 1:
        # print(storages[3])
        legacy_storages[5]['size'] = -1   # 修改/分区大小
    for info_legacy in storage[:]:
        legacy_storages.insert(len(legacy_storages) - 3, info_legacy)
    with open(legacy_newconfile, "w", encoding='utf-8') as outfile:
        yaml.dump(data_legacy, outfile, default_flow_style=False, allow_unicode=True, sort_keys=False)