class UserError(Exception):
    pass


class UserNotFoundError(UserError):
    pass


class InvalidUserPatchError(UserError):
    pass


class DuplicateUserEmailError(UserError):
    pass