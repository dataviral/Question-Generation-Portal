//const users = [{ username: 'test', password: 'test', firstName: 'Test', lastName: 'User' }];
var onGetRequest = function(req, res, next){
	res.sendFile('./public/login.html', { 'root': '.' });
}

var onPostRequest = function(req, res, next){
	const fs = require('fs');
	let rawdata = fs.readFileSync('./models/users.json');  
	const users = JSON.parse(rawdata);  
	//console.log(users);
	var username = req.body.username,
		password = req.body.password;
	const user = users["users"].find(u => u.username === username && u.password === password);

	if (!user) {
		//console.log(user);
		res.redirect('/login');
	} else {
		console.log("Error");
		req.session.user = user.username;
		res.redirect('/dashboard');
	}
}

var loginRoutes = {
	get: onGetRequest,
	post: onPostRequest
}

module.exports = loginRoutes
