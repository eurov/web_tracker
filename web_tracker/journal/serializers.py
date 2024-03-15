from urllib.parse import urlparse
from rest_framework import serializers

from web_tracker.journal.models import Visit


class LinksSerialazer(serializers.ModelSerializer):

    class Meta:
        model = Visit
        fields = "__all__"

    def to_internal_value(self, data):
        if isinstance(data, str):
            domain = urlparse(data).netloc
            data = {"domain": domain, "link": data}
        return super().to_internal_value(data)
