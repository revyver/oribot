# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Max, Sum

from model_utils import Choices, TimeStampedModel


class Artist(models.Model):
    name = models.CharField(max_length=255)
    romanized_name = models.CharField(max_length=255)
    slug = models.SlugField()

    def __unicode__(self):
        return u'%s' % (self.name)


class Release(TimeStampedModel):
    KIND = Choices(('album', 'Album'), ('single', 'Single'))

    parent = models.ForeignKey('self')
    kind = models.CharField(choices=KIND, default=KIND.single, max_length=6)
    artist = models.ForeignKey(Artist, related_name='releases')

    name = models.CharField(max_length=255)
    romanized_name = models.CharField(max_length=255)
    released = models.DateField()
    slug = models.SlugField()

    def __unicode__(self):
        return u'%s' % (self.name)

    def sales(self):
        return self.weeklies.annotate(total=Sum('sales'))

    def highest_weekly_rank(self):
        return self.weeklies.aggregate(total=Max('rank'))


class Entry(TimeStampedModel):
    sales = models.IntegerField(blank=True, null=True)
    rank = models.IntegerField(blank=True, null=True)

    class Meta:
        abstract = True


class Daily(Entry):
    release = models.ForeignKey(Release, related_name='dailies')
    date = models.DateField()

    def __unicode__(self):
        return u'%s: Daily for %s' % (self.release.name, self.date)


class Weekly(Entry):
    release = models.ForeignKey(Release, related_name='weeklies')
    date_starting = models.DateField()
    date_ending = models.DateField()

    def __unicode__(self):
        return u'%s: Week of %s' % (self.release.name, self.date_starting)


class Yearly(Entry):
    release = models.ForeignKey(Release, related_name='yearlies')
    date_starting = models.DateField()

    def __unicode__(self):
        return u'%s: Year' % (self.release.name)


def recalculate(created, instance, **kwargs):
    pass