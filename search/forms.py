from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML


class SearchForm(forms.Form):
    query = forms.CharField(max_length=155, label=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.disable_csrf = True  # disable csrf_token for GET request [search process]
        self.helper.layout = Layout(
            Row(
                Column('query', css_class='form-group col-8 mb-0'),
                Column(
                    HTML(
                        '<button type="submit" class="btn btn-primary rounded"><i class="bi bi-search"></i>&nbsp;&nbsp;Search</button>'
                    ), css_class='col-4'
                )
            )
        )
