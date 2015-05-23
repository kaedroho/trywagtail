var commander = require('commander');
    redis     = require('redis'),
    http      = require('http'),
    httpProxy = require('http-proxy');

commander
    .version('1.0.0')
    .option('-p, --port <n>', parseInt, 8000)
    .parse(process.argv);

var listenPort = commander.port;

var redisClient = redis.createClient();
var proxy = httpProxy.createProxyServer()

http.createServer(function(req, res) {
    var hostname = req.headers.host.split(':')[0];
    redisClient.hget('trywagtail_routes', hostname, function(err, target) {
        if (target) {
            console.log(hostname + ' => ' + target);
            proxy.web(req, res, {target: target});
        } else {
            console.log(hostname + ' => 404');
            res.writeHead(404);
            res.end();
        }
    });
}).listen(listenPort);

console.log("Listening on port " + listenPort);
