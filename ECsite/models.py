from django.db import models

class BaseInfo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    #Meta内で設定
    class Meta:
        abstract = True # テーブルを作らない抽象クラス

class Items(BaseInfo):
    name = models.CharField(max_length=30, unique=True)
    price = models.IntegerField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='items/',blank=True)

    def __str__(self):
        return self.name