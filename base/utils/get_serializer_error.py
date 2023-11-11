def get_serializer_error(serializer_errors):
    errors = serializer_errors.items()
    if not errors:
        return

    first_error = next(iter(errors), None)
    message = str(first_error[1][0])
    return message.capitalize()