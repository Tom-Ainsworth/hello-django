from django.test import TestCase
from .forms import ItemForm

# Create your tests here.
class TestItemForm(TestCase):
    def test_item_name_is_required(self):
        form = ItemForm({"name": ""}) # create a variable of ItemForm to test
        self.assertFalse(
            form.is_valid()
        )  # Test whether the name is not valid, as it shouldn't be because it's required.
        self.assertIn(
            "name", form.errors.keys()
        )  # Test whether the 'name' key appears in the form errors.
        self.assertEqual(
            form.errors["name"][0], "This field is required."
        )  # Test whether the error relating to the 'name' key is 'This field is required.' The test will return a list of errors, but I want to check that the first item in the list is the afortmentioned string.

    def test_done_field_is_not_required(self):
        form = ItemForm({"name": "Test Todo Item"}) # create a variable of ItemForm to test
        self.assertTrue(form.is_valid()) # test whether the form is valid even without done being checked. (it should be as done isn't required)

    def test_fields_are_explicit_in_form_meta_class(self):
        form = ItemForm()
        self.assertEqual(form.Meta.fields, ['name', 'done'])