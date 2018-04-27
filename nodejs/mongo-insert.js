var MongoClient = require('mongodb').MongoClient;
var url = process.env.MONGODBURL;

MongoClient.connect(url, function(err, db) {
  if (err) throw err;
  var dbo = db.db("test");
  var myobj = [];
  for(i=0; i<50000; i++){
    myobj[i] = {a:i}; // create doc here using json
  }
  dbo.collection("docs").insertMany(myobj, function(err, res) {
    if (err) throw err;
    console.log(res.insertedIds);
    db.close();
  });
});
