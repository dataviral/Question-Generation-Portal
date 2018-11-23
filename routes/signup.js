var onGetRequest = function(req, res, next){
	res.sendFile('./public/signup.html', { 'root': '.' });
}

var onPostRequest = function(req, res, next){
	const fs = require('fs');
	let rawdata = fs.readFileSync('./models/users.json');  
	var users = JSON.parse(rawdata);  
	var username = req.body.username,
	    password = req.body.password,
	    lastName = req.body.lastName,
            firstName = req.body.firstName;
	var user = users["users"].find(u => u.username === username );
	if (!user) {
		var obj = {"username" : username,
			   "password" : password,
			   "firstName": firstName, 
			   "lastName" : lastName};
		users["users"].push(obj);
		console.log(users);
		users = JSON.stringify(users);
		console.log(users);
		fs.writeFile('./models/users.json',users, function (err) { 
					if (err) {
        					console.error(err);
        					return;
        					}
        				console.log("File has been updated");
        				});
		res.redirect('/login');
	} else {
		console.log("Error");
		res.redirect('/signup');
	}

}

var signupRoutes = {
	get: onGetRequest,
	post: onPostRequest
}

module.exports = signupRoutes
