from django.test import TestCase
from .models import Skill, SkillArea

class SkillModelTest(TestCase):
    def setUp(self):
        self.area = SkillArea.objects.create(name="Backend")
        self.skill = Skill.objects.create(
            area=self.area,
            name="Python",
            sfia_level="L3",
            description="Python development"
        )
    
    def test_skill_creation(self):
        self.assertEqual(self.skill.name, "Python")
        self.assertEqual(self.skill.sfia_level, "L3")
    
    def test_slug_generation(self):
        self.assertIsNotNone(self.skill.slug)