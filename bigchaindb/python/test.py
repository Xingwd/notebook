from bigchaindb_driver import BigchainDB


bdb_root_url = 'http://192.168.1.154:9984'

bdb = BigchainDB(bdb_root_url)


help(bdb.transactions.prepare)