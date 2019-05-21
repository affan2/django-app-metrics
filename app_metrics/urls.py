from django.urls import re_path

from app_metrics.views import *

urlpatterns = [
    '',
    re_path(
        regex   = r'^reports/$',
        view    = metric_report_view,
        name    = 'app_metrics_reports',
        ),
]
