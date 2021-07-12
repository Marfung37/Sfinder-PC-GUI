const fs = require("fs");
const {decoder} = require('tetris-fumen');

var fumenCode = process.argv[2]
numPages = decoder.decode(fumenCode).length

fs.writeFile("fumenScripts/scriptsOutput.txt", numPages + "", function(err){
    if (err) return console.log(err);
});