import numpy as np, os
from PIL import Image
S="/tmp/claude-0/-home-user-canva/312d6e59-5646-5e80-80ec-b32288fc1bb9/scratchpad"
SRC=f"{S}/ofr_clean"          # already free of the cursor in frames 354-357
DST=f"{S}/ofr_final"; os.makedirs(DST, exist_ok=True)
N=len([f for f in os.listdir(SRC) if f.endswith(".png")])
def arr(i): return np.asarray(Image.open(f"{SRC}/f{i:04d}.png").convert("RGB")).astype(np.float32)
def gy(a): return a @ np.array([0.299,0.587,0.114],dtype=np.float32)

RY0,RY1,RX0,RX1 = 0,130,140,360      # smooth backdrop only, no product
F0,F1,W = 330, N-1, 10
MAXPIX, MAXBOX = 1400, (60,70)

rois={i: arr(i)[RY0:RY1,RX0:RX1] for i in range(max(0,F0-W), N)}
done=[]; skipped=[]
for i in range(N):
    a=arr(i)
    if F0<=i<=F1:
        idx=[j for j in range(i-W,i+W+1) if j in rois and j!=i]
        plate=np.median(np.stack([rois[j] for j in idx]),axis=0)
        m=np.abs(gy(rois[i])-gy(plate))>20
        if m.any():
            ys,xs=np.nonzero(m)
            bh,bw = ys.max()-ys.min()+1, xs.max()-xs.min()+1
            if m.sum()<=MAXPIX and bh<=MAXBOX[0] and bw<=MAXBOX[1]:
                g=m.copy()
                for _ in range(3):
                    g2=g.copy()
                    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                        g2|=np.roll(np.roll(g,dy,0),dx,1)
                    g=g2
                sub=a[RY0:RY1,RX0:RX1]; sub[g]=plate[g]; a[RY0:RY1,RX0:RX1]=sub
                done.append((i,int(m.sum()),int(bh),int(bw)))
            else:
                skipped.append((i,int(m.sum()),int(bh),int(bw)))
    Image.fromarray(np.clip(a,0,255).astype(np.uint8)).save(f"{DST}/f{i:04d}.png")
print("limpiados:", done)
print("omitidos por tamano (no es cursor):", skipped)
