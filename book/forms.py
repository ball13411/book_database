from django import forms

class TestForm(forms.Form):
    Query = forms.CharField()

class login_userForm(forms.Form):
    Username = forms.CharField()

class login_passwordForm(forms.Form):
    Password = forms.CharField(widget=forms.PasswordInput)

# class insert_submitForm(forms.Form):
#     Password = forms.
table_CHOICES =(
    ("---","--------"),
    ("Books", "Books"),
    ("Authors", "Authors"),
    ("Locations", "Locations"),
    ("Publishers", "Publishers"),
    ("Sent_to", "Sent_to"),
    ("Write_to", "Write_to"),
)

class SelecttableForm(forms.Form):
    Select_Table = forms.ChoiceField(choices=table_CHOICES)
