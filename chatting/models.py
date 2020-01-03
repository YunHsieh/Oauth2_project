from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class blog(models.Model):
    author = models.CharField()
    posted_date = models.DateField(auto_now_add=True)
    title = models.CharField()
    text = models.CharField()
    # first_name = models.CharField(_("First name"), max_length=200)
    # last_name = models.CharField(_("Last name"), max_length=200)
    # author_name = models.CharField(_("Author name"), max_length=200)

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")
        ordering = ("author_name",)
        app_label = 'test'
        db_table = 'test_model'

    def __str__(self):
        return self.author_name