from company.models import Company
from rest_framework import serializers


class CreateCompanySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Company
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set required fields
        self.fields['name'].required = True
        self.fields['email'].required = True
        self.fields['address'].required = True
        self.fields['gst'].required = True
        self.fields['pan_no'].required = True
        self.fields['owners_name'].required = True
        self.fields['owners_email'].required = True
        self.fields['owners_birth_date'].required = True
        self.fields['contact'].required = True
        self.fields['contact_person'].required = True
        self.fields['fees'].required = True
        self.fields['documents'].required = True



class GetAllCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class UpdateCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set required fields
        self.fields['name'].required = True
        self.fields['email'].required = True
        self.fields['address'].required = True
        self.fields['gst'].required = True
        self.fields['pan_no'].required = True
        self.fields['owners_name'].required = True
        self.fields['owners_email'].required = True
        self.fields['owners_birth_date'].required = True
        self.fields['contact'].required = True
        self.fields['contact_person'].required = True
        self.fields['fees'].required = True
