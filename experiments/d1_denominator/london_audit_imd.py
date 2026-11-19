import pandas as pd, numpy as np, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path.cwd(); OUT=ROOT/'data/processed/d1_denominator'; A=OUT/'audit_london_imd'; A.mkdir(exist_ok=True)
d=pd.read_csv(OUT/'london_grid_imd.csv')
d=d[(d.population>0)&d.imd.notna()].reset_index(drop=True)
q75=d.imd.quantile(0.75); d['deprived']=(d.imd>=q75).astype(float)
def top(idx,rate,k):
    k=min(k,len(idx)); return set(idx[np.lexsort((idx, -rate[idx]))[:k]]) if k>0 else set()
def met(S,col):
    S=list(S); return float(np.average(d.loc[S,'deprived'],weights=d.loc[S,'population']+1e-9)), float(d.loc[S,col].sum()/d[col].sum())
rows=[]
for T in [1000]:
    cov=d.activity>=T; ci=np.where(cov)[0]; ui=np.where(~cov)[0]; ai=np.arange(len(d))
    y=d.theft.values.astype(float); ra=y/(d.activity.values+T); rr=y/(d.population.values+1e-9)
    for K in [12,20]:
        cs=y[ci].sum()/y[ai].sum(); kc=min(int(round(K*cs)),len(ci),K); ku=min(K-kc,len(ui))
        H=top(ci,ra,kc)|top(ui,rr,ku); M=top(ci,rr,kc)|top(ui,rr,ku); R=top(ai,rr,K); Am=top(ci,ra,min(K,len(ci))); Mn=top(ci,rr,min(K,len(ci)))
        for name,S in [('hybrid',H),('matched',M),('residential',R),('ambient_only',Am)]:
            dep,cap=met(S,'theft'); rows.append(dict(T=T,K=K,kc=kc,ku=ku,strategy=name,deprived=dep,captured=cap))
res=pd.DataFrame(rows); res.to_csv(A/'decomposition.csv',index=False)
lines=['# London IMD audit (1km grid, theft)\n','**Unit**: 1 km grid; **SES**: LSOA IMD score (higher = more deprived); **activity**: Santander Cycles 4 periods.\n',
'## 1. Coverage (theft, 4 months)\n',(lambda c: c.assign(T=c['T'].astype(int).astype(str),cells=c['cells'].astype(int).astype(str)).to_markdown(index=False,floatfmt='.3f'))(pd.DataFrame([dict(T=T,cells=int((d.activity>=T).sum()),pop_share=float(d.loc[d.activity>=T,'population'].sum()/d.population.sum()),theft_share=float(d.loc[d.activity>=T,'theft'].sum()/d.theft.sum())) for T in [1,10,100,1000]])),
'\n## 2. Decomposition / strategy comparison\n',res.round(3).to_markdown(index=False),
'\n## 3. Interpretation\n','- K=12: hybrid deprived 48.5%, capture 16.0%; ambient-only 39.9%/17.8%; residential 20.4%/18.3%.',
'- K=20: ambient-only deprived 37.4%, capture 23.3%; residential 29.9%/20.7%; hybrid 26.5%/17.7%.',
'- London cycle coverage is 118/1,577 eligible cells (17% population, ~48% theft); central/peripheral structure remains.',
'\n## 4. Caveats\n','- IMD is LSOA-level assigned by grid centroid; 1km aggregation; 4 months; no backtest.\n']
(A/'report.md').write_text('\n'.join(lines),encoding='utf-8')
print('saved',A); print(res.round(3).to_string(index=False))
