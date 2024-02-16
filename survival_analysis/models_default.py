# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class IsoformStrutureInfo(models.Model):
    isoform_name = models.CharField(primary_key=True, max_length=100)
    gene_name = models.CharField(max_length=100, blank=True, null=True)
    chromsome = models.CharField(max_length=100, blank=True, null=True)
    strand = models.CharField(max_length=100, blank=True, null=True)
    isoform_region = models.CharField(max_length=100, blank=True, null=True)
    exon = models.TextField(blank=True, null=True)
    cds = models.TextField(db_column='CDS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Isoform_struture_info'


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


class NcbiGeneInfo20180201(models.Model):
    tax_id = models.CharField(max_length=100, blank=True, null=True)
    geneid = models.CharField(db_column='GeneID', primary_key=True, max_length=100)  # Field name made lowercase.
    gene_link = models.CharField(db_column='Gene_link', max_length=100, blank=True, null=True)  # Field name made lowercase.
    symbol = models.CharField(db_column='Symbol', max_length=100, blank=True, null=True)  # Field name made lowercase.
    locustag = models.TextField(db_column='LocusTag', blank=True, null=True)  # Field name made lowercase.
    synonyms = models.TextField(db_column='Synonyms', blank=True, null=True)  # Field name made lowercase.
    dbxrefs = models.TextField(db_column='dbXrefs', blank=True, null=True)  # Field name made lowercase.
    chromosome = models.TextField(blank=True, null=True)
    map_location = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    type_of_gene = models.TextField(blank=True, null=True)
    symbol_from_nomenclature_authority = models.TextField(db_column='Symbol_from_nomenclature_authority', blank=True, null=True)  # Field name made lowercase.
    full_name_from_nomenclature_authority = models.TextField(db_column='Full_name_from_nomenclature_authority', blank=True, null=True)  # Field name made lowercase.
    nomenclature_status = models.TextField(db_column='Nomenclature_status', blank=True, null=True)  # Field name made lowercase.
    other_designations = models.TextField(db_column='Other_designations', blank=True, null=True)  # Field name made lowercase.
    modification_date = models.TextField(db_column='Modification_date', blank=True, null=True)  # Field name made lowercase.
    feature_type = models.TextField(db_column='Feature_type', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NCBI_gene_info_20180201'


class NcbiTranscriptInfo20180209(models.Model):
    transcript_name = models.CharField(primary_key=True, max_length=100)
    definition = models.TextField(blank=True, null=True)
    transcript_variant = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'NCBI_transcript_info_20180209'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
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
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


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


class Hg38GeneTranscripts20180130(models.Model):
    gene = models.CharField(primary_key=True, max_length=100)
    transcripts = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hg38_gene_transcripts_20180130'


class QueryByDataBoxplot(models.Model):

    class Meta:
        managed = False
        db_table = 'query_by_data_boxplot'


class QueryByDataDetail(models.Model):

    class Meta:
        managed = False
        db_table = 'query_by_data_detail'


class QueryByDataFilter(models.Model):

    class Meta:
        managed = False
        db_table = 'query_by_data_filter'


class QueryByDataSummary(models.Model):

    class Meta:
        managed = False
        db_table = 'query_by_data_summary'


class QueryByGene2Boxplot(models.Model):

    class Meta:
        managed = False
        db_table = 'query_by_gene2_boxplot'


class QueryByGene2Others(models.Model):

    class Meta:
        managed = False
        db_table = 'query_by_gene2_others'


class QueryByGene2SurvivalPlot(models.Model):

    class Meta:
        managed = False
        db_table = 'query_by_gene2_survival_plot'


class QueryByGeneBoxplot(models.Model):

    class Meta:
        managed = False
        db_table = 'query_by_gene_boxplot'


class QueryByGeneDetail(models.Model):

    class Meta:
        managed = False
        db_table = 'query_by_gene_detail'


class QueryByGeneFilter(models.Model):

    class Meta:
        managed = False
        db_table = 'query_by_gene_filter'
