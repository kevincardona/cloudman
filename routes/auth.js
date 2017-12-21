var bcrypt			= require('bcryptjs')
var fs 					= require('fs')


var signup = function ( req,res ) {
	if ( !req.body.username || !req.body.password )
		return res.json({ success: false, message: 'No username/password provided' })


	var rawdata = {
		username: req.body.username,
		password: req.body.password
	}


	var contents = JSON.parse(fs.readFileSync('./users.json'))

	var users = contents.users

	for (user in users) {
		if (user.username == req.body.username)
			return res.json({ success: false, message: 'Username already exists' })
	}	
		
	fs.writeFileSync('users.json', JSON.stringify(contents))

	return res.json({ success: true, message: 'Successfully created user!' })
}

var login = function ( req,res ) {

}

var authenticate = function ( req,res,next ) {
	next()
}

var functions = {
	signup: signup,
	login: login,
	authenticate: authenticate
}

module.exports = functions
