from tornado.gen import coroutine, Return

from meeepo import controller
from meeepo.view import JsonView


@controller(r'{{api_path}}', ('get',))
@coroutine
def get_test(req):
    arg1 = req.get_argument()
    some_data = {}
    raise Return(JsonView(some_data))
