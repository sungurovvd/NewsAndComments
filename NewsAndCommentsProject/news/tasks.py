from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Subscribers
from datetime import datetime

def send_week_mails():
    subscribers = Subscribers.objects.all()
    for subs in subscribers:
        author = subs.author.user
        posts = subs.category.post_set.all().order_by('-create_time')
        post_count = 0
        name_of_new_posts = ''
        for post in posts:
            if datetime.now().timestamp() - post.create_time.timestamp() < 604800:
                name_of_new_posts = name_of_new_posts + post.article + ' ,'
                post_count = post_count + 1
            else:
                break

        html_content = render_to_string(
            'week_message.html',
            {
                'username': author.username,
                'category': subs.category.name,
                'count': post_count,
                'names': name_of_new_posts
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'{subs.category.name}',
            body=name_of_new_posts,
            from_email='viktorsung@yandex.ru',
            to=[author.email]
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()