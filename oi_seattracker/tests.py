from django.test import Client, TestCase, override_settings

from .models import Computer, Participant

@override_settings(LANGUAGE_CODE='en')
class SeattrackerTestCase(TestCase):
    def setUp(self):
        self.ip1 = '3.14.3.14'
        self.c1 = Client(REMOTE_ADDR=self.ip1)

        self.ip2 = '6.28.6.28'
        self.comp2 = Computer.objects.create(ip_address=self.ip2, nice_name='galaxy-brain')
        self.c2 = Client(REMOTE_ADDR=self.ip2)

        self.ip3 = '9.42.6.42'
        self.comp3 = Computer.objects.create(ip_address=self.ip3, nice_name='universe-brain')
        self.p3 = Participant.objects.create(id=42, full_name='Krzysztof Stencel', computer=self.comp3)
        self.c3 = Client(REMOTE_ADDR=self.ip3)

    def test_participant_str(self):
        self.assertEqual(str(self.p3), '42: Krzysztof Stencel')

    def test_dashboard(self):
        response = self.c1.get('/')
        self.assertContains(response, 'unregistered')
        self.assertNotContains(response, 'unassigned')
        self.assertNotContains(response, 'brain')

        response = self.c2.get('/')
        self.assertContains(response, self.comp2.nice_name)
        self.assertContains(response, 'unassigned')
        self.assertNotContains(response, 'unregistered')

        response = self.c3.get('/')
        self.assertContains(response, str(self.p3))
        self.assertContains(response, self.comp3.nice_name)
        self.assertNotContains(response, 'unregistered')
        self.assertNotContains(response, 'unassigned')

    @override_settings(LANGUAGE_CODE='pl')
    def test_dashboard_polish(self):
        response = self.c1.get('/')
        self.assertContains(response, 'niezarejestrowany')
        self.assertNotContains(response, 'nieprzypisany')
        self.assertNotContains(response, 'brain')

        response = self.c2.get('/')
        self.assertNotContains(response, 'niezarejestrowany')
        self.assertContains(response, 'galaxy-brain')
        self.assertContains(response, 'nieprzypisany')

        response = self.c3.get('/')
        self.assertNotContains(response, 'niezarejestrowany')
        self.assertNotContains(response, 'galaxy-brain')
        self.assertContains(response, 'universe-brain')
        self.assertNotContains(response, 'nieprzypisany')
