from openerp.tests.common import TransactionCase
from psycopg2 import IntegrityError


class TestIssue(TransactionCase):
    
    
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
        partner = self.env['res.partner'].search([])[0]
        self.env['academy.course'].create({'name' : 'course1',
                                           'responsible_id' : partner.id}) 
        with self.assertRaises(IntegrityError):
            self.env['academy.course'].create({'name' : 'course1'}) 