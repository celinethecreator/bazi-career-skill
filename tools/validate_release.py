"""Offline structure/release checks, not semantic or market validation."""
from pathlib import Path
import re
import yaml

ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/bazi-career'

def validate():
    text=(SKILL/'SKILL.md').read_text(encoding='utf-8')
    meta=yaml.safe_load(text.split('---',2)[1])
    assert set(meta)=={'name','description'}
    assert meta['name']=='bazi-career' and len(meta['description'])>30
    assert len(text.splitlines())<500
    for link in re.findall(r'\]\(([^)]+)\)',text):
        if '://' not in link:
            assert (SKILL/link).is_file(),link
    ui=yaml.safe_load((SKILL/'agents/openai.yaml').read_text())['interface']
    assert '$bazi-career' in ui['default_prompt']
    assert 25<=len(ui['short_description'])<=64
    for name in ('README.md','LICENSE','requirements.txt','THIRD_PARTY_NOTICES.md','evals/scenarios.md'):
        assert (ROOT/name).is_file(),name
    for p in ROOT.rglob('*'):
        if p.is_file() and not any(x in p.parts for x in ('.git','__pycache__','.venv')):
            assert not p.name.startswith('private-'),str(p)
    print('Release structure valid; behavioral and online verification remain separate.')

if __name__=='__main__':
    validate()
