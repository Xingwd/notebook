from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair

bdb_root_url = 'http://192.168.1.154:9984'

bdb = BigchainDB(bdb_root_url)

alice = generate_keypair()

hello_1 = {'data': {'msg': {'test': 'Hello xing 1!'},},}
hello_2 = {'data': {'msg': {'test': 'Hello xing 2!'},},}
hello_3 = {'data': {'msg': {'test': 'Hello xing 3!'},},}

# set the metadata to query for it in an example below
metadata={'planet': 'earth'}

prepared_creation_tx = bdb.transactions.prepare(
    operation='CREATE',
    signers=alice.public_key,
    asset=hello_1
)
fulfilled_creation_tx = bdb.transactions.fulfill(
    prepared_creation_tx, private_keys=alice.private_key)
bdb.transactions.send(fulfilled_creation_tx)

prepared_creation_tx = bdb.transactions.prepare(
    operation='CREATE',
    signers=alice.public_key,
    asset=hello_2
)
fulfilled_creation_tx = bdb.transactions.fulfill(
    prepared_creation_tx, private_keys=alice.private_key)
bdb.transactions.send(fulfilled_creation_tx)

prepared_creation_tx = bdb.transactions.prepare(
    operation='CREATE',
    signers=alice.public_key,
    asset=hello_3
)
fulfilled_creation_tx = bdb.transactions.fulfill(
    prepared_creation_tx, private_keys=alice.private_key)
bdb.transactions.send(fulfilled_creation_tx)

msgs = bdb.assets.get(search='xing')

sum = 0
for i in msgs:

    sum += 1
    print("sum = {0}".format(sum))