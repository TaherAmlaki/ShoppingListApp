from flask_wtf import Form, FlaskForm
from wtforms import StringField, DecimalField, SubmitField, FieldList, FormField
from wtforms.validators import DataRequired, Length, Optional, ValidationError

from .models import ShoppingList


class AddItemForm(FlaskForm):
    item_name = StringField("Item Name", validators=[DataRequired(), Length(min=1, max=50)])
    price = DecimalField("Price", validators=[Optional()])
    shop = StringField("Shop Name", validators=[Optional(), Length(max=20)])


class AddShoppingListForm(FlaskForm):
    name = StringField("name", validators=[DataRequired(), Length(min=1, max=50)])
    items = FieldList(FormField(AddItemForm), min_entries=1)
    submit = SubmitField("Save")

    def validate_name(self, name):
        shopping_list = ShoppingList.find_by_name(name.data)
        if shopping_list is not None:
            raise ValidationError(f"Shopping list with name '{name.data}' already exists. "
                                  f"Please choose another name.")