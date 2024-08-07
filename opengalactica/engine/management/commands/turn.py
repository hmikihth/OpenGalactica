from django.core.management.base import BaseCommand, CommandError

from ._battle import Battle
from engine.models import Fleet

class Command(BaseCommand):
    help = "Execute a turn"
    
    def execute_battles(self):
        self.stdout.write(
            self.style.SUCCESS('Execute battles...')
        )
        under_attack = {*Fleet.objects.filter(distance=0, role="Attackers").values("target")}
        for planet in under_attack:
            attackers = Fleet.objects.filter(distance=0, role="Attackers", target=planet)
            defenders = Fleet.objects.filter(distance=0, role="Defenders", target=planet)
            battle = Battle(attackers, defenders)


    def handle(self, *args, **options):
        # Moving new planets
        # Add resources
        # Production lines
        # Developments
        # Point and XP recounting
        # Fleet movements
        # Battles
        self.execute_battles()
        # Increase turn counter
        
        self.stdout.write(
            self.style.SUCCESS('Turn successfully executed!')
        )