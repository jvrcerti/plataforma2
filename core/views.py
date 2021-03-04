from rest_framework.views import APIView
from core.serializer import MicrogridSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView
from core.serializer import MicrogridSerializer, MicrogridParametersSerializer, ComponentSerializer, MicrogridSerializer, DataPointsSerializer
import json
from core.models import Microgrid
from itertools import chain, starmap

def flatten_parameters(microgrid_parameters):

    flattened_dict = {}
    flattened_dict['microgrid'] = microgrid_parameters['microgrid']
    flattened_dict['connection_type'] = microgrid_parameters['point_of_common_coupling']['connection_type']
    flattened_dict['connection_type'] = microgrid_parameters['point_of_common_coupling']['connection_type']
    flattened_dict['diesel_price'] = microgrid_parameters['point_of_common_coupling']['diesel_price']
    flattened_dict['natural_gas_price'] = microgrid_parameters['point_of_common_coupling']['natural_gas_price']
    flattened_dict['utility_name'] = microgrid_parameters['point_of_common_coupling']['utility']['utility_name']
    flattened_dict['group'] = microgrid_parameters['point_of_common_coupling']['utility']['consumer_type']['group']
    flattened_dict['subgroup'] = microgrid_parameters['point_of_common_coupling']['utility']['consumer_type']['subgroup']
    flattened_dict['tariff_type'] = microgrid_parameters['point_of_common_coupling']['utility']['consumer_type']['tariff_type']
    flattened_dict['pis_cofins'] = microgrid_parameters['point_of_common_coupling']['utility']['taxes']['pis_cofins']
    flattened_dict['icms_1_limit'] = microgrid_parameters['point_of_common_coupling']['utility']['taxes']['icms_1']['limit']
    flattened_dict['icms_1_value'] = microgrid_parameters['point_of_common_coupling']['utility']['taxes']['icms_1']['value']
    flattened_dict['icms_2_limit'] = microgrid_parameters['point_of_common_coupling']['utility']['taxes']['icms_2']['limit']
    flattened_dict['icms_2_value'] = microgrid_parameters['point_of_common_coupling']['utility']['taxes']['icms_2']['value']
    flattened_dict['icms_3_limit'] = microgrid_parameters['point_of_common_coupling']['utility']['taxes']['icms_1']['limit']
    flattened_dict['icms_3_value'] = microgrid_parameters['point_of_common_coupling']['utility']['taxes']['icms_1']['value']
    flattened_dict['tusd_d_peak'] = microgrid_parameters['point_of_common_coupling']['utility']['rates']['distribution']['tusd_d_peak']
    flattened_dict['tusd_d_base'] = microgrid_parameters['point_of_common_coupling']['utility']['rates']['distribution']['tusd_d_base']
    flattened_dict['tusd_e_peak'] = microgrid_parameters['point_of_common_coupling']['utility']['rates']['distribution']['tusd_e_peak']
    flattened_dict['tusd_e_intermediary'] = microgrid_parameters['point_of_common_coupling']['utility']['rates']['distribution']['tusd_e_intermediary']
    flattened_dict['tusd_e_base'] = microgrid_parameters['point_of_common_coupling']['utility']['rates']['distribution']['tusd_e_base']
    flattened_dict['energy_price_peak'] = microgrid_parameters['point_of_common_coupling']['utility']['rates']['energy']['energy_price_peak']
    flattened_dict['energy_price_intermediary'] = microgrid_parameters['point_of_common_coupling']['utility']['rates']['energy']['energy_price_intermediary']
    flattened_dict['energy_price_base'] = microgrid_parameters['point_of_common_coupling']['utility']['rates']['energy']['energy_price_base']
    flattened_dict['tariff_flag_signal'] = microgrid_parameters['point_of_common_coupling']['utility']['rates']['energy']['tariff_flag_signal']

    return flattened_dict

def flatten_component(lista):

    new_dict = {}
    new_dict['component_id'] = lista['component_id']
    new_dict['component_type'] = lista['component_type']
    new_dict['operation_status'] = lista['operation_status']
    new_dict['meters_id'] = lista['meters'][list(lista['meters'].keys())[0]]['meters_id']
    new_dict['data_points'] = lista['meters'][list(lista['meters'].keys())[0]]['data_points']

    return new_dict
    
def append_flattened_components(request, request_id):
    new_request_flattened = []
    for n in request:
        each_component_flattened = flatten_component(n)
        each_component_flattened['microgrid'] = request_id
        new_request_flattened.append(each_component_flattened)
    return new_request_flattened    



class MrConfig(APIView):

    def post(self, request):
        """Manipulate request data and validate with serializers"""
        
        """Slice microgrid_info""" 
        microgrid_info = request.data['microgrid_info']

        """Validate microgrid_info and save in database"""
        serializer = MicrogridSerializer(data=microgrid_info)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        """Slice microgrid_paramters"""
        microgrid_parameters = request.data["microgrid_parameters"]

        """Assign microgrid_id to microgrid_parameters"""
        microgrid_parameters['microgrid'] = serializer.data.get('id')

        """Slice microgrid_components"""
        microgrid_components = request.data['components']

        """Assign microgrid_id to microgrid_components"""
        microgrid_components = append_flattened_components(request.data["components"], serializer.data.get('id'))

        """Flatten microgrid_parameters"""
        new_dict = flatten_parameters(microgrid_parameters)

        """Validate microgrid_parameters and save in database"""
        serializer = MicrogridParametersSerializer(data=new_dict)
        if serializer.is_valid():
            serializer.save()
        
        """Validate microgrid_parameters and save in database"""
        serializer = ComponentSerializer(data=microgrid_components, many=True)
        if serializer.is_valid():
            serializer.save()
        
        """Assign component_id to each data_point"""
        microgrid_data_points = []
        for n in range(0, len(serializer.data)):
            data_point_per_component = microgrid_components[n]['data_points']
            for i in data_point_per_component:
                i['component'] = serializer.data[n]['id']
                microgrid_data_points.append(i)
        
        """Validate microgrid_data_points and save in database"""
        serializer = DataPointsSerializer(data=microgrid_data_points, many=True)
        if serializer.is_valid():
            serializer.save()
            message = 'Microrrede Adicionada Com Sucesso'
            return Response({'message' : message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        