const franc = require('franc')
const fs = require("fs");

franc('Alle menslike wesens word vry') // => 'afr'
franc('এটি একটি ভাষা একক IBM স্ক্রিপ্ট') // => 'ben'
franc('Alle menneske er fødde til fridom') // => 'nno'
franc('') // => 'und'
franc('the') // => 'und'

let text = fs.readFileSync("../Language_Detection/Dataset/y_new_test.txt");
let textByLine = text.toString().split("\n")