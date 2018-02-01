from tornado.gen import coroutine, Return

from meeepo import controller
from meeepo.view import JsonView


@controller(r'/api/(?P<name>.*)/hello', ('get', 'post'))
@coroutine
def your_controller(req, name):
    anything_else = req.get_argument('anything_else')
    some_data = {name: 'hello, this is {}'.format(name), 'anything else?': anything_else}
    raise Return(JsonView(some_data))
