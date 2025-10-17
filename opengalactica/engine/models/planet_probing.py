from django.core.exceptions import ObjectDoesNotExist

def planet_report(planet):
    return {
        "report_name": "Planet Probe Report",
        "name": planet.name,
        "coordinates": planet.coordinates,
        "points": planet.points,
        "plasmators": {
            "metal": planet.metal_plasmator,
            "crystal": planet.crystal_plasmator,
            "narion": planet.narion_plasmator,
            "neutral": planet.neutral_plasmator,
        },
        "resources": {
            "metal": planet.metal,
            "crystal": planet.crystal,
            "narion": planet.narion,
        },
        "production_capacity": {
            "metal": planet.gross_metal_production,
            "crystal": planet.gross_crystal_production,
            "narion": planet.gross_narion_production,
        },
        "developments": planet.development_count,
        "constructions": planet.construction_count,
        "ships": planet.n_ships,
        "pds": planet.n_pds,
    }

def ship_report(planet):
    ships = {}
    for fleet in planet.fleets:
        for s in fleet.ships:
            if s.ship_model.id not in ships and s.quantity > 0:
                ships[s.ship_model.id] = {"quantity":0}
            ships[s.ship_model.id]["name"] = s.ship_model.name
            ships[s.ship_model.id]["ship_class"] = s.ship_model.ship_class
            ships[s.ship_model.id]["quantity"] += s.quantity
    return {
        "report_name": "Ship Probe Report",
        "name": planet.name,
        "coordinates": planet.coordinates,
        "ships": ships
    }

def defense_report(planet):
    ships = {}
    for s in planet.base.pds:
        if s.ship_model.id not in ships and s.quantity > 0:
            ships[s.ship_model.id] = {"quantity":0}
        ships[s.ship_model.id]["name"] = s.ship_model.name
        ships[s.ship_model.id]["ship_class"] = s.ship_model.ship_class
        ships[s.ship_model.id]["quantity"] += s.quantity
    return {
        "report_name": "Defense Probe Report",
        "name": planet.name,
        "coordinates": planet.coordinates,
        "ships": ships
    }

def military_report(planet):
    ships = {}
    fleets = []
    for i, fleet in enumerate(planet.fleets):
        status = "At home"
        if fleet.task != "stand":
            if fleet.role == "Defenders":
                status = "Defend"
            else: 
                status = "Attack" 
            if fleet.task == "return":
                status = "Return From " + status
        fleets.append({
            "name": fleet.name,
            "formation": fleet.formation,
            "target": f"{fleet.target.name} ({fleet.target.coordinates})" if fleet.target else None,
            "distance": fleet.distance,
            "turns": fleet.turns,
            "status": status
        })
        for s in fleet.ships:
            if s.ship_model.id not in ships and s.quantity > 0:
                ships[s.ship_model.id] = {"quantity":[0,0,0,0,0]}
            ships[s.ship_model.id]["name"] = s.ship_model.name
            ships[s.ship_model.id]["ship_class"] = s.ship_model.ship_class
            ships[s.ship_model.id]["quantity"][i] += s.quantity
    return {
        "report_name": "Military Probe Report",
        "name": planet.name,
        "coordinates": planet.coordinates,
        "ships": ships,
        "fleets":fleets,
    }


def information_report(planet):
    from engine.models import Notification
    notification_objects = (
        Notification.objects
        .filter(planet=planet)
        .order_by('-round', '-turn', '-server_time')[:100]
    )
    
    notifications = []
    for o in notification_objects:
        notification = {
            "timestamp": f"{o.round}:{o.turn}:{o.server_time.minute}",
            "ntype": o.ntype,
            "content": o.content,
        }
        notifications.append(notification)

    return {
        "report_name": "Information Probe Report",
        "name": planet.name,
        "coordinates": planet.coordinates,
        "notifications": notifications,
    }


class PlanetProbing:
    def probing(self, sender=None, probe=None, quantity=0):
        if quantity <= 0:
            raise ValueError("The quantity of probes must be larger than 0")
        if not probe:
            raise ValueError("You must select a probe type")
        if not sender:
            raise ValueError("You must set a sender")

        from engine.models import StockedSatellite

        # Load probes
        try:
            stocked = StockedSatellite.objects.get(planet=sender, satellite_type=probe)
        except ObjectDoesNotExist:
            raise ValueError("You don't have enough probes")

        if stocked.quantity < quantity:
            raise ValueError("You don't have enough probes")

        # Handle required rockets
        if probe.requires_rocket:
            try:
                rockets = StockedSatellite.objects.get(planet=sender, satellite_type__code="rocket")
            except ObjectDoesNotExist:
                raise ValueError("You don't have enough rockets")

            total_rockets_needed = quantity * probe.rocket_required_count
            if rockets.quantity < total_rockets_needed:
                raise ValueError("You don't have enough rockets")

            rockets.quantity -= total_rockets_needed
            rockets.save()

        # Handle interceptors
        leftover = quantity
        try:
            interceptors = StockedSatellite.objects.get(planet=self, satellite_type__code="interceptor")
            destroyed = min(interceptors.quantity, quantity)
            interceptors.quantity -= destroyed
            interceptors.save()
            leftover = quantity - destroyed
        except ObjectDoesNotExist:
            pass

        stocked.quantity -= quantity
        stocked.save()        

        if leftover < 1:
            raise ValueError("Probing was not successful")

        if probe.code == "planet":
            data = planet_report(self)
        elif probe.code == "ship":
            data = ship_report(self)
        elif probe.code == "defense":
            data = defense_report(self)
        elif probe.code == "military":
            data = military_report(self)
        elif probe.code == "information":
            data = information_report(self)
        else:
            data = {"message": "Unknown probe type"}

        return data


    def plasmator_probing(self, quantity=0):
        if not(0 < quantity < 100):
            raise ValueError("The quantity of probes must be greater than 0 and less than 100.")

        from engine.models import StockedSatellite
        plasmator_probes = StockedSatellite.objects.get(planet=self, satellite_type__code="plasmator")

        if quantity > plasmator_probes.quantity:
            raise ValueError("You don't have enough plasmator probes to execute.")

        required_rockets = plasmator_probes.satellite_type.rocket_required_count * quantity
        rockets = StockedSatellite.objects.get(planet=self, satellite_type__code="rocket")

        if required_rockets > rockets.quantity:
            raise ValueError("You don't have enough rockets to execute.")

        import math 

        efficiency = max(0.01, math.exp(-self.plasmators / 100))
        new_plasmators = math.floor((1+quantity) * efficiency)
        
        plasmator_probes.quantity -= quantity
        plasmator_probes.save()

        rockets.quantity -= required_rockets
        rockets.save()

        self.neutral_plasmator += new_plasmators
        self.save()
        
        return new_plasmators

