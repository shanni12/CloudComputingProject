var express = require('express');
var app = express();
var registerUser = require('./registerUser.js');
var query = require('./queryChanging.js');
const port = 3000

app.use(function (req, res, next) {
    res.header("Access-Control-Allow-Origin", "*"); // update to match the domain you will make the request from
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, OPTIONS');


    next();
});
app.use(express.json())
app.get('/', (req, res) => {
    res.send('you have succesfully called a webservice')
});
app.post('/register', (req, res) => {

    console.log(req.body);
    var username = req.body.username
    console.log(username)
    // res.send("sha")
    registerUser.registerUser(username).then(result => {
        console.log("success");
        res.send(result)

    }).catch(error => {

        console.log("in catch block")
        console.log(error);
        res.status(404).send(error);
    });
});
app.get('/getallserverinfo',(req,res)=>{
    console.log(req.body);
    var username=req.body.username
    console.log(username)
    var chaincodeFunction=req.body.chaincodeFunction
    console.log(chaincodeFunction)
    query.query(username,chaincodeFunction,[]).then(result => {
        console.log("success",result)
        res.send(result)
    }).catch(error => {
        console.log("in catch block");
        console.log(error);
        res.status(404).send(error);
    })

})
app.listen(port, () => {
    console.log("This application is running on port no:", port);
});