from tornado.web import RequestHandler
from tornado.log import access_log as logger
from tornado.gen import coroutine

from .view import BasicView, ChainView, OptionView, JsonView
from .error import CoreError


class MetaHandler(RequestHandler):
    methods = None

    @coroutine
    def get(self, *args, **kwargs):
        try:
            method_info = self.methods.get('get')
            if method_info is None:
                self.send_error(status_code=404, reason="not found")
                return
            call_func = method_info['func']
            filter_funcs = method_info['filters']
            request_obj = MetaRequest(self)

            for each_filter in filter_funcs:
                view_obj = each_filter(request_obj)
                if not isinstance(view_obj, BasicView):
                    self.send_error(status_code=500, reason="internal error")
                    return

                if isinstance(view_obj, ChainView):
                    continue

                view_obj.render(request=self)
                return

            try:
                view_obj = yield call_func(request_obj, *args, **kwargs)
            except CoreError as e:
                logger.error('%s:%s' % (e.__class__.__name__, e.message))
                if getattr(e, "can_out_put", None):
                    msg = e.message
                else:
                    msg = ""
                view_obj = JsonView({'code': 'ERROR', 'msg': msg, 'data': {}})
                view_obj.render(request=self)
                return

            if not isinstance(view_obj, BasicView):
                self.send_error(status_code=500, reason="internal error")
                return
            view_obj.render(request=self)
        except Exception as e:
            logger.exception(e)
            self.send_error(status_code=500, reason='internal error')

    @coroutine
    def post(self, *args, **kwargs):
        try:
            method_info = self.methods.get('post')
            if method_info is None:
                self.send_error(status_code=404, reason="not found")
                return
            call_func = method_info['func']
            filter_funcs = method_info['filters']
            request_obj = MetaRequest(self)

            for each_filter in filter_funcs:
                view_obj = each_filter(request_obj)
                if not isinstance(view_obj, BasicView):
                    self.send_error(status_code=500, reason="internal error")
                    return

                if isinstance(view_obj, ChainView):
                    continue

                view_obj.render(request=self)
                return
            try:
                view_obj = yield call_func(request_obj, *args, **kwargs)
            except CoreError as e:
                logger.error('%s:%s' % (e.__class__.__name__, e.message))
                if getattr(e, "can_out_put", None):
                    msg = e.message
                else:
                    msg = ""
                view_obj = JsonView({'code': 'ERROR', 'msg': msg, 'data': {}})
                view_obj.render(request=self)
                return

            if not isinstance(view_obj, BasicView):
                self.send_error(status_code=500, reason="internal error")
                return
            view_obj.render(request=self)
        except Exception as e:
            logger.exception(e)
            self.send_error(status_code=500, reason='internal error')

    def options(self, *args, **kwargs):
        view_obj = OptionView()
        view_obj.render(request=self)


class MetaRequest:
    def __init__(self, request):
        if not isinstance(request, RequestHandler):
            raise Exception

        self.__http_request = request
        self.session = None
        self.user = None

    def get_argument(self, name, default=None):
        return self.__http_request.get_argument(name=name, default=default)

    def get_query_string(self):
        return self.__http_request.request.query

    def get_uri(self):
        return self.__http_request.request.path

    def get_header(self):
        return self.__http_request.request.headers

    def get_body(self):
        return self.__http_request.request.body

    def get_remote_ip(self):
        return self.__http_request.request.remote_ip

    def get_host(self):
        return self.__http_request.request.host

    def get_full_url(self):
        return self.__http_request.request.full_url

    def get_cookie(self, name):
        return self.__http_request.get_cookie(name)

    def set_cookie(self, name, value, exprie):
        return self.__http_request.set_cookie(name=name, value=value, expires=exprie)

    def set_session(self, session):
        self.session = session

    def get_session(self):
        return self.session

    def set_user(self, user_id):
        self.user = int(user_id)

    def get_user(self):
        return self.user

    def get_file(self, name):
        return self.__http_request.request.files.get(name, None)

    def get_raw_file(self):
        return self.__http_request.request.files
