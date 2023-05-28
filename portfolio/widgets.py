from django.forms.widgets import ClearableFileInput, TextInput, Select


class SvgFileInput(ClearableFileInput):
    template_name = 'widgets/svg_file.html'


class AccountInput(TextInput):
    template_name = 'widgets/account_input.html'


class SocialButtonSelect(Select):
    option_template_name = 'widgets/social_button_select_option.html'
