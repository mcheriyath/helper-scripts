from boto import kinesis
import testdata
import json

kinesis = kinesis.connect_to_region("us-east-1")

class Users(testdata.DictFactory):
    firstname = testdata.FakeDataFactory('firstName')
    lastname = testdata.FakeDataFactory('lastName')
    age = testdata.RandomInteger(10, 30)
    gender = testdata.RandomSelection(['female', 'male'])

for user in Users().generate(10):
    print(user)
    kinesis.put_record("push-notifications", json.dumps(user), "123")
