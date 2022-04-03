var fs = require("fs");
var sproto = require("./sproto");
var utils = require("./utils");

// var filename = "./test.spb";
// var buffer = fs.readFileSync(filename);
// if (buffer == null){
// 	console.log("read File err1");
// }
// console.log(sproto);

// var sp = sproto.createNew(buffer);
// console.log(sp);

// var req = {
// 	name : "abdef",
// 	isvip : true,
// 	boolarr : [ true, false, true, true, false, false ],
// }

// var binary = sp.encode("test.MyInfo", req);
// console.log(binary);


// var pack_binary = sp.pack(binary);
// console.log(pack_binary);

// var unpack_binary = sp.unpack(pack_binary);
// console.log(unpack_binary);

// var data = sp.decode("test.MyInfo", unpack_binary);
// console.log(data);



var filename = "./protocol.spb";
var buffer = fs.readFileSync(filename);
if (buffer == null){
	console.log("read File err1");
}
console.log(sproto);

var sp = sproto.createNew(buffer);
console.log(sp);

// var bin = [93, 2, 8, 2, 4, 2, 17, 3, 32, 255, 3, 48, 55, 49, 52, 57, 75, 85, 122, 48, 78, 107, 56, 55, 104, 49, 119, 111, 98, 86, 122, 48, 109, 101, 65, 85, 122, 48, 52, 57, 75, 85, 112, 112];
// var bin = [93, 2, 8, 2, 4, 2, 17, 3, 32, 255, 3, 48, 48, 49, 114, 84, 80, 80, 105, 49, 53, 100, 66, 99, 120, 48, 118, 68, 78, 80, 105, 49, 75, 103, 53, 81, 105, 49, 114, 84, 80, 80, 77, 77,]
// var un_bin = sp.unpack(bin);
// console.log(un_bin);

// var header = sp.decode("Package", un_bin);
// console.log(header);

// var used_sz = sp.objlen("Package", un_bin);
// var left_sz = un_bin.length - used_sz;
// var left_bin = un_bin.slice(used_sz, un_bin.length);
// var data = sp.decode("auth.WeiXinReq", left_bin);
// console.log(data);

var header = {
	session : 1,
	protoid : 259,
};

var req = {
	code : "001rTPPi15dBcx0vDNPi1Kg5Qi1rTPPM",
};

var header_buffer = sp.encode("Package", header);
var data_buffer = sp.encode("auth.WeiXinReq", req);
console.log(header_buffer);
console.log(data_buffer);
var concat_buffer = utils.arrayconcat(header_buffer, data_buffer);
var pack_buffer = sp.pack(concat_buffer);
console.log(pack_buffer);

