from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from engine.models import Alliance, Planet, Round
from engine.models import AllianceVoting, AllianceVotingChoice, AllianceVote

class AllianceVotingTestCase(TestCase):
    def setUp(self):
        self.round = Round.objects.create()
        self.alliance = Alliance.objects.create(name="Galactic Federation")
        self.planet1 = Planet.objects.create(name="Earth", alliance=self.alliance)
        self.planet2 = Planet.objects.create(name="Mars", alliance=self.alliance)
        
        self.voting = AllianceVoting.objects.create(
            alliance=self.alliance,
            title="New Leader Election",
            description="Choose the next leader.",
            public=True,
            end=50
        )

        self.choice1 = AllianceVotingChoice.objects.create(voting=self.voting, label="Candidate A")
        self.choice2 = AllianceVotingChoice.objects.create(voting=self.voting, label="Candidate B")

    def test_create_voting(self):
        voting = AllianceVoting.objects.create(
            alliance=self.alliance,
            title="War Declaration",
            description="Should we declare war on the neighboring faction?",
            public=False,
            end=60
        )
        self.assertEqual(voting.title, "War Declaration")
        self.assertFalse(voting.public)
        self.assertEqual(voting.end, 60)

    def test_create_voting_choice(self):
        choice = AllianceVotingChoice.objects.create(voting=self.voting, label="Candidate C")
        self.assertEqual(choice.label, "Candidate C")
        self.assertEqual(choice.voting, self.voting)

    def test_member_can_vote(self):
        vote = AllianceVote.objects.create(voting=self.voting, member=self.planet1, choice=self.choice1, note="Best choice")
        self.assertEqual(vote.voting, self.voting)
        self.assertEqual(vote.member, self.planet1)
        self.assertEqual(vote.choice, self.choice1)
        self.assertEqual(vote.note, "Best choice")

    def test_member_cannot_vote_twice(self):
        AllianceVote.objects.create(voting=self.voting, member=self.planet1, choice=self.choice1)

        with self.assertRaises(IntegrityError):
            AllianceVote.objects.create(voting=self.voting, member=self.planet1, choice=self.choice2)

    def test_voting_ends_prevents_votes(self):
        self.round.turn = 50
        self.round.save()
        self.voting.end = 10
        self.voting.save()

        with self.assertRaises(ValidationError):
            AllianceVote.objects.create(voting=self.voting, member=self.planet2, choice=self.choice2)

    def test_voting_choice_str(self):
        self.assertEqual(str(self.choice1), "Candidate A (Voting: New Leader Election)")

    def test_voting_str(self):
        self.assertEqual(str(self.voting), "New Leader Election (Galactic Federation)")

    def test_vote_str(self):
        vote = AllianceVote.objects.create(voting=self.voting, member=self.planet1, choice=self.choice1)
        self.assertEqual(str(vote), "Earth voted for Candidate A in New Leader Election")
