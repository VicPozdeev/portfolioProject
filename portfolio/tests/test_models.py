from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.translation import gettext_lazy as _
from wagtail.models import Page
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.html import format_html

from portfolio.models import Skill, Work, SocialButton, SocialAccount, PortfolioPage


class BaseTestCase(TestCase):
    def setUp(self):
        Page.objects.get(id=2).delete()
        self.parent = Page.objects.get(id=1)
        self.page = PortfolioPage(
            title="Test page",
            slug="test-page",
        )
        self.parent.add_child(instance=self.page)


class SkillModelTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.skill = Skill.objects.create(
            caption='Test Skill',
            portfolio=self.page,
        )

    def test_skill_str_method(self):
        # Check the __str__ method
        self.assertEqual(str(self.skill), 'Test Skill')

    def test_skill_stars_field_default_value(self):
        # Check the default value of the stars field
        self.assertEqual(self.skill.stars, 0)
        self.skill.full_clean()

    def test_skill_stars_negative_value(self):
        # Check validation for negative stars value
        self.skill.stars = -1
        with self.assertRaises(ValidationError):
            self.skill.full_clean()

    def test_skill_stars_greater_than_max_value(self):
        # Check validation for stars value greater than the max value
        self.skill.stars = 6
        with self.assertRaises(ValidationError):
            self.skill.full_clean()


class WorkModelTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.work = Work.objects.create(
            caption='Test work',
            portfolio=self.page,
        )

    def test_work_str_method(self):
        # Check the __str__ method
        self.assertEqual(str(self.work), 'Test work')


class SocialButtonModelTest(TestCase):
    def setUp(self):
        self.social_button = SocialButton.objects.create(
            name='Test',
            url='https://test.com/',
            svg=SimpleUploadedFile('test.svg', b'')
        )

    def test_social_button_svg_field(self):
        # Check the allowed extensions for the svg field
        field = SocialButton._meta.get_field('svg')
        self.assertEqual(field.validators[0].allowed_extensions, ['svg'])

    def test_social_button_str_method(self):
        # Check the __str__ method
        self.assertEqual(str(self.social_button), 'Test: https://test.com/')

    def test_social_button_full_clean_method(self):
        # Check the full_clean method
        # Expect that calling full_clean() does not raise a ValidationError
        self.social_button.full_clean()

        # Ensure that when attempting to enter an invalid URL, the application raises a
        # ValidationError with the correct error message.
        self.social_button.url = 'not_a_valid_url'
        with self.assertRaisesMessage(
                ValidationError,
                str(_('Enter a valid URL.')),  # Error message in different languages
        ):
            self.social_button.full_clean()

    def test_icon_method_returns_html(self):
        # Test that the 'icon' method returns HTML code that contains the correct CSS styles
        # and the URL of the 'svg' file as a background image.
        expected_html = format_html(
            '<span style="'
            'background: url({}) no-repeat;'
            'border-style: none;'
            'width: 2.5rem;'
            'height: 2.5rem;'
            'padding: 0;'
            'background-size: contain;'
            'display: block;'
            '"></span>',
            self.social_button.svg.url
        )
        self.assertEqual(self.social_button.icon(), expected_html)

    def test_icon_method_without_svg(self):
        # Test that the 'icon' method returns None when 'svg' is not set.
        self.social_button.svg.delete()
        self.assertEqual(self.social_button.icon(), None)


class SocialAccountModelTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.social_button = SocialButton.objects.create(
            name='Test',
            url='https://test.com/',
        )
        self.social_account = SocialAccount.objects.create(
            social_button=self.social_button,
            account='id12345',
            portfolio=self.page,
        )

    def test_social_account_str_method(self):
        # Check the __str__ method
        self.assertEqual(str(self.social_account), 'Test - https://test.com/id12345')
