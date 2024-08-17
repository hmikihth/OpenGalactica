from django.core.management.base import BaseCommand, CommandError

from ._battle import Battle
from ._fleet_movements import FleetMovements
from ._point_calculations import PointCalculations
from ._developments import Developments
from ._productions import Productions
from ._resources import Resources
from ._moving_planets import MovingPlanets

from engine.models import Fleet, Round


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
            battle.calculate()

    def end_turn(self):
        current_round = Round.objects.order_by("number").last()
        if not current_round:
            current_round = Round()
            current_round.save()
        return current_round.tick()
        
    def moving_planets(self):
        return MovingPlanets().run()
        
    def move_fleets(self):
        return FleetMovements().run()
        
    def calculate_points(self):
        return PointCalculations().run()
        
    def run_developments(self):
        return Developments().run()
        
    def run_productions(self):
        return Productions().run()
        
    def add_resources(self):
        return Resources().run()

    def handle(self, *args, **options):
        # Add resources
        self.add_resources()
        
        # Production lines
        self.run_productions()
        
        # Developments
        self.run_developments()
        
        # Point and XP recounting
        self.calculate_points()

        # Fleet movements
        self.move_fleets()

        # Battles
        self.execute_battles()

       # Moving new planets
        self.moving_planets()
 
        # Increase turn counter
        current_turn = self.end_turn()
        
        self.stdout.write(
            self.style.SUCCESS(f'Turn {current_turn} successfully executed!')
        )