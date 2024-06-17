import re
from django import template

register = template.Library()


@register.filter()
def censor(value):
    bad_words = ['мудаки', 'твари']

    if not isinstance(value, str):
        raise TypeError(f"unresolved type '{type(value)})' expected type 'str'")


    pattern = re.compile(r'\b(?:' + '|'.join(re.escape(word) for word in bad_words) + r')\b', re.IGNORECASE)

    censored_value = pattern.sub(lambda x: '*' * len(x.group()), value)

    return censored_value