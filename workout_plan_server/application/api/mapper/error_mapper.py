

class ErrorMapper(object):

    @staticmethod
    def to_dto(exception: Exception, http_status: int) -> dict:
        return {
            "message": str(exception),
            "status": http_status,
            "type": type(exception).__name__
        }
