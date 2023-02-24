import os
import re
from django import template

register = template.Library()

BAN_WORDS = []

with open(os.path.join('news/templatetags/ban_words.txt'), 'r', encoding='utf-8') as ban_word_file:
    for word in ban_word_file:
        BAN_WORDS.append(word.split('\n')[0])


@register.filter(name='multiply')
def multiply(value, arg):
    return str(value) * arg


@register.filter(name='censor')
def censor(value, arg):
    """
    Цензурный фильтр
    param value: Название или текст статьи
    param arg: символ, которым заменяются буквы нецензурного слова
    """
    if isinstance(value, str) and isinstance(arg, str):
        content = value.split()
        for idx, w in enumerate(value.split()):
            if w.lower() in BAN_WORDS:
                content[idx] = re.sub(w, f'{w[0]}{arg * (len(w) - 1)}', content[idx])
        return " ".join(content)
    else:
        raise ValueError()
