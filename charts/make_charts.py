"""PR charts from results.json. Plain horizontal bars, one idea each."""
import json,sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
R=json.load(open(sys.argv[1] if len(sys.argv)>1 else 'results.json'))
INK='#1a1a1a';MUTED='#6b6b6b';GRID='#e6e6e6';BASE='#9a9a9a';NEW='#2f6fde'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':15,'axes.edgecolor':GRID,'text.color':INK,
    'axes.labelcolor':MUTED,'xtick.color':MUTED,'ytick.color':INK})
def bars(panels,path,note=None):
    fig,axes=plt.subplots(1,len(panels),figsize=(8*len(panels),5.2),dpi=150)
    if len(panels)==1:axes=[axes]
    for ax,(title,rows,unit) in zip(axes,panels):
        names=[r[0] for r in rows][::-1];values=[r[1] for r in rows][::-1]
        colors=[BASE if n.startswith('v0.3') else NEW for n in names]
        b=ax.barh(names,values,color=colors,height=.62)
        top=max(values)
        for rect,v,n in zip(b,values,names):
            label=f'{v:.0f} {unit}' if v>=20 else f'{v:.1f} {unit}'
            t=ax.text(v+top*.015,rect.get_y()+rect.get_height()/2,label,va='center',ha='left',fontsize=14,color=INK)
            if not n.startswith('v0.3') and top/v>=1.05:
                ax.annotate(f'{top/v:.1f}×',xy=(1,.5),xycoords=t,xytext=(10,0),textcoords='offset points',va='center',ha='left',fontsize=12,color=MUTED)
        ax.set_xlim(0,top*1.42);ax.set_title(title,loc='left',fontsize=15,color=MUTED,pad=12)
        for s in ('top','right','left'):ax.spines[s].set_visible(False)
        ax.tick_params(axis='y',length=0);ax.xaxis.set_visible(False);ax.spines['bottom'].set_visible(False)
    if note:
        fig.suptitle(note,x=.012,y=.985,ha='left',fontsize=20,color=INK,fontweight='bold')
        fig.text(.012,.885,'Blue = new --quality tiers  ·  × = speedup over v0.3',fontsize=14,color=MUTED,ha='left')
    fig.tight_layout(rect=(0,0,1,.87 if note else 1));fig.savefig(path,facecolor='white');plt.close(fig)
def frontier(chart):
    fig,ax=plt.subplots(figsize=(10,5.6),dpi=150)
    pts=chart['points'];top=chart['identical_y']
    xs=[p['x'] for p in pts];ys=[top if p['y'] is None else p['y'] for p in pts]
    new=[(x,y) for p,x,y in zip(pts,xs,ys) if p['name']!='v0.3']
    ax.plot([x for x,_ in new],[y for _,y in new],color=NEW,lw=2,zorder=2)
    for p,x,y in zip(pts,xs,ys):
        old=p['name']=='v0.3'
        ax.scatter([x],[y],s=110,color=BASE if old else NEW,zorder=3,edgecolor='white',linewidth=2)
        dx,dy,ha=p.get('offset',(0,12,'center'))
        ax.annotate(p['name'],(x,y),textcoords='offset points',xytext=(dx,dy),ha=ha,fontsize=14,color=INK)
    ax.set_ylim(chart['ymin'],top-8);ax.set_xlim(0,max(xs)*1.1)
    ticks=chart['yticks'];ax.set_yticks(ticks+[top]);ax.set_yticklabels([f'{t} dB' for t in ticks]+['identical'])
    ax.set_xlabel(chart['xlabel'],labelpad=10);ax.set_ylabel(chart['ylabel'],labelpad=10)
    ax.grid(axis='y',color=GRID,lw=1);ax.set_axisbelow(True)
    ax.get_ygridlines()[-1].set_linestyle((0,(4,4)))
    ax.spines['left'].set_bounds(chart['ymin'],ticks[-1]-6)
    for s in ('top','right'):ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    fig.suptitle(chart['title'],x=.012,y=.985,ha='left',fontsize=18,color=INK,fontweight='bold')
    fig.tight_layout(rect=(0,0,1,.97));fig.savefig(chart['file'],facecolor='white');plt.close(fig);print(chart['file'])
for chart in R.get('frontiers',[]):frontier(chart)
for chart in R['charts']:
    bars([(p['title'],[(r['name'],r['value']) for r in p['rows']],p['unit']) for p in chart['panels']],chart['file'],chart.get('note'))
    print(chart['file'])
