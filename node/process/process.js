var http = require('http');
var fs = require('fs');
var cp = require('child_process');
var url = require('url');
var qs = require('querystring');

var sp1 = cp.spawn('node', ['test1.js', 'one', 'two', 'three', 'four'], { stdio: 'pipe' });
var sp2 = cp.spawn('node', ['test2.js'], { stdio: 'pipe' });

var str = '';

for (var i = 1; i <= 100000; i++) {
    str += i + ' coming: ' + new Date().getTime() + '&&' + i + '\r\n';
}
sp2.stdin.write(str);
sp2.stderr.on('data', function(data) {
    console.log(data.toString());
});
sp2.on('exit', function(code, signal) {
    console.log('text2 child proces exit，code：' + code + ' ，sign：' + signal);
    // process.exit()
});


sp1.stdout.on('data', function(data) {
    console.log('child process print：\r\n' + data);
});
sp1.stderr.on('data', function(data) {
    console.log(data.toString());
});
sp1.on('exit', function(code, signal) {
    console.log('text1 child proces exit，code：' + code + ' ，sign：' + signal);
    // process.exit()
});

/* fs.readFile('./test.js', 'utf-8', function(err, res) {
    console.log(process.argv);
    console.log(process.memoryUsage());
}); */
http.createServer(function(req, res) {
    console.log(qs.parse(req.url.split('?')[1]));
    sp2.kill('SIGTERM');
    res.setHeader('Content-Type', 'text/html;charset=utf-8');
    res.end('kill child proces successed');
}).listen('835');

/* var mp3 = fs.createReadStream('./message.txt');

mp3.byte = 0;
mp3.on('data', function(data) {
    console.log(data.length);
    mp3.byte += data.length;
});
mp3.on('end', function() {
    console.log('read %d byte', mp3.byte);
}); */