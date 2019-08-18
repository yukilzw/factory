var http=require('http');
var fs=require('fs');


var out=fs.createWriteStream('./message.txt')
process.stdin.on('data',(data)=>{
    out.write(data)
   //process.exit()
})
