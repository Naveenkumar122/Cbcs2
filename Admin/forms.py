from django import forms

class loginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30,widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(loginForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if not username and not password:
            raise forms.ValidationError('check username and password.')

class studentEditForm(forms.Form):
    Rollno = forms.CharField(max_length=20)
    Name = forms.CharField(max_length=50)
    Type = forms.CharField(max_length=70)
    Batch = forms.CharField(max_length=10)
    Department = forms.CharField(max_length=10)

    def clean(self):
        cleaned_data = super(studentEditForm,self).clean()
        Rollno = cleaned_data.get('Rollno')
        Name = cleaned_data.get('Name')
        Type = cleaned_data.get('Type')
        Batch = cleaned_data.get('Batch')
        Department = cleaned_data.get('Department')
        







