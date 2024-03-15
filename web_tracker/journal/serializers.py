from urllib.parse import urlparse
from rest_framework import serializers
from rest_framework.exceptions import APIException

from web_tracker.journal.models import Visit


class LinksSerialazer(serializers.ModelSerializer):

    class Meta:
        model = Visit
        fields = "__all__"

    def to_internal_value(self, data):
        if isinstance(data, str):
            domain = urlparse(data).netloc
            if not domain:
                raise APIException("make sure all links are valid")
            data = {"domain": domain, "link": data}
        return super().to_internal_value(data)
