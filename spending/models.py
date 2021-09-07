from django.db import models


# Create your models here.
class Spending(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.ForeignKey('SpendingType', on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        verbose_name = 'Трата'
        verbose_name_plural = "Траты"

    def __str__(self):
        return f'{self.type} {self.amount}'



class SpendingType(models.Model):
    type = models.TextField(max_length=256)
    subtype = models.TextField(max_length=256, default="", blank=True)


    class Meta:
        verbose_name = 'Тип траты'
        verbose_name_plural = "Типы трат"
        constraints = [models.UniqueConstraint(fields=['type', 'subtype'], name='type-subtype constraint')]

    def __str__(self):
        return f'{self.type} {self.subtype}'
