from django.db import models


class AttributeCategory(models.Model):
    attribute_id = models.PositiveBigIntegerField(blank=True, null=True)
    category_id = models.PositiveBigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'attribute_category'


class AttributeTranslations(models.Model):
    id = models.BigAutoField(primary_key=True)
    attribute_id = models.BigIntegerField()
    name = models.CharField(max_length=255)
    lang = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'attribute_translations'
        unique_together = (('id', 'name'),)


class Attributes(models.Model):
    id = models.BigAutoField(primary_key=True)
    branch_id = models.BigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=255)
    combination = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'attributes'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BranchTranslations(models.Model):
    id = models.BigAutoField(primary_key=True)
    branch_id = models.BigIntegerField()
    name = models.CharField(max_length=255)
    lang = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'branch_translations'
        unique_together = (('id', 'name'),)


class Branches(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'branches'


class BrandCategory(models.Model):
    brand_id = models.PositiveBigIntegerField(blank=True, null=True)
    category_id = models.PositiveBigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'brand_category'


class BrandTranslations(models.Model):
    id = models.BigAutoField(primary_key=True)
    brand_id = models.BigIntegerField()
    name = models.CharField(max_length=255)
    lang = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'brand_translations'
        unique_together = (('id', 'name'),)


class Brands(models.Model):
    name = models.CharField(max_length=255)
    logo = models.CharField(max_length=100, blank=True, null=True)
    top = models.IntegerField()
    slug = models.CharField(max_length=255, blank=True, null=True)
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'brands'


class Categories(models.Model):
    parent_id = models.IntegerField(blank=True, null=True)
    level = models.IntegerField()
    name = models.CharField(max_length=50)
    order_level = models.IntegerField()
    commision_rate = models.FloatField()
    banner = models.CharField(max_length=100, blank=True, null=True)
    icon = models.CharField(max_length=100, blank=True, null=True)
    featured = models.IntegerField()
    top = models.IntegerField()
    digital = models.IntegerField()
    slug = models.CharField(max_length=255, blank=True, null=True)
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)
    field_lft = models.PositiveIntegerField(db_column='_lft', blank=True, null=True)  # Field renamed because it started with '_'.
    field_rgt = models.PositiveIntegerField(db_column='_rgt', blank=True, null=True)  # Field renamed because it started with '_'.
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categories'
        unique_together = (('id', 'digital'),)


class CategoryTranslations(models.Model):
    id = models.BigAutoField(primary_key=True)
    category_id = models.BigIntegerField()
    name = models.CharField(max_length=255)
    lang = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'category_translations'


class CharacteristicTranslations(models.Model):
    id = models.BigAutoField(primary_key=True)
    characteristic_id = models.BigIntegerField()
    name = models.CharField(max_length=255)
    lang = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'characteristic_translations'
        unique_together = (('id', 'name'),)


class Characteristics(models.Model):
    id = models.BigAutoField(primary_key=True)
    attribute_id = models.PositiveBigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    slug = models.TextField(db_collation='utf8_unicode_ci')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'characteristics'


class ColorTranslations(models.Model):
    color_id = models.IntegerField()
    name = models.CharField(max_length=50)
    lang = models.CharField(max_length=10)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'color_translations'
        unique_together = (('id', 'name'),)


class Colors(models.Model):
    name = models.TextField(blank=True, null=True)
    code = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'colors'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class ElementTranslations(models.Model):
    id = models.BigAutoField(primary_key=True)
    element_id = models.BigIntegerField()
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    lang = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'element_translations'
        unique_together = (('id', 'element_id', 'name'),)


class Elements(models.Model):
    name = models.CharField(max_length=255)
    added_by = models.CharField(max_length=6)
    user_id = models.IntegerField()
    category_id = models.IntegerField(blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)
    brand_id = models.IntegerField(blank=True, null=True)
    photos = models.CharField(max_length=2000, blank=True, null=True)
    thumbnail_img = models.CharField(max_length=100, blank=True, null=True)
    video_provider = models.CharField(max_length=20, blank=True, null=True)
    video_link = models.CharField(max_length=100, blank=True, null=True)
    tags = models.CharField(max_length=1000, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    short_description = models.TextField(db_collation='utf8mb4_bin', blank=True, null=True)
    characteristics = models.TextField(blank=True, null=True)
    variations = models.TextField(blank=True, null=True)
    variation_attributes = models.TextField(blank=True, null=True)
    variation_colors = models.TextField(blank=True, null=True)
    todays_deal = models.IntegerField()
    published = models.IntegerField()
    featured = models.IntegerField()
    unit = models.CharField(max_length=20, blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    num_of_sale = models.IntegerField()
    meta_title = models.TextField(blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_img = models.CharField(max_length=255, blank=True, null=True)
    pdf = models.CharField(max_length=255, blank=True, null=True)
    slug = models.TextField()
    earn_point = models.FloatField()
    rating = models.FloatField()
    barcode = models.CharField(max_length=255, blank=True, null=True)
    digital = models.IntegerField()
    file_name = models.CharField(max_length=255, blank=True, null=True)
    file_path = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField()
    on_moderation = models.IntegerField()
    is_accepted = models.IntegerField()
    refundable = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'elements'
        unique_together = (('id', 'added_by', 'deleted_at'),)


class Products(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, blank=True, null=True)
    user_id = models.IntegerField()
    added_by = models.CharField(max_length=6, blank=True, null=True)
    currency_id = models.IntegerField(blank=True, null=True)
    price = models.FloatField()
    discount = models.FloatField(blank=True, null=True)
    discount_type = models.CharField(max_length=10, blank=True, null=True)
    discount_start_date = models.IntegerField(blank=True, null=True)
    discount_end_date = models.IntegerField(blank=True, null=True)
    variation_id = models.IntegerField(blank=True, null=True)
    todays_deal = models.IntegerField(blank=True, null=True)
    num_of_sale = models.IntegerField(blank=True, null=True)
    delivery_type = models.CharField(max_length=20, blank=True, null=True)
    qty = models.IntegerField()
    est_shipping_days = models.IntegerField(blank=True, null=True)
    low_stock_quantity = models.IntegerField(blank=True, null=True)
    published = models.IntegerField()
    approved = models.IntegerField()
    stock_visibility_state = models.CharField(max_length=10)
    cash_on_delivery = models.IntegerField()
    tax = models.FloatField(blank=True, null=True)
    tax_type = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    featured = models.IntegerField()
    seller_featured = models.IntegerField()
    refundable = models.IntegerField()
    on_moderation = models.IntegerField()
    is_accepted = models.IntegerField()
    digital = models.IntegerField()
    rating = models.FloatField()
    barcode = models.CharField(max_length=255, blank=True, null=True)
    earn_point = models.FloatField()
    element_id = models.IntegerField(blank=True, null=True)
    sku = models.CharField(max_length=255, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_quantity_multiplied = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'products'
        unique_together = (('id', 'name', 'user_id'),)


class Uploads(models.Model):
    file_original_name = models.CharField(max_length=255, blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    user_id = models.IntegerField()
    file_size = models.IntegerField(blank=True, null=True)
    extension = models.CharField(max_length=10, blank=True, null=True)
    model_type = models.CharField(max_length=15, blank=True, null=True)
    type = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'uploads'
        unique_together = (('id', 'user_id'),)


class VariationTranslations(models.Model):
    id = models.BigAutoField(primary_key=True)
    variation_id = models.BigIntegerField()
    name = models.CharField(max_length=255)
    lang = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'variation_translations'
        unique_together = (('id', 'name'),)


class Variations(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    lowest_price_id = models.IntegerField(blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True, null=True)
    partnum = models.CharField(max_length=255, blank=True, null=True)
    element_id = models.IntegerField()
    prices = models.TextField(blank=True, null=True)
    variant = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    short_description = models.TextField(db_collation='utf8mb4_bin', blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user_id = models.IntegerField()
    num_of_sale = models.IntegerField(blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    thumbnail_img = models.CharField(max_length=100, blank=True, null=True)
    photos = models.CharField(max_length=2000, blank=True, null=True)
    color_id = models.IntegerField(blank=True, null=True)
    characteristics = models.TextField(blank=True, null=True)
    deleted_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'variations'
        unique_together = (('id', 'user_id', 'deleted_at'),)
