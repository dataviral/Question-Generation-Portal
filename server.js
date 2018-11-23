var express = require('express');
var bodyParser = require('body-parser');
var cookieParser = require('cookie-parser');
var session = require('express-session');
var logger = require('morgan');

// invoke an instance of express application.
var app = express();

// set our application port
app.set('port', 9000);

// set logging
app.use(logger('dev'));

// initialize body-parser to parse incoming parameters requests to req.body
app.use(bodyParser.urlencoded({ extended: true }));

// initialize cookie-parser to allow us access the cookies stored in the browser.
app.use(cookieParser());

// initialize express-session to allow us track the logged-in user across sessions.
app.use(session({
    key: 'user_sid',
    secret: 'somerandonstuffs',
    resave: false,
    saveUninitialized: false,
    cookie: {
        expires: 600000
    }
}));


// This middleware will check if user's cookie is still saved in browser and user is not set, then automatically log the user out.
// This usually happens when you stop your express server after login, your cookie still remains saved in the browser.
app.use((req, res, next) => {
    if (req.cookies.user_sid && !req.session.user) {
        res.clearCookie('user_sid');
    }
    next();
});


// middleware function to check for logged-in users
var sessionChecker = (req, res, next) => {
    if (req.session.user && req.cookies.user_sid) {
        res.redirect('/dashboard');
    } else {
        next();
    }
};


// route for Home-Page
app.get('/', sessionChecker, (req, res) => {
    res.redirect('/home');
});

var homeRoutes = require('./routes/home');
app.route('/home').get(sessionChecker, homeRoutes.get);

//route for user signup
var signupRoutes = require('./routes/signup');
app.route('/signup')
    .get(sessionChecker, signupRoutes.get)
    .post(signupRoutes.post);	

//route for checking username
var existUserNameRoutes = require('./routes/existUserName');
app.route('/existUserName')
	.get(sessionChecker, existUserNameRoutes.get);

// route for user Login
var loginRoutes = require('./routes/login');
app.route('/login')
    .get(sessionChecker, loginRoutes.get)
    .post(loginRoutes.post);


// route for user's dashboard
var dashboardRoutes = require('./routes/dashboard')
app.get('/dashboard', dashboardRoutes.get);


// route for user logout
var logoutRoutes = require('./routes/logout')
app.get('/logout', logoutRoutes.get)


// route for handling 404 requests(unavailable routes)
app.use(function (err, req, res, next) {
  res.status(404).send("404 Page Not Found !")
});


// start the express server
app.listen(app.get('port'), () => console.log(`App started on port ${app.get('port')}`));


module.exports = app;
