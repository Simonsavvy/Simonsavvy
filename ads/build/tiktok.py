import subprocess, os
from PIL import Image, ImageDraw, ImageFont
W,H=1080,1920
B="/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
R="/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
U="/root/.claude/uploads/85553a0d-6a9c-5531-9d67-65ea6d12bafa/"
V3=U+"46bddeba-2026-09-19-101118565.mp4"; V4=U+"5e965a77-VID-20260919-WA0007.mp4"
APP=U+"3254dca2-Screenrecorder-2026-09-28-19-41-42-946.mp4"
G=(20,96,58); GOLD=(214,168,74); OFF=(247,245,238)
def wrap(d,t,f,mw):
    out,cur=[], ""
    for w in t.split():
        s=(cur+" "+w).strip()
        if d.textlength(s,font=f)<=mw: cur=s
        else: out.append(cur); cur=w
    return out+[cur]
def boxes(text,out,cy,size=58,ai=False,bg="white",fg="black"):
    """TikTok 'classic box' text: black text on white rounded boxes, centred."""
    im=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); f=ImageFont.truetype(B,size)
    lines=wrap(d,text,f,820); lh=size+30; y=cy-len(lines)*lh//2
    for l in lines:
        tw=d.textlength(l,font=f); x=(W-tw)/2
        d.rounded_rectangle((x-26,y-12,x+tw+26,y+size+14),18,fill=bg)
        d.text((x,y),l,font=f,fill=fg); y+=lh
    if ai:
        t=ImageFont.truetype(B,30); d.rounded_rectangle((40,170,262,222),14,fill=(0,0,0,160))
        d.text((58,180),"AI-generated",font=t,fill="white")
    im.save(out)
def endcard(l1,l2,out):
    im=Image.new("RGB",(W,H),G); d=ImageDraw.Draw(im)
    f1,f2,f3,f4=[ImageFont.truetype(p,s) for p,s in ((B,120),(B,58),(R,46),(R,36))]
    def c(y,s,f,col): d.text(((W-d.textlength(s,font=f))/2,y),s,font=f,fill=col)
    c(420,"SimoVet",f1,OFF); d.rectangle((400,575,680,583),fill=GOLD); y=640
    for l in wrap(d,l1,f2,900): c(y,l,f2,OFF); y+=72
    y+=16
    for l in wrap(d,l2,f3,900): c(y,l,f3,GOLD); y+=60
    d.rounded_rectangle((140,1060,940,1170),55,fill=OFF); c(1087,"simonetvetcare.co.ke",f2,G)
    c(1210,"Opens in any phone browser",f3,OFF); c(1280,"WhatsApp support: +254 181 454 640",f4,OFF)
    c(1380,"Video features an AI-generated actor",f4,(200,220,205)); im.save(out)
N="fps=30,setsar=1,format=yuv420p"
def hookf(src,crop):  # fill 9:16 + slow punch-in
    return f"{crop}scale=w='1080*(1+0.035*t)':h=-2:eval=frame,crop=1080:1920,{N}"
def ad(name,hsrc,hcrop,hst,hook,segs,end):
    boxes(hook,"hk.png",620,62,ai=True); endcard(*end,"end.png")
    ins=["-ss",str(hst),"-t","2.8","-i",hsrc,"-loop","1","-i","hk.png"]
    fc=f"[0:v]{hookf(hsrc,hcrop)}[h0];[h0][1:v]overlay=shortest=1,{N}[h];"; lst="[h]"; n=2
    for k,(kind,a,b,cap,yoff) in enumerate(segs):
        if kind=="S":
            subprocess.run(["ffmpeg","-v","error","-y","-ss",str(a),"-i",APP,"-frames:v","1",f"st{k}.png"],check=True)
            ins+=["-loop","1","-t",str(b),"-i",f"st{k}.png"]
        else: ins+=["-ss",str(a),"-t",str(round(b-a,2)),"-i",APP]
        boxes(cap,f"cap{k}.png",270,50,bg=(20,96,58),fg="white"); ins+=["-loop","1","-i",f"cap{k}.png"]
        fc+=(f"[{n}:v]crop=720:1280:0:{yoff},scale=w='1080*(1+0.025*t)':h=-2:eval=frame,crop=1080:1920,{N}[s{k}];"
             f"[s{k}][{n+1}:v]overlay=shortest=1,{N}[d{k}];"); lst+=f"[d{k}]"; n+=2
    ins+=["-loop","1","-t","2.5","-i","end.png"]
    fc+=f"[{n}:v]scale=w='1080*(1+0.02*t)':h=-2:eval=frame,crop=1080:1920,{N}[e];{lst}[e]concat=n={len(segs)+2}:v=1:a=0[v]"
    subprocess.run(["ffmpeg","-v","error","-y",*ins,"-f","lavfi","-i","anullsrc=r=44100:cl=stereo","-filter_complex",fc,
        "-map","[v]","-map",f"{n+1}:a","-shortest","-c:v","libx264","-profile:v","high","-crf","18","-preset","medium",
        "-c:a","aac","-b:a","128k","-movflags","+faststart",f"../{name}"],check=True); print("ok",name)
C3=""; C4="crop=405:720:437:0,"
if __name__=="__main__":
    ad("simovet_ad1_farmers_licensed.mp4",V3,C3,0,"how do you know your vet is actually licensed?",
       [("S",3.5,2.0,"every vet's KVB licence is checked by a person",120),
        ("V",4.0,5.0,"book and pay with m-pesa",120),
        ("V",32.8,34.9,"verified vets near you, nearest first",170)],
       ("Book a KVB-verified vet. Pay by M-Pesa.","Every vet's licence is checked by a person."))
    ad("simovet_ad2_vets_paid_first.mp4",V4,C4,6,"the farmer pays before you even see the request",
       [("V",4.0,5.0,"farmers pay by m-pesa when they book",120),
        ("S",8.9,3.2,"85% paid to your m-pesa after each confirmed visit",170)],
       ("Vets: free to join.","Set your own prices, hours and service area."))
    ad("simovet_ad3_farmers_prices.mp4",V3,C3,5,"vet prices shown before you book. finally.",
       [("V",39.5,44.8,"every vet card shows services + prices",170)],
       ("See each vet's services and prices before you book.","Pay by M-Pesa. Get a full visit record."))
    