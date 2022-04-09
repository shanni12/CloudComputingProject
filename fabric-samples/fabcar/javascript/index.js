// import {PythonShell} from 'python-shell';
const {PythonShell} = require('python-shell');
var options = {
  mode: 'text',
  pythonPath: '/usr/bin/python3',
  // pythonOptions: ['-u'],
  scriptPath: './',
  // args: ['value1', 'value2', 'value3']
};

PythonShell.run('1.py', options, function (err, results) {
  if (err) throw err;
  // results is an array consisting of messages collected during execution
  console.log('%j', results);
});