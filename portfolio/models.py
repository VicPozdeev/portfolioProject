from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.html import format_html
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page, Orderable

from .widgets import SvgFileInput, AccountInput, SocialButtonSelect


class Skill(Orderable):
    STARS_QUANTITY_CHOICES = [(i, str(i)) for i in range(0, 6)]

    figure = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    caption = models.CharField(max_length=70, blank=True, null=True)
    stars = models.IntegerField(choices=STARS_QUANTITY_CHOICES, default=0)

    portfolio = ParentalKey(
        'portfolio.PortfolioPage',
        on_delete=models.CASCADE,
        related_name='skills',
    )

    panels = [
        FieldPanel('figure'),
        FieldPanel('caption'),
        FieldPanel('stars'),
    ]

    def __str__(self):
        return self.caption or str(self.figure)

    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"


class Work(Orderable):
    figure = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    caption = models.CharField(max_length=250, blank=True, null=True)

    portfolio = ParentalKey(
        'portfolio.PortfolioPage',
        on_delete=models.CASCADE,
        related_name='works',
    )

    panels = [
        FieldPanel('figure'),
        FieldPanel('caption'),
    ]

    def __str__(self):
        return self.caption or str(self.figure)

    class Meta:
        verbose_name = "Work"
        verbose_name_plural = "Works"


class SocialButton(Orderable):
    name = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    svg = models.FileField(upload_to='svg',
                           validators=[FileExtensionValidator(['svg'])],
                           blank=True,
                           null=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
        FieldPanel('svg', widget=SvgFileInput),
    ]

    def __str__(self):
        return f"{self.name}: {self.url}"

    class Meta:
        verbose_name = "Social button"
        verbose_name_plural = "Social buttons"

    def icon(self):
        if self.svg:
            return format_html(
                '<span style="'
                'background: url({}) no-repeat;'
                'border-style: none;'
                'width: 2.5rem;'
                'height: 2.5rem;'
                'padding: 0;'
                'background-size: contain;'
                'display: block;'
                '"></span>',
                self.svg.url
            )


class SocialAccount(Orderable):
    social_button = models.ForeignKey(
        SocialButton,
        on_delete=models.CASCADE,
        related_name='social_buttons'
    )
    account = models.CharField(max_length=255, blank=True, null=True)

    portfolio = ParentalKey(
        'portfolio.PortfolioPage',
        on_delete=models.CASCADE,
        related_name='social_accounts',
    )

    panels = [
        FieldPanel('social_button', widget=SocialButtonSelect),
        FieldPanel('account', widget=AccountInput)
    ]

    def __str__(self):
        return f"{self.social_button.name} - {self.social_button.url}{self.account}"

    class Meta:
        verbose_name = "Social button"
        verbose_name_plural = "Social buttons"


class PortfolioPage(Page):
    parent_page_types = ['wagtailcore.Page']
    subpage_types = []
    max_count = 1

    first_name = models.CharField(max_length=35, blank=True, null=True)
    last_name = models.CharField(max_length=35, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    photo = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    profession = models.CharField(max_length=100, blank=True, null=True)
    short_info = models.CharField(max_length=100, blank=True, null=True)
    about_me = RichTextField(
        features=['h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                  'bold', 'italic', 'ol', 'ul', 'link'],
        blank=True,
        null=True,
    )
    skills_top_text = models.TextField(blank=True, null=True)
    contacts_cta = models.TextField(blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('first_name'),
        FieldPanel('last_name'),
        FieldPanel('photo'),
        FieldPanel('profession'),
        FieldPanel('short_info'),
        FieldPanel('about_me'),
        FieldPanel('skills_top_text'),
        MultiFieldPanel(
            [InlinePanel('skills')],
            heading='Skills'
        ),
        MultiFieldPanel(
            [InlinePanel('works')],
            heading='Works'
        ),
        FieldPanel('contacts_cta'),
        FieldPanel('email'),
        MultiFieldPanel(
            [InlinePanel('social_accounts')],
            heading='Social accounts'
        ),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Portfolio page"
