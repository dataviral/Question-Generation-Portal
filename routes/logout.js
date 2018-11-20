var onGetRequest = function(req, res, next){
	if (req.session.user && req.cookies.user_sid) {
		res.clearCookie('user_sid');
		res.redirect('/');
	} else {
		res.redirect('/login');
	}
}

var logoutRoutes = {
	get: onGetRequest,
}

module.exports = logoutRoutes
