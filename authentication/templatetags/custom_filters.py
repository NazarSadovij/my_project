from django import template

register = template.Library()

@register.filter(name="add_class")
def add_class(field, css):
    """Додає CSS-клас(и) до віджета поля форми."""
    existing = field.field.widget.attrs.get("class", "")
    classes = (existing + " " + css).strip()
    return field.as_widget(attrs={"class": classes})

@register.filter(name="attr")
def attr(field, args):
    """
    Додає/змінює атрибут: {{ field|attr:"placeholder:Введіть значення" }}
    """
    key, _, value = args.partition(":")
    attrs = {key: value}
    return field.as_widget(attrs=attrs)
