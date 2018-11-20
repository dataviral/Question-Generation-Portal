var onGetRequest = function(req, res, next){
	if (req.session.user && req.cookies.user_sid) {
		res.sendFile('./public/dashboard.html', { 'root': '.' });
	} else {
		res.redirect('/login');
	}
}

var dashboardRoutes = {
	get: onGetRequest,
}

module.exports = dashboardRoutes
