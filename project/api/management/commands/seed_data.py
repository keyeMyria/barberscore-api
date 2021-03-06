
# Django
from django.core.management.base import BaseCommand

# First-Party
from api.factories import AppearanceFactory
from api.factories import AssignmentFactory
from api.factories import AwardFactory
from api.factories import ChartFactory
from api.factories import CompetitorFactory
from api.factories import ContestantFactory
from api.factories import ContestFactory
from api.factories import ConventionFactory
from api.factories import EntryFactory
from api.factories import GrantorFactory
from api.factories import GroupFactory
from api.factories import MemberFactory
from api.factories import OfficeFactory
from api.factories import OfficerFactory
from api.factories import PanelistFactory
from api.factories import PersonFactory
from api.factories import RepertoryFactory
from api.factories import RoundFactory
from api.factories import ScoreFactory
from api.factories import SessionFactory
from api.factories import SongFactory
from api.factories import UserFactory
from api.factories import VenueFactory
from api.models import Appearance
from api.models import Assignment
from api.models import Award
from api.models import Chart
from api.models import Competitor
from api.models import Contest
from api.models import Contestant
from api.models import Convention
from api.models import Entry
from api.models import Grantor
from api.models import Group
from api.models import Member
from api.models import Office
from api.models import Officer
from api.models import Panelist
from api.models import Person
from api.models import Repertory
from api.models import Round
from api.models import Score
from api.models import Session
from api.models import Song
from api.models import User
from api.models import Venue


class Command(BaseCommand):
    help = "Command to sync database with BHS ."

    def add_arguments(self, parser):
        parser.add_argument(
            '-b',
            dest='breakpoint',
            nargs='?',
            default=None,
            help='Seed breakpoint',
        )

    def handle(self, *args, **options):
        # Create Persons
        admin_person = PersonFactory(
            first_name='Admin',
            last_name='Person',
            email='admin@barberscore.com',
        )
        scjc_person = PersonFactory(
            first_name='SCJC',
            last_name='Person',
            email='scjc@barberscore.com',
        )
        drcj_person = PersonFactory(
            first_name='DRCJ',
            last_name='Person',
            email='drcj@barberscore.com',
        )
        ca_person = PersonFactory(
            first_name='CA',
            last_name='Person',
            email='ca@barberscore.com',
        )
        quartet_lead_person = PersonFactory(
            first_name='Quartet',
            last_name='Lead',
            email='quartet_lead@barberscore.com',
        )
        quartet_tenor_person = PersonFactory(
            first_name='Quartet',
            last_name='Tenor',
        )
        quartet_baritone_person = PersonFactory(
            first_name='Quartet',
            last_name='Baritone',
        )
        quartet_bass_person = PersonFactory(
            first_name='Quartet',
            last_name='Bass',
        )
        chorus_manager_person = PersonFactory(
            first_name='Chorus',
            last_name='Admin',
            email='chorus_manager@barberscore.com',
        )
        music_judge_person = PersonFactory(
            first_name='Music',
            last_name='Judge',
            email='music_judge@barberscore.com',
        )
        performance_judge_person = PersonFactory(
            first_name='Performance',
            last_name='Judge',
            email='performance_judge@barberscore.com',
        )
        singing_judge_person = PersonFactory(
            first_name='Singing',
            last_name='Judge',
            email='singing_judge@barberscore.com',
        )
        # Create Users
        admin_user = UserFactory(
            username='admin',
            password='password',
            person=admin_person,
            is_staff=True,
        )
        scjc_user = UserFactory(
            username='auth0|5b180b77157859716f2ca0a4',
            password='password',
            person=scjc_person,
        )
        drcj_user = UserFactory(
            username='auth0|5b16f0b1157859716f2c6a9b',
            password='password',
            person=drcj_person,
        )
        ca_user = UserFactory(
            username='auth0|5b180b8e55f2302168ff06cc',
            password='password',
            person=ca_person,
        )
        quartet_lead_user = UserFactory(
            username='auth0|5b180b8e55f2302168ff06cd',
            password='password',
            person=quartet_lead_person,
        )
        chorus_manager_user = UserFactory(
            username='auth0|5b180b8f55f2302168ff06d0',
            password='password',
            person=chorus_manager_person,
        )
        music_judge_user = UserFactory(
            username='auth0|5b180b8f55f2302168ff06d2',
            password='password',
            person=music_judge_person,
        )
        performance_judge_user = UserFactory(
            username='auth0|5b180b90157859716f2ca0b4',
            password='password',
            person=performance_judge_person,
        )
        singing_judge_user = UserFactory(
            username='auth0|5b180b90a76b702169249b9d',
            password='password',
            person=singing_judge_person,
        )
        # Create Groups
        international = GroupFactory(
            name='International Group',
            code='INT',
            kind=Group.KIND.international,
        )
        district_alpha = GroupFactory(
            name='District Alpha',
            code='ALF',
            parent=international,
            kind=Group.KIND.district,
        )
        chapter_1 = GroupFactory(
            name='Chapter One',
            code='A-001',
            parent=district_alpha,
            kind=Group.KIND.chapter,
        )
        chorus_1 = GroupFactory(
            name='Chorus One',
            kind=Group.KIND.chorus,
            parent=chapter_1,
            bhs_id=40,
            international=international.code,
            district=district_alpha.code,
            chapter=chapter_1.name,
        )
        quartet_1 = GroupFactory(
            name='Quartet 1',
            kind=Group.KIND.quartet,
            parent=district_alpha,
            bhs_id=10,
            international=international.code,
            district=district_alpha.code,
        )
        quartet_2 = GroupFactory(
            name='Quartet 2',
            kind=Group.KIND.quartet,
            bhs_id=20,
            parent=district_alpha,
            international=international.code,
            district=district_alpha.code,
        )
        quartet_3 = GroupFactory(
            name='Quartet 3',
            kind=Group.KIND.quartet,
            bhs_id=30,
            parent=district_alpha,
            international=international.code,
            district=district_alpha.code,
        )
        # Sort tree
        Group.objects.sort_tree()

        # create Venue
        venue = VenueFactory()

        # create Chart
        chart_1 = ChartFactory(
            title='Chart 1',
        )
        chart_2 = ChartFactory(
            title='Chart 2',
        )
        chart_3 = ChartFactory(
            title='Chart 3',
        )
        chart_4 = ChartFactory(
            title='Chart 4',
        )
        chart_5 = ChartFactory(
            title='Chart 5',
        )
        chart_6 = ChartFactory(
            title='Chart 6',
        )

        # Create Offices
        scjc_office = OfficeFactory(
            name='Society Chairman of C&J',
            kind=Office.KIND.international,
            code=Office.CODE.scjc_chair,
            is_convention_manager=True,
            is_session_manager=True,
            is_round_manager=True,
            is_scoring_manager=True,
            is_group_manager=True,
            is_person_manager=True,
            is_award_manager=True,
            is_officer_manager=True,
            is_chart_manager=True,
            is_assignment_manager=True,
        )
        drcj_office = OfficeFactory(
            name='District Director C&J',
            kind=Office.KIND.district,
            code=Office.CODE.drcj,
            is_convention_manager=True,
            is_session_manager=True,
            is_award_manager=True,
        )
        ca_office = OfficeFactory(
            name='Contest Administrator',
            kind=Office.KIND.district,
            code=Office.CODE.judge_ca,
            is_round_manager=True,
            is_scoring_manager=True,
            is_officer_manager=True,
        )
        mus_office = OfficeFactory(
            name='Music Judge',
            kind=Office.KIND.district,
            code=Office.CODE.judge_mus,
            is_officer_manager=True,
        )
        per_office = OfficeFactory(
            name='Performance Judge',
            kind=Office.KIND.district,
            code=Office.CODE.judge_per,
            is_officer_manager=True,
        )
        sng_office = OfficeFactory(
            name='Singing Judge',
            kind=Office.KIND.district,
            code=Office.CODE.judge_sng,
            is_officer_manager=True,
        )
        chorus_manager = OfficeFactory(
            name='Chorus Manager',
            kind=Office.KIND.chapter,
            code=Office.CODE.chap_man,
            is_group_manager=True,
        )
        quartet_manager = OfficeFactory(
            name='Quartet Manager',
            kind=Office.KIND.quartet,
            code=Office.CODE.quartet_admin,
            is_group_manager=True,
        )
        # Create Core Officers
        scjc_officer = OfficerFactory(
            office=scjc_office,
            person=admin_person,
            group=international,
            status=Officer.STATUS.active,
        )
        drcj_alpha_officer = OfficerFactory(
            office=drcj_office,
            person=drcj_person,
            group=district_alpha,
            status=Officer.STATUS.active,
        )
        ca_officer = OfficerFactory(
            office=ca_office,
            person=ca_person,
            group=district_alpha,
            status=Officer.STATUS.active,
        )
        mus_judge = OfficerFactory(
            office=mus_office,
            person=music_judge_person,
            group=international,
            status=Officer.STATUS.active,
        )
        per_judge = OfficerFactory(
            office=per_office,
            person=performance_judge_person,
            group=international,
            status=Officer.STATUS.active,
        )
        sng_judge = OfficerFactory(
            office=sng_office,
            person=singing_judge_person,
            group=international,
            status=Officer.STATUS.active,
        )
        OfficerFactory(
            office=chorus_manager,
            person=admin_person,
            group=chorus_1,
            status=Officer.STATUS.active,
        )
        chapter_president = OfficerFactory(
            office=chorus_manager,
            person=chorus_manager_person,
            group=chorus_1,
            status=Officer.STATUS.active,
        )
        quartet_1_manager = OfficerFactory(
            office=quartet_manager,
            person=admin_person,
            group=quartet_1,
            status=Officer.STATUS.active,
        )
        quartet_2_manager = OfficerFactory(
            office=quartet_manager,
            person=quartet_lead_person,
            group=quartet_2,
            status=Officer.STATUS.active,
        )
        quartet_3_manager = OfficerFactory(
            office=quartet_manager,
            person=quartet_lead_person,
            group=quartet_3,
            status=Officer.STATUS.active,
        )
        # Create Awards
        international_quartet_championship = AwardFactory(
            name='International Quartet Championship',
            group=international,
            rounds=1,
            level=Award.LEVEL.championship,
            kind=Award.KIND.quartet,
            season=Award.SEASON.summer,
        )
        international_chorus_championship = AwardFactory(
            name='International Chorus Championship',
            group=international,
            rounds=1,
            level=Award.LEVEL.championship,
            kind=Award.KIND.chorus,
            season=Award.SEASON.summer,
        )
        district_alpha_quartet_championship = AwardFactory(
            name='District Alpha Quartet Championship',
            group=district_alpha,
            rounds=2,
            level=Award.LEVEL.championship,
            season=Award.SEASON.fall,
        )
        district_alpha_international_quartet_championship_qualifier = AwardFactory(
            name='District Alpha International Quartet Championship Qualifier',
            group=district_alpha,
            rounds=2,
            parent=international_quartet_championship,
            level=Award.LEVEL.qualifier,
            season=Award.SEASON.spring,
            kind=Award.KIND.quartet,
            advance=76.0,
        )
        district_alpha_international_chorus_championship_qualifier = AwardFactory(
            name='District Alpha International Chorus Championship Qualifier',
            group=district_alpha,
            rounds=1,
            parent=international_chorus_championship,
            level=Award.LEVEL.qualifier,
            season=Award.SEASON.fall,
            kind=Award.KIND.chorus,
            advance=73.0,
        )
        international_senior_quartet_championship = AwardFactory(
            name='International Senior Quartet Championship',
            group=international,
            rounds=1,
            level=Award.LEVEL.championship,
            kind=Award.KIND.quartet,
            season=Award.SEASON.midwinter,
        )

        # Create conventions
        international_midwinter_convention = ConventionFactory(
            name='International Midwinter Convention',
            group=international,
            panel=3,
            season=Convention.SEASON.midwinter,
        )
        GrantorFactory(
            group=international,
            convention=international_midwinter_convention,
        )
        district_alpha_fall_convention = ConventionFactory(
            name='District Alpha Fall Convention',
            group=district_alpha,
            panel=3,
            season=Convention.SEASON.fall,
        )
        GrantorFactory(
            group=district_alpha,
            convention=district_alpha_fall_convention,
        )
        district_alpha_spring_convention = ConventionFactory(
            name='District Alpha Spring Convention',
            group=district_alpha,
            panel=3,
            season=Convention.SEASON.spring,
        )
        GrantorFactory(
            group=district_alpha,
            convention=district_alpha_spring_convention,
        )
        # Create assignments
        AssignmentFactory(
            category=Assignment.CATEGORY.drcj,
            convention=district_alpha_fall_convention,
            person=admin_person,
        )
        AssignmentFactory(
            category=Assignment.CATEGORY.drcj,
            convention=district_alpha_fall_convention,
            person=drcj_person,
        )
        AssignmentFactory(
            category=Assignment.CATEGORY.ca,
            convention=district_alpha_fall_convention,
            person=ca_person,
        )
        AssignmentFactory(
            category=Assignment.CATEGORY.music,
            convention=district_alpha_fall_convention,
            person=music_judge_person,
        )
        AssignmentFactory(
            category=Assignment.CATEGORY.performance,
            convention=district_alpha_fall_convention,
            person=performance_judge_person,
        )
        AssignmentFactory(
            category=Assignment.CATEGORY.singing,
            convention=district_alpha_fall_convention,
            person=singing_judge_person,
        )
        AssignmentFactory(
            category=Assignment.CATEGORY.drcj,
            convention=district_alpha_spring_convention,
            person=admin_person,
        )
        AssignmentFactory(
            category=Assignment.CATEGORY.ca,
            convention=district_alpha_spring_convention,
            person=admin_person,
        )
        AssignmentFactory(
            category=Assignment.CATEGORY.music,
            convention=district_alpha_spring_convention,
            person=music_judge_person,
        )
        AssignmentFactory(
            category=Assignment.CATEGORY.performance,
            convention=district_alpha_spring_convention,
            person=performance_judge_person,
        )
        AssignmentFactory(
            category=Assignment.CATEGORY.singing,
            convention=district_alpha_spring_convention,
            person=singing_judge_person,
        )
        AssignmentFactory(
            category=Assignment.CATEGORY.drcj,
            convention=international_midwinter_convention,
            person=admin_person,
        )
        AssignmentFactory(
            category=Assignment.CATEGORY.ca,
            convention=international_midwinter_convention,
            person=admin_person,
        )
        AssignmentFactory(
            category=Assignment.CATEGORY.music,
            convention=international_midwinter_convention,
            person=music_judge_person,
        )
        AssignmentFactory(
            category=Assignment.CATEGORY.performance,
            convention=international_midwinter_convention,
            person=performance_judge_person,
        )
        AssignmentFactory(
            category=Assignment.CATEGORY.singing,
            convention=international_midwinter_convention,
            person=singing_judge_person,
        )
        international_midwinter_convention_quartet_session = SessionFactory(
            convention=international_midwinter_convention,
            kind=Session.KIND.quartet,
            num_rounds=1,
            is_invitational=True,
        )
        district_alpha_fall_convention_quartet_session = SessionFactory(
            convention=district_alpha_fall_convention,
            kind=Session.KIND.quartet,
            num_rounds=2,
        )
        district_alpha_spring_convention_quartet_session = SessionFactory(
            convention=district_alpha_spring_convention,
            kind=Session.KIND.quartet,
            num_rounds=2,
        )
        district_alpha_fall_convention_chorus_session = SessionFactory(
            convention=district_alpha_fall_convention,
            kind=Session.KIND.chorus,
            num_rounds=1,
        )
        # Create members
        member_quartet_lead = MemberFactory(
            part=Member.PART.lead,
            group=quartet_1,
            person=admin_person,
        )
        member_quartet_tenor = MemberFactory(
            part=Member.PART.tenor,
            group=quartet_1,
            person=quartet_tenor_person,
        )
        member_quartet_baritone = MemberFactory(
            part=Member.PART.baritone,
            group=quartet_1,
            person=quartet_baritone_person,
        )
        member_quartet_bass = MemberFactory(
            part=Member.PART.bass,
            group=quartet_1,
            person=quartet_bass_person,
        )
        member_chorus_manager = MemberFactory(
            part=Member.PART.lead,
            group=chorus_1,
            person=admin_person,
        )
        member_quartet_2_lead = MemberFactory(
            part=Member.PART.lead,
            group=quartet_2,
            person=quartet_lead_person,
        )
        member_quartet_2_tenor = MemberFactory(
            part=Member.PART.tenor,
            group=quartet_2,
            person=quartet_tenor_person,
        )
        member_quartet_2_baritone = MemberFactory(
            part=Member.PART.baritone,
            group=quartet_2,
            person=quartet_baritone_person,
        )
        member_quartet_2_bass = MemberFactory(
            part=Member.PART.bass,
            group=quartet_2,
            person=quartet_bass_person,
        )
        member_quartet_3_lead = MemberFactory(
            part=Member.PART.lead,
            group=quartet_3,
            person=quartet_lead_person,
        )
        member_quartet_3_tenor = MemberFactory(
            part=Member.PART.tenor,
            group=quartet_3,
            person=quartet_tenor_person,
        )
        member_quartet_3_baritone = MemberFactory(
            part=Member.PART.baritone,
            group=quartet_3,
            person=quartet_baritone_person,
        )
        member_quartet_3_bass = MemberFactory(
            part=Member.PART.bass,
            group=quartet_3,
            person=quartet_bass_person,
        )
        # Create repertories
        RepertoryFactory(
            group=quartet_1,
            chart=chart_1,
        )
        RepertoryFactory(
            group=quartet_1,
            chart=chart_2,
        )
        RepertoryFactory(
            group=quartet_1,
            chart=chart_3,
        )
        RepertoryFactory(
            group=quartet_1,
            chart=chart_4,
        )
        RepertoryFactory(
            group=quartet_1,
            chart=chart_5,
        )
        RepertoryFactory(
            group=quartet_1,
            chart=chart_6,
        )
        RepertoryFactory(
            group=chorus_1,
            chart=chart_1,
        )
        RepertoryFactory(
            group=chorus_1,
            chart=chart_2,
        )
        RepertoryFactory(
            group=quartet_2,
            chart=chart_1,
        )
        RepertoryFactory(
            group=quartet_2,
            chart=chart_2,
        )
        RepertoryFactory(
            group=quartet_2,
            chart=chart_3,
        )
        RepertoryFactory(
            group=quartet_2,
            chart=chart_4,
        )
        RepertoryFactory(
            group=quartet_2,
            chart=chart_5,
        )
        RepertoryFactory(
            group=quartet_2,
            chart=chart_6,
        )

        RepertoryFactory(
            group=quartet_3,
            chart=chart_1,
        )
        RepertoryFactory(
            group=quartet_3,
            chart=chart_2,
        )
        RepertoryFactory(
            group=quartet_3,
            chart=chart_3,
        )
        RepertoryFactory(
            group=quartet_3,
            chart=chart_4,
        )
        RepertoryFactory(
            group=quartet_3,
            chart=chart_5,
        )
        RepertoryFactory(
            group=quartet_3,
            chart=chart_6,
        )

        # Contests created via signal.
        international_midwinter_convention.activate()
        international_midwinter_convention.save()
        district_alpha_fall_convention.activate()
        district_alpha_fall_convention.save()
        district_alpha_spring_convention.activate()
        district_alpha_spring_convention.save()

        if options['breakpoint'] == 'session':
            return

        # Build sessions
        international_midwinter_convention_quartet_session.build()
        international_midwinter_convention_quartet_session.save()
        district_alpha_fall_convention_quartet_session.build()
        district_alpha_fall_convention_quartet_session.save()
        district_alpha_spring_convention_quartet_session.build()
        district_alpha_spring_convention_quartet_session.save()
        district_alpha_fall_convention_chorus_session.build()
        district_alpha_fall_convention_chorus_session.save()

        # Monkeypatch finals round
        district_alpha_fall_convention_quartet_session_round_one = district_alpha_fall_convention_quartet_session.rounds.first()
        district_alpha_fall_convention_quartet_session_round_one.spots = 2
        district_alpha_fall_convention_quartet_session_round_one.save()

        # Open sessions
        international_midwinter_convention_quartet_session.open()
        international_midwinter_convention_quartet_session.save()
        district_alpha_fall_convention_quartet_session.open()
        district_alpha_fall_convention_quartet_session.save()
        district_alpha_spring_convention_quartet_session.open()
        district_alpha_spring_convention_quartet_session.save()
        district_alpha_fall_convention_chorus_session.open()
        district_alpha_fall_convention_chorus_session.save()

        # Add entries
        senior_entry = EntryFactory(
            session=international_midwinter_convention_quartet_session,
            group=quartet_1,
            description='We would like to sing last',
        )
        senior_2_entry = EntryFactory(
            session=international_midwinter_convention_quartet_session,
            group=quartet_2,
        )
        senior_3_entry = EntryFactory(
            session=international_midwinter_convention_quartet_session,
            group=quartet_3,
        )
        quartet_entry = EntryFactory(
            session=district_alpha_fall_convention_quartet_session,
            group=quartet_1,
        )
        quartet_2_entry = EntryFactory(
            session=district_alpha_fall_convention_quartet_session,
            group=quartet_2,
        )
        quartet_3_entry = EntryFactory(
            session=district_alpha_fall_convention_quartet_session,
            group=quartet_3,
        )
        spring_quartet_entry = EntryFactory(
            session=district_alpha_spring_convention_quartet_session,
            group=quartet_1,
        )
        spring_quartet_2_entry = EntryFactory(
            session=district_alpha_spring_convention_quartet_session,
            group=quartet_2,
        )
        spring_quartet_3_entry = EntryFactory(
            session=district_alpha_spring_convention_quartet_session,
            group=quartet_3,
        )
        chorus_entry = EntryFactory(
            session=district_alpha_fall_convention_chorus_session,
            group=chorus_1,
        )

        # Build entries
        senior_entry.build()
        senior_entry.save()
        senior_2_entry.build()
        senior_2_entry.save()
        senior_3_entry.build()
        senior_3_entry.save()
        quartet_entry.build()
        quartet_entry.save()
        quartet_2_entry.build()
        quartet_2_entry.save()
        quartet_3_entry.build()
        quartet_3_entry.save()
        spring_quartet_entry.build()
        spring_quartet_entry.save()
        spring_quartet_2_entry.build()
        spring_quartet_2_entry.save()
        spring_quartet_3_entry.build()
        spring_quartet_3_entry.save()
        chorus_entry.build()
        chorus_entry.save()

        # Activate Contestants
        lst = [
            quartet_entry,
            quartet_2_entry,
            quartet_3_entry,
            chorus_entry,
        ]

        for l in lst:
            contestants = l.contestants.all()
            for contestant in contestants:
                contestant.include()
                contestant.save()


        # Approve entries
        senior_entry.submit()
        senior_entry.approve()
        senior_entry.save()
        senior_2_entry.approve()
        senior_2_entry.save()
        senior_3_entry.approve()
        senior_3_entry.save()
        quartet_entry.approve()
        quartet_entry.save()
        quartet_2_entry.approve()
        quartet_2_entry.save()
        quartet_3_entry.approve()
        quartet_3_entry.save()
        spring_quartet_entry.approve()
        spring_quartet_entry.save()
        spring_quartet_2_entry.approve()
        spring_quartet_2_entry.save()
        spring_quartet_3_entry.approve()
        spring_quartet_3_entry.save()
        chorus_entry.approve()
        chorus_entry.save()

        # Close sessions
        international_midwinter_convention_quartet_session.close()
        international_midwinter_convention_quartet_session.save()
        district_alpha_fall_convention_quartet_session.close()
        district_alpha_fall_convention_quartet_session.save()
        district_alpha_spring_convention_quartet_session.close()
        district_alpha_spring_convention_quartet_session.save()
        district_alpha_fall_convention_chorus_session.close()
        district_alpha_fall_convention_chorus_session.save()

        # Verify sessions
        international_midwinter_convention_quartet_session.verify()
        international_midwinter_convention_quartet_session.save()
        district_alpha_fall_convention_quartet_session.verify()
        district_alpha_fall_convention_quartet_session.save()
        district_alpha_spring_convention_quartet_session.verify()
        district_alpha_spring_convention_quartet_session.save()
        district_alpha_fall_convention_chorus_session.verify()
        district_alpha_fall_convention_chorus_session.save()

        # Start sessions
        international_midwinter_convention_quartet_session.start()
        international_midwinter_convention_quartet_session.save()
        district_alpha_spring_convention_quartet_session.start()
        district_alpha_spring_convention_quartet_session.save()
        district_alpha_fall_convention_quartet_session.start()
        district_alpha_fall_convention_quartet_session.save()
        district_alpha_fall_convention_chorus_session.start()
        district_alpha_fall_convention_chorus_session.save()

        # CA BREAKPOINT
        if options['breakpoint'] == 'round':
            return

        # Start First Round
        international_midwinter_convention_quartet_session_round_one = international_midwinter_convention_quartet_session.rounds.earliest()
        district_alpha_fall_convention_quartet_session_round_one = district_alpha_fall_convention_quartet_session.rounds.earliest()
        district_alpha_spring_convention_quartet_session_round_one = district_alpha_spring_convention_quartet_session.rounds.earliest()
        district_alpha_fall_convention_chorus_session_round_one = district_alpha_fall_convention_chorus_session.rounds.earliest()

        international_midwinter_convention_quartet_session_round_one.start()
        international_midwinter_convention_quartet_session_round_one.save()
        district_alpha_fall_convention_quartet_session_round_one.start()
        district_alpha_fall_convention_quartet_session_round_one.save()
        district_alpha_spring_convention_quartet_session_round_one.start()
        district_alpha_spring_convention_quartet_session_round_one.save()
        district_alpha_fall_convention_chorus_session_round_one.start()
        district_alpha_fall_convention_chorus_session_round_one.save()

        s = 70
        for appearance in international_midwinter_convention_quartet_session_round_one.appearances.order_by('num'):
            appearance.start()
            appearance.save()
            song_one = appearance.songs.earliest()
            song_two = appearance.songs.latest()
            song_one.chart = Chart.objects.get(title='Chart 1')
            song_two.chart = Chart.objects.get(title='Chart 2')
            song_one.save()
            song_two.save()
            appearance.finish()
            appearance.save()
            s += 5
            for song in appearance.songs.all():
                for score in song.scores.all():
                    score.points = s
                    score.save()
            appearance.confirm()
            appearance.save()

        s = 70
        for appearance in district_alpha_fall_convention_quartet_session_round_one.appearances.order_by('num'):
            appearance.start()
            appearance.save()
            song_one = appearance.songs.earliest()
            song_two = appearance.songs.latest()
            song_one.chart = Chart.objects.get(title='Chart 1')
            song_two.chart = Chart.objects.get(title='Chart 2')
            song_one.save()
            song_two.save()
            appearance.finish()
            appearance.save()
            s += 5
            for song in appearance.songs.all():
                for score in song.scores.all():
                    score.points = s
                    score.save()
            appearance.confirm()
            appearance.save()

        s = 70
        for appearance in district_alpha_spring_convention_quartet_session_round_one.appearances.order_by('num'):
            appearance.start()
            appearance.save()
            song_one = appearance.songs.earliest()
            song_two = appearance.songs.latest()
            song_one.chart = Chart.objects.get(title='Chart 1')
            song_two.chart = Chart.objects.get(title='Chart 2')
            song_one.save()
            song_two.save()
            appearance.finish()
            appearance.save()
            s += 5
            for song in appearance.songs.all():
                for score in song.scores.all():
                    score.points = s
                    score.save()
            appearance.confirm()
            appearance.save()

        if options['breakpoint'] == 'confirmed':
            return

        district_alpha_fall_convention_quartet_session_round_one.verify()
        district_alpha_fall_convention_quartet_session_round_one.save()
        district_alpha_fall_convention_quartet_session_round_one.finish()
        district_alpha_fall_convention_quartet_session_round_one.save()

        # Start Second Round
        district_alpha_fall_convention_quartet_session_round_two = district_alpha_fall_convention_quartet_session.rounds.get(num=2)

        district_alpha_fall_convention_quartet_session_round_two.start()
        district_alpha_fall_convention_quartet_session_round_two.save()

        s = 75
        for appearance in district_alpha_fall_convention_quartet_session_round_two.appearances.order_by('num'):
            appearance.start()
            appearance.save()
            song_one = appearance.songs.earliest()
            song_two = appearance.songs.latest()
            song_one.chart = Chart.objects.get(title='Chart 1')
            song_two.chart = Chart.objects.get(title='Chart 2')
            song_one.save()
            song_two.save()
            appearance.finish()
            appearance.save()
            s += 3
            for song in appearance.songs.all():
                for score in song.scores.all():
                    score.points = s
                    score.save()
            appearance.confirm()
            appearance.save()

        district_alpha_fall_convention_quartet_session_round_two.verify()
        district_alpha_fall_convention_quartet_session_round_two.save()

        district_alpha_fall_convention_quartet_session_round_two.finish()
        district_alpha_fall_convention_quartet_session_round_two.save()

        return
