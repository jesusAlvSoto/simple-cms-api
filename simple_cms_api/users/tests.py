from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model


class UserListCreateAPIView(APITestCase):

    def setUp(self):
        self.user_model = get_user_model()
        self.url = reverse('users:users-list')

        self.normal_user = self.user_model.objects.create(
            username='my_test_normal_username',
            password='my_test_normal_password',
            is_staff=False
        )
        self.normal_user_token = Token.objects.create(user=self.normal_user)

        self.admin_user = self.user_model.objects.create(
            username='my_test_admin_username',
            password='my_test_admin_password',
            is_staff=True
        )
        self.admin_user_token = Token.objects.create(user=self.admin_user)

    def test_anonymous_user_create_user_failure(self):
        """
        Ensure an anonymous user can't create a new user
        """

        new_user_data = {
            'username': 'my_new_user_username',
            'password': 'my_new_user_password',
            'is_staff': False
        }
        response = self.client.post(self.url, new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_normal_user_create_user_failure(self):
        """
        Ensure a normal user can't create a new user
        """

        new_user_data = {
            'username': 'my_new_user_username',
            'password': 'my_new_user_password',
            'is_staff': False
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_user_token.key)
        response = self.client.post(self.url, new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user_create_user(self):
        """
        Ensure an admin user can create a new user
        """
        new_user_data = {
            'username': 'my_new_user_username',
            'password': 'my_new_user_password',
            'is_staff': False
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_user_token.key)
        response = self.client.post(self.url, new_user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # check that the user was created with the correct data
        new_user = self.user_model.objects.get(username=new_user_data['username'])
        self.assertEqual(new_user.check_password(new_user_data['password']), True)
        self.assertEqual(new_user.is_staff, new_user_data['is_staff'])

    def test_anonymous_user_list_users_failure(self):
        """
        Ensure an anonymous user can't list users
        """

        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_normal_user_list_users_failure(self):
        """
        Ensure a normal user can't create a new user
        """

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_user_token.key)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user_list_users(self):
        """
        Ensure an admin user can create a new user
        """

        # create the user which we will retrieve later
        self.user_model.objects.create(
            username='my_test_username',
            password='my_test_username',
            is_staff=False
        )

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_user_token.key)
        response = self.client.get(self.url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check that at least one user has been listed
        num_users = self.user_model.objects.filter().count()
        self.assertGreaterEqual(num_users, 1)


class UserRetrieveUpdateDestroyAPIView(APITestCase):

    def setUp(self):
        self.user_model = get_user_model()

        # create a user so we can perform the retrieve(GET), update(PATCH & PUT) and destroy(DELETE) actions on it
        self.user_to_edit = self.user_model.objects.create(
            username='my_test_username',
            password='my_test_username',
            is_staff=False
        )
        self.url = reverse('users:user-detail', args=[self.user_to_edit.id])

        self.normal_user = self.user_model.objects.create(
            username='my_test_normal_username',
            password='my_test_normal_password',
            is_staff=False
        )
        self.normal_user_token = Token.objects.create(user=self.normal_user)

        self.admin_user = self.user_model.objects.create(
            username='my_test_admin_username',
            password='my_test_admin_password',
            is_staff=True
        )
        self.admin_user_token = Token.objects.create(user=self.admin_user)

    def test_anonymous_user_retrieve_user_failure(self):
        """
        Ensure an anonymous user can't retrieve an existing user
        """

        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_normal_user_retrieve_user_failure(self):
        """
        Ensure a normal user can't retrieve an existing user
        """

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_user_token.key)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user_retrieve_user(self):
        """
        Ensure an admin user can retrieve an existing user
        """

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_user_token.key)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check that the correct user has been retrieved
        self.assertEqual(response.data['id'], self.user_to_edit.id)

    def test_anonymous_user_patch_update_user_failure(self):
        """
        Ensure an anonymous user can't update with PATCH method an existing user
        """

        edit_user_data = {
            'username': 'edited_username'
        }
        response = self.client.patch(self.url, edit_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_normal_user_patch_update_user_failure(self):
        """
        Ensure a normal user can't update with PATCH method an existing user
        """

        edit_user_data = {
            'username': 'edited_username'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_user_token.key)
        response = self.client.patch(self.url, edit_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user_patch_update_user(self):
        """
        Ensure an admin user can update with PATCH method an existing user
        """

        edit_user_data = {
            'username': 'edited_username'
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_user_token.key)
        response = self.client.patch(self.url, edit_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check that the user's username has changed after updating it
        updated_user = self.user_model.objects.get(id=self.user_to_edit.id)
        self.assertEqual(edit_user_data['username'], updated_user.username)

    def test_anonymous_user_put_update_user_failure(self):
        """
        Ensure an anonymous user can't update with PUT method an existing user
        """

        edit_user_data = {
            'username': 'edited_username',
            'password': 'edited_password'
        }
        response = self.client.put(self.url, edit_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_normal_user_put_update_user_failure(self):
        """
        Ensure a normal user can't update with PUT method an existing user
        """

        edit_user_data = {
            'username': 'edited_username',
            'password': 'edited_password'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_user_token.key)
        response = self.client.put(self.url, edit_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user_put_update_user(self):
        """
        Ensure an admin user can update with PUT method an existing user
        """

        edit_user_data = {
            'username': 'edited_username',
            'password': 'edited_password'
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_user_token.key)
        response = self.client.put(self.url, edit_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check that the user's username and password have changed after updating them
        updated_user = self.user_model.objects.get(id=self.user_to_edit.id)
        self.assertEqual(edit_user_data['username'], updated_user.username)
        self.assertEqual(edit_user_data['password'], updated_user.password)

    def test_anonymous_user_delete_user_failure(self):
        """
        Ensure an anonymous user can't delete an existing user
        """

        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_normal_user_delete_user_failure(self):
        """
        Ensure a normal user can't delete an existing user
        """

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_user_token.key)
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user_delete_user(self):
        """
        Ensure an admin user can delete an existing user
        """

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_user_token.key)
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # check that the user does not exist in the database after deleting it
        num_users = self.user_model.objects.filter(id=self.user_to_edit.id).count()
        self.assertEqual(num_users, 0)
