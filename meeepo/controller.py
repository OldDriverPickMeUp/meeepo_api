from meeepo import controller
from meeepo.view import JsonView


@controller(r'{{api_path}}', ('get',))
async def get_test(req):
    arg1 = req.get_argument()
    some_data = {}
    return JsonView(some_data)
