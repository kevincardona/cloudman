var fs 					= require('fs')

var uploadfile = function ( req,res ) {
  var dir = "storage/" + req.decoded.username
  if (!fs.existsSync(dir))
    fs.mkdirSync(dir);

  return res.json({ success: true, message: "Successfully uploaded file!" })
}

var getfiles = function ( req,res ) {
  var dir = "storage/" + req.decoded.username
  if (!fs.existsSync(dir))
    fs.mkdirSync(dir);

  return res.json({ success: true, message: "Successfully retrieved files!" })
}

var functions = {
  getfiles: getfiles,
  uploadfile: uploadfile
}

module.exports = functions
