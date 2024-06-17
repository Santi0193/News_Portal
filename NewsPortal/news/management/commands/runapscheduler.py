import logging
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from news.models import Category, News

logger = logging.getLogger(__name__)

def send_weekly_digest():
    now = timezone.now()
    last_week = now - timedelta(days=7)

    categories = Category.objects.all()

    for category in categories:
        news_from_last_week = News.objects.filter(categories=category, created_at__gte=last_week)
        if not news_from_last_week.exists():
            continue

        for subscriber in category.subscribers.all():
            news_list = '\n\n'.join([
                f'{news.title}\n'
                f'{"{:.50}".format(news.text) if len(news.text) > 50 else news.text}...\n'
                f'Читать полностью: {settings.SITE_URL}/news/{news.pk}/'
                for news in news_from_last_week
            ])

            subject = f'Еженедельная рассылка: Новые статьи в разделе {category.name}'
            message = (
                f'Здравствуй, {subscriber.username},\n\n'
                f'За прошедшую неделю были добавлены следующие статьи в твоем любимом разделе!\n\n'
                f'{news_list}\n\n'
                f'С наилучшими пожеланиями,\n'
                f'Команда вашего новостного портала'
            )

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[subscriber.email],
            )

def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_weekly_digest,
            trigger=CronTrigger(
                day_of_week="sun", hour="00", minute="00"
            ),
            id="send_weekly_digest",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'send_weekly_digest'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")