import importlib
import os
from tornado.log import access_log as logger
from tornado.web import StaticFileHandler
from .settings import ALLOW_STATIC_FILE, STATIC_FILE_PATH
from .meta import MetaHandler


def _return_path_and_files(path):
    dir_paths = []
    py_files = []
    for each in os.listdir(path):
        if os.path.isdir(os.path.sep.join([path, each])):
            dir_paths.append(os.path.sep.join([path, each]))
        elif not each.startswith('_') and each.endswith('.py'):
            py_files.append(os.path.sep.join([path, each]))
    return dir_paths, py_files


def _get_py_files(path, recursive):
    py_files = []
    dir_paths, add_pyfiles = _return_path_and_files(path)
    py_files.extend(add_pyfiles)
    if dir_paths and recursive:
        for each_dir_path in dir_paths:
            py_files.extend(_get_py_files(each_dir_path, recursive))
    return py_files


def _scan_and_import(base_path, recursive=False):
    py_files = _get_py_files(base_path, recursive)
    module_pkgs = [((each_file.split('.')[0].replace(os.path.sep, '.'))
                    if not each_file.startswith('.') else (each_file.split('.')[1].replace(os.path.sep, '.')))
                   for each_file in py_files]
    for each_pkg in module_pkgs:
        if each_pkg.startswith('.'):
            importlib.import_module(each_pkg[1:])
        else:
            importlib.import_module(each_pkg)


class FilterManager:
    __filter_store = {}
    __global_filters = []

    @staticmethod
    def register(name, global_=False):
        def func_wrapper(func):
            FilterManager.__filter_store[name] = func
            logger.info("    |-- filtering: %s", func.__name__)
            if global_:
                FilterManager.__global_filters.append(name)
            return func

        return func_wrapper

    @staticmethod
    def get_filter(name):
        return FilterManager.__filter_store[name]

    @staticmethod
    def get_global_filters():
        return FilterManager.__global_filters


class ControllerManager:
    __control_store = {}
    count = 0

    @staticmethod
    def _get_one():
        ControllerManager.count += 1
        return ControllerManager.count

    @staticmethod
    def register(uri, method=('get', 'post'), filters=(), bypass=False):
        if not isinstance(method, (list, tuple)):
            update_method = [method]
        else:
            update_method = method
        update_method = [each.lower() for each in update_method]

        if not isinstance(filters, (list, tuple)):
            set_filters = [filters]
        else:
            set_filters = filters

        def func_wrapper(func):
            if uri in ControllerManager.__control_store.keys():
                controller_record = ControllerManager.__control_store[uri]
                for each_method in update_method:
                    if each_method in controller_record.keys():
                        raise Exception("Uri=%s for method %s has bean mapped" % (uri, method))
                    controller_record[each_method]['func'] = func
                    controller_record[each_method]['filters'] = set_filters
                    controller_record[each_method]['bypass'] = bypass
                    logger.info("mapping: %s %s --> %s", each_method.upper(), uri, func.__name__)
            else:
                controller_record = {}
                for each_method in update_method:
                    controller_record[each_method] = {}
                    controller_record[each_method]['func'] = func
                    controller_record[each_method]['filters'] = set_filters
                    controller_record[each_method]['bypass'] = bypass
                    logger.info("mapping: %s %s --> %s", each_method.upper(), uri, func.__name__)
                ControllerManager.__control_store[uri] = controller_record
            return func

        return func_wrapper

    @staticmethod
    def get_route_map():
        all_handlers = []
        for uri, build_info in ControllerManager.__control_store.items():
            all_handlers.append((uri, ControllerManager._build_handler(build_info)))
        if not all_handlers:
            raise Exception('No controller scanned, please start it with')
        if ALLOW_STATIC_FILE:
            all_handlers.append(
                [r'/html/(.*)', StaticFileHandler, {'path': os.path.sep.join([os.getcwd(), STATIC_FILE_PATH])}])
        return tuple(all_handlers)

    @staticmethod
    def _build_handler(build_info):
        type_dict = {}
        for method in build_info.keys():
            type_dict[method] = {}
            type_dict[method]['func'] = build_info[method]['func']
            filter_names = set(build_info[method]['filters'])
            if build_info[method]['bypass']:
                filter_names += set(FilterManager.get_global_filters())
            all_filter_funcs = [FilterManager.get_filter(each_name) for each_name in list(filter_names)]
            type_dict[method]['filters'] = all_filter_funcs
        return type('MetaHandler_' + str(ControllerManager._get_one()), (MetaHandler,), {'methods': type_dict})


def _scan_controller(path):
    _scan_and_import(path, True)


def get_route_map(path):
    _scan_controller(path)
    return ControllerManager.get_route_map()


controller = ControllerManager.register
filter = FilterManager.register
