from django.contrib.admin import RelatedFieldListFilter
from django.utils.encoding import smart_text
from django.utils.html import format_html
from django.core.urlresolvers import reverse

try:
    from django.contrib.admin.utils import get_model_from_relation
except ImportError: # Django 1.6
    from django.contrib.admin.util import get_model_from_relation

try:
    from django.forms.utils import flatatt
except ImportError: # Django 1.6
    from django.forms.util import flatatt


class RelatedFieldAjaxListFilter(RelatedFieldListFilter):
    ajax_attrs = None

    def has_output(self):
        return True

    def field_choices(self, field, request, model_admin):
        """
        This method should return every available choices for the list filter,
        as a list of tuples. Each tuple contains the pk and the string representation of
        a related model instance.

        For more information, see RelatedFieldListFilter implementation:
        https://github.com/django/django/blob/1.10.5/django/contrib/admin/filters.py#L161-L223
        """
        model = field.remote_field.model if hasattr(field, 'remote_field') else field.related_field.model
        app_label = model._meta.app_label
        model_name = model._meta.object_name

        self.ajax_attrs = format_html('{0}', flatatt({
            'data-app-label': app_label,
            'data-model': model_name,
            'data-ajax--url': reverse('jet:model_lookup'),
            'data-queryset--lookup': self.lookup_kwarg
        }))
        other_model = get_model_from_relation(field)
        if hasattr(field, 'rel'):
            rel_name = field.rel.get_related_field().name
        else:
            rel_name = other_model._meta.pk.name

        queryset = model._default_manager.all()
        return [(x._get_pk_val(), smart_text(x)) for x in queryset]
