import datetime

from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models, IntegrityError
from django.template.defaultfilters import slugify
from django.utils.timezone import utc
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.timezone import now

try:
    from django.db.transaction import atomic
except ImportError:
    # Django < 1.6 use noop context manager
    from contextlib import contextmanager
    atomic = contextmanager(lambda:(yield))


class Metric(models.Model):
    """ The type of metric we want to store """
    name = models.CharField(_('name'), max_length=50)
    slug = models.SlugField(_('slug'), unique=True, max_length=60, db_index=True)

    points = models.PositiveIntegerField(default=0)

    unique = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('metric')
        verbose_name_plural = _('metrics')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            self.slug = slugify(self.name)
            i = 0
            while True:
                try:
                    with atomic():
                        return super(Metric, self).save(*args, **kwargs)
                except IntegrityError:
                    i += 1
                    self.slug = "%s_%d" % (self.slug, i)
        else:
            return super(Metric, self).save(*args, **kwargs)


class MetricSet(models.Model):
    """ A set of metrics that should be sent via email to certain users """
    name = models.CharField(_('name'), max_length=50)
    metrics = models.ManyToManyField(Metric, verbose_name=_('metrics'))
    email_recipients = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_('email recipients'))
    no_email = models.BooleanField(_('no e-mail'), default=False)
    send_daily = models.BooleanField(_('send daily'), default=True)
    send_weekly = models.BooleanField(_('send weekly'), default=False)
    send_monthly = models.BooleanField(_('send monthly'), default=False)

    class Meta:
        verbose_name = _('metric set')
        verbose_name_plural = _('metric sets')

    def __str__(self):
        return self.name


class MetricItem(models.Model):
    """ Individual metric items """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'), related_name="user_metricitems", on_delete=models.CASCADE, )
    metric = models.ForeignKey(Metric, verbose_name=_('metric'), on_delete=models.CASCADE, )
    num = models.IntegerField(_('number'), default=1)
    item_content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.CASCADE, )
    item_object_id = models.PositiveIntegerField(blank=True, null=True)
    item_object = GenericForeignKey(
        ct_field="item_content_type",
        fk_field="item_object_id"
    )
    points = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    site = models.ForeignKey(Site, default=settings.SITE_ID, verbose_name='site', on_delete=models.CASCADE, )

    class Meta:
        verbose_name = _('metric item')
        verbose_name_plural = _('metric items')

    def __str__(self):
        return _("'%(name)s' of %(num)d on %(created)s") % {
            'name': self.metric.name,
            'num': self.num,
            'created': self.created
        }


class MetricDay(models.Model):
    """ Aggregation of Metrics on a per day basis """
    metric = models.ForeignKey(Metric, verbose_name=_('metric'), on_delete=models.CASCADE, )
    num = models.BigIntegerField(_('number'), default=0)
    created = models.DateField(_('created'), default=datetime.date.today)

    class Meta:
        verbose_name = _('day metric')
        verbose_name_plural = _('day metrics')

    def __str__(self):
        return _("'%(name)s' for '%(created)s'") % {
            'name': self.metric.name,
            'created': self.created
        }


class MetricWeek(models.Model):
    """ Aggregation of Metrics on a weekly basis """
    metric = models.ForeignKey(Metric, verbose_name=_('metric'), on_delete=models.CASCADE, )
    num = models.BigIntegerField(_('number'), default=0)
    created = models.DateField(_('created'), default=datetime.date.today)

    class Meta:
        verbose_name = _('week metric')
        verbose_name_plural = _('week metrics')

    def __str__(self):
        return _("'%(name)s' for week %(week)s of %(year)s") % {
            'name': self.metric.name,
            'week': self.created.strftime("%U"),
            'year': self.created.strftime("%Y")
        }


class MetricMonth(models.Model):
    """ Aggregation of Metrics on monthly basis """
    metric = models.ForeignKey(Metric, verbose_name=('metric'), on_delete=models.CASCADE, )
    num = models.BigIntegerField(_('number'), default=0)
    created = models.DateField(_('created'), default=datetime.date.today)

    class Meta:
        verbose_name = _('month metric')
        verbose_name_plural = _('month metrics')

    def __str__(self):
        return _("'%(name)s' for %(month)s %(year)s") % {
            'name': self.metric.name,
            'month': self.created.strftime("%B"),
            'year': self.created.strftime("%Y")
        }


class MetricYear(models.Model):
    """ Aggregation of Metrics on a yearly basis """
    metric = models.ForeignKey(Metric, verbose_name=_('metric'), on_delete=models.CASCADE, )
    num = models.BigIntegerField(_('number'), default=0)
    created = models.DateField(_('created'), default=datetime.date.today)

    class Meta:
        verbose_name = _('year metric')
        verbose_name_plural = _('year metrics')

    def __str__(self):
        return _("'%(name)s' for %(year)s") % {
            'name': self.metric.name,
            'year': self.created.strftime("%Y")
        }


class Gauge(models.Model):
    """
    A representation of the current state of some data.
    """
    name = models.CharField(_('name'), max_length=50)
    slug = models.SlugField(_('slug'), unique=True, max_length=60)
    current_value = models.DecimalField(_('current value'), max_digits=15, decimal_places=6, default='0.00')
    created = models.DateTimeField(_('created'), auto_now_add=True, blank=True)
    updated = models.DateTimeField(_('updated'), auto_now=True, editable=False)

    class Meta:
        verbose_name = _('gauge')
        verbose_name_plural = _('gauges')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            self.slug = slugify(self.name)

        self.updated = datetime.datetime.utcnow().replace(tzinfo=utc)
        return super(Gauge, self).save(*args, **kwargs)
