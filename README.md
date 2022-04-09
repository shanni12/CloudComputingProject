# Cloud-Computing
## Blockchain-Based Collaborative Task Offloading in MEC: A Hyperledger Fabric Framework


This is an implementation  of blockchain-based Collaborative task offloading in MEC.\
This is implemented in nodeJS , python and Hyperledger fabric blockchain .\
The cloud level is implemented in flask

## Requirements
Python3. scipy, pulp\
nodejs\
flask\
Hyperledger Fabric
## Steps to Run this simulation(Linux).

cd CloudComputingAssignment/fabric-samples/fabcar\
./startFabric.sh\
\
cd javascript\
\
node enrollAdmin.js\
\
node registerUser.js \<username> (Register as many servers you wish to)\
\
node invoke.js \<username> AddServer
\<server_number> \<cpu_clock_frequency> \<memory> \<hardware_value> \<computation_power>  (Add servers as many as you want)\
\
node invoke.js \<username> AddTaskToServer \<server_number>   "{'Task_number':\<task_number>, 'Task_size':/<task_size>, 'Cpu_cycles':\<cpu_cycles>,  'Deadline':\<deadline>}" (Add tasks to servers)\
\
node api.js (nodejs application for communication of flask with blockchain)\
\
python3 CloudcomputingAssignment/cloud_flask.py (cloud node)\
\
node task_offload.js \<username>  \<server_number>












