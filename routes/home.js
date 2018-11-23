var onGetRequest = function(req, res, next){
	res.sendFile('./public/home.html', { 'root': '.' });
}

var homeRoutes = {
	get: onGetRequest
}

module.exports = homeRoutes
