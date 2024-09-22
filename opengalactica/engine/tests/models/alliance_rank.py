from django.test import TestCase

from engine.models import AllianceRank

class RankTestCase(TestCase):
    
    def setUp(self):
        """Set up some default ranks for testing."""
        self.founder_rank = AllianceRank.objects.create(
            name="Founder Rank",
            is_founder=True,
            can_invite_members=True,
            can_remove_members=True,
            can_distribute_resources=True,
            can_manage_forum=True,
            can_set_tax=True,
            can_set_ranks=True,
            can_set_attack=True,
            can_set_defense=True,
            can_set_diplomacy=True,
            can_set_research=True,
            can_set_voting=True
        )
        self.commander_rank = AllianceRank.objects.create(
            name="Commander Rank",
            can_invite_members=True,
            can_remove_members=True,
            can_set_attack=True,
            can_set_defense=True
        )
        self.treasurer_rank = AllianceRank.objects.create(
            name="Treasurer Rank",
            can_distribute_resources=True,
            can_set_tax=True
        )
    
    def test_rank_creation(self):
        """Test if ranks are created correctly."""
        self.assertEqual(self.founder_rank.name, "Founder Rank")
        self.assertTrue(self.founder_rank.is_founder)
        self.assertTrue(self.commander_rank.can_invite_members)
        self.assertFalse(self.commander_rank.can_distribute_resources)

    def test_rank_rights(self):
        """Test rank rights and permissions."""
        # Founder should have all rights
        self.assertTrue(self.founder_rank.can_invite_members)
        self.assertTrue(self.founder_rank.can_set_diplomacy)
        self.assertTrue(self.founder_rank.can_manage_forum)

        # Commander has specific rights
        self.assertTrue(self.commander_rank.can_invite_members)
        self.assertTrue(self.commander_rank.can_set_attack)
        self.assertFalse(self.commander_rank.can_distribute_resources)

        # Treasurer can distribute resources but can't invite members
        self.assertTrue(self.treasurer_rank.can_distribute_resources)
        self.assertFalse(self.treasurer_rank.can_invite_members)

    def test_str_method(self):
        """Test the string representation of the rank."""
        self.assertEqual(str(self.founder_rank), "Founder Rank")
        self.assertEqual(str(self.commander_rank), "Commander Rank")

    def test_rank_default_permissions(self):
        """Test that default permissions are set to False for a new rank."""
        new_rank = AllianceRank.objects.create(name="New Rank")
        self.assertFalse(new_rank.can_invite_members)
        self.assertFalse(new_rank.can_set_attack)
        self.assertFalse(new_rank.can_manage_forum)
        
        
