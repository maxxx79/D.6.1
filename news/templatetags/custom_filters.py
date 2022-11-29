from django import template

register = template.Library()


@register.filter()
def censor(value):
    wrong_words = ['судорога', 'пельмень', 'балаклава', 'кочерыжка', 'родственник', 'статьи', 'редиска']
    for i in wrong_words:
        if i.find(value):
            value = value.replace(i[1::], "*" * len(i))
    return f'{value}'

#CURRENCIES_SYMBOLS = {
#   'rub': 'Р',
#   'usd': '$',
#}

# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
#@register.filter()
#def currency(value, code='rub'):
#   """
#   value: значение, к которому нужно применить фильтр
#   """
#   postfix = CURRENCIES_SYMBOLS[code]
   # Возвращаемое функцией значение подставится в шаблон.
#   return f'{value} {postfix}'