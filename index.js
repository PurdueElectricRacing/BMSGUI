const pytalk = require('pytalk');

var tester = pytalk.worker('./python_interface/communication.py');
var test = tester.method('test');

test('this some garbage yo', (err, retgarbage) => 
{
  console.log(retgarbage);
});