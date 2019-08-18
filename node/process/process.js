const http=require('http'),
      fs = require('fs'),
      cp=require('child_process'),
      url = require("url"),
      qs  = require("querystring");

let sp1=cp.spawn('node',['test1.js','one','two','three','four'],{stdio:'pipe'}),
    sp2=cp.spawn('node',['test2.js'],{stdio:'pipe'});

let str=''
for(let i=1;i<=100000;i++){
    str+=i+' 我进来了老铁 '+new Date().getTime()+'&&'+i+'\r\n';
}
sp2.stdin.write(str)
sp2.stderr.on('data',function(data){
    console.log(data.toString())
})
sp2.on('exit',function(code,signal){
    console.log('text2子进程退出，代码：'+code+' ，信号：'+signal)
    //process.exit()
})


sp1.stdout.on('data',function(data){
    console.log('子进程标准输出：\r\n'+data)
})
sp1.stderr.on('data',function(data){
    console.log(data.toString())
})
sp1.on('exit',function(code,signal){
    console.log('text1子进程退出，代码：'+code+' ，信号：'+signal)
    //process.exit()
})

/*fs.readFile('./test.js','utf-8',function(err,res){
    console.log(process.argv)
    console.log(process.memoryUsage())
})*/
http.createServer(function(req,res){
    console.log(qs.parse(req.url.split('?')[1]))
    sp2.kill('SIGTERM')
    res.setHeader('Content-Type','text/html;charset=utf-8')
    res.end('成功杀掉进程')
}).listen('835')

/*var mp3 = fs.createReadStream('./message.txt');
mp3.byte=0;
mp3.on('data',(data)=>{
    console.log(data.length)
    mp3.byte+=data.length;
})
mp3.on('end',()=>{
    console.log("读取到 %d 字节",mp3.byte)
})*/

