from django.db.models.signals import pre_save, m2m_changed, post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import News
from django.core.mail import send_mail
from django.conf import settings

@receiver(pre_save, sender=News)
def limit_news_per_user(sender, instance, **kwargs):
    if instance.pk is None:
        today = timezone.now().date()
        news_count = News.objects.filter(author=instance.author, created_at__date=today).count()
        if news_count >= 3:
            raise ValidationError("Нельзя публиковать более трёх новостей в сутки.")


@receiver(m2m_changed, sender=News.categories.through)
def notify_subscribers_on_news_creation(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        for category in instance.categories.all():
            subject = instance.title
            snippet = f'{instance.text[:50]}...' if len(instance.text) > 50 else instance.text
            for user in category.subscribers.all():
                try:
                    url = f"{settings.SITE_URL}/news/{instance.pk}/"
                    message = (
                        f'Здравствуй, {user.username}.\n'
                        f'Новая статья в твоём любимом разделе!\n\n'
                        f'{instance.title}\n\n'
                        f'{snippet}\n\n'
                        f'Читать полностью: {url}'
                    )
                    send_mail(
                        subject=subject,
                        message=message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email],
                    )
                except Exception as e:
                    print(f'Ошибка при отправке уведомления: {e}')

@receiver(post_save, sender=News)
def notify_subscribers_on_news_update(sender, instance, created, **kwargs):
    if not created:
        for category in instance.categories.all():
            subject = f"Новость обновлена в категории {category.name}: {instance.title}"
            snippet = f'{instance.text[:50]}...' if len(instance.text) > 50 else instance.text
            for user in category.subscribers.all():
                try:
                    url = f"{settings.SITE_URL}/news/{instance.pk}/"
                    message = (
                        f'Здравствуй, {user.username}.\n'
                        f'Новость была обновлена в твоём любимом разделе {category.name}!\n\n'
                        f'{instance.title}\n\n'
                        f'{snippet}\n\n'
                        f'Читать полностью: {url}'
                    )
                    send_mail(
                        subject=subject,
                        message=message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email],
                    )
                except Exception as e:
                    print(f'Ошибка при отправке уведомления: {e}')