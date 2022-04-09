from flask import Flask, request, jsonify
import requests
from ast import literal_eval
app=Flask(__name__)
serverinfo=[]
@app.route("/")
def home():
    return "Hello world"

@app.route("/register")
def register():
    dictToSend={'username':"cloud1"}
    res = requests.post('http://localhost:3000/register', json=dictToSend)
    print("response from server", res)
    return "Registering cloud"

@app.route("/getserverinfo")
def get_server_info():
    dictToSend={'username':"cloud1","chaincodeFunction":"QueryAllServers"}
    res = requests.get('http://localhost:3000/getallserverinfo',json=dictToSend)
    print("response from server", res.text)
    serverinfo=literal_eval(res.text)
    print(serverinfo,serverinfo[0])
    return "server info"
@app.route("/candidatenodes",methods=['GET','POST'])
def selectingcanditatenodes():
    dictToSend={'username':"cloud1","chaincodeFunction":"QueryAllServers"}
    res = requests.get('http://localhost:3000/getallserverinfo',json=dictToSend)
    print("response from server", res.text)
    server_info=literal_eval(res.text)

    print(server_info[0]['tasks'][0]['Deadline'])
    # print(request)
    data=request.get_json()
    # data=jsonify(data)
    server_no=data['server_number']
    print("data",data['server_number'])
    for server in server_info:    
        if ( int(server['server_number']) == int(server_no) ) : # get the server whose tasks are to be offloaded
            tsizes =   [int(t['Task_size']) for t in server['tasks']] # list of the sizes of the tasks to be offloaded
            break

    print(tsizes)
    size_smallest_task = min(tsizes) # size of the smallest task to be offloaded
    print(size_smallest_task)

    candidate_servers=[] # contains the list of candidate node servers
    print('sno','tl','tm','rm','sts')

    for server in server_info:
        if (int(server['server_number'])!=int(server_no)): # servers other than the server to be offloaded
            tsizes =   [int(t['Task_size']) for t in server['tasks']] #list of task sizes
            rem_mem = int(server['memory']) - sum(tsizes) # remaining memory of the server
            
        
            print( server['server_number'] , tsizes , server['memory'] , rem_mem , size_smallest_task )
            
            if ( rem_mem >= size_smallest_task ): # if rem_mem is greater than size of smallest task then choose it 
                candidate_servers.append(server['server_number'])

    print(candidate_servers)

    if len(candidate_servers) == 0:
        print('not enough resources to offload the task')
    return ' '.join(candidate_servers)




if __name__=="__main__":
    app.run(debug=True)