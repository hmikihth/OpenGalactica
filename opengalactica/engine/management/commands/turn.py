from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Execute a turn"

    def handle(self, *args, **options):
        # Moving new planets
        # Add resources
        # Production lines
        # Developments
        # Point and XP recounting
        # Fleet movements
        # Battles
        # Increase turn counter
        
        self.stdout.write(
            self.style.SUCCESS('Turn successfully executed!')
        )