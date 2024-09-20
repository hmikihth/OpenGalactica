from django.test import TestCase
from engine.models import Planet, Alliance, Round, AllianceInvitation

class AllianceInvitationTestCase(TestCase):
    fixtures = ["planets", "round"]

    def setUp(self):
        """Set up test data for planets, alliances, and rounds."""
        self.alliance = Alliance.objects.get(name="Test Alliance 1")
        self.planet = Planet.objects.get(name="Test Planet 1")
        self.new_planet = Planet.objects.get(name="Test Planet 2")
        self.round = Round.objects.all().order_by("number").last()

    def test_send_invitation(self):
        """Test sending an alliance invitation to a planet."""
        # Create an invitation
        invitation_message = "Join our alliance!"
        invitation = AllianceInvitation.objects.create(
            planet=self.new_planet,
            alliance=self.alliance,
            invited_by=self.planet,
            sent_turn=self.round.turn,
            message=invitation_message
        )

        # Check that the invitation is created with correct fields
        self.assertEqual(invitation.planet, self.new_planet, "Invitation should be sent to the correct planet.")
        self.assertEqual(invitation.alliance, self.alliance, "Invitation should be from the correct alliance.")
        self.assertEqual(invitation.invited_by, self.planet, "Invitation should reference the correct inviting planet.")
        self.assertEqual(invitation.sent_turn, self.round.turn, "Invitation should record the correct sent turn.")
        self.assertEqual(invitation.message, invitation_message, "Invitation should include the correct message.")

    def test_accept_invitation(self):
        """Test that a planet can accept an invitation to join the alliance."""
        # Create an invitation
        invitation = AllianceInvitation.objects.create(
            planet=self.new_planet,
            alliance=self.alliance,
            invited_by=self.planet,
            sent_turn=self.round.turn
        )

        # Accept the invitation
        invitation.accept()

        # Refresh planet from the database and check alliance assignment
        self.new_planet.refresh_from_db()
        self.assertEqual(self.new_planet.alliance, self.alliance, "Planet should be part of the alliance after accepting.")
        self.assertTrue(invitation.accepted, "Invitation should be marked as accepted.")
        self.assertEqual(invitation.accepted_turn, self.round.turn, "Accepted turn should match the current game turn.")

    def test_invitation_already_accepted(self):
        """Test that accepting an already accepted invitation does not reassign the planet."""
        # Create and accept an invitation
        invitation = AllianceInvitation.objects.create(
            planet=self.new_planet,
            alliance=self.alliance,
            invited_by=self.planet,
            sent_turn=self.round.turn
        )
        invitation.accept()

        # Try accepting again
        with self.assertRaises(ValueError, msg="Should raise an error if the invitation is already accepted."):
            invitation.accept()

    def test_reject_invitation(self):
        """Test rejecting an alliance invitation."""
        # Create an invitation
        invitation = AllianceInvitation.objects.create(
            planet=self.new_planet,
            alliance=self.alliance,
            invited_by=self.planet,
            sent_turn=self.round.turn
        )

        # Reject the invitation
        invitation.reject()

        # Ensure that the planet's alliance is not updated
        self.new_planet.refresh_from_db()
        self.assertIsNone(self.new_planet.alliance, "Planet should not have an alliance after rejecting the invitation.")
        self.assertFalse(invitation.accepted, "Invitation should not be marked as accepted.")
        self.assertIsNone(invitation.accepted_turn, "Accepted turn should remain None if the invitation is rejected.")
