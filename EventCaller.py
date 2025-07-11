import http.server
import random


class EventCaller(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        a = random.randint(0,1)
        if a == 0:
            self.wfile.write(bytes("""
                <html>
                <title>You can't get this page because xht depends on it.</title>
                <body>
                <script type="text/javascript" src="//qzonestyle.gtimg.cn/qzone/hybrid/app/404/search_children.js" charset="utf-8"></script>
                </body>
                </html>""", "utf-8"))
        elif a == 1:
            self.wfile.write(bytes("""
                <html>
                <head>
                    <meta charset="utf-8">
                    <title>You can't get this page because xht depends on it.</title>
                </head>
                <body>
                    <div>
                        无法显示当前页面内容，但是我们可以一起寻找失踪宝贝
                    </div>
                    <iframe frameborder="0" width=500 height=400 src="https://api.isoyu.com/gy/" id="iek8" class="c1797"></iframe>
                    <div>
                        信息来源：
                        <a href="https://baobeihuijia.com/bbhj/" target="_blank">宝贝回家论坛</a>
                        <br/>提示：本页面获取的失踪儿童信息可能已经失效
                    </div>
                </body>
                </html>""","utf-8"))

a=http.server.HTTPServer(('127.0.0.1', 8540), EventCaller)
a.serve_forever()