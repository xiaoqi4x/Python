from django.db import models

# Create your models here.


# class Config(models.Model):
#     rack = models.CharField(primary_key=True, max_length=10, null=False)
#     baseline = models.CharField(max_length=50, null=False)
#     platform = models.CharField(max_length=20, null=True)
#     FTP = models.CharField(max_length=20, null=True)
#     username = models.CharField(max_length=10, null=True)
#     password = models.CharField(max_length=10, null=True)
#     ping = models.CharField(max_length=20, null=True)
#     browsing = models.CharField(max_length=20, null=True)
#     sim0_operator = models.CharField(max_length=4, null=True)
#     sim0_num = models.CharField(max_length=11, null=True)
#     sim0_ref = models.CharField(max_length=11, null=True)
#     sim1_num = models.CharField(max_length=11, null=True)
#     sim1_ref = models.CharField(max_length=11, null=True)
#     data_status = models.CharField(max_length=3, null=True)
