"""Regenerate public Playcards PDFs. Optional authoring dependency: ReportLab.
The website build uses the checked-in PDFs and needs no extra dependencies.
"""
from pathlib import Path
from html import escape
import json, shutil
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.units import mm
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'website/assets'
OUT=ROOT/'output/pdf'; OUT.mkdir(parents=True,exist_ok=True)
PUBLIC=ASSETS/'playcards'; PUBLIC.mkdir(exist_ok=True)
for name,file in [('Display','font-1.ttf'),('Body','font-4.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(ASSETS/'fonts'/file)))
TEAL=HexColor('#173d40'); CREAM=HexColor('#fff9f3'); SAND=HexColor('#cfb77f'); LIGHT=HexColor('#f1e3c8')
W,H=105*mm,148*mm
cards=json.loads((ROOT/'website/playcards-content.json').read_text())

def para(c,text,font,size,color,x,y,width,leading=None):
    style=ParagraphStyle('card',fontName=font,fontSize=size,leading=leading or size*1.4,textColor=color)
    p=Paragraph(escape(text).replace('\n','<br/>'),style)
    _,height=p.wrap(width,H)
    p.drawOn(c,x,y-height)
    return height

def symbol(c):
    c.saveState();c.setStrokeColor(SAND);c.setLineWidth(.8)
    for dx,dy,angle in [(0,0,12),(7,-3,-12)]:
        c.saveState();c.translate(W-42+dx,H-42+dy);c.rotate(angle);c.roundRect(-9,-14,18,28,2,stroke=1,fill=0);c.restoreState()
    c.restoreState()

def frame(c,label,lang):
    c.setFillColor(CREAM);c.rect(0,0,W,H,stroke=0,fill=1)
    c.setFillColor(SAND);c.rect(14,11,W-23,H-23,stroke=0,fill=1)
    c.setFillColor(TEAL);c.rect(9,16,W-23,H-23,stroke=0,fill=1)
    symbol(c)
    c.setFillColor(LIGHT);c.setFont('Body',6.8);c.drawString(28,H-40,label)
    c.setStrokeColor(HexColor('#647b7b'));c.setLineWidth(.4);c.line(28,53,W-34,53)
    c.setFont('Body',5.6);c.drawString(28,39,'PLAYCARDS / CHANTAL VAN KEMPEN')
    c.setFillColor(TEAL);c.setFont('Body',5.5);c.drawRightString(W-12,4,lang.upper())

for lang in ['nl','en']:
    path=OUT/f'playcards-chantal-van-kempen-{lang}.pdf'
    c=canvas.Canvas(str(path),pagesize=(W,H),pageCompression=1,invariant=1)
    c.setTitle('Playcards - Time and space | Chantal van Kempen | '+lang.upper())
    c.setAuthor('Chantal van Kempen');c.setSubject('50 speelkaarten' if lang=='nl' else '50 playcards')
    frame(c,'TIME AND SPACE / 50 PLAYCARDS',lang)
    title_height=para(c,'Even spelen.\nAnders kijken.' if lang=='nl' else 'A little play.\nA fresh perspective.','Display',31,LIGHT,28,H-94,W-62,32)
    intro=('Een klein spel voor een frisse blik. Kies een kaart bij de start van een overleg of werkdag. Lees de opdracht samen en probeer het.\n\nDeze set bevat alle 50 kaarten. Eén kaart per pagina, op A6-formaat.' if lang=='nl' else 'A small game for a fresh perspective. Pick a card at the start of a meeting or working day. Read the prompt together and give it a go.\n\nThis set contains all 50 cards. One card per page, in A6 format.')
    intro_height=para(c,intro,'Body',10,CREAM,28,H-94-title_height-22,W-62,14)
    assert H-94-title_height-22-intro_height>65
    c.showPage()
    for card in cards:
        d=dict(card[lang]);d['title']=d['title'].replace('Swoboda-Fliess-Teltscher','Swoboda-Fliess-\nTeltscher');frame(c,('SPEELKAART' if lang=='nl' else 'PLAYCARD')+f' / {card["id"]:02d}',lang)
        # Fit the complete title, principle and prompt above the footer; never clip text.
        for scale in [1,.97,.94,.91,.88,.85,.82]:
            title_size=min(26*scale,min((W-62)/pdfmetrics.stringWidth(word,'Display',1) for word in d['title'].split()))
            styles=[('title','Display',title_size,title_size*1.06),('principle','Body',9*scale,12.5*scale),('text','Body',11*scale,15.5*scale)]
            heights=[]
            for key,font,size,leading in styles:
                p=Paragraph(escape(d[key]).replace('\n','<br/>'),ParagraphStyle('measure',fontName=font,fontSize=size,leading=leading))
                heights.append(p.wrap(W-62,H)[1])
            total=sum(heights)+30
            if total<=H-144:break
        else:raise ValueError(f'Card does not fit: {lang} {card["id"]}')
        y=H-81
        for (key,font,size,leading),height in zip(styles,heights):
            para(c,d[key],font,size,LIGHT if key!='text' else CREAM,28,y,W-62,leading)
            y-=height+(14 if key=='title' else 16)
        assert y>=57,(lang,card['id'],y)
        c.showPage()
    c.save();shutil.copy2(path,PUBLIC/path.name)
    print(f'{path}: {len(cards)+1} pages, A6')
