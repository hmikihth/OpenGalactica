from django.core.management.base import BaseCommand, CommandError

from engine.models import ShipModel, Species, Planet, Ship, Fleet

class Command(BaseCommand):
    help = "Clean database"
    
    def handle(self, *args, **options):
        
        Species.objects.all().delete()
        Ship.objects.all().delete()
        ShipModel.objects.all().delete()
        Fleet.objects.all().delete()
        Planet.objects.all().delete()
        
        self.stdout.write(
            self.style.SUCCESS(f'Database cleaning successfully executed!')
        )
