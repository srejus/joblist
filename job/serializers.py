from rest_framework import serializers

from job.models import *

class CreateJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        exclude = ['posted_by','posted_time','no_of_applicants','company']
        depth=1
    
    def validate(self,data):
        errors = []
        salary_from = data.get('salary_from')
        salary_to = data.get('salary_upto')
        company = self.initial_data.get('company')
        experience = data.get('experience')
        
        if not self.partial:
            if not company:
                errors.append({"company":"This field is requried"})
            try:
                company = int(company)
                if company and not Company.objects.filter(id=company).exists():
                    errors.append({"company":"Invalid company id"})
                
                data['company'] = company
            except TypeError:
                errors.append({"company":"Invalid company id"})
        
            if experience and experience < 0:
                errors.append({"experience":"This field must be a positive number"})
                
            if salary_from and salary_to and salary_from > salary_to:
                errors.append({"salary":"salary_from must be less than salary_upto"})
            
            if errors:
                raise serializers.ValidationError({"errors":errors})
        
        return data

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        depth=1
    