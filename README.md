# meeepo_api
a simple package you can use tornado to build an api server using flask style
## get started

### register a controller
```python
from tornado.gen import coroutine, Return
 
from meeepo import controller
from meeepo.view import JsonView
 
 
@controller(r'/api/(?P<name>.*)/hello', ('get', 'post'))
@coroutine
def your_controller(req, name):
    anything_else = req.get_argument('anything_else')
    some_data = {name: 'hello, this is {}'.format(name), 'anything else?': anything_else}
    raise Return(JsonView(some_data))
    
```
### start your api server
```python
from meeepo import start_server
 
 
def startup():
    scan_path = 'example_app/controllers'
    port = 8080
    start_server(scan_path, port)
 
 
if __name__ == '__main__':
    startup()
```
## test
```
$ curl -XGET localhost:8080/api/tornado/hello
{"tornado": "hello, this is tornado", "anything else?": null}
```
```
$ curl -XPOST localhost:8080/api/kenny/hello?anything_else=not_dead_yet
{"kenny": "hello, this is kenny", "anything else?": "not_dead_yet"}
```