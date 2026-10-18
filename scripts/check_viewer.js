/* Logic-only smoke checks in Node; deliberately not described as browser QA. */
const fs=require('node:fs');const path=require('node:path');const vm=require('node:vm');const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');const html=fs.readFileSync(path.join(root,'viewer/index.html'),'utf8');
const match=html.match(/<script>const DATA=([\s\S]*?);<\/script>/);assert(match,'embedded data');const data=JSON.parse(match[1]);
const elements=new Map();const get=id=>{if(!elements.has(id))elements.set(id,{innerHTML:'',textContent:'',value:id==='order-status'?'all':'',focus(){},scrollIntoView(){}});return elements.get(id);};
const context={DATA:data,Intl,Set,Blob,setTimeout:()=>{},URL:{createObjectURL:()=>'',revokeObjectURL:()=>{}},document:{getElementById:get,querySelectorAll:()=>[],addEventListener:()=>{},createElement:()=>({click(){}})}};
vm.createContext(context);vm.runInContext(fs.readFileSync(path.join(root,'viewer/app.js'),'utf8'),context);
let checks=0;function test(code){vm.runInContext(code,context);checks++;}
for(const view of ['overview','orders','process','requirements','analysis','uat','evidence','library']){test(`navigate('${view}')`);assert(get('content').innerHTML.length>100);}
test("navigate('orders');document.getElementById('order-search').value='NS-ORD-1001';drawOrders()");assert(get('order-count').textContent.startsWith('1 of 300'));
test("showOrder('NS-ORD-1001')");assert(get('detail').innerHTML.includes('No shipment records.'));assert(get('detail').innerHTML.includes('£2,500.00'));
test("document.getElementById('order-search').value='';document.getElementById('order-status').value='Cancelled';drawOrders()");assert(get('order-count').textContent.startsWith('17 of 300'));
test("navigate('requirements');document.getElementById('req-search').value='FR-004';drawRequirements();showRequirement('FR-004')");assert(get('req-detail').innerHTML.includes('TC-005;TC-006'));
test("navigate('uat')");assert(get('content').innerHTML.includes('TC-022'));assert(!get('content').innerHTML.includes('SAP cases passed'));
test("navigate('evidence')");assert(get('content').innerHTML.includes('Unverified; do not use as proof'));
const p=path.join(root,'quality/viewer-checks.json');fs.writeFileSync(p,JSON.stringify({date:'2026-10-11',checks,passed:true,type:'Executed Node logic smoke checks with minimal DOM stub',limitations:'Not a browser render, accessibility audit or real user test'},null,2));
console.log(`${checks} viewer logic smoke checks passed; browser rendering not tested.`);
