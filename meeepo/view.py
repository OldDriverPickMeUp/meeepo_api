import json
import datetime
from decimal import Decimal
from tornado.web import RequestHandler


class DataEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.__str__()
        if isinstance(obj, Decimal):
            return obj.__str__()

        return obj.__dict__


class BasicView(object):
    def render(self, request):
        raise NotImplementedError()


class JsonView(BasicView):
    def __init__(self, obj):
        self.dataPkg = obj
        pass

    def render(self, request):
        if not isinstance(request, RequestHandler):
            raise Exception

            # header set json header
        request.set_header("Content-Type", "application/json;charset=UTF-8")
        request.set_header("Access-Control-Allow-Origin", "*")
        request.write(json.dumps(self.dataPkg, ensure_ascii=False, cls=DataEncoder))


class OptionView(BasicView):
    def render(self, request):
        request.set_header('Access-Control-Allow-Headers', 'Authorization,Content-Type')
        request.set_header('Access-Control-Allow-Methods', 'GET,POST')
        request.set_header("Access-Control-Allow-Origin", "*")
        request.finish()


class StringView(BasicView):
    def __init__(self, string):
        self.data_pkg = string

    def render(self, request):
        if not isinstance(request, RequestHandler):
            raise Exception

        request.set_header("Content-Type", "text/html;charset=UTF-8")
        request.write(self.data_pkg)


class HttpStatusView(BasicView):
    def __init__(self, status_code, msg):
        self.status_code = status_code
        self.msg = msg

    def render(self, request):
        if not isinstance(request, RequestHandler):
            raise Exception

        request.send_error(self.status_code, reason=self.msg)


class ChainView(BasicView):
    def __init__(self):
        pass

    def render(self, request):
        pass


class ViewMaker:
    def __init__(self):
        pass

    @staticmethod
    def json_view(obj):
        return JsonView(obj)

    @staticmethod
    def string_view(string):
        return StringView(string)

    @staticmethod
    def http_status_view(status_code, msg):
        return HttpStatusView(status_code, msg)

    @staticmethod
    def chain_view():
        return ChainView()
