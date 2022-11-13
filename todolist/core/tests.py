from django.contrib.auth.hashers import make_password
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from core.models import User


class SignUpTestCase(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.url = reverse('signup')

    def test_user_correctly_created_with_minimal_fields(self):
        response = self.client.post(
            path=self.url,
            data={
                'username': 'test_user_name',
                'password': '123qwert#!@!3%',
                'password_repeat': '123qwert#!@!3%'
            })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_user = User.objects.last()
        self.assertDictEqual(
            response.json(),
            {
                'id': created_user.id,
                'username': 'test_user_name',
                'first_name': '',
                'last_name': '',
                'email': ''}
        )
        self.assertTrue(created_user.check_password('123qwert#!@!3%'))

    def test_success_signup(self):
        response = self.client.post(
            path=self.url,
            data={
                'username': 'test_user_name',
                'email': 'test@skypro.com',
                'first_name': 'test_first_name',
                'last_name': 'test_last_name',
                'password': '123qwert#!@!3%',
                'password_repeat': '123qwert#!@!3%'
            })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.last()
        self.assertDictEqual(
            response.json(),
            {
                'id': user.id,
                'username': 'test_user_name',
                'email': 'test@skypro.com',
                'first_name': 'test_first_name',
                'last_name': 'test_last_name',
            }
        )
        self.assertTrue(user.check_password('123qwert#!@!3%'))

    def test_empty_signup(self):
        response = self.client.post(
            path=self.url,
            data={
                'username': '',
                'email': '',
                'first_name': '',
                'last_name': '',
                'password': '',
                'password_repeat': ''
            })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {
                'username': ['This field may not be blank.'],
                'password': ['This field may not be blank.'],
                'password_repeat': ['This field may not be blank.']
            }
        )

    def test_passwords_not_match(self):
        response = self.client.post(
            path=self.url,
            data={
                'username': 'test_user_name',
                'password': '123qwert#!@!3%',
                'password_repeat': '1'
            })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {
                'password_repeat': ['Passwords does not match'],
                'password': ['Passwords does not match']
            }
        )

    def test_weak_password(self):

        test_data = [
            ['123', ['This password is too short. It must contain at least 8 characters.',
                     'This password is too common.',
                     'This password is entirely numeric.']],
            ['12345678', ['This password is too common.', 'This password is entirely numeric.']],
            ['56416496135876', ['This password is entirely numeric.']],
            ['qwerty123', ['This password is too common.']],
        ]

        for i in range(1, len(test_data) + 1):
            with self.subTest(msg=f'weak_password_test_{i}'):
                for password, error_data in test_data:
                    response = self.client.post(
                        path=self.url,
                        data={
                            'username': 'test_user_name',
                            'password': password,
                            'password_repeat': password
                        })
                    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                    self.assertDictEqual(
                        response.json(),
                        {
                            'password': error_data
                        }
                    )

    def test_email(self):
        response = self.client.post(
            path=self.url,
            data={
                'username': 'test_user_name',
                'email': 'random_incorrect_email',
                'password': '123qwert#!@!3%',
                'password_repeat': '123qwert#!@!3%'
            })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {
                'email': ['Enter a valid email address.']
            }
        )

    def test_user_already_exists(self):
        User.objects.create(username='test_user_name', password=make_password('password'))
        created_user = User.objects.last()
        response = self.client.post(
            path=self.url,
            data={
                'username': 'test_user_name',
                'password': '123qwert#!@!3%',
                'password_repeat': '123qwert#!@!3%'
            })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {
                'username': [f'User "{created_user.username}" already exists']
            }
        )
