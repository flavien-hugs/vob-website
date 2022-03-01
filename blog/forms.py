# blog.forms.py

from django import forms

from blog.models import Comment


class CommentForm(forms.ModelForm):

    parent_comment_id = forms.IntegerField(
        widget=forms.HiddenInput, required=False
    )

    class Meta:
        model = Comment
        fields = ["name", "email", "content"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control shadow-none'})
