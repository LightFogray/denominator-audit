import pandas as pd, numpy as np, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path.cwd(); OUT=ROOT/'data/processed/d1_denominator'
socio=pd.read_csv(ROOT/'data/processed/grid_socio.csv').set_index('grid_id').reindex(range(1246))
sub=pd.read_csv(OUT/'property_subtypes_grid.csv').set_index('grid_id').reindex(range(1246))
z=np.load(ROOT/'data/processed/od_corrected/divvy_2022_2023_activity.npz'); act=(z['inflow']+z['outflow']).sum(axis=(0,1))
pop=socio['pop'].values; pov=socio['poverty'].values; y=sub['THEFT'].values.astype(float)
elig=pop>=100; ai=np.where(elig)[0]
def top(idx,rate,k):
    k=min(k,len(idx)); return set(idx[np.lexsort((idx, -rate[idx]))[:k]]) if k>0 else set()
def met(S,total):
    S=list(S); return np.average(pov[S],weights=pop[S]+1e-9), y[S].sum()/total
rows=[]
for T in [10000,25000,50000]:
    ci,ui=np.where(elig&(act>=T))[0],np.where(elig&(act<T))[0]
    ra=y/(act+T); rr=y/(pop+1e-9); total=y[ai].sum(); cs=y[ci].sum()/total
    for K in [45,119,200]:
        kc=min(int(round(K*cs)),len(ci),K); ku=min(K-kc,len(ui)); kc_n=min(K,len(ci))
        H=top(ci,ra,kc)|top(ui,rr,ku); M=top(ci,rr,kc)|top(ui,rr,ku); R=top(ai,rr,K)
        A=top(ci,ra,kc_n); Mn=top(ci,rr,kc_n)
        hp, hc=met(H,total); mp, mc=met(M,total); rp, rc=met(R,total); ap, ac=met(A,total); np_, nc=met(Mn,total)
        rows.append(dict(T=T,K=K,kc=kc,ku=ku,
                         pov_den=hp-mp,pov_cov=mp-rp,cap_den=(hc-mc)*100,cap_cov=(mc-rc)*100,
                         naive_pov_den=ap-np_,naive_pov_cov=np_-rp,naive_cap_den=(ac-nc)*100,naive_cap_cov=(nc-rc)*100))
res=pd.DataFrame(rows); res.to_csv(OUT/'audit_chicago/sensitivity.csv',index=False)
print(res.round(2).to_string(index=False))
