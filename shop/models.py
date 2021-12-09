from django.db import models
from django.shortcuts import reverse
from django.utils.html import mark_safe

from .managers import TagManager, MacaronManager, MacaronImageManager, MacaronSetManager,\
    MacaronCollectionItemManager, MacaronCollectionManager, MacaronCollectionImageManager


TAG_CHOICES = (
    ('Vegan', 'Vegan'),
    ('Gluten Free', 'Gluten Free'),
    ('Halal', 'Halal'),
    ('Nut Free', 'Nut Free')
)


class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    name = models.CharField(max_length=40, choices=TAG_CHOICES, unique=True)
    slug = models.SlugField(blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TagManager()

    def __str__(self) -> str:
        return f"{self.name}"

    def save(self, *args, **kwargs):
        # if tag is set to inactive, remove tag from association with macaron
        if not self.active:
            self.macaron_set.clear()
        super(Tag, self).save(*args, **kwargs)


class Macaron(models.Model):
    class Meta:
        verbose_name = 'Macaron'
        verbose_name_plural = 'Macarons'

    name = models.CharField(max_length=120)
    description = models.TextField(max_length=5000)
    tags = models.ManyToManyField(Tag, limit_choices_to={"active": True}, blank=True)
    active = models.BooleanField(default=True)
    slug = models.SlugField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MacaronManager()

    def __str__(self) -> str:
        return f"{self.name}"

    def get_macaron_tags(self):
        output = ''
        for item in self.tags.all():
            output += f"<li>{item.name}</li>"
        return mark_safe(output)
        # Output tags in a single line separated by a ','
        # for index, item in enumerate(self.tags.all()):
        #     output += item.name
        #     if index != len(self.tags.all()) - 1:
        #         output += ', '
        # return output

    get_macaron_tags.short_description = 'Tags'

    def get_short_description(self):
        return self.description.split('.')[0]


class MacaronImage(models.Model):
    class Meta:
        verbose_name = 'Macaron Image'
        verbose_name_plural = 'Macaron Images'

    macaron = models.ForeignKey(Macaron, on_delete=models.CASCADE, related_name='images')
    picture = models.ImageField(upload_to='macarons/images/')
    alt_text = models.CharField(max_length=120)
    caption = models.TextField(max_length=5000)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MacaronImageManager()

    def __str__(self):
        return f"{self.macaron.name}'s Image"


class MacaronSet(models.Model):
    class Meta:
        verbose_name = 'Macaron Set'
        verbose_name_plural = 'Macaron Sets'

    macaron = models.ForeignKey(Macaron, on_delete=models.CASCADE, limit_choices_to={"active": True})
    quantity = models.IntegerField(default=6, help_text="Number of macarons per box.")
    price = models.DecimalField(max_digits=5, decimal_places=2,
                                help_text="Price of <b>each</b> macaron. <b>NOT</b> price of entire box.")
    sale_price = models.DecimalField(max_digits=5, decimal_places=2, default=0.0,
                                     help_text="Price of <b>each</b> macaron. <b>NOT</b> price of entire box.")
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    slug = models.SlugField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MacaronSetManager()

    def __str__(self) -> str:
        return f"{self.macaron.name} | {self.quantity} for ${self.get_total()}"

    def get_absolute_url(self):
        return reverse('shop:set_detail', kwargs={'slug': self.slug})

    def get_name(self) -> str:
        return f"{self.macaron.name}"

    get_name.short_description = "Macaron"

    def get_all_images(self):
        return self.macaron.images.all()

    def get_featured_image(self):
        return self.macaron.images.featured()

    def get_description(self):
        return f"{self.macaron.description}"

    # Get the price of each maracon
    @property
    def get_price(self):
        if self.sale_price < self.price and self.sale_price != 0:
            return self.sale_price
        return self.price

    def get_original_price(self):
        return self.quantity * self.price

    def display_price(self):
        if self.is_on_sale():
            return mark_safe(
                f"<span style='color:#b53211;'>&nbsp;${self.get_total()}</span> &nbsp;")
        else:
            return mark_safe(f"<span>${self.get_total()}</span>")

    def is_on_sale(self):
        if self.sale_price < self.price and self.sale_price != 0:
            return True
        return False

    # Get price of the macarons and the final price (original price or sale price)
    def get_total(self):
        return self.quantity * self.get_price

    def display_total(self):
        if self.is_on_sale():
            return mark_safe(
                f"<span class='price' style='font-size:18px;text-decoration:line-through;'>&nbsp;${self.get_original_price()}&nbsp;</span> &nbsp;"
                f"<span class='price' style='font-size:20px;color:#91363d;'>${self.get_total()}</span>")
        else:
            return mark_safe(f"<span class='price' style='font-size:20px;'>${self.get_total()}</span>")

    def admin_get_price(self):
        return self.price

    admin_get_price.short_description = "Price - Each"

    def admin_sale_price(self):
        if self.sale_price > 0:
            return mark_safe(f"<span style='font-weight:bold; color:#fb523b;'>${self.sale_price}</span>")
        return '-'

    admin_sale_price.short_description = "Sale Price - Each"

    def admin_get_total(self):
        if self.sale_price > 0:
            return mark_safe(f"<span style='font-weight:bold;font-size:14px;color:#fb523b;'>${self.get_total()}</span>")
        return mark_safe(f"<span style='font-weight:bold;font-size:14px;'>${self.get_total()}</span>")

    admin_get_total.short_description = mark_safe(
        "<span style='text-decoration:underline;'>Set Total Price</span>"
    )


class MacaronCollectionItem(models.Model):
    class Meta:
        verbose_name = 'Macaron Collection Item'
        verbose_name_plural = 'Macaron Collection Items'

    macaron = models.ForeignKey(Macaron, on_delete=models.CASCADE, limit_choices_to={"active": True})
    quantity = models.IntegerField(default=3)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MacaronCollectionItemManager()

    def __str__(self) -> str:
        return f"{self.macaron.name}"

    def admin_collection_list(self) -> str:
        output = ""
        for collection in self.macaroncollection_set.all():
            output += f"<li>{collection.name}</li>"
        return mark_safe(output)

    admin_collection_list.short_description = "In Collections"


class MacaronCollection(models.Model):
    class Meta:
        verbose_name = 'Macaron Collection'
        verbose_name_plural = 'Macaron Collections'

    name = models.CharField(max_length=120)
    macarons = models.ManyToManyField(MacaronCollectionItem, limit_choices_to={"active": True})
    description = models.TextField(max_length=5000)
    price = models.DecimalField(max_digits=5, decimal_places=2, help_text="Price for entire collection.")
    sale_price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00,
                                     help_text="Discounted price for entire collection.")
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    slug = models.SlugField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MacaronCollectionManager()

    def __str__(self) -> str:
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('shop:collection_detail', kwargs={'slug': self.slug})

    def get_name(self) -> str:
        return self.name

    def get_all_images(self):
        return self.images.all()

    def get_featured_image(self):
        return self.images.featured()

    def get_description(self) -> str:
        return self.description

    def get_short_description(self) -> str:
        return self.description.split('.')[0]

    def get_macaron_list(self) -> str:
        output = ''
        for item in self.macarons.all():
            output += f"{item.macaron.name} &nbsp;(<b>{item.quantity}</b>)<br />"
        return mark_safe(output)

    get_macaron_list.short_description = "Macaron List"

    # Get the price of the collection (original price or sale price)
    @property
    def get_price(self):
        if self.is_on_sale():
            return self.sale_price
        return self.price

    def get_original_price(self):
        return self.price

    def get_total(self):
        return self.get_price

    def display_price(self):
        if self.is_on_sale():
            return mark_safe(f"<span style='color:#b53211;'>${self.get_total()}</span>")
        else:
            return mark_safe(f"<span>${self.get_total()}</span>")

    def display_total(self):
        if self.is_on_sale():
            return mark_safe(
                f"<span class='price' style='font-size:18px;text-decoration:line-through;'>&nbsp;${self.get_original_price()}&nbsp;</span> &nbsp;"
                f"<span class='price' style='font-size:20px;color:#91363d;'>${self.get_total()}</span>")
        else:
            return mark_safe(f"<span class='price' style='font-size:20px;'>${self.get_total()}</span>")

    def is_on_sale(self):
        if self.sale_price < self.price and self.sale_price != 0:
            return True
        return False

    def get_quantity_each_collection(self):
        total_macarons = 0
        for macaron in self.macarons.all():
            total_macarons += macaron.quantity
        return total_macarons

    def admin_sale_price(self):
        if self.sale_price > 0:
            return mark_safe(f"<span style='color:#fb523b;'>${self.sale_price}</span>")
        return '-'

    admin_sale_price.short_description = "Sale Price"

    def admin_get_total(self):
        if self.sale_price > 0:
            return mark_safe(f"<span style='font-weight:bold;font-size:14px;color:#fb523b;'>${self.get_total()}</span>")
        return mark_safe(f"<span style='font-weight:bold;font-size:14px;'>${self.get_total()}</span>")

    admin_get_total.short_description = mark_safe("<u>Collection Total</u>")


class MacaronCollectionImage(models.Model):
    class Meta:
        verbose_name = 'Macaron Collection Image'
        verbose_name_plural = 'Macaron Collection Images'

    collection = models.ForeignKey(MacaronCollection, on_delete=models.CASCADE, related_name='images')
    picture = models.ImageField(upload_to='macarons/images/collection/')
    alt_text = models.CharField(max_length=120)
    caption = models.TextField(max_length=5000)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MacaronCollectionImageManager()

    def __str__(self):
        return f"{self.collection.name}'s Image"

