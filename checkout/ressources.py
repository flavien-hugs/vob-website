# checkout.ressources.py

from import_export import resources
from import_export.fields import Field

from checkout.models import Checkout, RegisterCourse


class CheckoutBookResource(resources.ModelResource):

    id_checkout = Field(attribute="id_checkout", column_name="N° Commande")
    payment = Field(attribute="payment", column_name="Moyen de paiement")
    transaction_number = Field(
        attribute="transaction_number",
        column_name="Numéro de la Transaction")
    transaction_code = Field(
        attribute="transaction_code",
        column_name="ID de la Transaction")
    book = Field(attribute="book", column_name="Livre")
    price = Field(attribute="price", column_name="Prix (FRCFA)")
    first_name = Field(attribute="first_name", column_name="Nom")
    last_name = Field(attribute="last_name", column_name="Prénom")
    phone = Field(attribute="phone", column_name="N° de Téléphone 1")
    phone_two = Field(attribute="phone_two", column_name="N° de Téléphone 2")
    city = Field(attribute="city", column_name="Ville")
    country = Field(attribute="country", column_name="Pays")
    address = Field(attribute="address", column_name="Adresse de livraison")
    date_added = Field(attribute="date_added", column_name="Date de la commande")

    class Meta:
        model = Checkout
        fields = (
            "id_checkout",
            "payment", "transaction_number",
            "transaction_code",
            "book", "price",
            "first_name", "last_name",
            "phone", "phone_two",
            "city", "country",
            "address", "date_added",
        )
        export_order = fields

    def dehydrate_id_checkout(self, obj):
        return str(obj.id_checkout)

    def dehydrate_book(self, obj):
        return str(obj.book.name)

    def dehydrate_price(self, obj):
        return str(obj.book.price)

    def dehydrate_date_added(self, obj):
        return obj.date_added.strftime("%d-%m-%Y")


class RegisterCourseBookResource(resources.ModelResource):

    id_checkout = Field(attribute="id_checkout", column_name="ID Inscription")
    course = Field(attribute="course", column_name="Formation")
    price = Field(attribute="price", column_name="Prix (FRCFA)")
    first_name = Field(attribute="first_name", column_name="Nom")
    last_name = Field(attribute="last_name", column_name="Prénom")
    phone = Field(attribute="phone", column_name="N° de Téléphone 1")
    phone_two = Field(attribute="phone_two", column_name="N° de Téléphone 2")
    option = Field(attribute="option", column_name="Type de la formation")
    date_of_course = Field(attribute="date_of_course", column_name="Début de la formation")
    date_added = Field(attribute="date_added", column_name="Date d'Inscription")

    class Meta:
        model = RegisterCourse
        fields = (
            "id_checkout", "course", "price",
            "first_name", "last_name",
            "phone", "phone_two",
            "option", "date_of_course",
            "date_added",
        )
        export_order = fields

    def dehydrate_id_checkout(self, obj):
        return str(obj.id_checkout)

    def dehydrate_course(self, obj):
        return str(obj.course.name)

    def dehydrate_price(self, obj):
        return str(obj.course.price)

    def dehydrate_option(self, obj):
        return str(obj.course.option)

    def dehydrate_date_added(self, obj):
        return obj.date_added.date()

    def dehydrate_date_of_course(self, obj):
        return obj.course.date_of_course.date()
