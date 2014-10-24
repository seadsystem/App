from django.test import TestCase
from contacts.models import contact
from django.test.client import Client
from django.test.client import RequestFactory
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

class contactTests(TestCase):
    """contact model tests."""

    def test_str(self):

        contact = contact(first_name='John', last_name='Smith')

        self.assertEquals(
            str(contact),
            'John Smith',
        )

class contactListViewTests(TestCase):
    """contact list view tests."""

    def test_contacts_in_the_context(self):

        client = Client()
        response = client.get('/')

        self.assertEquals(list(response.context['object_list']), [])

        contact.objects.create(first_name='foo', last_name='bar')
        response = client.get('/')
        self.assertEquals(response.context['object_list'].count(), 1)

    def test_contacts_in_the_context_request_factory(self):

        factory = RequestFactory()
        request = factory.get('/')

        response = ListcontactView.as_view()(request)

        self.assertEquals(list(response.context_data['object_list']), [])

        contact.objects.create(first_name='foo', last_name='bar')
        response = ListcontactView.as_view()(request)
        self.assertEquals(response.context_data['object_list'].count(), 1)

class contactListIntegrationTests(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(contactListIntegrationTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(contactListIntegrationTests, cls).tearDownClass()

    def test_contact_listed(self):

        # create a test contact
        contact.objects.create(first_name='foo', last_name='bar')

        # make sure it's listed as <first> <last> on the list
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.assertEqual(
            self.selenium.find_elements_by_css_selector('.contact')[0].text,
            'foo bar'
        )

    def test_add_contact_linked(self):

        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.assert_(
            self.selenium.find_element_by_link_text('add contact')
        )

    def test_add_contact(self):

        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.selenium.find_element_by_link_text('add contact').click()

        self.selenium.find_element_by_id('id_first_name').send_keys('test')
        self.selenium.find_element_by_id('id_last_name').send_keys('contact')
        self.selenium.find_element_by_id('id_email').send_keys('test@example.com')

        self.selenium.find_element_by_id("save_contact").click()
        self.assertEqual(
            self.selenium.find_elements_by_css_selector('.contact')[-1].text,
            'test contact'
        )