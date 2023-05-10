from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from movieswebapp.moviesapp.permissions import IsAdminOrReadOnly
from movieswebapp.moviesapp.utils import run_sql_script


class GenericSqlView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    script_path = ""

    def __init__(self, script_path: str):
        super().__init__()
        self.script_path = script_path

    def post(self, request: Request) -> Response:
        self.check_permissions(request)
        run_sql_script(self.script_path)
        return Response({"message": "SQL script executed successfully"})
