from django.core.exceptions import PermissionDenied
from engine.models import Planet, Alliance, AllianceRank, AllianceMember, AllianceInvitation, Round
from engine.models import Attack, AttackTarget, AttackSubscription, Defense, DefenseTarget, Diplomacy 
from engine.models import Research, AllianceResearch
from django.test import TestCase

class AllianceMemberTestCase(TestCase):
    fixtures = ['planets', 'ranks', 'round']

    def setUp(self):
        self.alliance = Alliance.objects.get(name="Test Alliance 1")
        self.target_alliance = Alliance.objects.get(name="Test Alliance 2")
        self.member1 = Planet.objects.get(name="Test Planet 1")
        self.member2 = Planet.objects.get(name="Test Planet 2")
        self.target= Planet.objects.get(name="Test Planet 3")
        self.rank_commander = AllianceRank.objects.get(name="Commander")
        self.rank_treasurer = AllianceRank.objects.get(name="Treasurer")
        self.member1.rank=self.rank_commander
        self.member2.rank=self.rank_treasurer
        self.member1.alliance=self.alliance
        self.member2.alliance=self.alliance
        self.member1.save()
        self.member2.save()
        self.round = Round.objects.all().order_by("number").last()
        self.research = Research.objects.create(
            name="Hyperdrive", 
            species="alliance", 
            metal = 11,
            crystal = 12,
            narion = 13,
            development_time = 14
        )

        
    def test_invite_member_success(self):
        """Test that an alliance member with invite permissions can send an invitation."""
        new_planet = Planet.objects.create(name="New Planet 1")
        self.member1.invite_member(new_planet)
        invitation = AllianceInvitation.objects.get(planet=new_planet, alliance=self.alliance)

        self.assertIsNotNone(invitation)
        self.assertEqual(invitation.invited_by, self.member1)
        self.assertEqual(invitation.alliance, self.alliance)
        self.assertEqual(invitation.sent_turn, self.round.turn)

    def test_invite_member_no_permission(self):
        new_planet = Planet.objects.create(name="New Planet 2")
        self.member2.rank.can_invite_members = False
        with self.assertRaises(PermissionDenied):
            self.member2.invite_member(new_planet)

    def test_remove_member(self):
        self.member1.remove_member(self.member2)
        self.member2.refresh_from_db()
        self.assertIsNone(self.member2.alliance, "Removed member should have no alliance.")
        self.assertIsNone(self.member2.rank, "Removed member should have no rank.")

    def test_leave_alliance(self):
        self.member2.leave_alliance()
        self.member2.refresh_from_db()
        self.assertIsNone(self.member2.alliance, "Leaving member should have no alliance.")
        self.assertIsNone(self.member2.rank, "Leaving member should have no rank.")

    def test_remove_member_no_permission(self):
        self.member2.rank.can_remove_members = False
        with self.assertRaises(PermissionDenied):
            self.member2.remove_member(self.member1)

    def test_distribute_resources(self):
        self.alliance.metal = 1000
        self.alliance.crystal = 1000
        self.alliance.narion = 1000
        self.alliance.credit = 500
        self.alliance.save()

        self.member1.metal = 0
        self.member1.crystal = 0
        self.member1.narion = 0
        self.member1.credit = 0
        self.member1.save()
        
        self.member2.distribute_resources(self.member1, 100, 50, 25, 10)
        
        self.member1.refresh_from_db()

        self.assertEqual(self.member1.metal, 100, "Metal should be added to member1's planet.")
        self.assertEqual(self.alliance.metal, 900, "Metal should be deducted from alliance.")

        self.assertEqual(self.member1.crystal, 50, "Crystal should be added to member1's planet.")
        self.assertEqual(self.alliance.crystal, 950, "Crystal should be deducted from alliance.")

        self.assertEqual(self.member1.narion, 25, "Narion should be added to member1's planet.")
        self.assertEqual(self.alliance.narion, 975, "Narion should be deducted from alliance.")

        self.assertEqual(self.member1.credit, 10, "Credit should be added to member1's planet.")
        self.assertEqual(self.alliance.credit, 490, "Credit should be deducted from alliance.")


    def test_distribute_resources_no_permission(self):
        self.member1.rank.can_distribute_resources = False
        with self.assertRaises(PermissionDenied):
            self.member1.distribute_resources(self.member2, 100, 50, 25, 10)

    def test_rename_alliance(self):
        self.member1.rank.is_founder = True
        self.member1.rename_alliance("New Alliance Name", "NA123")
        self.alliance.refresh_from_db()
        self.assertEqual(self.alliance.name, "New Alliance Name", "Alliance name should be updated.")

    def test_rename_alliance_no_permission(self):
        self.member2.rank.is_founder = False
        with self.assertRaises(PermissionDenied):
            self.member2.rename_alliance("Invalid Rename", "IR123")

    def test_delete_alliance(self):
        self.member1.rank.is_founder = True
        self.member1.delete_alliance()
        self.alliance = Alliance.objects.filter(name="Test Alliance 1").first()
        self.assertEqual(self.alliance, None, "Alliance should be deleted.")

        self.member1.refresh_from_db()
        self.member2.refresh_from_db()
        self.assertEqual(self.member1.alliance, None, "Member1's alliance must be None")
        self.assertEqual(self.member2.alliance, None, "Member2's alliance must be None")
        

    def test_delete_alliance_no_permission(self):
        with self.assertRaises(PermissionDenied):
            self.member2.delete_alliance()

    def test_set_rank(self):
        self.member1.set_rank(self.member2, self.rank_commander)
        self.member2.refresh_from_db()
        self.assertEqual(self.member2.rank, self.rank_commander, "Member's rank should be updated.")

    def test_set_rank_no_permission(self):
        self.member2.rank.can_set_ranks = False
        with self.assertRaises(PermissionDenied):
            self.member2.set_rank(self.member1, self.rank_treasurer)
            
    def test_set_news(self):
        """Test that an alliance member with permission can set news."""
        self.member1.rank.can_set_news = True
        self.member1.alliance.set_news = lambda content: setattr(self.alliance, 'news', content)  # Mock method

        self.member1.set_news("New alliance announcement")
        self.assertEqual(self.alliance.news, "New alliance announcement", "Alliance news should be updated.")

    def test_set_news_no_permission(self):
        """Test that an alliance member without permission cannot set news."""
        self.member2.rank.can_set_news = False
        with self.assertRaises(PermissionDenied):
            self.member2.set_news("Unauthorized news update")

    def test_set_attack(self):
        self.member1.rank.can_set_attack = True
        
        response = self.member1.set_attack(target=self.target, start_turn=10, short_description="Surprise attack", description="A large-scale surprise attack on enemy planets.")
        self.assertTrue(response, "The set_attack method must to return True")
        
        attacks = Attack.objects.filter(organizer=self.member1).count()
        self.assertEqual(attacks, 1, "The set_attack method must create exactly one Attack object")

    def test_set_attack_no_permission(self):
        self.member2.rank.can_set_attack = False
        with self.assertRaises(PermissionDenied):
            self.member2.set_attack(target=self.target, start_turn=10, short_description="Surprise attack", description="A large-scale surprise attack on enemy planets.")

    def test_add_attack_target(self):
        self.member1.rank.can_set_attack = True
        attack = self.member1.set_attack(
            target=self.target,
            start_turn=10,
            short_description="Surprise attack",
            description="A large-scale surprise attack on enemy planets."
        )
        
        attack_instance = Attack.objects.get(organizer=self.member1)
        attack_instance.add_target(self.target, "Primary objective")
        
        attack_targets = AttackTarget.objects.filter(attack=attack_instance)
        self.assertEqual(attack_targets.count(), 1, "The add_target method must create exactly one AttackTarget object")
        self.assertEqual(attack_targets.first().description, "Primary objective", "The AttackTarget description must match the input description")
    
    def test_subscribe_to_attack(self):
        self.member1.rank.can_set_attack = True
        attack = self.member1.set_attack(
            target=self.target,
            start_turn=10,
            short_description="Surprise attack",
            description="A large-scale surprise attack on enemy planets."
        )
        
        attack_instance = Attack.objects.get(organizer=self.member1)
        attack_target = AttackTarget.objects.create(attack=attack_instance, target=self.target, description="Primary objective")
        attack_target.subscribe(self.member2, "Joining the attack")
        
        subscriptions = AttackSubscription.objects.filter(attack_target=attack_target)
        self.assertEqual(subscriptions.count(), 1, "The subscribe method must create exactly one AttackSubscription object")
        self.assertEqual(subscriptions.first().note, "Joining the attack", "The AttackSubscription note must match the input note")


    def test_set_defense(self):
        self.member1.rank.can_set_defense = True
        
        response = self.member1.set_defense(
            target=self.target,
            arrival_turn=12,
            short_description="Defense initiative",
            description="Mobilizing fleets for planetary defense."
        )
        self.assertTrue(response, "The set_defense method must return True")
        
        defenses = Defense.objects.filter(organizer=self.member1).count()
        self.assertEqual(defenses, 1, "The set_defense method must create exactly one Defense object")

    def test_set_defense_no_permission(self):
        self.member2.rank.can_set_defense = False
        with self.assertRaises(PermissionDenied):
            self.member2.set_defense(
                target=self.target,
                arrival_turn=12,
                short_description="Defense initiative",
                description="Mobilizing fleets for planetary defense."
            )

    def test_add_defense_target(self):
        self.member1.rank.can_set_defense = True
        defense = self.member1.set_defense(
            target=self.target,
            arrival_turn=12,
            short_description="Defense initiative",
            description="Mobilizing fleets for planetary defense."
        )
        
        defense_instance = Defense.objects.get(organizer=self.member1)
        defense_instance.add_target(self.target, "Protecting key installations")
        
        defense_targets = DefenseTarget.objects.filter(defense=defense_instance)
        self.assertEqual(defense_targets.count(), 1, "The add_target method must create exactly one DefenseTarget object")
        self.assertEqual(defense_targets.first().description, "Protecting key installations", "The DefenseTarget description must match the input description")

    def test_set_diplomacy(self):
        self.member1.rank.can_set_diplomacy = True

        response = self.member1.set_diplomacy(
            alliance=self.target_alliance,
            diplo_type="Neutral",
            expiration=150,
            termination=20,
            description="Temporary neutrality pact."
        )
        self.assertTrue(response, "The set_diplomacy method must return True")

        diplomacies = Diplomacy.objects.filter(sender=self.member1.alliance, receiver=self.target_alliance)
        self.assertEqual(diplomacies.count(), 1, "The set_diplomacy method must create exactly one Diplomacy object")
        self.assertFalse(diplomacies.first().accepted, "Diplomacy must not be accepted by default")

    def test_set_diplomacy_no_permission(self):
        self.member2.rank.can_set_diplomacy = False
        with self.assertRaises(PermissionDenied):
            self.member2.set_diplomacy(
                alliance=self.target_alliance,
                diplo_type="Ally",
                expiration=150,
                termination=20,
                description="Strategic alliance."
            )

    def test_accept_diplomacy(self):
        diplomacy = Diplomacy.objects.create(
            sender=self.target_alliance,
            receiver=self.member1.alliance,
            diplo_type="Trade",
            expiration=120,
            termination=15,
            description="Trade agreement"
        )

        self.assertFalse(diplomacy.accepted, "Diplomacy should not be accepted by default")

        self.member1.rank.can_set_diplomacy = True
        response = self.member1.accept_diplomacy(diplomacy)

        self.assertTrue(response, "The accept_diplomacy method must return True")
        self.assertTrue(diplomacy.accepted, "Diplomacy should be accepted after calling accept_diplomacy")

    def test_accept_diplomacy_no_permission(self):
        diplomacy = Diplomacy.objects.create(
            sender=self.target_alliance,
            receiver=self.member2.alliance,
            diplo_type="War",
            expiration=180,
            termination=30
        )

        self.member2.rank.can_set_diplomacy = False
        with self.assertRaises(PermissionDenied):
            self.member2.accept_diplomacy(diplomacy)

    def test_accept_diplomacy_wrong_receiver(self):
        diplomacy = Diplomacy.objects.create(
            sender=self.member1.alliance,
            receiver=self.target_alliance,
            diplo_type="Non-Aggression Pact",
            expiration=200,
            termination=25
        )

        self.member1.rank.can_set_diplomacy = True
        with self.assertRaises(ValueError):
            self.member1.accept_diplomacy(diplomacy)  # The receiver is the target_alliance, not member1's alliance


    def test_set_research(self):
        self.member1.rank.can_set_research = True
        response = self.member1.set_research(self.research)
        
        self.assertTrue(response, "The set_research method must to return True")
        
        n = AllianceResearch.objects.filter(alliance=self.alliance, research=self.research).count()
        self.assertEqual(n, 1, "The set create method must create exactly one AllianceResearch object")

    def test_set_research_no_permission(self):
        self.member2.rank.can_set_research = False
        with self.assertRaises(PermissionDenied):
            self.member2.set_research(self.research)

    def test_set_tax(self):
        self.member1.rank.can_set_tax = True
        self.member1.alliance.set_tax = lambda tax: setattr(self.alliance, 'tax_rate', tax)  # Mock method
        
        self.member1.set_tax(15)
        self.assertEqual(self.alliance.tax, 15, "Alliance tax rate should be updated.")
        self.assertEqual(self.alliance.tax_rate, 0.15, "Alliance tax rate should be updated.")

    def test_set_tax_no_permission(self):
        self.member2.rank.can_set_tax = False
        with self.assertRaises(PermissionDenied):
            self.member2.set_tax(20)

    def test_set_rank(self):
        self.member1.rank.can_set_ranks = True
        self.member1.set_rank(self.member2, self.rank_commander)
        self.member2.refresh_from_db()
        self.assertEqual(self.member2.rank, self.rank_commander, "Member's rank should be updated.")

    def test_set_rank_no_permission(self):
        self.member2.rank.can_set_ranks = False
        with self.assertRaises(PermissionDenied):
            self.member2.set_rank(self.member1, self.rank_treasurer)

    