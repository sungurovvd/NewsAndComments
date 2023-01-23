from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .models import PostCategory, Post

@receiver(post_save, sender = PostCategory)
def notify_subscribers(sender, instance, created, **kwargs):
    subscribers = instance.category.author_set.all()
    for aut in subscribers:
        html_content = render_to_string(
            'message.html',
            {
                'user': aut,
                'category': instance.category.name,
                'post': instance.post
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'{instance.category.name}',
            body=instance.post.text,
            from_email='viktorsung@yandex.ru',
            to=[aut.user.email]
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()

