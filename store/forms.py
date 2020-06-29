from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class RatingForms(forms.Form):

	rating = forms.IntegerField(help_text="Enter ratings from 1 to 10 (10 being the best)")

	def clean_rating (self):
		
		data=self.cleaned_data['rating']

		if data<1 or data>10 :
			raise ValidationError(_('Invalid rating'))

		else :
			return True

class SignupForms(UserCreationForm):

	first_name=forms.CharField(max_length=30,required=True,help_text="Enter your first name")
	last_name=forms.CharField(max_length=30,required=False,help_text="Enter your last name (optional)")
	email=forms.EmailField(max_length=256,required=True,help_text="Enter your email address")

	class Meta:
		model=User
		fields=('username','password','first_name','last_name','email')
	