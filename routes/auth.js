var bcrypt			= require('bcryptjs')
var fs 					= require('fs')
var jwt 				= require('jsonwebtoken')
var secret 			= "suuperSecret"

var signup = function ( req,res ) {
	if ( !req.body.username || !req.body.password )
		return res.json({ success: false, message: 'No username/password provided' })
	bcrypt.hash(req.body.password, 10, function (err, hash) {
		var newuser = {
			username: req.body.username,
			password: hash
		}
		var contents = JSON.parse(fs.readFileSync('./users.json'))
		var users = contents.users
		for (user in users) {
			if (users[user].username == req.body.username)
				return res.json({ success: false, message: 'Username already exists' })
		}
		users.push(newuser);
		fs.writeFileSync('users.json', JSON.stringify(contents))
		return res.json({ success: true, message: 'Successfully created user!' })
	})
}

var login = function ( req,res ) {
	if ( !req.body.username || !req.body.password )
		return res.json({ success: false, message: 'No username/password provided' })
	var users = JSON.parse(fs.readFileSync('./users.json')).users
	for (user in users) {
		if ( users[user].username == req.body.username) {
			bcrypt.compare(req.body.password, users[user].password, function (err, match) {
				if (match) {
					var token = jwt.sign({ username: users[user].username }, "supersecret", {
						expiresIn: 86400 // 24 Hours
					})
					return res.json({ success: true, message: "Successfully logged in!", token: token })
				} else {
					return res.json({ success: false, message: "Invalid login information." })
				}
			})
		}
	}
}

var authenticate = function ( req,res,next ) {
	var token = req.header('token')

	if (!token)
		return res.json({ success: false, message: 'No token' })

		jwt.verify(token, "supersecret", function(err, decoded) {
			if (err) {
				return res.send({ success: false, message: 'Failed to authenticate token' });
			} else {
					req.decoded = decoded;
					next();
			}
		});
}

var functions = {
	signup: signup,
	login: login,
	authenticate: authenticate
}

module.exports = functions
