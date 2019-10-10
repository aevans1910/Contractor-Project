# tests.py

from unittest import TestCase, main as unittest_main, mock
from app import app
from bson.objectid import ObjectId

sample_dog_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_dog = {
    'name': 'Rex',
    'description': 'Is a dog',
    'image': [
        'https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/gettyimages-1094874726.png?crop=0.542xw:0.814xh;0.0472xw,0.127xh&resize=640:*'
        'https://static.independent.co.uk/s3fs-public/thumbnails/image/2019/09/04/13/istock-1031307988.jpg?w968h681'
    ]
}
sample_form_data = {
    'name': sample_dog['name'],
    'description': sample_dog['description'],
    'iamge': '\n'.join(sample_dog['image'])
}

class DogsTests(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test the homepage."""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Dogs', result.data)

    def test_new(self):
        """Test the new dog listing creation page."""
        result = self.client.get('/dogs/new')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Adopt a dog!', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_dog(self, mock_find):
        """Test showing a single dog."""
        mock_find.return_value = sample_dog

        result = self.client.get(f'/dogs/{sample_dog_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Rex', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_edit_dog(self, mock_find):
        """Test editing a single listing."""
        mock_find.return_value = sample_dog

        result = self.client.get(f'/dogs/{sample_dog_id}/edit')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Rex', result.data)

    @mock.patch('pymongo.collection.Collection.insert_one')
    def test_submit_dog(self, mock_insert):
        """Test submitting a new listing"""
        result = self.client.post('/dogs', data=sample_form_data)

        # After submitting, should redirect to that listing's page
        self.assertEqual(result.status, '302 FOUND')
        mock_insert.assert_called_with(sample_dog)

    @mock.patch('pymongo.collection.Collection.update_one')
    def test_update_dog(self, mock_update):
        result = self.client.post(f'/dogs/{sample_dog_id}', data=sample_form_data)

        self.assertEqual(result.status, '302 FOUND')
        mock_update.assert_called_with({'_id': sample_dog_id}, {'$set': sample_dog})

    @mock.patch('pymongo.collection.Collection.delete_one')
    def test_delete_dog(self, mock_delete):
        form_data = {'_method': 'DELETE'}
        result = self.client.post(f'/dogs/{sample_dog_id}/delete', data=form_data)
        self.assertEqual(result.status, '302 FOUND')
        mock_delete.assert_called_with({'_id': sample_dog_id})

if __name__ == '__main__':
    unittest_main()