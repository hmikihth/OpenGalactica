from django.core.exceptions import PermissionDenied
from .alliance_invitation import AllianceInvitation
from .alliance_voting import AllianceVoting
from .round import Round
from .attack import Attack
from .defense import Defense
from .diplomacy import Diplomacy

class AllianceMember:
    """ A parent class of the Planet model. Implements alliance membership methods"""
    def invite_member(self, new_planet):
        if not self.rank.can_invite_members:
            raise PermissionDenied(f"{self.name} does not have permission to invite members.")
        
        # Get the current game turn
        current_turn = Round.objects.all().order_by("number").last().turn
        
        # Logic to send an invitation to the planet
        if AllianceInvitation.objects.filter(planet=new_planet, alliance=self.alliance).exists():
            raise ValueError(f"{new_planet.name} already has an invitation from this alliance.")
        
        AllianceInvitation.objects.create(
            planet=new_planet, 
            alliance=self.alliance, 
            invited_by=self,
            sent_turn=current_turn
        )

    def remove_member(self, target_member):
        if not self.rank.can_remove_members:
            raise PermissionDenied(f"{self.name} does not have permission to remove members.")
        target_member.alliance = None
        target_member.rank = None
        target_member.save()

    def set_new_founder(self):
        self.alliance.set_new_founder()

    def leave_alliance(self):
        old_alliance = None
        if self.rank.is_founder and self.alliance.founder == self:
            old_alliance = self.alliance
        self.alliance = None
        self.rank = None
        self.save()
        if old_alliance:
            old_alliance.founder = old_alliance.set_new_founder()
            old_alliance.save()

    def distribute_resources(self, target_member, metal, crystal, narion, credits):
        if not self.rank.can_distribute_resources:
            raise PermissionDenied(f"{self.name} does not have permission to distribute resources.")
        
        if self.alliance.metal < metal or self.alliance.crystal < crystal or self.alliance.narion < narion or self.alliance.credit < credits:
            raise ValueError("Not enough resources in the alliance treasury.")
        
        self.alliance.metal -= metal
        self.alliance.crystal -= crystal
        self.alliance.narion -= narion
        self.alliance.credit -= credits
        self.alliance.save()

        target_member.metal += metal
        target_member.crystal += crystal
        target_member.narion += narion
        target_member.credit += credits
        target_member.save()

    def manage_forum(self, related_post, action, value):
        if not self.rank.can_manage_forum:
            raise PermissionDenied(f"{self.name} does not have permission to manage the forum.")
        # Logic for managing the forum, such as editing or deleting posts

    def set_tax(self, new_tax_rate):
        if not self.rank.can_set_tax:
            raise PermissionDenied(f"{self.name} does not have permission to set the tax rate.")
        self.alliance.tax = new_tax_rate
        self.alliance.save()
        
    def rename_alliance(self, name, identifier):
        if not self.rank.is_founder:
            raise PermissionDenied(f"{self.name} is not allowed to rename the alliance.")
        self.alliance.name = name
        self.alliance.identifier = identifier
        self.alliance.save()
        
    def delete_alliance(self):
        if not self.rank.is_founder:
            raise PermissionDenied(f"{self.name} is not allowed to delete the alliance.")
        self.alliance.members.update(alliance=None)
        self.alliance.delete()
        return True

    def set_rank(self, member, rank):
        if not self.rank.can_set_ranks:
            raise PermissionDenied(f"{self.name} does not have permission to set ranks.")
        member.rank = rank
        member.save()
        return True

    def set_attack(self, target, start_turn, short_description, description):
        if not self.rank.can_set_attack:
            raise PermissionDenied(f"{self.name} does not have permission to set an attack.")
        Attack.objects.create(  organizer=self, alliance=self.alliance, start=start_turn, 
                                short_description=short_description, description=description)
        return True
    
    def set_defense(self, target, arrival_turn, short_description, description):
        if not self.rank.can_set_defense:
            raise PermissionDenied(f"{self.name} does not have permission to set defense.")
        Defense.objects.create(  organizer=self, alliance=self.alliance, arrival=arrival_turn, 
                                short_description=short_description, description=description)
        return True

    def set_diplomacy(self, alliance, diplo_type, expiration, termination, description=""):
        """Creates a new Diplomacy agreement if the member has the necessary permission."""
        if not self.rank.can_set_diplomacy:
            raise PermissionDenied(f"{self.name} does not have permission to set diplomacy.")

        # Ensure a diplomacy agreement of the same type does not already exist
        existing_diplomacy = Diplomacy.objects.filter(sender=self.alliance, receiver=alliance, diplo_type=diplo_type)
        if existing_diplomacy.exists():
            raise ValueError(f"A diplomacy of type '{diplo_type}' already exists between these alliances.")

        Diplomacy.objects.create(
            sender=self.alliance,
            receiver=alliance,
            diplo_type=diplo_type,
            expiration=expiration,
            termination=termination,
            description=description
        )
        return True

    def accept_diplomacy(self, diplomacy):
        """Allows a member to accept a diplomacy agreement if they have permission."""
        if not self.rank.can_set_diplomacy:
            raise PermissionDenied(f"{self.name} does not have permission to accept diplomacy.")

        if diplomacy.receiver != self.alliance:
            raise ValueError(f"This diplomacy is not directed at {self.alliance.name}.")

        diplomacy.accept()
        return True
    
    def set_research(self, research):
        if not self.rank.can_set_research:
            raise PermissionDenied(f"{self.name} does not have permission to set research.")
        # Logic for setting alliance-wide research
        return True

    def set_voting(self, title, description, end, public):
        if not self.rank.can_set_voting:
            raise PermissionDenied(f"{self.name} does not have permission to set voting.")
        return AllianceVoting.objects.create(title=title, description=description, end=end, public=public)

    def set_news(self, content):
        if not self.rank.can_set_news:
            raise PermissionDenied(f"{self.name} does not have permission to set alliance news.")
        else:
            self.alliance.set_news(content)
        return True
