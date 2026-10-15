"""Reproducible screenshot/OCR extraction. Never infer a missing answer.
Usage: python scripts/extract.py /absolute/path/Assignments.pdf --work /path/to/work
Requires: pymupdf pillow numpy, and the tesseract executable.
The reviewed inventory specifies native screenshot coordinates (not PDF points).
"""
import argparse, pathlib, json, subprocess, concurrent.futures, re, hashlib
import pymupdf
from PIL import Image, ImageChops
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1]
a=argparse.ArgumentParser();a.add_argument('pdf');a.add_argument('--work',default=str(ROOT/'work'));args=a.parse_args()
work=pathlib.Path(args.work);(work/'pages').mkdir(parents=True,exist_ok=True);(work/'crops').mkdir(exist_ok=True)
assets=ROOT/'public/assets';assets.mkdir(exist_ok=True);(ROOT/'public/data').mkdir(exist_ok=True)
pdf=pymupdf.open(args.pdf)
for i,p in enumerate(pdf):
 imgs=p.get_images(full=True)
 assert len(imgs)==1, f'Unexpected structure on page {i+1}'
 pymupdf.Pixmap(pdf,imgs[0][0]).save(work/f'pages/{i+1:02}.png')

def crop(im,box,name):
 c=im.crop(tuple(map(int,box))).convert('RGB')
 # Tight bounds preserve the complete source ink; four pixels padding.
 arr=np.asarray(c);ys,xs=np.where(np.min(arr,axis=2)<205)
 if len(xs):c=c.crop((max(0,int(xs.min())-4),max(0,int(ys.min())-4),min(c.width,int(xs.max())+5),min(c.height,int(ys.max())+5)))
 c.save(assets/(name+'.png'));return c
jobs=[];bank=[]
for line in (ROOT/'scripts/inventory.txt').read_text().splitlines():
 if not line or line.startswith('#'):continue
 w,q,p,top,centers,ky,ans,typ=line.split('|');w,q,p,top,ky=map(int,[w,q,p,top,ky]);centers=list(map(int,centers.split(',')))
 id=f'week{w}-q{q}';im=Image.open(work/f'pages/{p:02}.png')
 statement=crop(im,(30,top,1250,centers[0]-18),id+'-statement')
 jobs.append((id+'-statement',statement))
 opts=[]
 for j,y in enumerate(centers):
  start=(centers[j-1]+y)//2 if j else y-18
  end=(y+centers[j+1])//2 if j<len(centers)-1 else min(750,y+18)
  c=crop(im,(63,start,1250,end),id+'-'+chr(65+j));jobs.append((id+'-'+chr(65+j),c))
  opts.append({'id':chr(65+j),'text':'','sourceImage':f'/assets/{id}-{chr(65+j)}.png'})
 if ky:
  im.crop((210, max(153,ky-20),1310,min(751,ky+22))).save(assets/(id+'-key.png'))
 bank.append({'id':id,'week':w,'questionNumber':q,'questionText':'','type':{'single':'single-select','multi':'multi-select','tf':'true-false'}[typ],'options':opts,'correctAnswers':None if ans=='?' else list(ans),'explanation':None,'sourcePages':[p],'sourceImage':f'/assets/{id}-statement.png','answerEvidence':f'/assets/{id}-key.png' if ky else None,'verification':'needs-review' if ans=='?' else 'source-verified','issues':[],'diagrams':[]})

def ocr(job):
 name,im=job;path=work/'crops'/f'{name}.png';im.resize((im.width*3,im.height*3)).save(path)
 out=subprocess.run(['tesseract',str(path),'stdout','--psm','6'],capture_output=True,text=True,check=True).stdout.strip()
 return name,out
texts=dict(concurrent.futures.ThreadPoolExecutor(max_workers=6).map(ocr,jobs))
for q in bank:
 q['questionText']=re.sub(r'^\d+[.,]?\s*','',texts[q['id']+'-statement']).strip()
 for o in q['options']:o['text']=texts[q['id']+'-'+o['id']]
 if q['verification']=='needs-review':q['issues']=['Page 12 cuts off the end of the option list and all answer feedback. Three complete choices are visible. Additional choice(s) and the accepted key require a better source. This question is ungraded.']
(ROOT/'public/data/questions-ocr.json').write_text(json.dumps(bank,ensure_ascii=False,indent=2))
(work/'crop-transcripts.txt').write_text('\n\n'.join(f"{q['id']}\n{q['questionText']}\n"+'\n'.join(o['id']+': '+o['text'] for o in q['options']) for q in bank))
print(f'Processed {len(pdf)} pages, {len(bank)} questions, {len(jobs)} text regions.')
print('Apply reviewed corrections with scripts/finalize.py; raw OCR is not the final bank.')
