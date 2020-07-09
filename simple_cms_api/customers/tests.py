from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
import boto3
from io import BytesIO
from .models import Customer


class CustomerCreate(APITestCase):

    def setUp(self):
        self.user_model = get_user_model()
        self.url = reverse('customers:customers-list')

        self.normal_user = self.user_model.objects.create(
            username='my_test_normal_username',
            password='my_test_normal_password',
            is_staff=False
        )
        self.normal_user_token = Token.objects.create(user=self.normal_user)

        img = BytesIO(b'mybinarydata')
        img.name = 'myimage.jpg'
        self.new_customer_data = {
            'name': 'my_new_user_username',
            'surname': 'my_new_user_password',
            'photo': img
        }

    def tearDown(self):
        # delete the customer's photo that has been uplaoded to the S3 bucket
        try:
            new_customer = Customer.objects.get(name=self.new_customer_data['name'])
            if new_customer and new_customer.photo:
                s3_client = boto3.client(
                    's3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    endpoint_url=settings.AWS_S3_ENDPOINT_URL
                )
                s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=new_customer.photo.name)
        except ObjectDoesNotExist:
            # the customer was not created, so we don't need to delete the photo from the S3 bucket
            pass

    def test_anonymous_user_create_customer_failure(self):
        """
        Ensure an anonymous user can't create a new customer
        """

        response = self.client.post(self.url, self.new_customer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_create_customer(self):
        """
        Ensure an authenticated user can create a new customer
        """

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_user_token.key)
        response = self.client.post(self.url, self.new_customer_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # check that the customer was created with the correct data
        new_customer = Customer.objects.get(name=self.new_customer_data['name'])
        self.assertEqual(new_customer.surname, self.new_customer_data['surname'])

    def test_authenticated_user_create_customer_image_name_changed(self):
        """
        Ensure that a customer's photo filename is changed when the cutomer is created
        """

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_user_token.key)
        response = self.client.post(self.url, self.new_customer_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # check that the customer photo filename changed
        new_customer = Customer.objects.get(name=self.new_customer_data['name'])
        self.assertNotEqual(new_customer.photo.name, self.new_customer_data['photo'].name)


class CustomerList(APITestCase):

    def setUp(self):
        self.user_model = get_user_model()
        self.url = reverse('customers:customers-list')

        self.normal_user = self.user_model.objects.create(
            username='my_test_normal_username',
            password='my_test_normal_password',
            is_staff=False
        )
        self.normal_user_token = Token.objects.create(user=self.normal_user)

    def test_anonymous_user_list_customers_failure(self):
        """
        Ensure an anonymous user can't list customers
        """

        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_list_customers(self):
        """
        Ensure an authenticated user can list customers
        """

        # create the customer which we will list later
        Customer.objects.create(
            name='my_test_name',
            surname='my_test_surname',
            created_by=self.normal_user
        )

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_user_token.key)
        response = self.client.get(self.url, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check that at least one user has been listed
        num_customers = Customer.objects.filter().count()
        self.assertGreaterEqual(num_customers, 1)


class CustomerRetrieveUpdateDestroy(APITestCase):

    def setUp(self):
        self.user_model = get_user_model()

        self.normal_user = self.user_model.objects.create(
            username='my_test_normal_username',
            password='my_test_normal_password',
            is_staff=False
        )
        self.normal_user_token = Token.objects.create(user=self.normal_user)

        # create a customer so we can perform the retrieve(GET), update(PATCH & PUT) and destroy(DELETE) actions on it
        self.customer_to_edit = Customer.objects.create(
            name='my_test_name',
            surname='my_test_surname',
            created_by=self.normal_user
        )

        self.url = reverse('customers:customer-detail', args=[self.customer_to_edit.id])

    def tearDown(self):
        # delete the customer's photo that has been uplaoded to the S3 bucket
        try:
            new_customer = Customer.objects.get(id=self.customer_to_edit.id)
            if new_customer and new_customer.photo:
                s3_client = boto3.client(
                    's3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    endpoint_url=settings.AWS_S3_ENDPOINT_URL
                )
                s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=new_customer.photo.name)
        except ObjectDoesNotExist:
            # the customer was not created, so we don't need to delete the photo from the S3 bucket
            pass

    def test_anonymous_user_retrieve_customers_failure(self):
        """
        Ensure an anonymous user can't retrieve an existing customer
        """

        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_retrieve_customers(self):
        """
        Ensure an authenticated user can retrieve an existing customer
        """

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_user_token.key)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check that the correct customer has been retrieved
        self.assertEqual(response.data['id'], self.customer_to_edit.id)

    def test_anonymous_user_patch_update_customer_failure(self):
        """
        Ensure an anonymous user can't update with PATCH method an existing customer
        """

        edit_customer_data = {
            'name': 'edited_name'
        }

        response = self.client.patch(self.url, edit_customer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_authenticated_user_patch_update_customer(self):
        """
        Ensure an authenticated user can update with PATCH method an existing customer
        """

        edit_customer_data = {
            'name': 'edited_name'
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_user_token.key)
        response = self.client.patch(self.url, edit_customer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check that the user's username has changed after updating it
        updated_customer = Customer.objects.get(id=self.customer_to_edit.id)
        self.assertEqual(edit_customer_data['name'], updated_customer.name)

    def test_anonymous_user_put_update_customer_failure(self):
        """
        Ensure an anonymous user can't update with PUT method an existing customer
        """

        edit_customer_data = {
            'name': 'edited_name',
            'surname': 'edited_surname'
        }
        response = self.client.put(self.url, edit_customer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_put_update_customer(self):
        """
        Ensure an authenticated user can update with PUT method an existing customer
        """

        edit_customer_data = {
            'name': 'edited_name',
            'surname': 'edited_surname'
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_user_token.key)
        response = self.client.put(self.url, edit_customer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check that the customer's name, surname have changed after updating them
        updated_customer = Customer.objects.get(id=self.customer_to_edit.id)
        self.assertEqual(edit_customer_data['name'], updated_customer.name)
        self.assertEqual(edit_customer_data['surname'], updated_customer.surname)

    def test_authenticated_user_put_update_customer_image_name_changed(self):
        """
        Ensure that a customer's photo filename is changed when the cutomer is created
        """

        img = BytesIO(b'mybinarydata')
        img.name = 'myimage.jpg'
        edit_customer_data = {
            'name': 'edited_name',
            'surname': 'edited_surname',
            'photo': img
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_user_token.key)
        response = self.client.put(self.url, edit_customer_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check that the customer photo filename changed
        updated_customer = Customer.objects.get(id=self.customer_to_edit.id)
        self.assertNotEqual(updated_customer.photo.name, self.customer_to_edit.photo.name)