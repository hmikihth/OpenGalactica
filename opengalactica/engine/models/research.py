from django.db import models

class Research(models.Model):
    name = models.CharField(max_length=128)
    research_type = models.CharField(max_length=128)
    species = models.CharField(max_length=128)
    description = models.TextField()
    metal = models.IntegerField()
    crystal = models.IntegerField()
    narion = models.IntegerField()
    development_time = models.IntegerField()  # in turns
    requirement = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='dependent_research')

    # Bonus provided by the research (e.g., better accuracy, increased production)
    bonus_type = models.CharField(max_length=64, null=True, blank=True)
    bonus_value = models.FloatField(default=0, null=True, blank=True)
    
    # Fine provided by the research (e.g., decreased accuracy, slower ships, etc)
    fine_type = models.CharField(max_length=64, null=True, blank=True)
    fine_value = models.FloatField(default=0, null=True, blank=True)

    # Mutually exclusive research group
    exclusive_group = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.name
        
    @property
    def bonus(self):
        if self.bonus_type:
            return {self.bonus_type : self.bonus_value}
        return {}

    @property
    def fine(self):
        if self.fine_type:
            return {self.fine_type : self.fine_value}
        return {}

    @property
    def points(self):
        return sum((self.metal, self.crystal, self.narion))


class PlanetResearch(models.Model):
    planet = models.ForeignKey("Planet", on_delete=models.CASCADE)
    research = models.ForeignKey(Research, on_delete=models.CASCADE)
    turns_remaining = models.IntegerField()  # How many turns are left for development
    completed = models.BooleanField(default=False)

    def start_research(self):
        """Start or continue research."""
        if not self.completed and self.turns_remaining > 0:
            self.turns_remaining -= 1
            if self.turns_remaining == 0:
                self.completed = True
            self.save()

    def can_start(self):
        """Check if research can be started by verifying if the requirements are met."""
        # Check if mutually exclusive research has been developed
        if self.research.exclusive_group:
            exclusive_research = PlanetResearch.objects.filter(
                planet=self.planet,
                research__exclusive_group=self.research.exclusive_group,
                completed=True
            ).exists()
            if exclusive_research:
                return False

        # Check other research requirements
        if self.research.requirement:
            return PlanetResearch.objects.filter(
                planet=self.planet, 
                research=self.research.requirement, 
                completed=True
            ).exists()
        return True

    def __str__(self):
        return f"{self.planet} - {self.research.name} (Turns left: {self.turns_remaining})"
       
    @property
    def bonus(self):
        """Returns with the related bonus"""
        return self.research.bonus
        
    @property
    def fine(self):
        """Returns with the related fine"""
        return self.research.fine
        
    @property
    def points(self):
        return self.research.points
