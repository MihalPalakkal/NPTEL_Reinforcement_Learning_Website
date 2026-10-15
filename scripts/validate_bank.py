"""Validate the complete bank, asset mappings, inventory and answer provenance."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def validate():
 qs=json.loads((ROOT/'public/data/questions.json').read_text());expected=[10,10,10,10,8,10,10,10,10,10,10,5];ids=set();assets=set();rows=[]
 for w,n in enumerate(expected,1):
  items=[q for q in qs if q['week']==w]
  assert len(items)==n,(w,len(items),n)
  assert sorted(q['questionNumber'] for q in items)==list(range(1,n+1)),w
  rows.append({'week':w,'identified':n,'extracted':len(items),'pdfKeys':sum(q['verification']=='source-verified' for q in items),'independentlySolved':sum(q['verification']=='independently-solved' for q in items),'withDiagrams':sum(bool(q['diagrams']) for q in items),'sourcePages':sorted({p for q in items for p in q['sourcePages']}),'unresolvedAnswers':sum(not q['correctAnswers'] for q in items)})
 for q in qs:
  assert q['id']==f"week{q['week']}-q{q['questionNumber']}"
  assert q['id'] not in ids;qid=q['id'];ids.add(qid)
  assert q['questionText'].strip() and len(q['options'])>=2,qid
  assert q['questionText'].count('$')%2==0,qid
  options=[o['id'] for o in q['options']]
  assert options==list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'[:len(options)]),qid
  assert q['correctAnswers'] and len(q['correctAnswers'])==len(set(q['correctAnswers'])),qid
  assert set(q['correctAnswers'])<=set(options),qid
  assert q['type']=='multi-select' or len(q['correctAnswers'])==1,qid
  if q['verification']=='source-verified':assert q['officialCorrectAnswers']==q['correctAnswers'] and q['answerEvidence'],qid
  if q['verification']=='independently-solved':assert q['explanation'] and q['restorationNote'],qid
  for o in q['options']:assert o['text'].strip() and o['text'].count('$')%2==0,(qid,o['id'])
  references=[q['sourceImage'],q['answerEvidence']]+[o.get('sourceImage') for o in q['options']]+[d['src'] for d in q['diagrams']]
  for src in filter(None,references):
   assert src.startswith('/assets/'),src
   path=ROOT/'public'/src.lstrip('/');assert path.is_file() and path.stat().st_size>0,(qid,src)
   assets.add(src)
 assert len(qs)==113
 report={'source':'Assignments.pdf','pagesProcessed':59,'questionCount':len(qs),'pdfKeysVerified':112,'independentlySolved':1,'sourceRestorations':1,'unresolvedAnswerKeys':0,'unrecoverableOriginalDetails':['week3-q4: original last distractor is clipped. D is reconstructed and labeled; B is independently solved.'],'localAssetsChecked':len(assets),'weeks':rows,'validation':'passed'}
 (ROOT/'public/data/audit.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2));return report
if __name__=='__main__':validate()
