from rest_framework.exceptions import ParseError


def get_value_or_throw_error(request, name):
    value = request.query_params.get(name)
    if not value:
        raise ParseError(f"{name} field is required")
    return value
