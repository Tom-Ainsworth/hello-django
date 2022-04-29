from tokenize import Ignore
from urllib import response
from django.test import TestCase
from .models import Item

# Create your tests here.
class TestViews(TestCase):
    def test_get_todo_list(self):
        response = self.client.get("/") # set the variable to use.
        self.assertEqual(response.status_code, 200) # test which status_code is returned when running
        self.assertTemplateUsed(response, "todo/todo_list.html") # test which template is used during the function

    def test_get_add_item_page(self):
        response = self.client.get("/add") # set the variable
        self.assertEqual(response.status_code, 200) # test the status_code
        self.assertTemplateUsed(response, "todo/add_item.html") # test the returned template

    def test_get_edit_item_page(self):
        item = Item.objects.create(name="Test Todo Item") # create a dummy item in the Item model (import from .models at the top)
        response = self.client.get(f"/edit/{item.id}") # test the returned url. Usually associated to task, but here it's a new one.
        self.assertEqual(response.status_code, 200) # test status_code
        self.assertTemplateUsed(response, "todo/edit_item.html") # test template used.

    def test_can_add_item(self):
        response = self.client.post('/add', {'name': 'Test Added Item'})
        self.assertRedirects(response, '/')


    def test_can_delete_item(self):
        item = Item.objects.create(name="Test Todo Item") # create a dummy item in the Item model (import from .models at the top)
        response = self.client.get(f"/delete/{item.id}") # test the returned url. Usually associated to task, but here it's a new one.
        self.assertRedirects(response, '/')
        existing_items = Item.objects.filter(id=item.id)
        self.assertEqual(len(existing_items), 0)
        
    def test_can_toggle_item(self):
        item = Item.objects.create(name="Test Todo Item", done=True) # create a dummy item in the Item model (import from .models at the top)
        response = self.client.get(f"/toggle/{item.id}") # test the returned url. Usually associated to task, but here it's a new one.
        self.assertRedirects(response, '/')
        update_item = Item.objects.get(id=item.id)
        self.assertFalse(update_item.done)
        
    def test_can_edit_item(self):
        item = Item.objects.create(name="Test Todo Item") # create a dummy item in the Item model (import from .models at the top)
        response = self.client.post(f"/edit/{item.id}", {'name': 'Updated Name'})
        self.assertRedirects(response, '/') # test the returned url. Usually associated to task, but here it's a new one.
        update_item = Item.objects.get(id=item.id)
        self.assertEqual(update_item.name, 'Updated Name')