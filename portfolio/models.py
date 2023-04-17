from django.db import models
from django.core.validators import FileExtensionValidator

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel
from modelcluster.fields import ParentalKey


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


class SocialButton(Orderable):
    name = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    svg = models.FileField(upload_to='svg',
                           validators=[FileExtensionValidator(['svg'])],
                           blank=True,
                           null=True)

    portfolio = ParentalKey(
        'portfolio.PortfolioPage',
        on_delete=models.CASCADE,
        related_name='social_buttons',
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
        FieldPanel('svg'),
    ]

    def __str__(self):
        return f'{self.name}: {self.url}'


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
        FieldRowPanel(
            [FieldPanel('social_button'),
             FieldPanel('account')]
        )
    ]


class PortfolioPage(Page):
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

    settings_panels = [
        MultiFieldPanel(
            [InlinePanel('social_buttons')],
            heading='Social buttons'
        ),
    ]
