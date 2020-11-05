from dataclasses import dataclass


@dataclass
class Request:
    headers: dict
    POST: dict
    GET: dict

    @staticmethod
    def from_env(env: dict) -> "Request":
        """
        WSGIインターフェースのenvからリクエストオブジェクトを生成するファクトリーメソッド
        """
        raise NotImplementedError