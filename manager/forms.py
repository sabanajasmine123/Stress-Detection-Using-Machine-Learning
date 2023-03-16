from django import forms


class Subscribe(forms.Form):
    Email = forms.EmailField()
    def _str_(self):
        return self.Email