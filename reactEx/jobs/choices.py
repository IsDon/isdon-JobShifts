from django.utils.translation import ugettext as _

STATUS_POSITION_CHOICES = (
    (1, _("Open")),
    (2, _("Filled")),
    (3, _("Inviting")),
    (4, _("Reviewing")),
    (5, _("Cancelled"))
)

STATUS_RESPONSE_CHOICES = (
    (1, _("Reviewing")),
    (2, _("Offer")),
    (3, _("Available")),
    (4, _("Unavailable")),
    (5, _("Cancelled"))
)