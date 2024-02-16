# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

## edward_miRNA
class HsaMir29A3P(models.Model):
    gene_name = models.CharField(max_length=15, blank=True, null=True)
    gene_id = models.CharField(max_length=15, blank=True, null=True)
    mirna_name = models.CharField(max_length=14, blank=True, null=True)
    mirna_id = models.CharField(max_length=12, blank=True, null=True)
    experiments = models.IntegerField(blank=True, null=True)
    publications = models.IntegerField(blank=True, null=True)
    cell_lines = models.IntegerField(blank=True, null=True)
    micro_tscore = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hsa-miR-29a-3p'


class HsaMir29A5P(models.Model):
    gene_name = models.CharField(max_length=15, blank=True, null=True)
    gene_id = models.CharField(max_length=15, blank=True, null=True)
    mirna_name = models.CharField(max_length=14, blank=True, null=True)
    mirna_id = models.CharField(max_length=12, blank=True, null=True)
    experiments = models.IntegerField(blank=True, null=True)
    publications = models.IntegerField(blank=True, null=True)
    cell_lines = models.IntegerField(blank=True, null=True)
    micro_tscore = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hsa-miR-29a-5p'

## default
# the most useful in default database
class Hg38GeneTranscripts20180130(models.Model):
    gene = models.CharField(primary_key=True, max_length=100)
    transcripts = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hg38_gene_transcripts_20180130'

class MutualRelationshipSearch3(models.Model):
    no = models.IntegerField(db_column='No', primary_key=True)  # Field name made lowercase.
    primary_site = models.CharField(max_length=100, blank=True, null=True)
    project = models.CharField(max_length=100, blank=True, null=True)
    condition1 = models.CharField(max_length=100, blank=True, null=True)
    condition2 = models.CharField(max_length=100, blank=True, null=True)
    genes = models.CharField(max_length=100, blank=True, null=True)
    isoforms = models.CharField(max_length=100, blank=True, null=True)
    field_of_normal = models.CharField(db_column='#_of_normal', max_length=100)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_of_stage_1 = models.CharField(db_column='#_of_stage_1', max_length=100)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_of_stage_2 = models.CharField(db_column='#_of_stage_2', max_length=100)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_of_stage_3 = models.CharField(db_column='#_of_stage_3', max_length=100)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_of_stage_4 = models.CharField(db_column='#_of_stage_4', max_length=100)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_of_stage_5 = models.CharField(db_column='#_of_stage_5', max_length=100)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_of_nos = models.CharField(db_column='#_of_nos', max_length=100)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_of_is = models.CharField(db_column='#_of_is', max_length=100)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_of_tumor = models.CharField(db_column='#_of_tumor', max_length=100)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'Mutual_Relationship_search3'

class MutualRelationship(models.Model):
    no = models.IntegerField(db_column='No', primary_key=True)  # Field name made lowercase.
    primary_site = models.CharField(max_length=100, blank=True, null=True)
    project = models.CharField(max_length=100, blank=True, null=True)
    condition1 = models.CharField(max_length=100, blank=True, null=True)
    condition2 = models.CharField(max_length=100, blank=True, null=True)
    genes = models.CharField(max_length=100, blank=True, null=True)
    isoforms = models.CharField(max_length=100, blank=True, null=True)
    field_of_normal = models.CharField(db_column='#_of_normal', max_length=100)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_of_stage_1 = models.CharField(db_column='#_of_stage_1', max_length=100)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_of_stage_2 = models.CharField(db_column='#_of_stage_2', max_length=100)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_of_stage_3 = models.CharField(db_column='#_of_stage_3', max_length=100)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_of_stage_4 = models.CharField(db_column='#_of_stage_4', max_length=100)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_of_stage_5 = models.CharField(db_column='#_of_stage_5', max_length=100)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_of_nos = models.CharField(db_column='#_of_nos', max_length=100)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_of_is = models.CharField(db_column='#_of_is', max_length=100)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_of_tumor = models.CharField(db_column='#_of_tumor', max_length=100)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'Mutual_Relationship'
