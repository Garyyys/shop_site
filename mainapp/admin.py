from PIL import Image

from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.contrib import admin
from mainapp.models import *
from django.utils.safestring import mark_safe




class NotebookAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe(f'<span style="color:red">'
        f' Изображение не должно быть меньше '
        f'{Product.MIN_RESOLUTION[0]}х{Product.MIN_RESOLUTION[1]} '
        f'и больше {Product.MAX_RESOLUTION[0]}х{Product.MAX_RESOLUTION[1]}'
                                                   f'</span>'
        )

    def clean_image(self):
        image = self.cleaned_data['image']
        img = Image.open(image)
        min_height, min_width = self.MIN_RESOLUTION
        max_height, max_width = self.MAX_RESOLUTION
        if image.size > Product.MAX_IMAGE_SIZE:
            raise ValidationError('Размер слишком большой, не больше 3 MB')
        if img.height < min_height or img.width < min_width:
            raise ValidationError('Изображение слишком маленькое')
        if img.height > max_height or img.width > max_width:
            raise ValidationError('Изображение слишком большое')
        return image

class NotebookAdmin(admin.ModelAdmin):

    form = NotebookAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug=
                                                                  'notebooks'))


class SmartphoneAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug=
                                                                'smartphones'))


admin.site.register(Category)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
