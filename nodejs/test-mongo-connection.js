var MongoClient = require('mongodb').MongoClient
  , assert = require('assert');

// Connection URL

var url = 'mongodb://node1:27017,node2:27017,node3:27017/sampleDB?replicaSet=rs0';

// Use connect method to connect to the server
MongoClient.connect(url, function(err, db) {
  assert.equal(null, err);
  console.log("Connected successfully to server");

  db.close();
});
