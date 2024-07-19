from django.db import models


class Fruit(models.Model):
    name = models.CharField(max_length=20)
    color = models.ForeignKey(
        "Color",
        blank=True,
        null=True,
        related_name="fruits",
        on_delete=models.CASCADE,
    )
# class Fruit(models.Model):
#     id = '1'
#     name = 'AAA'
#     color = 'red'


class Color(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        managed = True
        db_table = 'color'
