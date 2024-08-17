from django.core.management.base import BaseCommand, CommandError

from engine.models import ShipModel

class Command(BaseCommand):
    help = "Clean database"
    
    def handle(self, *args, **options):
        
        ShipModel.objects.all().delete()
        
        self.stdout.write(
            self.style.SUCCESS(f'Database cleaning successfully executed!')
        )
