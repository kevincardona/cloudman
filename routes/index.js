var router		= require('express').Router()
var auth			= require('./auth')
var user			= require('./user')

router.get('/', ( req,res ) => {
	res.send({ success: 'true', message: 'Connected!' })
})

router.post('/signup', auth.signup)
router.post('/login', auth.login)
//router.use(auth.authenticate)
//Requires Authenticated User


module.exports = router;
