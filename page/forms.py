# page.forms.py

from django import forms

from page.models import Contact


CHOICE_OBJECT_TYPES = (
    ("Je veux annuler une commande", "Je veux annuler une commande"),
    ("Mon article n'a pas été livré", "Mon article n'a pas été livré"),
    ("J'aimerais signaler une erreur", "J'aimerais signaler une erreur"),
    ("Rendre un témoignage sur l'achat", "Rendre un témoignage sur l'achat"),
    ("J'ai un problème avec le paiement", "J'ai un problème avec le paiement"),
    ("Je veux être un partenaire de Made In Gbeke.", "Je veux être un partenaire de Made In Gbeke."),
)


class ContactForm(forms.ModelForm):
    
    name = forms.CharField(
        max_length=150,
        required=True,
        label="Nom & prénom",
        widget=forms.TextInput(),
    )
    email = forms.EmailField(
        max_length=150,
        required=True,
        label="Adresse e-mail",
        widget=forms.EmailInput(),
    )
    reason = forms.ChoiceField(
        required=True,
        choices=CHOICE_OBJECT_TYPES,
        widget=forms.Select(),
    )
    message = forms.CharField(
        required=True,
        label="Saisir votre message ici.",
        widget=forms.Textarea(attrs={"rows": 5}),
    )

    class Meta:
        model = Contact
        fields = [
            "name",
            "email", "phone",
            "reason", "message"
        ]

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control shadow-none'

            if self.fields['reason']:
                self.fields['reason'].widget.attrs.update(
                    {'class': 'form-control custom-select'}
                )
