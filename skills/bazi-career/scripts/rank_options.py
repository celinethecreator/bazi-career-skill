"""Compare explicitly weighted practical evidence; never score birth charts."""
import json
import math
import sys

DIMENSIONS = {'tasks','skills','income','growth','stability','work_style','location'}

def finite_number(x):
    return type(x) in (int,float) and math.isfinite(x)

def compare(data):
    if set(data)-{'weights','options','weights_confirmed'}:
        raise ValueError('Unsupported fields')
    if data.get('weights_confirmed') is not True:
        raise ValueError('User-confirmed weights required')
    weights=data['weights']
    if not weights or set(weights)-DIMENSIONS or any(
        not finite_number(w) or w<=0 for w in weights.values()):
        raise ValueError('Use positive finite weights for practical dimensions only')
    if not math.isclose(sum(weights.values()),1,abs_tol=1e-8):
        raise ValueError('Weights must sum to 1')
    results=[]
    names=set()
    if not isinstance(data['options'],list) or not data['options']:
        raise ValueError('At least one option required')
    for opt in data['options']:
        if not isinstance(opt.get('name'),str) or not opt['name'].strip() or opt['name'] in names:
            raise ValueError('Unique option names required')
        names.add(opt['name'])
        if set(opt)-{'name','hard_constraints','scores','evidence'}:
            raise ValueError('Unsupported option fields')
        hard=opt.get('hard_constraints')
        if not isinstance(hard,dict) or not hard:
            raise ValueError('At least one explicit hard constraint required')
        if any(v is not None and type(v) is not bool for v in hard.values()):
            raise ValueError('Hard constraints must be true/false/null')
        scores=opt.get('scores',{})
        if set(scores)-set(weights):
            raise ValueError('Scores must match selected dimensions')
        evidence=opt.get('evidence',{})
        coverage=0; weighted=0; missing=[]
        for dim,w in weights.items():
            s=scores.get(dim)
            if s is None:
                missing.append(dim);continue
            if not finite_number(s) or not 1<=s<=5:
                raise ValueError('Scores must be 1–5 or null')
            if not isinstance(evidence.get(dim),str) or not evidence[dim].strip():
                raise ValueError('Each score requires evidence')
            coverage+=w;weighted+=w*s
        excluded=any(v is False for v in hard.values())
        pending=any(v is None for v in hard.values()) or missing
        status='excluded' if excluded else ('needs_verification' if pending else 'comparable')
        # Bounds do not impute unknown values; they show how unknowns could alter order.
        results.append({'name':opt['name'],'status':status,
                        'coverage':round(coverage,4),'missing_dimensions':missing,
                        'unknown_hard_constraints':[k for k,v in hard.items() if v is None],
                        'failed_hard_constraints':[k for k,v in hard.items() if v is False],
                        'preference_index':round(weighted/5*100,1) if status=='comparable' else None,
                        'possible_index_range':[round((weighted+1-coverage)/5*100,1),
                                                round((weighted+5*(1-coverage))/5*100,1)]
                                               if not excluded else None,
                        'evidence':evidence})
    return {'interpretation':'User preference index, not career suitability or success probability',
            'options':results,'ranking_policy':'Only fully verified comparable options can be ordered; do not rank pending options'}

def main():
    try:
        result=compare(json.load(sys.stdin))
    except (ValueError,TypeError,KeyError,AttributeError):
        print('{"error":"invalid_comparison_input"}',file=sys.stderr);return 2
    print(json.dumps(result,ensure_ascii=False,indent=2));return 0

if __name__=='__main__':
    sys.exit(main())
