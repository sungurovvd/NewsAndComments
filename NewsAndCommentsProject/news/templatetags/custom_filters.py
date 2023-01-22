from django import template


register = template.Library()

@register.filter()
def censor(value):
   answer = ''
   words = value.split()
   bad_words = ['бля', 'гандон', 'гнида', 'говно', 'дроч', 'еба', 'ёба', 'ёбн', 'ёбы', 'ёпт', 'жопа', 'залупа', 'конч', 'лох', 'мразь', 'мудак', 'мудач', 'педик', 'пидор', 'пидр', 'пизд', 'поскуд', 'сать', 'сосать', 'сука', 'уебан', 'хер', 'хуё', 'хует', 'хуит', 'хуй', 'хуя', 'шалава', 'шлюха']
   for word in words:
      check = word.lower()
      if check in bad_words:
         word = word.replace(word, "*" * len(word))
      answer = answer + ' ' + word
   return answer



@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
   d = context['request'].GET.copy()
   for k, v in kwargs.items():
       d[k] = v
   return d.urlencode()