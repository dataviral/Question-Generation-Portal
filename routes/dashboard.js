var router = require('express').Router();
var server = require('http').createServer(router).listen(9001);
var io = require('socket.io')(server);
var PythonShell = require('python-shell').PythonShell;


var onGetRequest = function(req, res, next){
	if (req.session.user && req.cookies.user_sid) {
		res.sendFile('./public/dashboard.html', { 'root': '.' });
	} else {
		res.redirect('/login');
	}
}

var generateQuestions =  function(data, socket){
	var options = {
		mode: 'text',
		pythonPath: '/home/aviral/anaconda3/bin/python',
		scriptPath: './question-generator/',
		args: [JSON.stringify(data)]
	}
	 PythonShell.run('Gen1.py', options, function (err, results) {
      if (err) throw err;
	  socket.emit('generatedQuestions', {'data': JSON.parse(results)});
    });
}

var pFetch = function(val, socket){
	var fs = require('fs');
	var obj = JSON.parse(fs.readFileSync('examples.json', 'utf8'));
	socket.emit('pFetched', obj[val]);
}

io.on('connection', (socket) => {
	socket.on('generateQuestions', (data) => {
		generateQuestions(data, socket);
	});
	socket.on('pFetch', (val) => {
		pFetch(val, socket);
	});
});


var dashboardRoutes = {
	get: onGetRequest,
}

module.exports = dashboardRoutes
