#!/usr/bin/env python
# coding: utf-8

# In[4]:


import numpy as np
import pandas as pd
# only the candidate servers

#############REquired input########

server_info = [ {'server_number': '1', 'cpu_clock_frequency': '10', 'memory': '60', 'power':'100','hardware_info':'90','tasks': [{'Task_number': '1', 'Task_size': '10', 'Cpu_cycles': '2', 'Deadline': '2'} , {'Task_number': '2', 'Task_size': '40', 'Cpu_cycles': '2', 'Deadline': '2'} ]} ,

  {'server_number': '2', 'cpu_clock_frequency': '12', 'memory': '40', 'power':'100','hardware_info':'80','tasks': [{'Task_number': '1', 'Task_size': '20', 'Cpu_cycles': '2', 'Deadline': '2'} , {'Task_number': '2', 'Task_size': '15', 'Cpu_cycles': '2', 'Deadline': '2'}]} ,
 
  
 
   {'server_number': '4', 'cpu_clock_frequency': '13', 'memory': '100','power':'100' , 'hardware_info':'45' ,'tasks': [{'Task_number': '1', 'Task_size': '70', 'Cpu_cycles': '2', 'Deadline': '2'}]} , 
 
   {'server_number': '5', 'cpu_clock_frequency': '30', 'memory': '200','power':'100' , 'hardware_info':'50','tasks': [{'Task_number': '1', 'Task_size': '60', 'Cpu_cycles': '2', 'Deadline': '2'} , {'Task_number': '2', 'Task_size': '50', 'Cpu_cycles': '2', 'Deadline': '2'} , {'Task_number': '3', 'Task_size': '10', 'Cpu_cycles': '2', 'Deadline': '2'} , {'Task_number': '4', 'Task_size': '20', 'Cpu_cycles': '2', 'Deadline': '2'} , {'Task_number': '5', 'Task_size': '10', 'Cpu_cycles': '2', 'Deadline': '2'} ]}  
 
  

]


server_no = '3'  #ordering server num


#######################################

cand_ccf = { s['server_number']:s['cpu_clock_frequency'] for s in server_info }
#print(cand_ccf)

offloaded_server = {'server_number': '3', 'cpu_clock_frequency': '3', 'memory': '50', 'power':'100', 'hardware_info':'57' ,'tasks': [{'Task_number': '1', 'Task_size': '30', 'Cpu_cycles': '2', 'Deadline': '2'} , {'Task_number': '2', 'Task_size': '10', 'Cpu_cycles': '5', 'Deadline': '2'} , {'Task_number': '3', 'Task_size': '5', 'Cpu_cycles': '2', 'Deadline': '2'}]} 

offloaded_tasks =  { t['Task_number'] : { 'Task_size': t['Task_size']  , 'Cpu_cycles' : t['Cpu_cycles'] ,  'Deadline' : t['Deadline']  } for t in offloaded_server['tasks'] }

print('Tasks to be offloaded : ',offloaded_tasks)
print('\n')


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

print('phi', phi)

print('\n')

print('eamn',eamn)

print('\n')

print('tamn',tamn)

print('\n')

print('tm',tm)

print('\n')

print('em',em)


# In[ ]:




