def get_serializer_error(serializer_errors):
    if not serializer_errors:
        return

    if isinstance(serializer_errors, dict):
        errors = serializer_errors.items()

    if isinstance(serializer_errors, list):
        errors = serializer_errors[0].items()

    first_error = next(iter(errors), None)
    field_name = str(first_error[0]).replace('_', ' ').capitalize()
    field_message = str(first_error[1][0]).capitalize()

    return f"{field_name}: {field_message}"