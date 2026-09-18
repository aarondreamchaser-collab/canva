import numpy as np, os
from PIL import Image

S = "/tmp/claude-0/-home-user-canva/312d6e59-5646-5e80-80ec-b32288fc1bb9/scratchpad"
D = f"{S}/fr"
N = len([f for f in os.listdir(D) if f.endswith(".png")])

def load(i): return np.asarray(Image.open(f"{D}/f{i:04d}.png").convert("RGB")).astype(np.float32)
def gray(a): return a @ np.array([0.299,0.587,0.114], dtype=np.float32)

TY0,TY1,TX0,TX1 = 162,188,118,136
tpl = gray(load(420))[TY0:TY1, TX0:TX1]
th, tw = tpl.shape
med = np.median(tpl); mask = np.abs(tpl-med) > 28
tm0 = tpl[mask] - tpl[mask].mean()
tnorm = np.sqrt((tm0*tm0).sum()) + 1e-6

# region of interest the cursor travels through, plus generous margin
RY0, RY1, RX0, RX1 = 40, 660, 0, 260

def scan(g):
    sub = np.ascontiguousarray(g[RY0:RY1, RX0:RX1])
    H, W = sub.shape
    s0, s1 = sub.strides
    win = np.lib.stride_tricks.as_strided(
        sub, (H-th+1, W-tw+1, th, tw), (s0,s1,s0,s1), writeable=False)
    v = win[:, :, mask].astype(np.float32)
    v0 = v - v.mean(axis=2, keepdims=True)
    ncc = (v0*tm0).sum(axis=2) / (np.sqrt((v0*v0).sum(axis=2))*tnorm + 1e-6)
    iy, ix = np.unravel_index(int(np.argmax(ncc)), ncc.shape)
    return float(ncc[iy,ix]), RY0+iy, RX0+ix

FIRST, LAST, ACCEPT = 330, N-1, 0.60
raw = {}
for i in range(FIRST, LAST+1):
    s, y, x = scan(gray(load(i)))
    if s >= ACCEPT:
        raw[i] = (y, x, s)

ks = sorted(raw)
print(f"deteccion bruta: {len(ks)} fotogramas, {ks[0]}..{ks[-1]} "
      f"(t {ks[0]/30:.2f}s .. {ks[-1]/30:.2f}s)")

# drop spatial outliers: a real cursor moves smoothly
good = []
for i in ks:
    y, x, s = raw[i]
    near = [raw[j] for j in ks if abs(j-i) <= 3 and j != i]
    if not near or min(abs(y-b[0])+abs(x-b[1]) for b in near) < 60:
        good.append(i)
print("tras filtrar saltos:", len(good))

a0, b0 = good[0], good[-1]
path = {i: raw[i][:2] for i in good}
for k in range(a0, b0+1):                     # interpolate any gap
    if k in path: continue
    lo = max(j for j in good if j < k); hi = min(j for j in good if j > k)
    f = (k-lo)/(hi-lo)
    path[k] = (round(path[lo][0]+f*(path[hi][0]-path[lo][0])),
               round(path[lo][1]+f*(path[hi][1]-path[lo][1])))
print(f"parcheando {len(path)} fotogramas: {a0}..{b0} (t {a0/30:.2f}s .. {b0/30:.2f}s)")

PAD = 5
OUT = f"{S}/fr_clean"; os.makedirs(OUT, exist_ok=True)
for i in range(N):
    a = load(i)
    if i in path:
        y, x = path[i]
        y0,y1 = max(0,y-PAD), min(a.shape[0], y+th+PAD)
        x0,x1 = max(0,x-PAD), min(a.shape[1], x+tw+PAD)
        left  = a[y0:y1, max(0,x0-1)][:,None,:]
        right = a[y0:y1, min(a.shape[1]-1,x1)][:,None,:]
        t = np.linspace(0.,1., x1-x0, dtype=np.float32)[None,:,None]
        a[y0:y1, x0:x1] = left*(1-t) + right*t
    Image.fromarray(np.clip(a,0,255).astype(np.uint8)).save(f"{OUT}/f{i:04d}.png")
print("escritos:", len(os.listdir(OUT)))
