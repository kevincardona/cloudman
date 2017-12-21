var express			= require('express')
var app					= express()
var bodyParser	= require('body-parser')
var routes			= require('./routes')

var port				= process.env.PORT || 5000

app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())

app.use('/', routes)

app.listen( port )
console.log('Starting server on port ' + port)
