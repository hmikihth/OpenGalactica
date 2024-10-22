from engine.models import Planet

class Resources:
    def run(self):
        for planet in Planet.objects.all():
            planet.generate_resources()
