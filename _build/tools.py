# Free online calculators: (slug, title, h1, meta description, intro html, tool html+js, related paid slug, related free slug)
T = [
("grocery-unit-price-calculator",
 "Grocery Unit Price Calculator",
 "Grocery Unit Price Calculator: Which Pack Is Cheaper?",
 "Free grocery unit price calculator. Compare up to 4 packs or stores in oz, lb, fl oz, g, kg, ml or l and see which one is really cheaper and by how much.",
 "<p>Type the price and size of up to four options. The calculator converts everything to the same unit and shows which pack is cheapest and how much more the others cost.</p>",
 """<div class="calc" id="up"><div class="row head"><span>Option</span><span>Price</span><span>Size</span><span>Unit</span></div>
<div id="uprows"></div>
<div class="out" id="upout">Enter at least two options.</div></div>
<script>
(function(){const U={g:['w',1],kg:['w',1000],oz:['w',28.3495],lb:['w',453.592],ml:['v',1],l:['v',1000],'fl oz':['v',29.5735],item:['n',1]};
const rows=document.getElementById('uprows');const names=['A','B','C','D'];
rows.innerHTML=names.map((n,i)=>`<div class="row"><span><input id="un${i}" value="Option ${n}" aria-label="Option name"></span><span><input id="up${i}" type="number" step="0.01" min="0" placeholder="3.99" aria-label="Price"></span><span><input id="us${i}" type="number" step="0.01" min="0" placeholder="16" aria-label="Size"></span><span><select id="uu${i}" aria-label="Unit">${Object.keys(U).map(k=>`<option${k==='oz'?' selected':''}>${k}</option>`).join('')}</select></span></div>`).join('');
function run(){const it=[];for(let i=0;i<4;i++){const p=+document.getElementById('up'+i).value,s=+document.getElementById('us'+i).value,u=document.getElementById('uu'+i).value;if(p>0&&s>0)it.push({n:document.getElementById('un'+i).value,t:U[u][0],per:p/(s*U[u][1]),u});}
const o=document.getElementById('upout');if(it.length<2){o.innerHTML='Enter at least two options.';return;}
const types=new Set(it.map(x=>x.t));if(types.size>1){o.innerHTML='Use the same kind of unit for every option (all weight, all volume or all items).';return;}
const t=it[0].t;const base=t==='w'?['100 g',100]:t==='v'?['100 ml',100]:['item',1];it.sort((a,b)=>a.per-b.per);const best=it[0];
o.innerHTML=`<p class="win">Cheapest: <strong>${best.n}</strong> at ${(best.per*base[1]).toFixed(3)} per ${base[0]}</p><ul>`+it.slice(1).map(x=>`<li>${x.n}: ${(x.per*base[1]).toFixed(3)} per ${base[0]}, <strong>${Math.round((x.per/best.per-1)*100)}% more</strong></li>`).join('')+'</ul>';}
document.getElementById('up').addEventListener('input',run);})();
</script>""",
 "grocery-price-book-deal-finder", "free-grocery-unit-price-calculator"),

("black-friday-countdown",
 "Black Friday Countdown & Deal Checker",
 "Black Friday 2026 Countdown and Deal Checker",
 "How many days until Black Friday, Cyber Monday and Boxing Day 2026? Free countdown plus a quick check to see if a sale price is really a deal.",
 "<p>See how many days are left until the big sales, then check any deal: enter the regular price, your target price and the sale price.</p>",
 """<div class="calc"><div id="cd" class="cd"></div>
<h3>Is it a real deal?</h3>
<div class="row"><label>Regular price<input id="bfr" type="number" step="0.01" placeholder="349.99"></label><label>Your target price<input id="bft" type="number" step="0.01" placeholder="249.99"></label><label>Sale price today<input id="bfs" type="number" step="0.01" placeholder="279.99"></label></div>
<div class="out" id="bfout">Enter the three prices.</div></div>
<script>
(function(){function bf(y){const d=new Date(y,10,1);const add=(4-d.getDay()+7)%7;return new Date(y,10,1+add+21+1);}
const now=new Date();let y=now.getFullYear();if(new Date(y,11,27)<now)y++;const B=bf(y),C=new Date(B.getFullYear(),B.getMonth(),B.getDate()+3),X=new Date(y,11,26);
const days=t=>Math.max(0,Math.ceil((t-new Date(now.getFullYear(),now.getMonth(),now.getDate()))/864e5));const f=t=>t.toLocaleDateString('en-US',{weekday:'short',month:'short',day:'numeric',year:'numeric'});
document.getElementById('cd').innerHTML=[['Black Friday',B],['Cyber Monday',C],['Boxing Day (UK & Canada)',X]].map(([n,t])=>`<div class="box"><div class="big">${days(t)}</div><div>days to <strong>${n}</strong></div><div class="mut">${f(t)}</div></div>`).join('');
function run(){const r=+bfr.value,t=+bft.value,s=+bfs.value,o=document.getElementById('bfout');if(!(r>0&&s>0)){o.innerHTML='Enter the three prices.';return;}
const save=r-s,pc=save/r*100;let v;if(t>0&&s<=t)v='<p class="win">BUY NOW: the price is at or below your target.</p>';else if(t>0&&s<=t*1.1)v='<p>Close to your target (within 10%). Check other stores first.</p>';else v='<p>Wait: the price is still above your target.</p>';
o.innerHTML=v+`<p>You save <strong>${save.toFixed(2)}</strong> (${pc.toFixed(0)}% off the regular price).</p>`;}
['bfr','bft','bfs'].forEach(i=>document.getElementById(i).addEventListener('input',run));})();
</script>""",
 "black-friday-deal-planner-2026", "free-black-friday-wishlist"),

("car-lease-vs-buy-calculator",
 "Car Lease vs Buy Calculator",
 "Car Lease vs Buy Calculator: Monthly Payment and True Cost",
 "Free lease vs buy calculator: compare a car loan and a lease side by side with monthly payment, total cost and value left at the end. Works in any currency.",
 "<p>Enter the car price and both offers. The calculator shows the monthly payment and the true cost of each option over the same number of months.</p>",
 """<div class="calc"><div class="row"><label>Car price (after discounts)<input id="cp" type="number" value="35000"></label><label>Down payment<input id="cd0" type="number" value="3000"></label><label>Sales tax / VAT % (0 if included)<input id="ct" type="number" value="7"></label></div>
<h3>Buy with a loan</h3><div class="row"><label>APR %<input id="ca" type="number" step="0.01" value="6.5"></label><label>Loan term (months)<input id="cn" type="number" value="60"></label><label>Value of the car at the end<input id="cr" type="number" value="17000"></label></div>
<h3>Lease</h3><div class="row"><label>Lease term (months)<input id="ln" type="number" value="36"></label><label>Residual value %<input id="lr" type="number" value="58"></label><label>Money factor (APR ÷ 2400)<input id="lm" type="number" step="0.00001" value="0.0025"></label><label>Fees due at signing<input id="lf" type="number" value="1500"></label></div>
<div class="out" id="cout"></div></div>
<script>
(function(){const g=i=>+document.getElementById(i).value||0;function run(){const P=g('cp'),D=g('cd0'),tx=g('ct')/100;
const fin=P*(1+tx)-D,r=g('ca')/1200,n=Math.max(1,g('cn'));const pay=r?fin*r/(1-Math.pow(1+r,-n)):fin/n;const totalBuy=D+pay*n-g('cr');
const N=Math.max(1,g('ln')),res=P*g('lr')/100,mf=g('lm');const dep=(P-D-res)/N,fee=(P-D+res)*mf,lp=(dep+fee)*(1+tx);const totalLease=D+g('lf')+lp*N;
const perMB=totalBuy/n,perML=totalLease/N;
document.getElementById('cout').innerHTML=`<table class="tbl"><tr><th></th><th>Buy (loan)</th><th>Lease</th></tr><tr><td>Monthly payment</td><td>${pay.toFixed(2)}</td><td>${lp.toFixed(2)}</td></tr><tr><td>Total paid minus value kept</td><td>${totalBuy.toFixed(0)}</td><td>${totalLease.toFixed(0)}</td></tr><tr><td>True cost per month</td><td><strong>${perMB.toFixed(2)}</strong></td><td><strong>${perML.toFixed(2)}</strong></td></tr></table><p class="win">${perMB<perML?'Buying':'Leasing'} is cheaper per month of use in this example.</p><p class="mut">Estimates only. Fuel, insurance and maintenance are not included; check final numbers with your dealer and lender.</p>`;}
document.querySelectorAll('.calc input').forEach(e=>e.addEventListener('input',run));run();})();
</script>""",
 "car-deal-analyzer", "free-simple-monthly-budget"),

("debt-snowball-calculator",
 "Debt Snowball vs Avalanche Calculator",
 "Debt Snowball vs Avalanche Calculator",
 "Free debt payoff calculator: enter up to 5 debts and an extra monthly payment to compare the snowball and avalanche methods, payoff months and total interest.",
 "<p>Add your debts and how much extra you can pay each month. The calculator simulates both methods month by month.</p>",
 """<div class="calc"><div class="row head"><span>Debt</span><span>Balance</span><span>APR %</span><span>Minimum payment</span></div><div id="drows"></div>
<div class="row"><label>Extra payment per month<input id="dx" type="number" value="200"></label></div><div class="out" id="dout"></div></div>
<script>
(function(){const S=[['Credit card',4500,22.9,120],['Car loan',9800,7.5,260],['Medical bill',800,0,50],['',0,0,0],['',0,0,0]];
document.getElementById('drows').innerHTML=S.map((s,i)=>`<div class="row"><span><input id="dn${i}" value="${s[0]}" placeholder="Name"></span><span><input id="db${i}" type="number" value="${s[1]||''}"></span><span><input id="da${i}" type="number" step="0.1" value="${s[2]||''}"></span><span><input id="dm${i}" type="number" value="${s[3]||''}"></span></div>`).join('');
const g=i=>+document.getElementById(i).value||0;
function sim(order){let ds=[];for(let i=0;i<5;i++){const b=g('db'+i);if(b>0)ds.push({b,r:g('da'+i)/1200,m:g('dm'+i)});}if(!ds.length)return null;
ds.sort(order);const budget=ds.reduce((a,d)=>a+d.m,0)+g('dx');let month=0,interest=0;
while(ds.some(d=>d.b>0.005)&&month<600){month++;ds.forEach(d=>{if(d.b>0){const it=d.b*d.r;interest+=it;d.b+=it;}});let left=budget;ds.forEach(d=>{if(d.b>0){const p=Math.min(d.m,d.b);d.b-=p;left-=p;}});for(const d of ds){if(d.b>0&&left>0){const p=Math.min(left,d.b);d.b-=p;left-=p;}}}
return {month,interest};}
function run(){const s=sim((a,b)=>a.b-b.b),a=sim((x,y)=>y.r-x.r),o=document.getElementById('dout');if(!s){o.innerHTML='Enter at least one debt.';return;}
const fm=m=>m>=600?'more than 50 years (raise your payment)':`${Math.floor(m/12)} years ${m%12} months`;
o.innerHTML=`<table class="tbl"><tr><th></th><th>Snowball (smallest balance first)</th><th>Avalanche (highest APR first)</th></tr><tr><td>Debt-free in</td><td>${fm(s.month)}</td><td>${fm(a.month)}</td></tr><tr><td>Total interest</td><td>${s.interest.toFixed(0)}</td><td>${a.interest.toFixed(0)}</td></tr></table><p class="win">${a.interest<s.interest-1?'Avalanche saves '+(s.interest-a.interest).toFixed(0)+' in interest.':'Both methods cost about the same here; snowball gives quicker wins.'}</p>`;}
document.querySelectorAll('.calc input').forEach(e=>e.addEventListener('input',run));run();})();
</script>""",
 "debt-payoff-calculator", "free-simple-monthly-budget"),

("mortgage-payment-calculator",
 "Mortgage Payment Calculator",
 "Mortgage Payment Calculator with Tax, Insurance and PMI",
 "Free mortgage calculator: monthly payment with principal, interest, property tax, home insurance, PMI and HOA, plus total interest over the loan.",
 "<p>Enter the home price and loan details to see the full monthly payment, not just principal and interest.</p>",
 """<div class="calc"><div class="row"><label>Home price<input id="mp" type="number" value="400000"></label><label>Down payment %<input id="md" type="number" value="10"></label><label>Interest rate %<input id="mr" type="number" step="0.01" value="6.75"></label><label>Term (years)<input id="mt" type="number" value="30"></label></div>
<div class="row"><label>Property tax per year<input id="mx" type="number" value="4800"></label><label>Home insurance per year<input id="mi" type="number" value="1800"></label><label>PMI % per year (if down &lt; 20%)<input id="mm" type="number" step="0.01" value="0.6"></label><label>HOA per month<input id="mh" type="number" value="0"></label></div>
<div class="out" id="mout"></div></div>
<script>
(function(){const g=i=>+document.getElementById(i).value||0;function run(){const P=g('mp'),dp=g('md')/100,L=P*(1-dp),r=g('mr')/1200,n=g('mt')*12||1;
const pi=r?L*r/(1-Math.pow(1+r,-n)):L/n,tax=g('mx')/12,ins=g('mi')/12,pmi=dp<0.2?L*g('mm')/1200:0,hoa=g('mh'),tot=pi+tax+ins+pmi+hoa;
document.getElementById('mout').innerHTML=`<p class="win">Monthly payment: <strong>${tot.toFixed(2)}</strong></p><table class="tbl"><tr><td>Principal &amp; interest</td><td>${pi.toFixed(2)}</td></tr><tr><td>Property tax</td><td>${tax.toFixed(2)}</td></tr><tr><td>Insurance</td><td>${ins.toFixed(2)}</td></tr><tr><td>PMI</td><td>${pmi.toFixed(2)}</td></tr><tr><td>HOA</td><td>${hoa.toFixed(2)}</td></tr><tr><td>Loan amount</td><td>${L.toFixed(0)}</td></tr><tr><td>Total interest over the loan</td><td>${(pi*n-L).toFixed(0)}</td></tr></table><p class="mut">Estimate only, not lending advice.</p>`;}
document.querySelectorAll('.calc input').forEach(e=>e.addEventListener('input',run));run();})();
</script>""",
 "home-buying-planner-mortgage-calculator", "free-simple-monthly-budget"),

("budget-calculator-50-30-20",
 "50/30/20 Budget Calculator",
 "50/30/20 Budget Calculator: How to Split Your Paycheck",
 "Free 50/30/20 budget calculator. Enter your take-home pay to see how much to spend on needs, wants and savings each month, week or paycheck.",
 "<p>The 50/30/20 rule splits take-home pay into 50% needs, 30% wants and 20% savings and debt payoff. Adjust the percentages if your situation is different.</p>",
 """<div class="calc"><div class="row"><label>Take-home pay<input id="bp" type="number" value="4000"></label><label>Paid<select id="bf"><option value="12">Monthly</option><option value="26">Every 2 weeks</option><option value="52">Weekly</option><option value="24">Twice a month</option></select></label></div>
<div class="row"><label>Needs %<input id="b1" type="number" value="50"></label><label>Wants %<input id="b2" type="number" value="30"></label><label>Savings & debt %<input id="b3" type="number" value="20"></label></div><div class="out" id="bout"></div></div>
<script>
(function(){const g=i=>+document.getElementById(i).value||0;function run(){const p=g('bp'),f=+document.getElementById('bf').value,m=p*f/12,a=[g('b1'),g('b2'),g('b3')],s=a[0]+a[1]+a[2];
const L=['Needs (rent, bills, groceries, transport)','Wants (eating out, fun, shopping)','Savings and extra debt payments'];
document.getElementById('bout').innerHTML=(s!==100?`<p>Your percentages add up to ${s}%, not 100%.</p>`:'')+`<table class="tbl"><tr><th></th><th>Per paycheck</th><th>Per month</th></tr>`+a.map((x,i)=>`<tr><td>${L[i]}</td><td>${(p*x/100).toFixed(2)}</td><td><strong>${(m*x/100).toFixed(2)}</strong></td></tr>`).join('')+'</table>';}
document.querySelectorAll('.calc input,.calc select').forEach(e=>e.addEventListener('input',run));run();})();
</script>""",
 "paycheck-budget-planner", "free-simple-monthly-budget"),
]

TOOL_CSS = """.calc{background:#fff;border:1px solid var(--line);border-radius:14px;padding:20px;margin:20px 0}
.calc .row{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:8px 0}.calc .row.head{font-weight:700;color:var(--mut);font-size:14px}
.calc label{display:flex;flex-direction:column;font-size:14px;color:var(--mut);gap:4px}.calc input,.calc select{font:inherit;padding:9px 10px;border:1px solid #cbd5e1;border-radius:8px;width:100%;background:#fefce8;color:#0f172a}
.calc h3{margin:18px 0 4px}.out{margin-top:16px;padding:14px;background:#f1f5f9;border-radius:10px}.win{color:#166534;font-weight:700;font-size:18px}
.tbl{border-collapse:collapse;width:100%;margin:8px 0}.tbl td,.tbl th{border-bottom:1px solid var(--line);padding:8px;text-align:left}.mut{color:var(--mut);font-size:14px}
.cd{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px}.cd .box{background:#0f172a;color:#fff;border-radius:12px;padding:16px;text-align:center}.cd .big{font-size:42px;font-weight:800;color:#fbbf24}.cd .mut{color:#cbd5e1}
.kofi{display:inline-block;background:#ff5e5b;color:#fff;padding:10px 18px;border-radius:10px;font-weight:700;text-decoration:none}"""
