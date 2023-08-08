def format_error_message(errors):
    for field, message_list in errors.items():
        return f"{field.capitalize()}: {message_list[0].capitalize()}"