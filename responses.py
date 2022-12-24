def sample_response(message):
    user_input = str(message).lower()

    if user_input == "sample_input":
        return "sample_output"
    return f"Я тебя не понимаю"
