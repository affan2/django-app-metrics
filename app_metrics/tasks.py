import base64
import json
import urllib.request, urllib.parse, urllib.error

import datetime

try:
    from celery.task import task
except ImportError:
    from celery.decorators import task

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.utils.timezone import utc

from app_metrics.models import Metric, MetricItem, Gauge
# from brabeion import badges
# #from actstream import action
#
# from people.utils import save_user_points


# For statsd support
try:
    # Not required. If we do this once at the top of the module, we save
    # ourselves the pain of importing every time the task fires.
    import statsd
except ImportError:
    statsd = None

# For redis support
try:
    import redis
except:
    redis = None

# For librato support
try:
    import librato
    from librato.metrics import Gauge as LibratoGauge
    from librato.metrics import Counter as LibratoCounter
except ImportError:
    librato = None


class MixPanelTrackError(Exception):
    pass

# DB Tasks


@task(serializer='pickle')
def db_metric_task(slug, num=1, **kwargs):
    met = Metric.objects.get(slug=slug)
    user = kwargs['user']

    if met.unique:
        obj, created = MetricItem.objects.get_or_create(
            metric=met,
            user=user,
            item_content_type=kwargs['content_type'],
            item_object_id=kwargs['object_id'],
            site_id=settings.SITE_ID
        )

        if created:
            obj.points = met.points
            obj.num = 1
            obj.save()

            # if met.points > 0:
            #     save_user_points(user, met.points)
    else:
        MetricItem.objects.create(metric=met, num=num, user=user, points=met.points, site_id=settings.SITE_ID)
        # if met.points > 0:
        #     save_user_points(user, met.points)

    # if kwargs.get('badge'):
    #     badges.possibly_award_badge(kwargs['badge']['event'], **kwargs['badge']['state'])


@task(serializer='pickle')
def db_gauge_task(slug, current_value, **kwargs):
    gauge, created = Gauge.objects.get_or_create(slug=slug, defaults={
        'name': slug,
        'current_value': current_value,
    })

    if not created:
        gauge.current_value = current_value
        gauge.save()


def _get_token():
    token = getattr(settings, 'APP_METRICS_MIXPANEL_TOKEN', None)

    if not token:
        raise ImproperlyConfigured("You must define APP_METRICS_MIXPANEL_TOKEN when using the mixpanel backend.")
    else:
        return token

# Mixpanel tasks


@task(serializer='pickle')
def mixpanel_metric_task(slug, num, properties=None, **kwargs):
    token = _get_token()
    if properties is None:
        properties = dict()

    if "token" not in properties:
        properties["token"] = token

    url = getattr(settings, 'APP_METRICS_MIXPANEL_API_URL', "http://api.mixpanel.com/track/")

    params = {"event": slug, "properties": properties}
    b64_data = base64.b64encode(json.dumps(params))

    data = urllib.parse.urlencode({"data": b64_data})
    with urllib.request.urlopen(url, data) as f:
        if f.read() == '0':
            raise MixPanelTrackError('MixPanel returned 0')


# Statsd tasks

def get_statsd_conn():
    if statsd is None:
        raise ImproperlyConfigured("You must install 'python-statsd' in order to use this backend.")

    conn = statsd.Connection(
        host=getattr(settings, 'APP_METRICS_STATSD_HOST', 'localhost'),
        port=int(getattr(settings, 'APP_METRICS_STATSD_PORT', 8125)),
        sample_rate=float(getattr(settings, 'APP_METRICS_STATSD_SAMPLE_RATE', 1)),
    )
    return conn


@task(serializer='pickle')
def statsd_metric_task(slug, num=1, **kwargs):
    conn = get_statsd_conn()
    counter = statsd.Counter(slug, connection=conn)
    counter += num


@task(serializer='pickle')
def statsd_timing_task(slug, seconds_taken=1.0, **kwargs):
    conn = get_statsd_conn()

    # You might be wondering "Why not use ``timer.start/.stop`` here?"
    # The problem is that this is a task, likely running out of process
    # & perhaps with network overhead. We'll measure the timing elsewhere,
    # in-process, to be as accurate as possible, then use the out-of-process
    # task for talking to the statsd backend.
    timer = statsd.Timer(slug, connection=conn)
    timer.send('total', seconds_taken)


@task(serializer='pickle')
def statsd_gauge_task(slug, current_value, **kwargs):
    conn = get_statsd_conn()
    gauge = statsd.Gauge(slug, connection=conn)
    # We send nothing here, since we only have one name/slug to work with here.
    gauge.send('', current_value)

# Redis tasks


def get_redis_conn():
    if redis is None:
        raise ImproperlyConfigured("You must install 'redis' in order to use this backend.")
    conn = redis.StrictRedis(
        host=getattr(settings, 'APP_METRICS_REDIS_HOST', 'localhost'),
        port=getattr(settings, 'APP_METRICS_REDIS_PORT', 6379),
        db=getattr(settings, 'APP_METRICS_REDIS_DB', 0),
    )
    return conn


@task(serializer='pickle')
def redis_metric_task(slug, num=1, **kwargs):
    # Record a metric in redis. We prefix our key here with 'm' for Metric
    # and build keys for each day, week, month, and year
    r = get_redis_conn()

    # Build keys
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    day_key = "m:%s:%s" % (slug, now.strftime("%Y-%m-%d"))
    week_key = "m:%s:w:%s" % (slug, now.strftime("%U"))
    month_key = "m:%s:m:%s" % (slug, now.strftime("%Y-%m"))
    year_key = "m:%s:y:%s" % (slug, now.strftime("%Y"))

    # Increment keys
    r.incrby(day_key, num)
    r.incrby(week_key, num)
    r.incrby(month_key, num)
    r.incrby(year_key, num)


@task(serializer='pickle')
def redis_gauge_task(slug, current_value, **kwargs):
    # We prefix our keys with a 'g' here for Gauge to avoid issues
    # of having a gauge and metric of the same name
    r = get_redis_conn()
    r.set("g:%s" % slug, current_value)

# Librato tasks


@task(serializer='pickle')
def librato_metric_task(name, num, **kwargs):
    api = librato.connect(settings.APP_METRICS_LIBRATO_USER,
                          settings.APP_METRICS_LIBRATO_TOKEN)
    source = settings.APP_METRICS_LIBRATO_SOURCE
    api.submit(name, num, source=source, **kwargs)
