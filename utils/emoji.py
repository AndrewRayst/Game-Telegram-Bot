import emoji


def emojize(text: str) -> str:
    return emoji.emojize(f'{text}', variant='emoji_type')


def demojize(text: str) -> str:
    return emoji.demojize(f'{text}')
