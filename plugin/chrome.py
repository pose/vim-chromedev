import os
import threading

#import vim

from sh import cake, cp

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
    
glbs = set()

class NotificationHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        glbs.add(self)
        print 'new connection'
        self.write_message("Hello World")
      
    def on_message(self, message):
        print 'message received %s' % message
 
    def on_close(self):
        print 'connection closed'
        glbs.remove(self)


### Swagger UI ###
SWAGGER_PATH = os.environ['SWAGGER_PATH']
SWAGGER_UI_PATH = os.environ['SWAGGER_UI_PATH']

class CdAndExec(object):
    def __init__(self, code_dir, what_to_exec):
        self.code_dir = code_dir
        self.what_to_exec = what_to_exec

    def __call__(self):
        old_cwd = os.getcwd()
        os.chdir(self.code_dir)
        print self.what_to_exec()
        os.chdir(old_cwd)

class SwaggerUIRefresh(object):
  def on_save(self):
    CdAndExec(SWAGGER_PATH, cake.bake('bake'))()
    cp('%s/lib/swagger.js' % SWAGGER_PATH, '%s/lib' % SWAGGER_UI_PATH) 
    CdAndExec(SWAGGER_UI_PATH, cake.bake('dist'))()

swaggerUI = SwaggerUIRefresh()

### / Swagger UI ###

def start():
    if tornado.ioloop.IOLoop.instance().running():
        print 'Server already running. Not running it again'
    else:
        t = threading.Thread(target=_realStart)
        t.start()

def _realStart():
    print 'Starting server...'
    
    application = tornado.web.Application([
        (r'/websocket', NotificationHandler),
    ])
     
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    http_server.start()
    tornado.ioloop.IOLoop.instance().start()

def ping():
    print 'Ping...'
    swaggerUI.on_save()
    #time.sleep(0.4)
    for i in iter(glbs):
        try:
            i.write_message("ping")
        except:
            pass

def test():
    print glbs

def stop():
    print 'Stopping server'
    tornado.ioloop.IOLoop.instance().stop()
