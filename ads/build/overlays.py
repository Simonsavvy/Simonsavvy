from PIL import Image, ImageDraw, ImageFont
W,H=720,1280
B="/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
R="/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
def wrap(d,text,font,maxw):
    words,lines,cur=text.split(),[], ""
    for w in words:
        t=(cur+" "+w).strip()
        if d.textlength(t,font=font)<=maxw: cur=t
        else: lines.append(cur); cur=w
    lines.append(cur); return lines
def hook(text,out):
    im=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    f=ImageFont.truetype(B,50); lines=wrap(d,text,f,600); lh=62
    y=int(H*0.30)-len(lines)*lh//2
    for l in lines:
        x=(W-d.textlength(l,font=f))/2
        d.text((x,y),l,font=f,fill="white",stroke_width=5,stroke_fill="black"); y+=lh
    t=ImageFont.truetype(B,22); d.rounded_rectangle((20,20,190,58),10,fill=(0,0,0,150))
    d.text((34,28),"AI-generated",font=t,fill="white")
    im.save(out)
def endcard(line1,line2,out):
    G=(20,96,58); GOLD=(214,168,74); OFF=(247,245,238)
    im=Image.new("RGB",(W,H),G); d=ImageDraw.Draw(im)
    f1=ImageFont.truetype(B,84); f2=ImageFont.truetype(B,40); f3=ImageFont.truetype(R,34); f4=ImageFont.truetype(R,26)
    def c(y,s,f,col): d.text(((W-d.textlength(s,font=f))/2,y),s,font=f,fill=col)
    c(330,"SimoVet",f1,OFF); d.rectangle((260,440,460,446),fill=GOLD)
    y=500
    for l in wrap(d,line1,f2,620): c(y,l,f2,OFF); y+=52
    y+=10
    for l in wrap(d,line2,f3,620): c(y,l,f3,GOLD); y+=46
    d.rounded_rectangle((90,800,630,880),40,fill=OFF); c(820,"simonetvetcare.co.ke",f2,G)
    c(920,"Opens in any phone browser",f3,OFF)
    c(970,"WhatsApp support: +254 181 454 640",f4,OFF)
    c(1210,"Video features an AI-generated actor",f4,(200,220,205))
    im.save(out)
hook("how do you know your vet is actually licensed?","hookA.png")
hook("the farmer pays before you even see the request","hookB.png")
hook("vet prices shown before you book. finally.","hookC.png")
endcard("Book a KVB-verified vet. Pay by M-Pesa.","Every vet's licence is checked by a person.","endA.png")
endcard("Vets: free to join.","Farmers pay upfront. 85% goes to your M-Pesa after each confirmed visit.","endB.png")
endcard("See each vet's services and prices before you book.","Pay by M-Pesa. Get a full visit record.","endC.png")
