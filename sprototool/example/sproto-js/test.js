var fs = require("fs");
var sproto = require("./sproto");
var utils = require("./utils");
var md5 = require("./md5")

var filename = "./protocol.spb";
var buffer = fs.readFileSync(filename);
if (buffer == null){
	console.log("read File err1");
}

console.log(sproto);
console.log(md5(buffer));
var sp = sproto.createNew(buffer);
console.log(sp);

var player = {
    "playerid" :  99662333,
	"nickname" : "helloworld0123456789abcdefg",
	"headid"   : 1001,
	"headurl"  : "http://img5.duitang.com/uploads/item/201410/17/20141017235209_MEsRe.thumb.700_0.jpeg",
	"sex"      : 0,
	"isvip"    : true,
	"gold"     : 21442,
    "signs"     : [false, false, true, false, true],
    "pets"      : [10038, 10039, 10040, 10041, 10042],
    "mails"     : ["hello", "world", "how", "are", "you"],
    "master"      : { "playerid" : 12345, "nickname" : "李飞haha"},
    "friends"    : [
        { "playerid" : 1001, "nickname" : "小张"}, 
        { "playerid" : 1002, "nickname" : "小王"},
        { "playerid" : 1003, "nickname" : "小飞"},
        { "playerid" : 1004, "nickname" : "小龙"}
    ]
}

var buffer = sp.encode("auth.Player", player)

console.log("xxxxxxxxxxxxxxxx decode:")
var result = sp.decode("auth.Player", buffer)
console.log(result)