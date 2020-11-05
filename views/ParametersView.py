from my_http.Request import Request
from my_http.Response import Response


class ParametersView:
    def get_response(self, request: Request) -> Response:
        """
        /parameters のパスにきたリクエストに対して、適切なレスポンスを生成して返す
        :param request:
        :return:
        """
        raise NotImplementedError

    def get(self, request: Request) -> Response:
        """
        リクエストメソッドがGETだった時の処理
        """
        raise NotImplementedError

    def post(self, request: Request) -> Response:
        """
        リクエストメソッドがPOSTだった時の処理
        """
        raise NotImplementedError
