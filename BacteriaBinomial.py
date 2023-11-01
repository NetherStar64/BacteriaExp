import matplotlib.pyplot as plt
import numpy as np
import random
from tqdm import tqdm

NPetri = 5_000      # Anzahl der Petrischalen 
NBac  = 40_000      # Anzahl der Bakterien pro Petrischale

μCFU = 0.05
σCFU = 0.015
μKILL = 0.04
σKILL = 0.004

GleichePetrischalen = False
ExtraInfo = False

def clip(val, vmin, vmax):
    return min(max(val,vmin),vmax)
def pclip(val):
    return clip(val,0,1)

resC = []
resT = []

fig, ax = plt.subplots(1, 2, sharey=False, tight_layout=True)

for Petri in tqdm(range(NPetri)):   # Für jede Petrischale
    TestAliveBacteria = NBac
    ControlAliveBacteria = NBac

    if GleichePetrischalen == False:
      PCFU = np.random.default_rng().normal(μCFU, σCFU,1)[0]      # Wahrscheinlichkeit, dass Bakterium Kolonie bildet
      PCFU = pclip(PCFU)                                          # Begrenzen der Wahrscheinlichkeit zwischen 0-1
      PKILL = np.random.default_rng().normal(μKILL, σKILL,1)[0]   # Wahrscheinlichkeit, Elektrizität zu überleben
      PKILL = pclip(PKILL)                                        # Begrenzen der Wahrscheinlichkeit zwischen 0-1
    else:   # Falls Petrischalen gleich sein sollen
      PCFU = μCFU
      PKILL = μKILL

    # Testgruppe
    NewTestAliveBacteria = 0
    for i in range(TestAliveBacteria):      # Bakterien werden mit strom umgebracht
        t = random.random()
        if t < PKILL:
            NewTestAliveBacteria += 1
    TestAliveBacteria = NewTestAliveBacteria

    NewTestAliveBacteria = 0
    for i in range(TestAliveBacteria):      # Bakterien sterben auf Petrischale
        t = random.random()
        if t < PCFU:
            NewTestAliveBacteria += 1
    TestAliveBacteria = NewTestAliveBacteria

    # Kontrollgruppe
    NewControlAliveBacteria = 0
    for i in range(ControlAliveBacteria):      # Bakterien sterben auf Petrischale
        t = random.random()
        if t < PCFU:
            NewControlAliveBacteria += 1
    ControlAliveBacteria = NewControlAliveBacteria
    if ExtraInfo:
        tqdm.write(f"Petri {Petri} has {TestAliveBacteria} on Test and {ControlAliveBacteria} in Control | pcfu {round(PCFU,2)} pkill {round(PKILL,2)} | EV T {round(NBac*PKILL*PCFU,1)} C {round(NBac*PCFU,1)}")
    resC.append(ControlAliveBacteria)
    resT.append(TestAliveBacteria)

if GleichePetrischalen:
    nbinc = list(range(1750,2200,4))
    nbint = list(range(50,130,1))
else:
    nbinc = list(range(0,5000,48))
    nbint = list(range(0,200,2))

ax[0].hist(resC,bins=nbinc)
ax[0].set_title("Kontrollgruppe")
ax[0].set_xlabel("Bakterien")
ax[1].hist(resT,bins=nbint)
ax[1].set_title("Testgruppe")
ax[1].set_xlabel("Bakterien")
plt.show()
