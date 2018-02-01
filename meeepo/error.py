class UserError(Exception):
    pass


class CoreError(Exception):
    def __init__(self, message, can_out_put=False):
        self.message = message
        self.can_out_put = can_out_put


class ControllerError(CoreError):
    pass


class ServiceError(CoreError):
    pass
