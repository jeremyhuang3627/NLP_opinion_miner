var natural = require("natural");
var pos = require("pos");
var fs = require('fs');
var path = require('path');

var TfIdf = natural.TfIdf,
    tfidf = new TfIdf(),
    tokenizer = new natural.WordTokenizer();
var filePath = path.join(__dirname + '/data/test.txt');

natural.PorterStemmer.attach();

fs.readFile(filePath, {encoding: 'utf-8'}, function(err,data){
    if (!err){

    	var dataObj = JSON.parse(data);
    	var re = new RegExp("[^\.!\?\n]+[\.!\?\n]+","g");
    	var lines = [];

    	var res =dataObj.reviews[2].match(re);
    	for(var j=0;j<res.length;j++){
    		console.log('---------- new sentence ------------');
    		var words = new pos.Lexer().lex(res[j]);
			var taggedWords = new pos.Tagger().tag(words);
			for (i in taggedWords) {
			    var taggedWord = taggedWords[i];
			    var word = taggedWord[0];
			    var tag = taggedWord[1];
			    
			}
    	}

    	/*var dataArr = data.tokenizeAndStem();
   		var dict = {};

   		for(var i=0;i<dataArr.length;i++)
   		{
   			dict[dataArr[i]] = (dict[dataArr[i]]!=undefined) ? (dict[dataArr[i]]+1) : 0 ;	
   		}

   		var sortable = [];

   		for(var key in dict)
   		{
   			sortable.push([key,dict[key]]);
   		}

   		sortable.sort(function(a, b) {return b[1] - a[1]});

   		for(var i=0;i<sortable.length;i++)
   		{
   			console.log(sortable[i]);
   		} */

    }else{
        console.log(err);
    }
});
