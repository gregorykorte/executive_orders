from __future__ import unicode_literals
from django.template.defaultfilters import slugify
from django.urls import reverse, reverse_lazy
from django.db import models
from django.contrib import admin
from datetime import datetime, timedelta
import datetime, re
from mechanize import Browser
from BeautifulSoup import BeautifulSoup

def scrape(url):
    mech = Browser()
    page = mech.open(url)
    html = page.read()
    return BeautifulSoup(html)

def wordcount(input_string):
    word_list = re.findall(r"[\w']+", input_string) # need to add separate regex to find html <> tags and then subtract from word count
    return len(word_list)

def slugify_max(text, max_length=50): # truncate long slugs from title 
    slug = slugify(text)
    if len(slug) <= max_length:
        return slug
    trimmed_slug = slug[:max_length].rsplit('-', 1)[0]
    if len(trimmed_slug) <= max_length:
        return trimmed_slug
    # First word is > max_length chars, so we have to break it
    return slug[:max_length]

def get_story_title(url):
    soup = scrape(url)
    title = soup.find("title").text
    return title.decode('utf-8')

def get_order_text(url):
    soup = scrape(url)
    order_raw_html = str(soup.find("div", { "class" : "field-item even" })).decode('utf-8')
    #remove_extra_breaks = re.sub('<br\s*/?>', '\n', order_raw_html)
    order_html = re.sub('<p class="rtecenter">', '<p>', order_raw_html)
    return unicode.join(u'',map(unicode,order_html))

def get_order_posted_date(url):
    date = datetime.datetime.strptime(re.search('(?<!\d)\d{4,4}(?!\d).{6}', url).group(0), "%Y/%m/%d").strftime("%Y-%m-%d")
    return date

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
    story_url = models.URLField()
    story_title = models.CharField(null=True, blank=True, max_length=120)
    presto_id = models.IntegerField('Presto', null=True, blank = True, unique = True)
    story_date = models.DateField(blank=True, null=True)   

    class Meta:
        verbose_name = "story"
        verbose_name_plural = "stories"
        ordering = ['-story_date']

    def __unicode__(self):
        return self.story_title

    def save(self, *args, **kwargs): #fetches date string from URL and converts to formatted date on save 
        self.story_date = datetime.datetime.strptime(re.search('(?<!\d)\d{4,4}(?!\d).{6}', self.story_url).group(0), "%Y/%m/%d").strftime("%Y-%m-%d")
        self.presto_id = re.search('(\d*)\/$', self.story_url).group(1) #fetches Presto ID and automatically saves.
        if not self.story_title:
            self.story_title = get_story_title(self.story_url)
        super(Stories,self).save(*args, **kwargs)
    
class Order (models.Model):

    president = models.ForeignKey(President, default=45)
        
    order_type = models.ForeignKey(OrderType, null = True)

    sign_date = models.DateField(null = True)
    posted_date = models.DateField(null = True, blank = True)

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
    eo_proc_no = models.CharField(max_length=6, blank = True, null = True, verbose_name = 'EO num')

    abstract = models.TextField(blank = True, null = True)

    order_text = models.TextField(blank = True, null = True)

    order_words = models.IntegerField(blank = True, null = True)

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

    related_story = models.ManyToManyField(Stories, blank=True)

    # new_related_story = models.ForeignKey(RelatedStories, blank=True, null = True)

    order_slug = models.SlugField(blank=True)

    last_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs): 
        if not self.order_text:
            if self.wh_url:
                self.order_text = get_order_text(self.wh_url)
                self.posted_date = get_order_posted_date(self.wh_url)
        if not self.order_words:
            self.order_words = wordcount(self.order_text)
        if not self.order_slug:
            self.order_slug = slugify_max(self.title) #converts order title into a slugified url-ready string
        super(Order,self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["-sign_date"]

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

class Deadline(models.Model):

    order = models.ForeignKey(Order, null=True)
    deadline_days = models.IntegerField(blank=True, null=True)
    deadline_date = models.DateField(blank=True, null=True)
    followup_title = models.CharField(max_length = 100, null=True)
    followup_item = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs): #converts order title into a slugified url-ready string
        order_info = Order.objects.all()[0]
        self.deadline_date = order_info.sign_date + timedelta(days = self.deadline_days)
        super(Deadline,self).save(*args, **kwargs)

    def __unicode__(self):
        return self.followup_title
    

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


