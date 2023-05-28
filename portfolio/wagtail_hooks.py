from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail import hooks
from .models import SocialButton


@hooks.register("register_icons")
def register_icons(icons):
    return icons + ['svg/users-solid.svg']


class SocialButtonAdmin(ModelAdmin):
    model = SocialButton
    base_url_path = 'social-buttons'  # customise the URL from default to admin/bookadmin
    menu_label = 'Social buttons'  # ditch this to use verbose_name_plural from model
    menu_icon = 'users-solid'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    list_display = ('name', 'url', 'icon')


modeladmin_register(SocialButtonAdmin)
