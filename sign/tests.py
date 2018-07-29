from django.test import TestCase
from sign.models import Event, Guest
from django.test import Client
from django.contrib.auth.models import User
from datetime import datetime
# Create your tests here.


class ModelTest(TestCase):
    def setUp(self):
        Event.objects.create(id=1, name="oneplues 3 event", status=True, limit=2000,
                             address='shenzhen', start_time='2016-08-31 02:18:22')
        Guest.objects.create(id=1, event_id=1, realname='alen',
                             phone='13711001101', email='alen@mail.com', sign=False)

    def test_event_models(self):
        result =Event.objects.get(name='oneplues 3 event')
        self.assertEquals(result.address, "shenzhen")
        self.assertTrue(result.status)

    def test_guest_models(self):
        result = Guest.objects.get(phone='13711001101')
        self.assertEqual(result.realname, "alen")
        self.assertFalse(result.sign)


class IndexPageTest(TestCase):

    def test_index_page_renders_index_template(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class LoginActionTest(TestCase):
    def setUp(self):
        User.objects.create_user('admin','admin@mail.com','admin123456')
        self.c = Client()

    def test_login_action_username_password_null(self):
        test_data = {'username': '', 'password': ''}
        response = self.c.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password error!", response.content)

    def test_login_action_username_password_error(self):
        test_data = {'username': 'abc', 'password': '123'}
        response = self.c.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password error!", response.content)

    def test_login_action_success(self):
        test_data = {'username': 'admin', 'password': 'admin123456'}
        response = self.c.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 302)

class EventManageTest(TestCase):
    def setUp(self):
        Event.objects.create(id=2,name='xiaomi5',limit=2000,status=True,
                             address='beijing',start_time=datetime(2016,8,10,14,0,0))
        self.c = Client()

    def test_event_manage_success(self):
        response = self.c.post('/event_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"xiaomi5", response.content)
        self.assertIn(b"beijing", response.content)

    def tets_event_manage_search_success(self):
        response = self.c.post('/search_name/', {"name":"xiaomi5"})
        self.assertEquals(response.status_code, 200)
        self.assertIn(b"xiaomi5", response.content)
        self.assertIn(b"beijing",response.content)



