"""Local, stdin-only BaZi calendar adapter. No files, network or career predictions."""
import json
import sys
from datetime import datetime, timedelta
from importlib.metadata import version


def calculate(data):
    if not isinstance(data, dict):
        raise ValueError("Input must be a JSON object")
    from lunar_python import Solar
    if version('lunar-python') != '1.4.8':
        raise ValueError('Require lunar-python==1.4.8 for reproducible output')
    if data.get('calendar') != 'solar' or data.get('timezone') != 'Asia/Shanghai':
        raise ValueError('Only solar calendar and Asia/Shanghai civil time are supported')
    day = datetime.strptime(data['date'], '%Y-%m-%d')
    if not 1901 <= day.year <= 2099:
        raise ValueError('Supported years: 1901–2099')
    if 1986 <= day.year <= 1991 and 4 <= day.month <= 9:
        raise ValueError('Historical DST may apply; use an externally verified chart')
    sect = data.get('sect', 2)
    if type(sect) is not int or sect not in (1, 2):
        raise ValueError('sect must be 1 or 2')
    if data.get('true_solar_time'):
        raise ValueError('True solar time is not implemented; do not silently approximate')
    exact = data.get('time')
    if exact and ('time_start' in data or 'time_end' in data):
        raise ValueError('Choose exact time OR a range')
    if ('time_start' in data) != ('time_end' in data):
        raise ValueError('Both time_start and time_end are required')
    def parse_time(value):
        t = datetime.strptime(value, '%H:%M')
        return day.replace(hour=t.hour, minute=t.minute)
    if exact:
        start = end = parse_time(exact)
    elif 'time_start' in data:
        start, end = parse_time(data['time_start']), parse_time(data['time_end'])
        if end < start:
            raise ValueError('Split cross-midnight ranges into separate dates')
    else:
        start, end = day, day.replace(hour=23, minute=59)
    candidates = {}
    current = start
    while current <= end:
        ec = Solar.fromYmdHms(current.year, current.month, current.day,
                             current.hour, current.minute, 0).getLunar().getEightChar()
        ec.setSect(sect)
        pillars = [getattr(ec, 'get'+p)() for p in ('Year','Month','Day','Time')]
        key = tuple(pillars)
        if key not in candidates:
            candidates[key] = {
                'pillars': dict(zip(('year','month','day','hour'),pillars)),
                'day_master': ec.getDayGan(),
                'visible_stem_ten_gods': {p.lower():getattr(ec,'get'+p+'ShiShenGan')()
                                          for p in ('Year','Month','Time')},
                'branch_hidden_ten_gods': {p.lower():getattr(ec,'get'+p+'ShiShenZhi')()
                                           for p in ('Year','Month','Day','Time')},
            }
        current += timedelta(minutes=1)
    values = list(candidates.values())
    invariant = {p: values[0]['pillars'][p] for p in ('year','month','day','hour')
                 if len({c['pillars'][p] for c in values}) == 1}
    return {'engine':'lunar-python','version':version('lunar-python'),
            'calendar':'solar','timezone':'Asia/Shanghai','sect':sect,
            'time_basis':'civil time; no true-solar correction; minute precision',
            'precision':'exact-minute' if exact else 'candidate-range',
            'candidate_count':len(values),'invariant_pillars':invariant,
            'candidates':values,
            'limits':['Calendar output is not evidence of career prediction accuracy',
                      'No strength, favorable-element, luck-cycle or career scoring calculation']}


def main():
    try:
        result = calculate(json.load(sys.stdin))
    except (ValueError, KeyError, TypeError, ImportError) as exc:
        # No birth data or traceback in errors.
        print(json.dumps({'error':'chart_unavailable','reason':
              'Check schema, date/time, supported calendar/timezone/DST, sect and dependency version'},ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0

if __name__ == '__main__':
    sys.exit(main())
