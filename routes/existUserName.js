var onGetRequest = function(req, res, next){
	//console.log("Get Request called");
	const fs = require('fs');
	let rawdata = fs.readFileSync('./models/users.json');  
	var users = JSON.parse(rawdata);  
	//console.log("Get Request Users file called");
	var username = req.query.uname;
	//console.log(username);
	var user = users["users"].find(u => u.username === username );
	if (!user) {
		res.send({'exist':false}).status(200);
		
	} else {
		res.send({'exist':true}).status(200);
	}

}


var existUserNameRoutes = {
	get: onGetRequest
}

module.exports = existUserNameRoutes
