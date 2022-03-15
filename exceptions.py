class MessageSentError(Exception):
    pass


class ResponseError(Exception):
    pass


class HomeworksIsNotListError(Exception):
    pass


class NoRequiredTokensError(Exception):
    pass


class EmptyHomeworksError(Exception):
    pass


class NoHomeworkKeyInResponseError(Exception):
    pass


class NoCurrentDateKeyInResponseError(Exception):
    pass


class ResponseIsNotDictError(Exception):
    pass
