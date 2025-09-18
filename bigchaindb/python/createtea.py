from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair

from python.getjson import getJson

bdb_root_url = 'http://192.168.0.121:9984'

bdb = BigchainDB(bdb_root_url)

alice = generate_keypair()

url = "http://www.redoop.com/xingliannong/teaIndex"

teainfo = getJson(url)

# set the metadata to query for it in an example below
#teametadata={'planet': 'earth'}

for i in teainfo:
    i.pop('id')
    i.pop('ethhash')
    tea_asset = {'data': i}
    prepared_creation_tx = bdb.transactions.prepare(
        operation='CREATE',
        signers=alice.public_key,
        asset=tea_asset
        #metadata = teametadata
    )
    fulfilled_creation_tx = bdb.transactions.fulfill(
        prepared_creation_tx, private_keys=alice.private_key)
    bdb.transactions.send(fulfilled_creation_tx)
