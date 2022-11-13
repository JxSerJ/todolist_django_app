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

    def test_username_regex_compliance(self):
        response = self.client.post(
            path=self.url,
            data={
                'username': 'incorrect_user_uname/',
                'password': '123qwert#!@!3%',
                'password_repeat': '123qwert#!@!3%'
            })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {
                'username': ['This value does not match the required pattern.'],
            }
        )


class LoginTestCase(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.url = reverse('login')

        self.user = User.objects.create_user(
            username='test_user_name',
            password='123qwert#!@!3%',
            email='test@skypro.com',
            first_name='test_first_name',
            last_name='test_last_name'
        )

    def test_login_success(self):
        response = self.client.post(
            path=self.url,
            data={
                'username': 'test_user_name',
                'password': '123qwert#!@!3%',
            })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(
            response.json(),
            {
                'username': self.user.username,
                'email': self.user.email,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'status': 'success'
            }
        )

    def test_invalid_password(self):
        response = self.client.post(
            path=self.url,
            data={
                'username': 'test_user_name',
                'password': '12345678'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {
                'password': ['Incorrect password']
            }
        )

    def test_invalid_username(self):
        response = self.client.post(
            path=self.url,
            data={
                'username': 'username',
                'password': '123qwert#!@!3%'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {
                'username': ['User "username" does not exist']
            }
        )


class UpdatePasswordTestCase(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.url = reverse('update_password')

        self.user = User.objects.create_user(
            username='test_user_name',
            password='123qwert#!@!3%',
            email='test@skypro.com',
            first_name='test_first_name',
            last_name='test_last_name'
        )

    def test_password_update_success(self):
        self.client.force_login(self.user)  # Do not use login(), excessive db querying
        response = self.client.patch(
            path=self.url,
            data={
                'old_password': '123qwert#!@!3%',
                'new_password': 'ntk4j3ht98un;',
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.json(),
            {'status': 'success'}
        )
        self.user.refresh_from_db(fields=('password',))
        self.assertTrue(self.user.check_password('ntk4j3ht98un;'))

    def test_invalid_old_password(self):
        self.client.force_login(self.user)
        response = self.client.patch(
            path=self.url,
            data={
                'old_password': '123',
                'new_password': 'ntk4j3ht98un;',
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {'old_password': ['Incorrect password']}
        )
        self.user.refresh_from_db(fields=('password',))
        self.assertTrue(self.user.check_password('123qwert#!@!3%'))

    def test_invalid_new_password(self):
        self.client.force_login(self.user)
        response = self.client.patch(
            path=self.url,
            data={
                'old_password': '123qwert#!@!3%',
                'new_password': 'qwerty123',
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {'new_password': ['This password is too common.']}
        )
        self.user.refresh_from_db(fields=('password',))
        self.assertTrue(self.user.check_password('123qwert#!@!3%'))

    def test_authentication(self):
        response = self.client.patch(
            path=self.url,
            data={
                'old_password': '123qwert#!@!3%',
                'new_password': 'ntk4j3ht98un;',
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertDictEqual(
            response.json(),
            {'detail': 'Authentication credentials were not provided.'}
        )
        self.user.refresh_from_db(fields=('password',))
        self.assertTrue(self.user.check_password('123qwert#!@!3%'))


class ProfileTestCase(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.url = reverse('profile')

        self.user = User.objects.create_user(
            username='test_user_name',
            password='123qwert#!@!3%',
            email='test@skypro.com',
            first_name='test_first_name',
            last_name='test_last_name'
        )

    def test_logout(self):
        self.client.force_login(self.user)
        response = self.client.delete(
            path=self.url
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_detail(self):
        self.client.force_login(self.user)
        response = self.client.get(
            path=self.url
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.json(),
            {
                'id': self.user.id,
                'username': 'test_user_name',
                'email': 'test@skypro.com',
                'first_name': 'test_first_name',
                'last_name': 'test_last_name',
            }
        )

    def test_profile_update(self):
        self.client.force_login(self.user)
        response = self.client.patch(
            path=self.url,
            data={
                'username': '_test_user_name',
                'email': '_test@skypro.com',
                'first_name': '_test_first_name',
                'last_name': '_test_last_name',
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.json(),
            {
                'id': self.user.id,
                'username': '_test_user_name',
                'email': '_test@skypro.com',
                'first_name': '_test_first_name',
                'last_name': '_test_last_name',
            }
        )
        self.user.refresh_from_db(fields=('username', 'email', 'first_name', 'last_name'))
        self.assertDictEqual(
            response.json(),
            {
                'id': self.user.id,
                'username': self.user.username,
                'email': self.user.email,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
            }
        )
