var router		= require('express').Router()
var auth			= require('./auth')
var user			= require('./user')

router.get('/', ( req,res ) => {
	res.send({ success: 'true', message: 'Connected!' })
})

router.post('/signup', auth.signup)
router.post('/login', auth.login)

//Requires Authenticated User
router.use(auth.authenticate)
router.get('/files', user.getfiles)
router.post('/upload', user.uploadfile)

module.exports = router;
