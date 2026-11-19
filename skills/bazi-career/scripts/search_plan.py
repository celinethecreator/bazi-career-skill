"""Generate non-sensitive queries. Does not browse or claim to find jobs."""
import json
import sys

ALLOWED = {'roles','cities','skills','scenario','graduation_year'}
SCENARIOS = {'campus','experienced','plateau','offer','transition'}

def plan(data):
    if set(data) - ALLOWED:
        raise ValueError('Only non-sensitive search fields are accepted')
    for key in ('roles','cities','skills'):
        value = data.get(key, [])
        if not isinstance(value,list) or len(value)>12 or any(
            not isinstance(s,str) or not s.strip() or len(s)>100 for s in value):
            raise ValueError('Use short lists of public role/city/skill terms')
    if not data.get('roles'):
        raise ValueError('At least one role is required')
    if data.get('scenario') not in SCENARIOS:
        raise ValueError('Unknown scenario')
    if data['scenario']=='campus':
        y=data.get('graduation_year')
        if type(y) is not int or not 2000 <= y <= 2100:
            raise ValueError('Campus search needs graduation_year')
    queries=[]
    for role in data['roles']:
        for city in data.get('cities') or ['']:
            suffix = ('校园招聘 '+str(data['graduation_year'])) if data['scenario']=='campus' else '招聘 careers'
            queries.append(' '.join(x for x in [role,city,*data.get('skills',[])[:3],suffix] if x))
    return {'mode':'search-plan-only','queries':queries,
            'source_priority':['employer careers','verified employer ATS','public job listing'],
            'verification_fields':['url','accessed_at','published_at','status','requirements','salary_basis'],
            'privacy':'Schema rejects birth fields; callers must also remove personal data from free text'}

def main():
    try:
        result=plan(json.load(sys.stdin))
    except (ValueError,TypeError,KeyError):
        print('{"error":"invalid_search_input"}',file=sys.stderr)
        return 2
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0

if __name__=='__main__':
    sys.exit(main())
