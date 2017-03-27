from __future__ import unicode_literals
from django.template.defaultfilters import slugify
from django.urls import reverse, reverse_lazy
from django.db import models
from django.contrib import admin

class President (models.Model):
    potus_id = models.IntegerField('potus', primary_key=True) # i.e., Trump = 45
    first_name = models.CharField('first name', max_length=50)
    last_name = models.CharField('last name', max_length=50)
    party = models.CharField('party', max_length=20)
    potus_slug = models.SlugField('potus slug for seo', max_length = 20, default='', unique=True)

    def __unicode__(self):
        return self.last_name

class Authorities (models.Model):
    authority = models.CharField(max_length=50, blank = True, null = True) 
    authority_section = models.CharField(max_length=50, blank = True, null = True)

    class Meta:
        verbose_name = "authority"
        verbose_name_plural = "authorities"

    def __unicode__(self):
        return self.authority

class Agencies (models.Model):
    agency_short = models.CharField(max_length=10)
    agency_long = models.CharField(max_length=100)

    class Meta:
        verbose_name = "agency"
        verbose_name_plural = "agencies"
        ordering = ['agency_long']

    def __unicode__(self):
        return self.agency_long

class OrderType (models.Model):
    short_type = models.CharField(max_length=5)
    long_type = models.CharField(max_length=50)
    type_description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.long_type

class Stories(models.Model):
    presto_id = models.IntegerField('Presto', null=True, blank = True, unique = True)
    story_title = models.CharField(max_length=100)
    story_url = models.URLField()
    story_date = models.DateField()   

    class Meta:
        verbose_name = "story"
        verbose_name_plural = "stories"
        ordering = ['-story_date']

    def __unicode__(self):
        return self.story_title

    def date_save(self, *args, **kwargs): #fetches date string from URL and converts to formatted date on save 
        self.story_date = datetime.datetime.strptime(re.search('(?<!\d)\d{4,4}(?!\d).{6}', story_url).group(0), "%Y/%m/%d").strftime("%d-%m-%Y")
        super(Stories,self).save(*args, **kwargs)

    def presto_save(self, *args, **kwargs): #fetches Presto ID and automatically saves. 
        self.presto_id = re.search('(\d*)\/$', story_url).group(1)
        super(Stories,self).save(*args, **kwargs)
    
class Order (models.Model):

    president = models.ForeignKey(President, default=45)
        
    order_type = models.ForeignKey(OrderType, null = True)

    sign_date = models.DateField(null = True)

    title = models.CharField(max_length=512)

    fr_pub = models.NullBooleanField(verbose_name = 'Published in Federal Register')
    fr_doc_no = models.CharField(max_length=20, blank = True, null = True, verbose_name = 'Federal Register Document Number')
    fr_date = models.DateField(blank = True, null = True, verbose_name = 'Date Published in the Federal Register')
    fr_url = models.URLField(blank = True, null = True, verbose_name = 'Federal Register URL')
    fr_pdf_url = models.URLField(blank = True, null = True, verbose_name = 'Federal Register PDF URL')
    bud_impact_url = models.URLField(blank = True, null = True, verbose_name = 'OMB Budgetary Impact Statement URL')
    wh_url = models.URLField(blank = True, null = True, verbose_name = 'White House URL')
    ucsb_url = models.URLField(blank = True, null = True, verbose_name = 'American Presidency Project URL') # URL for page at American Presidency Project

    #short_title = models.CharField(max_length=20) # e.g., EO 11030
    eo_proc_no = models.CharField(max_length=6, blank = True, null = True, verbose_name = 'EO or Proclamation number')

    abstract = models.TextField(blank = True, null = True)

    authority = models.ManyToManyField(Authorities, blank=True)

    agency = models.ManyToManyField(Agencies, blank = True)

    signed_location = models.CharField(max_length=100, blank = True, null = True)
    presidential_statement = models.TextField(blank = True, null = True) # Verbal statement by POTUS

    #disposition = models.ManyToManyField('self', through='Disposition',
    #    symmetrical=False, related_name='related_to')

    # rescinds = models.ManytoManyField(Order) # See NARA disposition table
    # amends = models.ManytoManyField(Order)

    subj_to_appropriations = models.NullBooleanField()
    judicial_review = models.NullBooleanField()

    related_story = models.ManyToManyField(Stories)

    # new_related_story = models.ForeignKey(RelatedStories, blank=True, null = True)

    order_slug = models.SlugField(max_length=256, default='')

    last_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs): #converts order title into a slugified url-ready string
        self.order_slug = slugify(self.title)
        super(Order,self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["-sign_date"]

class Deadline(models.Model):

    deadline_order = models.ForeignKey(Order)
    followup_item = models.TextField(blank=True, null=True)
    deadline_days = models.DurationField(blank=True, null=True)
    deadline_date = models.DateField(blank=True, null=True)
    
class StoriesAdmin(admin.ModelAdmin):
    readonly_fields = ('presto_id', 'story_date')


class DeadlineInline(admin.TabularInline):
    model = Deadline

class OrderAdmin(admin.ModelAdmin):
    inlines = [
        DeadlineInline,
    ]

    def get_absolute_url(self):
        kwargs = {
              #'potus_slug': President.potus_slug,
              'year': self.sign_date.year,
              'month': self.sign_date.month,
              'day': self.sign_date.day,
              'slug': self.order_slug,
              'pk': self.pk
              }
        return reverse_lazy('order_detail', kwargs=kwargs)
'''

#class Disposition(models.Model):
#    revokes = models.ForeignKey(Order, related_name='revokes')
#    revoked_by = models.ForeignKey(Order, related_name='revoked_by')
#    status = models.IntegerField(choices=DISPOSITION_STATUSES)

#    DISPOSITION_REVOKES = 1
#    DISPOSITION_AMENDS = 2
#    DISPOSITION_STATUSES = (
#    (DISPOSITION_REVOKES, 'Revokes'),
#    (DISPOSITION_AMENDS, 'Amends'),
#)

'''


