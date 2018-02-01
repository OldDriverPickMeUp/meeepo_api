from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.log import access_log
from tornado.web import Application

from .scanner import get_route_map


def start_server(scan_path, port=9987, number_of_process=0, debug=False):
    if debug:
        access_log.log('in debug mode,will only start one process')
        number_of_process = 1
        http_server = HTTPServer(Application(get_route_map(scan_path),debug=True))
    else:
        http_server = HTTPServer(Application(get_route_map(scan_path)))
    access_log.info("Server started on port {}".format(port))
    http_server.bind(port)

    try:
        http_server.start(number_of_process)
        IOLoop.current().start()
    except (KeyboardInterrupt, SystemExit):
        pass