from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers
from .models import Car, Rating


class CarSerializer(serializers.ModelSerializer):
    ratings = serializers.StringRelatedField(many=True, default=[])

    class Meta:
        model = Car
        fields = ['id', 'make_name', 'model_name', 'ratings']

    def to_representation(self, instance):
        output = super().to_representation(instance)
        avg = 0
        for i in output['ratings']:
            avg += int(i)
        if avg != 0:
            output['ratings'] = avg / len(output['ratings'])
        else:
            output['ratings'] = "Rating not available"

        return output



class RatingSerializer(serializers.ModelSerializer):
    score = serializers.IntegerField(validators=[MinValueValidator(1),
                                                 MaxValueValidator(5)])

    class Meta:
        model = Rating
        fields = ['score']

    def create(self, validated_data):
        car_id = list(CarSerializer(Car.objects.filter(make_name=self.context['request'].data["make_name"], model_name=self.context['request'].data['model_name']), many=True).data[0].items())[0][1]
        validated_data['car_id'] = car_id
        return super().create(validated_data)



