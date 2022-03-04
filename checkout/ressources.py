# checkout.ressources.py

from import_export import resources
from import_export.fields import Field

from checkout.models import Checkout, RegisterCourse


class CheckoutBookResource(resources.ModelResource):

    id_checkout = Field(attribute="id_checkout", column_name="N° Commande")
    book = Field(attribute="book", column_name="Livre")
    price = Field(attribute="price", column_name="Prix (FRCFA)")
    first_name = Field(attribute="first_name", column_name="Nom")
    last_name = Field(attribute="last_name", column_name="Prénom")
    phone = Field(attribute="phone", column_name="N° de Téléphone 1")
    phone_two = Field(attribute="phone_two", column_name="N° de Téléphone 2")
    city = Field(attribute="city", column_name="Ville")
    country = Field(attribute="country", column_name="Pays")
    address = Field(attribute="address", column_name="Adresse de livraison")
    created_at = Field(attribute="created_at", column_name="Date de la commande")

    class Meta:
        model = Checkout
        fields = (
            "id_checkout", "book", "price",
            "first_name", "last_name",
            "phone", "phone_two",
            "city", "country",
            "address", "created_at",
        )
        export_order = fields

    def dehydrate_id_checkout(self, obj):
        return str(obj.id_checkout)

    def dehydrate_price(self, obj):
        return str(obj.book.price)

    def dehydrate_created_at(self, obj):
        return obj.created_at.strftime("%d-%m-%Y")
