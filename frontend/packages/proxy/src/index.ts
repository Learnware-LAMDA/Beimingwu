import http from "http";
import httpProxy from "http-proxy";
import { program } from "commander";

program
  .requiredOption("-p, --port <port>", "Source URL")
  .requiredOption("-t, --target <target>", "Target URL")
  .parse(process.argv);

const opts = program.opts();

const proxy = httpProxy.createProxyServer({
  target: opts.target,
  secure: false,
  changeOrigin: true,
});

proxy.on("proxyReq", function (_proxyReq, req: http.IncomingMessage) {
  console.log("method:", req.method);
  console.log("url:", req.url);
  console.log("headers:", req.headers);
  console.log("body:", req.read()?.toString());
});

proxy.on("error", function (err, _req, res) {
  console.log("proxy error", err);
  res.end("Something went wrong. And we are reporting a custom error message.");
});

const proxy_server = http.createServer(function (req, res) {
  proxy.web(req, res);
});

proxy_server.listen(opts.port, function () {
  console.log("proxy server is running");
});
