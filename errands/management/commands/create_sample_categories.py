from django.core.management.base import BaseCommand
from errands.models import Category

class Command(BaseCommand):
    help = 'Creates sample categories for the ErrandMate application'

    def handle(self, *args, **kwargs):
        categories = [
            {
                'name': 'Grocery Shopping',
                'description': 'Get your groceries delivered or picked up from the store'
            },
            {
                'name': 'House Cleaning',
                'description': 'Professional cleaning services for your home'
            },
            {
                'name': 'Pet Care',
                'description': 'Pet walking, sitting, and grooming services'
            },
            {
                'name': 'Moving & Delivery',
                'description': 'Help with moving furniture and delivering packages'
            },
            {
                'name': 'Home Repairs',
                'description': 'Basic home repairs and maintenance services'
            },
            {
                'name': 'Tech Support',
                'description': 'Computer setup, troubleshooting, and tech assistance'
            }
        ]

        for category_data in categories:
            Category.objects.get_or_create(
                name=category_data['name'],
                defaults={'description': category_data['description']}
            )

        self.stdout.write(self.style.SUCCESS('Successfully created sample categories')) 