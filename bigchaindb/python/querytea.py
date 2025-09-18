from bigchaindb_driver import BigchainDB
import os

bdb_root_url = "http://192.168.0.121:9984"

bdb = BigchainDB(bdb_root_url)

msgs = bdb.assets.get(search="种植")

sum = 0
ids = open("../data/ids.txt", "wt")
for i in msgs:
    print("id = {0}".format(i["id"]))
    # print(i)
    sum += 1
    # for item in i:
    #    print("k= {0}, v= {1}".format(item, i[item]))
    # tea = i['data']
    # tea.pop('id')
    # print(tea)

    # 将id信息写入文件
    ids.write("tea_id{0} = {1}".format(sum, i["id"]) + "\n")


ids.close()
print("sum = {0}".format(sum))
