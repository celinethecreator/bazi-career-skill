import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest
R=Path(__file__).resolve().parents[1]
S=R/'skills/bazi-career/scripts'
def load(n):
 s=importlib.util.spec_from_file_location(n,S/(n+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
c=load('chart');r=load('rank_options');q=load('search_plan')
class Tools(unittest.TestCase):
 def birth(self,**kw):
  d=dict(date='2005-12-23',time='08:37',calendar='solar',timezone='Asia/Shanghai');d.update(kw);return d
 def option(self):
  return dict(weights_confirmed=True,weights={'tasks':.5,'income':.5},options=[dict(name='A',hard_constraints={'city':True},scores={'tasks':4,'income':3},evidence={'tasks':'project evidence','income':'written offer'})])
 def test_upstream_fixture(self):
  self.assertEqual(list(c.calculate(self.birth())['candidates'][0]['pillars'].values()),['乙酉','戊子','辛巳','壬辰'])
 def test_second_fixture(self):
  self.assertEqual(list(c.calculate(self.birth(date='2022-08-28',time='01:50'))['candidates'][0]['pillars'].values()),['壬寅','戊申','癸丑','癸丑'])
 def test_unknown_time(self):
  d=self.birth();d.pop('time');a=c.calculate(d);self.assertGreaterEqual(a['candidate_count'],12);self.assertNotIn('hour',a['invariant_pillars'])
 def test_hour_boundary(self):
  d=self.birth();d.pop('time');d.update(time_start='08:59',time_end='09:01');self.assertEqual(c.calculate(d)['candidate_count'],2)
 def test_day_boundary(self):
  a=c.calculate(self.birth(time='23:30',sect=1));b=c.calculate(self.birth(time='23:30',sect=2));self.assertNotEqual(a['candidates'][0]['pillars']['day'],b['candidates'][0]['pillars']['day'])
 def test_unsupported_chart(self):
  for kw in ({'calendar':'lunar'},{'timezone':'America/New_York'},{'date':'1988-07-01'},{'date':'2005-02-30'},{'sect':True},{'time':'24:00'},{'true_solar_time':True}):
   with self.subTest(kw=kw),self.assertRaises(ValueError):c.calculate(self.birth(**kw))
 def test_cross_midnight(self):
  d=self.birth();d.pop('time');d.update(time_start='23:00',time_end='01:00')
  with self.assertRaises(ValueError):c.calculate(d)
 def test_complete_comparison(self):
  a=r.compare(self.option())['options'][0];self.assertEqual(a['preference_index'],70);self.assertEqual(a['status'],'comparable')
 def test_unknown_score(self):
  d=self.option();d['options'][0]['scores']['income']=None;a=r.compare(d)['options'][0];self.assertIsNone(a['preference_index']);self.assertEqual(a['coverage'],.5);self.assertEqual(a['possible_index_range'],[50,90])
 def test_hard_conditions(self):
  for val,expected in ((False,'excluded'),(None,'needs_verification')):
   d=self.option();d['options'][0]['hard_constraints']['city']=val;a=r.compare(d)['options'][0];self.assertEqual(a['status'],expected);self.assertIsNone(a['preference_index'])
 def test_bad_weights(self):
  for val in (True,float('nan'),float('inf'),0,-1):
   d=self.option();d['weights']['tasks']=val
   with self.assertRaises(ValueError):r.compare(d)
 def test_birth_not_scored(self):
  d=self.option();d['weights']={'bazi':1}
  with self.assertRaises(ValueError):r.compare(d)
 def test_evidence_and_confirmation(self):
  d=self.option();d['weights_confirmed']=False
  with self.assertRaises(ValueError):r.compare(d)
  d=self.option();d['options'][0]['evidence']={}
  with self.assertRaises(ValueError):r.compare(d)
 def test_search_plan_only(self):
  a=q.plan({'scenario':'transition','roles':['内容策略'],'cities':['上海']});self.assertEqual(a['mode'],'search-plan-only');self.assertNotIn('jobs',a)
 def test_birth_search_field_rejected(self):
  with self.assertRaises(ValueError):q.plan({'scenario':'transition','roles':['内容策略'],'birth_date':'2000-01-01'})
 def test_campus_year(self):
  with self.assertRaises(ValueError):q.plan({'scenario':'campus','roles':['运营']})
  self.assertIn('2027',q.plan({'scenario':'campus','roles':['运营'],'graduation_year':2027})['queries'][0])
 def test_cli_examples(self):
  for script,fixture in [('chart','birth'),('rank_options','offer'),('search_plan','search')]:
   a=subprocess.run([sys.executable,str(S/(script+'.py'))],input=(R/'examples'/f'{fixture}-input.json').read_text(),text=True,capture_output=True);self.assertEqual(a.returncode,0,a.stderr);json.loads(a.stdout)
 def test_cli_error_privacy(self):
  a=subprocess.run([sys.executable,str(S/'chart.py')],input=json.dumps(self.birth(date='1988-07-01')),text=True,capture_output=True);self.assertEqual(a.returncode,2);self.assertNotIn('1988',a.stderr);self.assertNotIn('Traceback',a.stderr)
if __name__=='__main__':unittest.main()
