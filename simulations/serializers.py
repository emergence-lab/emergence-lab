from rest_framework import serializers

from .models import Simulation


class SimSerializer(serializers.ModelSerializer):
    """
    Serializes the Sim model.

    """

    class Meta:
        model = Simulation
        fields = ('id', 'user', 'request_date', 'start_date', 'finish_date',
                  'priority', 'execution_node', 'file_path')
