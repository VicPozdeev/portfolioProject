from wagtail.models import Page
from wagtail.test.utils import WagtailPageTestCase

from portfolio.models import PortfolioPage


class PortfolioPageTests(WagtailPageTestCase):
    def setUp(self):
        Page.objects.get(id=2).delete()
        self.parent = Page.objects.get(id=1)
        self.page = PortfolioPage(
            title="Test page",
            slug="test-page",
        )
        self.parent.add_child(instance=self.page)

    def test_creatable(self):
        # Check if PortfolioPage can be created at Page
        self.assertCanCreateAt(Page, PortfolioPage)
        # Check if Page cannot be created at PortfolioPage
        self.assertCanNotCreateAt(PortfolioPage, Page)
        # Check if PortfolioPage cannot be created at another PortfolioPage
        self.assertCanNotCreateAt(PortfolioPage, PortfolioPage)

    def test_editable(self):
        # Check if the page is editable
        self.assertPageIsEditable(self.page)

    def test_previewable(self):
        # Check if the page is previewable
        self.assertPageIsPreviewable(self.page)

    def test_content_page_parent_pages(self):
        # Check the allowed parent page types for PortfolioPage
        self.assertAllowedParentPageTypes(
            PortfolioPage, {Page})
