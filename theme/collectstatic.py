
from django.core.management import call_command
from django.contrib.staticfiles.management.commands.collectstatic import (
    Command as CollectStaticCommand,
)
# https://www.khanna.law/blog/deploying-django-tailwind-to-heroku

class Command(CollectStaticCommand):
    def handle(self, *args, **options):
        call_command("tailwind", "build")
        super().handle(*args, **options)
        
        