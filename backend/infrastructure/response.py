from rest_framework import status
from rest_framework.response import Response


def ok(obj_dict) -> Response:
    return Response(data=obj_dict, status=status.HTTP_200_OK)


def created(obj_dict) -> Response:
    return Response(obj_dict, status=status.HTTP_201_CREATED)


def ok_no_content() -> Response:
    return Response(status=status.HTTP_204_NO_CONTENT)


def not_found() -> Response:
    return Response(status=status.HTTP_404_NOT_FOUND)


def bad_request(message: str) -> Response:
    return Response(
        data={"message": message},
        status=status.HTTP_400_BAD_REQUEST,
    )
