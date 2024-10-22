from odoo.tests.common import TransactionCase


class TestSupplierContactPerson(TransactionCase):

    def setUp(self):
        super(TestSupplierContactPerson, self).setUp()
        self.supplier = self.env['scm.supplier'].create({
            'name': 'Supplier 1',
        })

    def test_create_contact_person(self):
        """Test creation of a supplier contact person."""
        contact_person = self.env['scm.supplier_contact_person'].create({
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '1234567890',
            'position': 'Manager',
            'supplier_id1': self.supplier.id,
        })
        self.assertTrue(contact_person, "Supplier contact person")
