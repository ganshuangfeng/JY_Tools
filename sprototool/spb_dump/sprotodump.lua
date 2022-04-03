package.path =  "./lualib/?.lua;"
package.cpath = "./luaclib/?.dll;"

local lfs = require "lfs"
local class = require "class"
local parser = require "sprotoparser"
local base64 = require "base64"

local function dump_sproto(_from_file,_to_file)
	local f = assert(io.open(_from_file), "Can't open " .. _from_file)
	local text = f:read "a"
	f:close()
	local content = parser.parse(text)

	local f2 = assert(io.open(_to_file, "w+b"), "can't open " .. _to_file)
	f2:write(content)
	f2:close()
	print("dump " .. _from_file .. " => " .. _to_file .. " ok!")
end

dump_sproto("./whole_proto_c2s.txt","./whole_proto_c2s.spb")
dump_sproto("./whole_proto_s2c.txt","./whole_proto_s2c.spb")
