from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import DataRequest


class DataRequestTests(TestCase):

    fixtures = ['admin']

    def setUp(self):
        """
        Create 20 data requests for testing
        """
        for x in range(20):
            data_request = DataRequest(
                name="Test Request {}".format(x),
                description="Test Description for {}".format(x),
                requestor_name="Joe",
                requestor_email="joe@asdadas.fj",
                source="NASA_{}".format(x)
            )
            data_request.save()

    def test_data_request_form_url(self):
        """
        Test data request form endpoint
        """
        response = self.client.get(reverse('data_request_new'))
        self.assertEquals(response.status_code, 200)

    def test_data_request_detail_url(self):
        """
        Test data request detail endpoint
        """
        response = self.client.get(reverse('data_request_detail', args=[1]))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Extended description of NASA SRTM data")

    def test_data_request_edit_url(self):
        """
        Test data request edit endpoint
        """
        response = self.client.get(reverse('data_request_edit', args=[1]))
        self.assertEquals(response.status_code, 302)
        self.client.login(username='bobby', password='bob')
        response = self.client.get(reverse('data_request_edit', args=[1]))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response,
                            "Update NASA SRTM mission data for Greenland")

    def test_data_request_list_url(self):
        """
        Test data request list endpoint
        """
        response = self.client.get(reverse('data_request_list'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "NASA SRTM mission data for Greenland")
        self.assertContains(response, "USGS Earthquake Data")
        self.assertContains(response, "22 data requests")
