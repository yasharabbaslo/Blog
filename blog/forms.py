from django import forms
from .models import Comment, Newsletter, Message


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        widgets = {
            'name': forms.TextInput(attrs={
                                    'class':"form-control", 
                                    'placeholder':"Enter Name", 
                                    'onfocus':"this.placeholder = ''", 
                                    'onblur':"this.placeholder = 'Enter Name'"
                                    }),
            'email': forms.EmailInput(attrs={
                                    'class':"form-control", 
                                    'placeholder':"Enter email address", 
                                    'onfocus':"this.placeholder = ''", 
                                    'onblur':"this.placeholder = 'Enter email address'"
                                    }),
            'body': forms.Textarea(attrs={
                                    'class':"form-control mb-10", 
                                    'rows':"5", 
                                    'placeholder':"Messege", 
                                    'onfocus':"this.placeholder = ''", 
                                    'onblur':"this.placeholder = 'Messege'"
                                    })
        }


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput(attrs={
                                    'class':"form-control", 
                                    'id':"inlineFormInputGroup", 
                                    'placeholder':"Enter email", 
                                    'onfocus':"this.placeholder = ''", 
                                    'onblur':"this.placeholder = 'Enter email'"
                                    })
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('name', 'email', 'subject', 'body')
        widgets = {
            'name': forms.TextInput(attrs={
                                    'class':"form-control", 
                                    'placeholder':"Enter your name",                                    
                                    }),
            'email': forms.EmailInput(attrs={
                                    'class':"form-control", 
                                    'placeholder':"Enter email address",                                    
                                    }),
            'subject': forms.TextInput(attrs={
                                    'class':"form-control", 
                                    'placeholder':"Enter Subject",                                    
                                    }),
            'body': forms.Textarea(attrs={
                                    'class':"form-control different-control w-100", 
                                    'rows':"5", 
                                    'cols':"30",
                                    'placeholder':"Enter messege",                                    
                                    })
        }


class SearchForm(forms.Form):
    query = forms.CharField()