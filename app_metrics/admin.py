from django.contrib import admin

from app_metrics.models import (
    Metric, MetricSet, MetricItem, MetricDay,
    MetricWeek, MetricMonth, MetricYear
)


class MetricAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'slug', )
    search_fields = ['name', 'slug', ]

    def slug(self, obj):
        return obj.metric.slug


admin.site.register(Metric, MetricAdmin)


class MetricItemAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user', 'metric', ]


admin.site.register(MetricItem, MetricItemAdmin)


class MetricPeriodAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'slug', 'num')
    list_filter = ['metric__name']
    autocomplete_fields = ['metric', ]

    def slug(self, obj):
        return obj.metric.slug


admin.site.register(MetricDay, MetricPeriodAdmin)
admin.site.register(MetricWeek, MetricPeriodAdmin)
admin.site.register(MetricMonth, MetricPeriodAdmin)
admin.site.register(MetricYear, MetricPeriodAdmin)


class MetricSetAdmin(admin.ModelAdmin):
    autocomplete_fields = ['metrics', 'email_recipients', ]


admin.site.register(MetricSet, MetricSetAdmin)
