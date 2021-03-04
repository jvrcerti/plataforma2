from rest_framework import serializers

from core.models import Microgrid, MicrogridAddress, MicrogridParameters, MicrogridComponent, DataPoints


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = MicrogridAddress
        fields = '__all__'
        

class MicrogridSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    class Meta:
        model = Microgrid
        fields = '__all__'
        #['microgrid_id', 'microgrid_key', 'microgrid_name', 'client_name', 'client_id', 'time_zone', 'address'] 

    def create(self, validated_data):

        validated_data_address = validated_data.get('address')
        validated_data.pop('address')
        #print(validated_data)
        #print(validated_data_address)
        microgrid_address_obj, _ = MicrogridAddress.objects.get_or_create(**validated_data_address)
        print(validated_data)
        microgrid_info_obj = Microgrid.objects.create(**validated_data, address=microgrid_address_obj)
        #microgrid_info_obj, _ = Microgrid.objects.get_or_create(microgrid_id=validated_data.pop('microgrid_id'),defaults=validated_data.update({'address':microgrid_address_obj}))
        return microgrid_info_obj

class MicrogridParametersSerializer(serializers.ModelSerializer):
    class Meta:
        model = MicrogridParameters
        fields =[
            'microgrid', 
            'connection_type', 
            'diesel_price', 
            'natural_gas_price',
            'utility_name',
            'group',
            'subgroup',
            'tariff_type',
            'pis_cofins',
            'icms_1_value',
            'icms_1_limit',
            'icms_2_value',
            'icms_2_limit',
            'icms_3_value',
            'icms_3_limit',
            'tusd_d_peak',
            'tusd_e_peak',
            'tusd_e_intermediary',
            'tusd_d_base',
            'tusd_e_base',
            'energy_price_peak',
            'energy_price_intermediary',
            'energy_price_base',
            'tariff_flag_signal',
            ]
    
    # def create(self, validated_data):
    #     data = validated_data.pop('microgrid')
    #     data2 = dict(data)
    #     data2['address'] = dict(data2['address'])
    #     microgrid_address_obj_2= MicrogridAddress.objects.create(**data2.pop('address'))
    #     microgrid_info_obj_2 = Microgrid.objects.create(**data2, address=microgrid_address_obj_2)
    #     microgrid_parameters_obj = MicrogridParameters.objects.create(**validated_data, microgrid=microgrid_info_obj_2)
    #     return microgrid_parameters_obj

class DataPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataPoints
        fields = '__all__'

class ComponentSerializer(serializers.ModelSerializer):
    #data_points = DataPointsSerializer(many=True)
    class Meta:
        model = MicrogridComponent
        fields = '__all__'
    
    # def create(self, validated_data):
    #     breakpoint()
    #     data = validated_data.pop('data_points')
    #     microgrid_address_obj_3= MicrogridAddress.objects.create(**data2.pop('address'))
    #     microgrid_info_obj_3 = Microgrid.objects.create(**data2, address=microgrid_address_obj_3)
    #     microgrid_component_obj = MicrogridComponent.objects.create(**validated_data, microgrid=microgrid_info_obj_3)
    #     return microgrid_component_obj

    



  

    

   
     

    


