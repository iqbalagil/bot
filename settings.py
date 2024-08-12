from random import choice, randint


def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == '':
        return "well, you\'re actually silent"
    elif 'hello' in lowered:
        return '`Hello there`'
    elif 'how are you' in lowered:
        return 'Good, thanks!'
    elif 'roll dice' in lowered:
        return f"You rolled: {randint(1, 6)}"
    else:
        return choice(['i do not understand',
                       'What are you talking about',
                       'Do you mind rephrasing that'])