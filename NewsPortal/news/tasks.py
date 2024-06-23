from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from news.models import News, Category
from datetime import datetime, timedelta


@shared_task
def send_news_notification(news_id):
    try:
        news = News.objects.get(id=news_id)
        for category in news.categories.all():
            subject = f"Новая новость в категории {category.name}: {news.title}"
            snippet = f'{news.text[:50]}...' if len(news.text) > 50 else news.text
            for user in category.subscribers.all():
                try:
                    url = f"{settings.SITE_URL}/news/{news.pk}/"
                    message = (
                        f'Здравствуй, {user.username}.\n'
                        f'В категории {category.name} появилась новая новость!\n\n'
                        f'{news.title}\n\n'
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
    except News.DoesNotExist:
        print(f'Новость с id {news_id} не найдена')

@shared_task
def send_weekly_digest():
    one_week_ago = datetime.now() - timedelta(days=7)
    recent_news = News.objects.filter(dateCreation__gte=one_week_ago)

    for category in Category.objects.all():
        category_news = recent_news.filter(categories=category)
        if not category_news.exists():
            continue

        subscribers = category.subscribers.all()
        if not subscribers:
            continue

        subject = f"Еженедельная рассылка новостей в категории {category.name}"
        message = render_to_string('weekly_digest.html', {
            'category': category,
            'news_list': category_news,
        })

        for user in subscribers:
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                )
            except Exception as e:
                print(f'Ошибка при отправке рассылки: {e}')