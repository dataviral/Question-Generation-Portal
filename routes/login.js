var onGetRequest = function(req, res, next){
	res.sendFile('./public/login.html', { 'root': '.' });
}

var onPostRequest = function(req, res, next){
	var username = req.body.username,
		password = req.body.password;

		if (username!='admin' && password != '123') {
			res.redirect('/login');
		} else {
			req.session.user =  ['admin',123]; //user.dataValues;
			res.redirect('/dashboard');
		}
}

var loginRoutes = {
	get: onGetRequest,
	post: onPostRequest
}

module.exports = loginRoutes
