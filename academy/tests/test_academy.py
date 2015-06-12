from openerp.tests.common import TransactionCase
from openerp import SUPERUSER_ID
from openerp.exceptions import AccessError, except_orm
from psycopg2 import IntegrityError
import openerp
import os

class TestIssue(TransactionCase):
    
    def setUp(self):
        load_test = os.getenv('LOAD_TEST', 'all')
        load_test = load_test.split(',')
        if 'all' not in load_test:
            test_name = str(self).partition(" ")
            if test_name[0] not in load_test:
                raise self.skipTest(test_name[0])
        print "RUN TEST", test_name[0]
        super(TestIssue, self).setUp()
    
    
    def test_create_course(self):
        """ [TEST.ACADEMY] CREATE COURSE
        """
        user = self.browse_ref('academy.user_demo_academy_manager')
        manager = user.sudo(user.id)
        course_record = manager.env['academy.course'].create({'name' : 'Course Test'})
        self.assertEqual(course_record.name, 'Course Test', "Course name is wrong")
         
    def test_course_unique(self):
        """ [TEST.ACADEMY] Check duplicate constraints
        """
        self.env['academy.course'].create({'name' : 'course1',
                                           'responsible_id' : SUPERUSER_ID}) 
        with self.assertRaises(IntegrityError):
            self.env['academy.course'].create({'name' : 'course1'}) 
            
    def test_responsible_can_update_course(self):
        """ [TEST.ACADEMY] CAN UPDATE COURSE
        """
        course_record = self.browse_ref('academy.course02')
        course_record = course_record.sudo(course_record.responsible_id.id)
        course_record.description = "Autre"

        
    def test_simple_user_cannot_update_course(self):
        """ [TEST.ACADEMY] CANNOT UPDATE COURSE
        """
        
        course_record = self.browse_ref('academy.course02')
        not_responsible_user = self.browse_ref('academy.user_simple1')
        course_record = course_record.sudo(not_responsible_user.id)
        with self.assertRaises(AccessError):
            course_record.description = "Autre"