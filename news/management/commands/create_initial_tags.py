from django.core.management.base import BaseCommand
from news.models import Tag

class Command(BaseCommand):
    help = 'Creates initial tags for the application'

    def handle(self, *args, **kwargs):
        initial_tags = [
            'Technology',
            'Programming',
            'Python',
            'JavaScript',
            'Web Development',
            'AI',
            'Machine Learning',
            'Data Science',
            'Security',
            'Open Source'
        ]

        for tag_name in initial_tags:
            Tag.objects.get_or_create(name=tag_name)
            self.stdout.write(self.style.SUCCESS(f'Created tag: {tag_name}'))
