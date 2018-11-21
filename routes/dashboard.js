var router = require('express').Router();
var server = require('http').createServer(router).listen(9001);
var io = require('socket.io')(server);
var PythonShell = require('python-shell');
var options = {
	mode: 'text',
	pythonPath: '/home/aviral/anaconda3/bin/python',
	scriptPath: './question-generator/app.py'
}

var onGetRequest = function(req, res, next){
	if (req.session.user && req.cookies.user_sid) {
		res.sendFile('./public/dashboard.html', { 'root': '.' });
	} else {
		res.redirect('/login');
	}
}

var generateQuestions = function(data){
	console.log(data);
	return {"data": [['ROW1COL1', 'ROW1COL2'], ['OLA', 'OLA2']]};
}

io.on('connection', (socket) => {
	socket.on('generateQuestions', (data) => {
		socket.emit('generatedQuestions', generateQuestions(data));
	});
});

var dashboardRoutes = {
	get: onGetRequest,
}

module.exports = dashboardRoutes
