import json
import os
from django.db import transaction
from main.models import *



# 파일에서 JSON 데이터를 읽어오는 함수
def load_json_data(file_name):
    file_path = os.path.join('data', file_name)
    with open(file_path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)

def load_companies_and_tech_stacks_and_job_positions(companies_data, tech_stacks_data, job_positions_data):
    for company, job_position, tech_stack in zip(companies_data, job_positions_data, tech_stacks_data):
        jp, job_position_created = JobPosition.objects.get_or_create(name=job_position['name'])
        comp, company_created = Company.objects.get_or_create(name=company['name'],
                                                sido=company['sido'],
                                                sigg=company['sigg'])
        tech_stack_exist = TechStack.objects.filter(name=tech_stack['name'], type=tech_stack['type']).count() # tech_stack 존재여부

        if tech_stack_exist and not company_created and not job_position_created: #중복을 방지하기 위해서 기존에 세 데이터가 존재하는지 확인
            continue
        else:
            ts = TechStack.objects.create(name=tech_stack['name'], type=tech_stack['type'])
            ts.companies.add(comp) #기업과 기술스택 연결
            ts.job_positions.add(jp) #직무와 기술스택 연결



# 메인 함수: 모든 데이터를 적재하는 함수
@transaction.atomic
def main_load_function():
    # JSON 데이터를 로드
    tech_stacks_data = load_json_data('tech_stacks_data.json')
    job_positions_data = load_json_data('job_positions_data.json')
    companies_data = load_json_data('companies_data.json')
    
    # 데이터를 적재
    load_companies_and_tech_stacks_and_job_positions(companies_data, tech_stacks_data, job_positions_data)

