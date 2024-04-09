from django.db import models


class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(verbose_name='title', max_length=50)
    description = models.TextField(blank=True)
    avatar = models.ImageField(blank=True, upload_to='categories/')
    is_enabled = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        # verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(verbose_name='title', max_length=50)
    description = models.TextField(blank=True)
    avatar = models.ImageField(blank=True, upload_to='products/')
    is_enabled = models.BooleanField(default=False)
    categories = models.ManyToManyField('Category', blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.title


class File(models.Model):
    FILE_AUDIO = 1
    FILE_VIDEO = 2
    FILE_PDF = 3
    FILE_TYPE = (
        (FILE_AUDIO, 'audio'),
        (FILE_VIDEO, 'video'),
        (FILE_PDF, 'pdf'),
    )
    file_type = models.PositiveSmallIntegerField('file type', choices=FILE_TYPE, default=FILE_VIDEO)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='files')
    title = models.CharField(max_length=50)
    file = models.FileField(upload_to='files/%Y/%m/%d')
    is_enabled = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'files'

    def __str__(self):
        return self.title
