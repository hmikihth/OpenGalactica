from django.core.exceptions import PermissionDenied
from engine.models import Planet, Alliance, AllianceRank, AllianceMember, AllianceInvitation, Round
from django.test import TestCase

class AllianceMemberTestCase(TestCase):
    fixtures = ['planets', 'ranks', 'round']

    def setUp(self):
        self.alliance = Alliance.objects.get(name="Test Alliance 1")
        self.member1 = Planet.objects.get(name="Test Planet 1")
        self.member2 = Planet.objects.get(name="Test Planet 2")
        self.rank_commander = AllianceRank.objects.get(name="Commander")
        self.rank_treasurer = AllianceRank.objects.get(name="Treasurer")
        self.member1.rank=self.rank_commander
        self.member2.rank=self.rank_treasurer
        self.member1.alliance=self.alliance
        self.member2.alliance=self.alliance
        self.member1.save()
        self.member2.save()
        self.round = Round.objects.all().order_by("number").last()
        
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
        self.assertEqual(Alliance.objects.count(), 0, "Alliance should be deleted.")

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

    # Additional tests for attack, defense, diplomacy, research, and voting can follow the same pattern.
    