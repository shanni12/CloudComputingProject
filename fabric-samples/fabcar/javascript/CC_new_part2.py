# #!/usr/bin/env python
# # coding: utf-8

# # In[ ]:





# # In[7]:




# #############REquired input########

import sys, json,ast
dataform = str(sys.argv[1]).split(";")

# data=ast.literal_eval(dataform)
# print(type(dataform),dataform)
dataform2=str(sys.argv[2])
# print(type(ast.literal_eval(dataform2)),dataform2)
offloaded_server=ast.literal_eval(dataform2)
# print(offloaded_server['server_number'])
server_info=[]
for i in dataform:
    # print(type(ast.literal_eval(i)))
    server_info.append(ast.literal_eval(i))

# print(server_info)
# print(ast.literal_eval(dataform)['server_number'])
# print(json.loads(r"""dataform"""))
# a={'1':'1','2':'2'}
# print(a)
# # only the candidate servers

# server_info = [ {'server_number': '13', 'cpu_clock_frequency': '10', 'memory': '60', 'power':'100','hardware_info':'90','tasks': [{'Task_number': '1', 'Task_size': '10', 'Cpu_cycles': '2', 'Deadline': '2'} , {'Task_number': '2', 'Task_size': '40', 'Cpu_cycles': '2', 'Deadline': '2'} ]} ,
#   {'server_number': '24', 'cpu_clock_frequency': '12', 'memory': '40', 'power':'100','hardware_info':'80','tasks': [{'Task_number': '3', 'Task_size': '20', 'Cpu_cycles': '2', 'Deadline': '2'} , {'Task_number': '4', 'Task_size': '15', 'Cpu_cycles': '2', 'Deadline': '2'}]} ,
 
  
 
#    {'server_number': '4', 'cpu_clock_frequency': '13', 'memory': '100','power':'100' , 'hardware_info':'45' ,'tasks': [{'Task_number': '5', 'Task_size': '70', 'Cpu_cycles': '2', 'Deadline': '2'}]} , 
 
#    {'server_number': '52', 'cpu_clock_frequency': '30', 'memory': '200','power':'100' , 'hardware_info':'50','tasks': [{'Task_number': '6', 'Task_size': '60', 'Cpu_cycles': '2', 'Deadline': '2'} , {'Task_number': '7', 'Task_size': '50', 'Cpu_cycles': '2', 'Deadline': '2'} , {'Task_number': '8', 'Task_size': '10', 'Cpu_cycles': '2', 'Deadline': '2'} , {'Task_number': '9', 'Task_size': '20', 'Cpu_cycles': '2', 'Deadline': '2'} , {'Task_number': '10', 'Task_size': '10', 'Cpu_cycles': '2', 'Deadline': '2'} ]}  
 
  

# ]





# offloaded_server = {'server_number': '1', 'cpu_clock_frequency': '3', 'memory': '50', 'power':'100', 'hardware_info':'57' ,'tasks': [{'Task_number': '11', 'Task_size': '1', 'Cpu_cycles': '2', 'Deadline': '10'} , {'Task_number': '12', 'Task_size': '3', 'Cpu_cycles': '5', 'Deadline': '8'} , {'Task_number': '13', 'Task_size': '4', 'Cpu_cycles': '2', 'Deadline': '6'}]} 



# #######################################


# # In[8]:


import numpy as np
import pandas as pd

server_no = offloaded_server['server_number']  #ordering server or the server to ve offloaded

cand_ccf = { s['server_number']:s['cpu_clock_frequency'] for s in server_info }
#print(cand_ccf)



                                                                                                                                                                                            
offloaded_tasks =  { t['Task_number'] : { 'Task_size': t['Task_size']  , 'Cpu_cycles' : t['Cpu_cycles'] ,  'Deadline' : t['Deadline']  } for t in offloaded_server['tasks'] }




phi = { t['Task_number']: { cand['server_number'] : '' for cand in server_info } for t in offloaded_server['tasks'] }

#print(phi)

tm = { t['Task_number'] : '' for t in offloaded_server['tasks'] } # time taken on ordering server for a given task
em = { t['Task_number'] : '' for t in offloaded_server['tasks'] } # energy required to run the given task on the ordering server

eamn = { t['Task_number']: { cand['server_number'] : '' for cand in server_info } for t in offloaded_server['tasks'] }  # taskno,serverno,tmna
tamn = { t['Task_number']: { cand['server_number'] : '' for cand in server_info } for t in offloaded_server['tasks'] }   # taskno,serverno,emna

thfb = 0.2 # hyper ledger fabric block chain latency : constant
R =  10 #data rate : constant 10Gbs
weights = [ 0.25, 0.25, 0.25, 0.25 ]

for task in phi:
    
    tloc = int(offloaded_tasks[task]['Cpu_cycles']) / int(offloaded_server['cpu_clock_frequency'])
    
    eloc = int(offloaded_server['hardware_info']) * int(offloaded_server['cpu_clock_frequency']) * int(offloaded_server['cpu_clock_frequency']) * int(offloaded_tasks[task]['Cpu_cycles']) 
    
    tm[task] = tloc
    
    em[task] = eloc
    
    
    for cand in phi[task]:
        
        tcand = ( int(offloaded_tasks[task]['Task_size']) / R )  + ( int(offloaded_tasks[task]['Cpu_cycles']) / int(cand_ccf[cand]) )  + thfb
        
        ecand = ( int(offloaded_tasks[task]['Task_size']) / R ) * int(offloaded_server['power'])
        
        tsur  = ( tloc - tcand ) / tloc 
         
        esur  =  ( eloc - ecand ) / eloc 
        
        etsr =  0.9 # endorsed transaction success rate
        
        nbsr =  0.7 #normalised block size rate
        
        eamn[task][cand] = ecand
        
        tamn[task][cand] = tcand
        
        phi[task][cand] =  tsur * weights[0] + esur * weights[1] + etsr * weights[2] + nbsr * weights[3]




















# In[9]:


import scipy
import pulp
from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable

rem_mem = {}

for server in server_info:
        tsizes =   [int(t['Task_size']) for t in server['tasks']]
        rem_mem[server['server_number']] = int(server['memory']) - sum(tsizes)
        




tasklist=offloaded_tasks.keys() 


serverlist=[]

for s in server_info:
    serverlist.append(s['server_number'])



var = [] # contains the decision variables
for t in tasklist:
    for s in serverlist:
        var.append(t+'_'+s)
        
####### Solving the problem #######
        
model = LpProblem(name="small-problem", sense=LpMaximize)

x = {i: LpVariable(name=f"x{i}", cat="Binary") for i in var}

model += lpSum( [  phi [ v.split('_')[0] ] [  v.split('_')[1] ] * x[v] for v in var  ])


for t in tasklist:
    model += lpSum( [  x[t+"_"+s] for s in serverlist ] ) == 1  # one task on only one server


for t in tasklist:
    for s in serverlist:
        model += ( tamn[t][s] * x[ t+"_"+s ] <= tm[t] )  # time constraint
        



for t in tasklist:
    for s in serverlist:
        model += ( eamn[t][s] * x[ t+"_"+s ] <= em[t] )   # energy constraint
        


for t in tasklist:
    for s in serverlist:
        model += ( tamn[t][s] * x[ t+"_"+s ] <= int(offloaded_tasks[t]['Deadline']) ) #deadline constraint
        

for t in tasklist:
    for s in serverlist: # resource constraint
        model += ( int ( offloaded_tasks[t]['Task_size'] ) / rem_mem[s] ) * x [ t + '_' + s ] <= 1

# Solve the problem
status = model.solve()



if ( status == 1 ):
    
    solution = {}
    for var in model.variables():
        #print(var.name , var.value())
        if (var.value() == 1):
            solution [var.name[1:].split('_')[0]] = var.name[1:].split('_')[1]
    print(solution)
else:
    unknown=1
    
    


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




