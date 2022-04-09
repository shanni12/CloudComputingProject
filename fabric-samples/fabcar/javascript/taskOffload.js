
'use strict';

const { Gateway, Wallets } = require('fabric-network');
const path = require('path');
const fs = require('fs');
var request = require('request-promise');
const {PythonShell} = require('python-shell');
const { off } = require('process');
// console.log(dataToSend)
async function main(){
    try {
        var username;
        var server_number;
        if(process.argv.length < 4){
            console.log('Enter proper arguments')
            return;
        }
        else{
            username=process.argv[2]
            server_number=process.argv[3]
        }
        const ccpPath = path.resolve(__dirname, '..', '..', 'test-network', 'organizations', 'peerOrganizations', 'org1.example.com', 'connection-org1.json');
        const ccp = JSON.parse(fs.readFileSync(ccpPath, 'utf8'));
        const walletPath = path.join(process.cwd(), 'wallet');
        const wallet = await Wallets.newFileSystemWallet(walletPath);
        console.log(`Wallet path: ${walletPath}`);
        const identity = await wallet.get(username);
        if (!identity) {
            console.log(`An identity for the user ${username} does not exist in the wallet`);
            console.log('Run the registerUser.js application before retrying');
            return;
        }
        console.log("Username exists")
        var serverinfo={
            'server_number': server_number
        }
       import('node-fetch').then(({default: fetch}) => fetch("http://127.0.0.1:5000/getserverinfo", 
        {
        method: 'POST',
        headers: {
        'Content-type': 'application/json',
        'Accept': 'application/json'
        },
        // Strigify the payload into JSON:
        body:JSON.stringify(serverinfo)}).then(res=>
            res ).then(jsonResponse=>{
        
        // Log the response data in the console
        console.log(jsonResponse)
        } 
        ).catch((err) => console.error(err)));
        var options = {
           method: 'POST',
           uri: 'http://127.0.0.1:5000/candidatenodes',
           body: serverinfo,
           json: true
    };
        let result;
        var sendrequest = await request(options)
          .then(function (parsedBody) {
            console.log(parsedBody);
            
            result = parsedBody;
            
        })
        .catch(function (err) {
            console.log(err);
        });
        console.log(result.split(" "));
        result=result.split(" ");
        console.log("in main function")
        const gateway = new Gateway();
        await gateway.connect(ccp, { wallet, identity: username, discovery: { enabled: true, asLocalhost: true } });
        const network = await gateway.getNetwork('mychannel');
        console.log("in main function")

        const contract = network.getContract('fabcar');
        
        var orderedserver = await contract.evaluateTransaction('QueryServer',server_number);
        console.log("in main fucntion")
        orderedserver=JSON.stringify(orderedserver)
        console.log("ordered server",orderedserver)
        var candidateservers=[]
        for(let i=0;i<result.length;i++)
        {
            var candidateserver = await contract.evaluateTransaction('QueryServer',result[i]);
            // candidateserver=candidateserver.toString()
            // console.log(candidateserver)
            candidateservers.push(JSON.stringify(candidateserver))
        }
        // console.log("candidate servers",candidateservers[0])
        
        
        console.log(`Transaction has been evaluated, result is: ${result.toString()}`);
        var options = {
        mode: 'text',
        pythonPath: '/usr/bin/python3',
        // pythonOptions: ['-u'],
        scriptPath: './',
        args: [candidateservers.join(";"),orderedserver]
        };
        var res;
        PythonShell.run('CC_new_part2.py', options, function (err, results) {
        if (err) throw err;
        // results is an array consisting of messages collected during execution
        // console.log('%j', results);
        res=results
        // console.log(res)
        });
        var obj;
        var tasks=JSON.parse(orderedserver)['tasks']
        setTimeout(()=>{ 
            var resu=res[0]
            obj = eval("(" + resu + ")");
            for([key, val] of Object.entries(obj)) {
                for(let i=0;i<tasks.length;i++)
                {
                    if(tasks[i]['Task_number']==key)
                    {
                        break;
                    }
                }
                var tasktosend=JSON.stringify(tasks[i]);
                contract.submitTransaction('ExchangeTask',server_number,val,tasktosend);
                console.log(key, val);
              }
            console.log(JSON.parse(JSON.stringify(res)),"results");},10000)
            

        // await gateway.disconnect();
    } catch (error) {
        // console.error(`Failed to register user ${username}: ${error}`);
        // process.exit(1);
    }
}
main()