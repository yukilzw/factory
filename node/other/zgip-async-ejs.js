var express = require('express');
var bodyParser = require('body-parser');
var mysql = require('mysql');
var http = require('http');
var path = require('path');
var fs = require('fs');
var zlib = require('zlib');
var ejs = require('ejs');
var ejsExcel = require('ejsexcel');
var async = require('async');
var app = express();

var connection = mysql.createConnection({
    host: 'localhost',
    user: 'lzw',
    password: '19940825',
    database: 'test_db'
});

// 创建 application/x-www-form-urlencoded 编码解析
app.use(bodyParser.urlencoded({ extended: false }));
app.set('view engine', 'ejs');
app.engine('*', require('ejs').__express);
app.all('*', function(req, res, next) {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Headers', 'X-Requested-With');
    res.header('Access-Control-Allow-Methods', 'PUT,POST,GET,DELETE,OPTIONS');
    res.header('X-Powered-By', ' 3.2.1');
    // res.header('Content-Type', 'application/json;charset=utf-8');
    next();
});

app.all('*', function (req, res, next) {
    console.log(req.path);
    next();
});
app.use(express.static(path.join(__dirname, './hospital-app')));
app.listen(12345, function () {
    console.log('12345 start');
});
app.get('/', function (req, res) {
    console.log(req.connection.remoteAddress);
    res.header('Content-Type', 'text/html');
    res.header('Content-Encoding', 'gzip');
    var output = fs.createWriteStream('./hospital-app/app-dist/min.gz');
    var input = fs.createReadStream('./hospital-app/app-dist/min.js');
    var responseData = [];

    fs.readFile('./staff.png', 'binary', function(err, data) {
        res.write(data, 'binary');
        res.end(data, 'binary');
        console.log(req.headers['accept-encoding'].indexOf('gzip'));
        switch (req.headers['content-encoding']) {
            case 'gzip':
                data.pipe(zlib.createGunzip()).pipe(output);
                break;
            case 'deflate':
                data.pipe(zlib.createInflate()).pipe(output);
                break;
            default:
                data.pipe(output);
                break;
        }
        input.on('data', function(chunk) {
            responseData.push(chunk);
        });
        input.on('end', function() {
            var finalData = Buffer.concat(responseData);

            res.write(finalData);
            res.end();
        });
    });
    input.pipe(zlib.createGzip()).pipe(output);
    res.redirect('./app-dist/dist.html');
});
app.use(function (req, res) {
    console.log(req.path + '!404!');
    res.send('404');
});

function gzip() {
    var output = fs.createWriteStream('./hospital-app/app-dist/min.gz');
    var input = fs.createReadStream('./hospital-app/app-dist/min.js');

    input.pipe(zlib.createGzip()).pipe(output);
}
// gzip()

function baobiao() {
    var arr = [];

    for (var i = 0; i < 10000; i++) {
        var content = !(i % 2) ? { 'wodege': 'aaa', 'we': 6666 } : { 'wodege': '恩', 'we': '哦？' };

        arr[i] = content;
    }
    console.time(0);
    var moban = fs.readFileSync('./baobiao.xlsx');

    ejsExcel.renderExcelCb(moban, arr, function(err, exlBuf2) {
        if (err) {
            console.log('表格生成失败');
        } else {
            fs.writeFileSync('./baobiao2.xlsx', exlBuf2);
            console.timeEnd(0);
        }
    });
}
// baobiao()


function asynsDemo() {
    console.time(1);
    async.series([function(cb) {
        setTimeout(function() {
            cb(null, 1);
        }, 2000);
    }, function(cb) {
        setTimeout(cb, 1000, null, 2);
    }], function(err, result) {  // result是每个回调函数传进来的data参数，result=[1,2]
        if (err) {
            console.error(err);
        } else {
            console.log(result);
        }
        console.timeEnd(1);
    });
}
// asynsDemo()


connection.connect(function(err) {
    if (err) {
        console.log(err);
    } else {
        console.log('连接数据库成功');
        app.get('/mysql', function (req, res) {
            connection.query('INSERT INTO lzw1 SET ?',
                { id: 12, name: '厉害了我的哥', point: 3, time: '2017-3-14', assess: '留言内容' },
                function (err, result) {
                    if (err) {
                        console.log(err);
                        connection.end(function (err) {
                            if (err) {
                                console.log('关闭数据库失败');
                            } else {
                                console.log('关闭数据库成功');
                            }
                        });
                    } else {
                        var reArr = [];

                        for (var i = 0; i < result.length; i++) {
                            reArr[i] = result[i];
                        }
                        console.log(reArr);
                        res.end(JSON.stringify(reArr));
                    }
                }
            );
        });
    }
});
