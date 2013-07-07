from django.forms import ModelForm, Form, FileField
from django.contrib.localflavor.us.forms import USSocialSecurityNumberField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Fieldset, Hidden, Field
from crispy_forms.bootstrap import FormActions, AppendedPrependedText, AppendedText
from task_manager.models import Task, WorkProject, Ticket


class NewTask(ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewTask, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = '#'
        self.helper.layout = Layout(
            Fieldset('Create Task', 
                     'title',
                     'user',
                     'project',
                     'task_type',
                     'scheduled_date',
                     'start_time',
                     'end_time'),
            Hidden('time_specific', False),
            Hidden('completion', False),
            FormActions(
                Submit('submit', 'Submit', css_class='button white')
            )
        )

    class Meta:
        model = Task


class NewWorkProject(ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewWorkProject, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = '#'
        self.helper.layout = Layout(
            Fieldset('Create Project',
                     'title',
                     Field('start_date'),
                     Field('due_date'),
                     'status',
                     'project_type',
                     'copy_link',
                     'final_link'),
            FormActions(
                Submit('submit', 'Submit', css_class='button white')
            )
        )

    class Meta:
        model = WorkProject


class NewTicket(ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewTicket, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = '#'
        self.helper.layout = Layout(
            Fieldset('Create Project',
                     'title',
                     Field('description', css_class='input-block-level'),
                     'project_type',

                     ),
            FormActions(
                Submit('submit', 'Submit', css_class='button white')
            )
        )

    class Meta:
        model = Ticket


class NewEmail(ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewEmail, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = '#'
        self.helper.layout = Layout(
            Field('subject', css_class="input-block-level"),
            Field('body', css_class="input-block-level"),
            Hidden('completion', True),
            FormActions(
                Submit('submit', 'Send', css_class='button white')
            )
        )

    class Meta:
        model = Task
