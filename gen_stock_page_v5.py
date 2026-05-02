# -*- coding: utf-8 -*-
"""
选股策略系统 v5 - 修复f-string嵌套问题
读取strategy_data.json生成4个策略页面
"""
import json
import os

OUTPUT_DIR = r'D:/workbuddy/每日复盘'
DATA_FILE = os.path.join(OUTPUT_DIR, 'strategy_data.json')

# 读取数据
print("读取strategy_data.json...")
with open(DATA_FILE, 'r', encoding='utf-8') as f:
    records = json.load(f)

s1_list = [r for r in records if r.get('s1')]
s2_list = [r for r in records if r.get('s2')]
s3_list = [r for r in records if r.get('s3')]
s4_list = [r for r in records if r.get('s4')]
all_list = records

print(f"策略一: {len(s1_list)} 策略二: {len(s2_list)} 策略三: {len(s3_list)} 策略四: {len(s4_list)} 命中: {len(all_list)}")

# 共享CSS
SHARED_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif; background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%); min-height: 100vh; color: #212529; font-size: 14px; }
.top-nav { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 0 24px; display: flex; align-items: center; height: 56px; position: sticky; top: 0; z-index: 100; box-shadow: 0 2px 12px rgba(0,0,0,0.15); }
.top-nav a { color: rgba(255,255,255,0.7); text-decoration: none; font-size: 13px; padding: 6px 14px; border-radius: 6px; transition: all 0.2s; display: inline-flex; align-items: center; gap: 6px; }
.top-nav a:hover { color: #fff; background: rgba(255,255,255,0.1); }
.top-nav a.active { color: #ffd700; background: rgba(255,215,0,0.15); }
.nav-brand { font-size: 16px; font-weight: 700; color: #ffd700 !important; margin-right: 32px; }
.container { max-width: 1400px; margin: 0 auto; padding: 24px; }
.hero { text-align: center; padding: 40px 20px 32px; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); border-radius: 20px; margin-bottom: 32px; }
.hero h1 { font-size: 32px; font-weight: 800; color: #fff; margin-bottom: 12px; }
.hero .subtitle { color: rgba(255,255,255,0.8); font-size: 15px; display: flex; justify-content: center; gap: 24px; flex-wrap: wrap; }
.grid4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 32px; }
.card { background: #fff; border-radius: 16px; padding: 24px; text-align: center; cursor: pointer; transition: all 0.3s; border: 2px solid transparent; position: relative; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
.card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px; }
.card:hover { transform: translateY(-4px); box-shadow: 0 12px 40px rgba(0,0,0,0.15); }
.card.s1 { --c: #339af0; } .card.s1::before { background: linear-gradient(90deg, #339af0, #74c0fc); }
.card.s2 { --c: #51cf66; } .card.s2::before { background: linear-gradient(90deg, #51cf66, #8ce99a); }
.card.s3 { --c: #ff6b6b; } .card.s3::before { background: linear-gradient(90deg, #ff6b6b, #ff8e8e); }
.card.s4 { --c: #845ef7; } .card.s4::before { background: linear-gradient(90deg, #845ef7, #b197fc); }
.card.all { --c: #ff922b; } .card.all::before { background: linear-gradient(90deg, #ff922b, #ffc078); }
.card .count { font-size: 48px; font-weight: 800; color: var(--c); line-height: 1; margin: 12px 0 8px; }
.card .desc { font-size: 12px; color: #868e96; line-height: 1.4; }
.footer { text-align: center; padding: 24px; color: #868e96; font-size: 12px; }
.detail-header { background: #fff; border-radius: 16px; padding: 24px; margin-bottom: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); }
.detail-title { font-size: 24px; font-weight: 700; color: #212529; display: flex; align-items: center; gap: 12px; }
.detail-count { font-size: 14px; padding: 4px 14px; border-radius: 20px; margin-left: 12px; color: #fff; }
.actions { display: flex; gap: 12px; margin-top: 16px; flex-wrap: wrap; }
.btn { padding: 8px 16px; border-radius: 8px; border: 1px solid #dee2e6; background: #fff; color: #495057; font-size: 13px; cursor: pointer; }
.btn:hover { border-color: #ffd700; }
.btn.primary { background: linear-gradient(135deg, #ffd700, #ffed4e); color: #212529; border: none; font-weight: 600; }
.btn.active { background: linear-gradient(135deg, #ffd700, #ffed4e); color: #212529; border: none; }
.table-wrap { background: #fff; border-radius: 12px; overflow: auto; box-shadow: 0 4px 20px rgba(0,0,0,0.06); margin-bottom: 20px; }
table { width: 100%; border-collapse: collapse; }
th { padding: 12px 14px; text-align: left; font-size: 11px; font-weight: 700; color: #495057; border-bottom: 2px solid #dee2e6; white-space: nowrap; cursor: pointer; }
th:hover { background: #f8f9fa; }
td { padding: 10px 14px; border-bottom: 1px solid #f1f3f5; font-size: 12px; vertical-align: middle; }
tr:hover { background: #f8f9fa; }
tr:nth-child(even) { background: #fafbfc; }
.code { font-family: monospace; color: #339af0; cursor: pointer; padding: 2px 8px; background: rgba(51,154,240,0.1); border-radius: 4px; font-size: 12px; }
.name { font-weight: 600; cursor: pointer; }
.name:hover { color: #ffd700; }
.pos { color: #ff6b6b; font-weight: 600; }
.neg { color: #51cf66; font-weight: 600; }
.tag { display: inline-block; font-size: 10px; padding: 2px 6px; border-radius: 4px; font-weight: 600; margin: 1px; }
.tag-s1 { background: rgba(51,154,240,0.15); color: #339af0; border: 1px solid rgba(51,154,240,0.3); }
.tag-s2 { background: rgba(81,207,102,0.15); color: #51cf66; border: 1px solid rgba(81,207,102,0.3); }
.tag-s3 { background: rgba(255,107,107,0.15); color: #ff6b6b; border: 1px solid rgba(255,107,107,0.3); }
.tag-s4 { background: rgba(132,94,247,0.15); color: #845ef7; border: 1px solid rgba(132,94,247,0.3); }
.tag-star { background: linear-gradient(135deg, #ffd700, #ffed4e); color: #212529; border: none; }
.pagination { display: flex; align-items: center; justify-content: center; gap: 8px; padding: 16px 0 8px; flex-wrap: wrap; }
.pg-btn { min-width: 36px; height: 36px; border-radius: 8px; border: 1px solid #dee2e6; background: #fff; color: #495057; cursor: pointer; font-size: 13px; }
.pg-btn.active { background: linear-gradient(135deg, #ffd700, #ffed4e); color: #212529; border-color: #ffd700; font-weight: 700; }
.pg-btn:disabled { opacity: 0.4; cursor: default; }
.pg-info { font-size: 12px; color: #868e96; padding: 0 8px; }
.sector-layout { display: flex; gap: 20px; }
.sector-sidebar { width: 280px; flex-shrink: 0; }
.sector-list { background: #fff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.06); }
.sector-item { padding: 12px 16px; border-bottom: 1px solid #f1f3f5; cursor: pointer; display: flex; align-items: center; justify-content: space-between; }
.sector-item.active { background: rgba(255,215,0,0.05); border-left: 3px solid #ffd700; }
.sector-main { flex: 1; }
.sector-tbl-wrap { background: #fff; border-radius: 12px; overflow: auto; box-shadow: 0 4px 20px rgba(0,0,0,0.06); }
.sort-icon { font-size: 10px; margin-left: 4px; opacity: 0.5; }
th.sorted .sort-icon { opacity: 1; }
@media (max-width: 1200px) { .grid4 { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 768px) { .grid4 { grid-template-columns: 1fr; } .sector-layout { flex-direction: column; } .sector-sidebar { width: 100%; } }
"""

def gen_nav_page():
    """生成主导航页"""
    html = '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>选股策略 · A股工具箱</title>
<style>''' + SHARED_CSS + '''</style>
</head><body>
<nav class="top-nav">
  <a href="index.html" class="nav-brand">📊 A股工具箱</a>
  <a href="index.html">🏠 首页</a>
  <a href="市场复盘_20260430_v4.html">📈 每日复盘</a>
  <a href="选股策略_导航.html" class="active">🎯 选股策略</a>
</nav>
<div class="container">
  <div class="hero"><h1>🎯 选股策略系统</h1><div class="subtitle"><span>📊 四大维度量化筛选</span><span>🔢 九宽数据</span></div></div>
  <div class="grid4">
    <div class="card s1" onclick="location.href='选股策略_持股增长.html'">
      <div style="font-size:42px">💎</div>
      <div style="font-size:15px;font-weight:700;margin:8px 0">持股增长</div>
      <div class="count">''' + str(len(s1_list)) + '''</div>
      <div class="desc">前十大股东连续增持<br>机构资金持续流入</div>
    </div>
    <div class="card s2" onclick="location.href='选股策略_盈利质量.html'">
      <div style="font-size:42px">📈</div>
      <div style="font-size:15px;font-weight:700;margin:8px 0">盈利质量</div>
      <div class="count">''' + str(len(s2_list)) + '''</div>
      <div class="desc">ROE·毛利·净利三年升<br>全方位盈利提升</div>
    </div>
    <div class="card s3" onclick="location.href='选股策略_全速前进.html'">
      <div style="font-size:42px">🚀</div>
      <div style="font-size:15px;font-weight:700;margin:8px 0">全速前进</div>
      <div class="count">''' + str(len(s3_list)) + '''</div>
      <div class="desc">扣非净利+营收双加速<br>业绩增速持续扩大</div>
    </div>
    <div class="card s4" onclick="location.href='选股策略_机构持股增长.html'">
      <div style="font-size:42px">🏢</div>
      <div style="font-size:15px;font-weight:700;margin:8px 0">机构持股增长</div>
      <div class="count">''' + str(len(s4_list)) + '''</div>
      <div class="desc">机构持股连续增持<br>专业投资者看好</div>
    </div>
  </div>
  <div class="grid4">
    <div class="card all" onclick="location.href='选股策略_命中股票.html'">
      <div style="font-size:42px">📋</div>
      <div style="font-size:15px;font-weight:700;margin:8px 0">命中股票</div>
      <div class="count">''' + str(len(all_list)) + '''</div>
      <div class="desc">命中任一策略<br>覆盖所有优质标的</div>
    </div>
  </div>
  <div class="footer">数据来源：策略筛选结果_v3.xlsx | 更新：2026-05-02</div>
</div>
</body></html>'''

    with open(os.path.join(OUTPUT_DIR, '选股策略_导航.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    print("✅ 选股策略_导航.html")

# 各策略的JS变量定义
STRATEGY_CONFIG = {
    's1': {
        'title': '持股增长',
        'color': '#339af0',
        'extra_th': '<th onclick="sortTable(4)">26Q1<span class="sort-icon">⇅</span></th><th onclick="sortTable(5)">25Q4<span class="sort-icon">⇅</span></th><th onclick="sortTable(6)">25Q3<span class="sort-icon">⇅</span></th>',
        'list_td': "html += '<td>' + (s.six_q&&s.six_q[0]!=null?(s.six_q[0]/1e4).toFixed(0)+'万':'—') + '</td>';html += '<td>' + (s.six_q&&s.six_q[1]!=null?(s.six_q[1]/1e4).toFixed(0)+'万':'—') + '</td>';html += '<td>' + (s.six_q&&s.six_q[2]!=null?(s.six_q[2]/1e4).toFixed(0)+'万':'—') + '</td>';",
        'csv_header': "\\n,26Q1持股,25Q4持股,25Q3持股",
        'csv_row': "+',' + (s.six_q&&s.six_q[0]!=null?(s.six_q[0]/1e4).toFixed(0)+'万':'') + ',' + (s.six_q&&s.six_q[1]!=null?(s.six_q[1]/1e4).toFixed(0)+'万':'') + ',' + (s.six_q&&s.six_q[2]!=null?(s.six_q[2]/1e4).toFixed(0)+'万':'')",
    },
    's2': {
        'title': '盈利质量',
        'color': '#51cf66',
        'extra_th': '<th onclick="sortTable(4)">ROE25<span class="sort-icon">⇅</span></th><th onclick="sortTable(5)">毛利25<span class="sort-icon">⇅</span></th><th onclick="sortTable(6)">净利25<span class="sort-icon">⇅</span></th>',
        'list_td': "html += '<td>' + (s.roe!=null?s.roe.toFixed(2)+'%':'—') + '</td>';html += '<td>' + (s.毛利率!=null?s.毛利率.toFixed(2)+'%':'—') + '</td>';html += '<td>' + (s.净利!=null?(s.净利/1e8).toFixed(2)+'亿':'—') + '</td>';",
        'csv_header': "\\n,ROE25,毛利25,净利25",
        'csv_row': "+',' + (s.roe!=null?s.roe.toFixed(2)+'%':'') + ',' + (s.毛利率!=null?s.毛利率.toFixed(2)+'%':'') + ',' + (s.净利!=null?(s.净利/1e8).toFixed(2)+'亿':'')",
    },
    's3': {
        'title': '全速前进',
        'color': '#ff6b6b',
        'extra_th': '<th onclick="sortTable(4)">营收25<span class="sort-icon">⇅</span></th><th onclick="sortTable(5)">扣非25<span class="sort-icon">⇅</span></th><th onclick="sortTable(6)">增速<span class="sort-icon">⇅</span></th>',
        'list_td': "html += '<td>' + (s.营收25!=null?(s.营收25/1e8).toFixed(2)+'亿':'—') + '</td>';html += '<td>' + (s.净利!=null?(s.净利/1e8).toFixed(2)+'亿':'—') + '</td>';html += '<td>' + (s.kg25!=null?(s.kg25>=0?'<span class=pos>+'+ (s.kg25*100).toFixed(1)+'%</span>':'<span class=neg>'+ (s.kg25*100).toFixed(1)+'%</span>'):'—') + '</td>';",
        'csv_header': "\\n,营收25,扣非25,增速",
        'csv_row': "+',' + (s.营收25!=null?(s.营收25/1e8).toFixed(2)+'亿':'') + ',' + (s.净利!=null?(s.净利/1e8).toFixed(2)+'亿':'') + ',' + (s.kg25!=null?(s.kg25*100).toFixed(1)+'%':'')",
    },
    's4': {
        'title': '机构持股增长',
        'color': '#845ef7',
        'extra_th': '<th onclick="sortTable(4)">26Q1机构<span class="sort-icon">⇅</span></th><th onclick="sortTable(5)">25Q4机构<span class="sort-icon">⇅</span></th><th onclick="sortTable(6)">25Q3机构<span class="sort-icon">⇅</span></th>',
        'list_td': "html += '<td>' + (s.j1!=null?(s.j1/1e4).toFixed(0)+'万':'—') + '</td>';html += '<td>' + (s.j2!=null?(s.j2/1e4).toFixed(0)+'万':'—') + '</td>';html += '<td>' + (s.j3!=null?(s.j3/1e4).toFixed(0)+'万':'—') + '</td>';",
        'csv_header': "\\n,26Q1机构,25Q4机构,25Q3机构",
        'csv_row': "+',' + (s.j1!=null?(s.j1/1e4).toFixed(0)+'万':'') + ',' + (s.j2!=null?(s.j2/1e4).toFixed(0)+'万':'') + ',' + (s.j3!=null?(s.j3/1e4).toFixed(0)+'万':'')",
    },
}

def gen_detail_page(key, data_list):
    """生成策略详情页"""
    cfg = STRATEGY_CONFIG.get(key, {})
    name = cfg.get('title', key)
    color = cfg.get('color', '#666')
    extra_th = cfg.get('extra_th', '')
    list_td = cfg.get('list_td', '')
    csv_header = cfg.get('csv_header', '')
    csv_row = cfg.get('csv_row', '')

    data_json = json.dumps(data_list, ensure_ascii=False)
    count = len(data_list)

    js = '''
const DATA = ''' + data_json + ''';
const PAGE_SIZE = 20;
let currentPage = 1;
let sortCol = -1;
let sortAsc = true;

function fmtNum(v) {
  if(v==null||v===0) return '—';
  if(Math.abs(v)>=1e8) return (v/1e8).toFixed(2)+'亿';
  if(Math.abs(v)>=1e4) return (v/1e4).toFixed(0)+'万';
  return v.toFixed(2);
}

function getTags(s) {
  var h = '';
  if(s.s1) h += '<span class="tag tag-s1">持股</span>';
  if(s.s1_sub) h += '<span class="tag tag-star">★</span>';
  if(s.s2) h += '<span class="tag tag-s2">盈利</span>';
  if(s.s3) h += '<span class="tag tag-s3">加速</span>';
  if(s.s4) h += '<span class="tag tag-s4">机构</span>';
  if(s.s4_sub) h += '<span class="tag tag-star">★</span>';
  return h;
}

function renderList(pg) {
  currentPage = pg;
  var sorted = DATA.slice();
  if(sortCol >= 0) {
    sorted.sort(function(a,b) {
      var va = Object.values(a)[sortCol], vb = Object.values(b)[sortCol];
      if(va==null) va = 0; if(vb==null) vb = 0;
      if(typeof va === 'string') return sortAsc ? va.localeCompare(vb) : vb.localeCompare(va);
      return sortAsc ? va - vb : vb - va;
    });
  }
  var start = (pg-1)*PAGE_SIZE;
  var end = Math.min(start + PAGE_SIZE, sorted.length);
  var html = '';
  for(var i=start; i<end; i++) {
    var s = sorted[i];
    html += '<tr>';
    html += '<td><span class="code" onclick="showDetail(\\''+s.code+'\\')">'+s.code+'</span></td>';
    html += '<td class="name">'+s.name+'</td>';
    html += '<td>'+(s.industry||'—')+'</td>';
    html += '<td>'+getTags(s)+'</td>';
    ''' + list_td + '''
    html += '</tr>';
  }
  document.getElementById('tbody').innerHTML = html;
  var total = Math.ceil(sorted.length / PAGE_SIZE);
  var ph = '<div class="pagination">';
  ph += '<button class="pg-btn" onclick="renderList('+(pg-1)+')" '+(pg<=1?'disabled':'')+'>‹</button>';
  for(var i=1; i<=total; i++) {
    if(Math.abs(i-pg)<3 || i===1 || i===total) ph += '<button class="pg-btn '+(i===pg?'active':'')+'" onclick="renderList('+i+')">'+i+'</button>';
    else if(Math.abs(i-pg)===3) ph += '<span class="pg-info">…</span>';
  }
  ph += '<button class="pg-btn" onclick="renderList('+(pg+1)+')" '+(pg>=total?'disabled':'')+'>›</button>';
  ph += '<span class="pg-info">'+pg+'/'+total+'页 · '+DATA.length+'条</span></div>';
  document.getElementById('pager-top').innerHTML = ph;
  document.getElementById('pager-bot').innerHTML = ph;
}

function sortTable(col) {
  if(sortCol === col) sortAsc = !sortAsc;
  else { sortCol = col; sortAsc = false; }
  renderList(currentPage);
}

function showView(v, btn) {
  document.getElementById('view-list').style.display = v==='list'?'block':'none';
  document.getElementById('view-sector').style.display = v==='sector'?'block':'none';
  document.querySelectorAll('.btn').forEach(function(b){b.classList.remove('active');});
  btn.classList.add('active');
  if(v==='list') renderList(1);
  if(v==='sector') renderSectorList();
}

function renderSectorList() {
  var map = {};
  DATA.forEach(function(s) {
    var ind = s.industry || '未分类';
    if(!map[ind]) map[ind] = [];
    map[ind].push(s);
  });
  var sorted = Object.entries(map).sort(function(a,b){return b[1].length - a[1].length;});
  var sh = '';
  sorted.forEach(function(item, i) {
    var ind = item[0], stocks = item[1];
    sh += '<div class="sector-item '+(i===0?'active':'')+'" onclick="selectSector(this,\\''+ind.replace(/'/g,"\\\\'")+'\\')"><span>'+ind+'</span><span class="pg-info">'+stocks.length+'</span></div>';
  });
  document.getElementById('sector-list').innerHTML = sh;
  if(sorted.length > 0) selectSector(document.querySelector('.sector-item'), sorted[0][0]);
}

function selectSector(el, ind) {
  document.querySelectorAll('.sector-item').forEach(function(e){e.classList.remove('active');});
  el.classList.add('active');
  var stocks = DATA.filter(function(s){return (s.industry||'未分类')===ind;});
  document.getElementById('sector-info').innerHTML = '板块: <b>'+ind+'</b> | '+stocks.length+' 只';
  var html = '';
  stocks.forEach(function(s) {
    html += '<tr>';
    html += '<td><span class="code" onclick="showDetail(\\''+s.code+'\\')">'+s.code+'</span></td>';
    html += '<td class="name">'+s.name+'</td>';
    html += '<td>'+getTags(s)+'</td>';
    ''' + list_td + '''
    html += '</tr>';
  });
  document.getElementById('sector-tbody').innerHTML = html;
}

function showDetail(code) {
  window.location.href = 'stock_detail.html?code=' + code;
}

function exportCSV() {
  var csv = '\\uFEFF代码,名称,行业''' + csv_header + ''',策略\\n';
  DATA.forEach(function(s) {
    var row = s.code + ',' + s.name + ',' + (s.industry||'')''' + csv_row + ''';
    var st = [];
    if(s.s1) st.push('持股增长');
    if(s.s1_sub) st.push('持股★');
    if(s.s2) st.push('盈利质量');
    if(s.s3) st.push('全速前进');
    if(s.s4) st.push('机构持股');
    if(s.s4_sub) st.push('机构★');
    row += ',' + st.join('|');
    csv += row + '\\n';
  });
  var blob = new Blob([csv], {type:'text/csv;charset=utf-8'});
  var a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = '''' + name + '''' + '_' + new Date().toISOString().slice(0,10) + '.csv';
  a.click();
}

document.addEventListener('DOMContentLoaded', function(){renderList(1);});
'''

    html = '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>''' + name + ''' · 选股策略</title>
<style>''' + SHARED_CSS + '''</style>
</head><body>
<nav class="top-nav">
  <a href="index.html" class="nav-brand">📊 A股工具箱</a>
  <a href="index.html">🏠 首页</a>
  <a href="市场复盘_20260430_v4.html">📈 每日复盘</a>
  <a href="选股策略_导航.html" class="active">🎯 选股策略</a>
</nav>
<div class="container">
  <div class="detail-header" style="border-top: 4px solid ''' + color + '''">
    <div class="detail-title">''' + name + '''<span class="detail-count" style="background:''' + color + '''">''' + str(count) + ''' 只</span></div>
    <div class="actions">
      <button class="btn active" onclick="showView('list',this)">📋 股票列表</button>
      <button class="btn" onclick="showView('sector',this)">🏢 板块共振</button>
      <button class="btn primary" onclick="exportCSV()">📥 导出CSV</button>
    </div>
  </div>
  <div id="view-list">
    <div id="pager-top"></div>
    <div class="table-wrap"><table id="tbl"><thead><tr><th onclick="sortTable(0)">代码<span class="sort-icon">⇅</span></th><th onclick="sortTable(1)">名称<span class="sort-icon">⇅</span></th><th onclick="sortTable(2)">行业<span class="sort-icon">⇅</span></th><th>策略</th>''' + extra_th + '''</tr></thead><tbody id="tbody"></tbody></table></div>
    <div id="pager-bot"></div>
  </div>
  <div id="view-sector" style="display:none">
    <div class="sector-layout">
      <div class="sector-sidebar"><div class="sector-list" id="sector-list"></div></div>
      <div class="sector-main">
        <div id="sector-info" style="margin-bottom:12px;font-size:13px;color:#868e96"></div>
        <div class="table-wrap"><table id="sector-tbl"><thead><tr><th>代码</th><th>名称</th><th>策略</th>''' + extra_th + '''</tr></thead><tbody id="sector-tbody"></tbody></table></div>
      </div>
    </div>
  </div>
</div>
<script>
''' + js + '''
</script>
</body></html>'''

    filename = '选股策略_' + name + '.html'
    with open(os.path.join(OUTPUT_DIR, filename), 'w', encoding='utf-8') as f:
        f.write(html)
    print("✅ " + filename)

# 生成所有页面
print("\n生成页面...")
gen_nav_page()
gen_detail_page('s1', s1_list)
gen_detail_page('s2', s2_list)
gen_detail_page('s3', s3_list)
gen_detail_page('s4', s4_list)

# 命中股票页面
all_json = json.dumps(all_list, ensure_ascii=False)
html_all = '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>命中股票 · 选股策略</title>
<style>''' + SHARED_CSS + '''</style>
</head><body>
<nav class="top-nav">
  <a href="index.html" class="nav-brand">📊 A股工具箱</a>
  <a href="index.html">🏠 首页</a>
  <a href="市场复盘_20260430_v4.html">📈 每日复盘</a>
  <a href="选股策略_导航.html" class="active">🎯 选股策略</a>
</nav>
<div class="container">
  <div class="detail-header" style="border-top: 4px solid #ff922b">
    <div class="detail-title">命中股票<span class="detail-count" style="background:#ff922b">''' + str(len(all_list)) + ''' 只</span></div>
    <div class="actions">
      <button class="btn primary" onclick="exportAll()">📥 导出CSV</button>
    </div>
  </div>
  <div class="table-wrap"><table id="tbl"><thead><tr><th>代码</th><th>名称</th><th>行业</th><th>策略</th><th>ROE25</th><th>净利25</th></tr></thead><tbody id="tbody"></tbody></table></div>
</div>
<script>
const DATA = ''' + all_json + ''';

DATA.forEach(function(s) {
  var html = '<tr>';
  html += '<td><span class="code" onclick="showDetail(\\''+s.code+'\\')">'+s.code+'</span></td>';
  html += '<td class="name">'+s.name+'</td>';
  html += '<td>'+(s.industry||'—')+'</td>';
  var st = [];
  if(s.s1) st.push('<span class="tag tag-s1">持股</span>');
  if(s.s1_sub) st.push('<span class="tag tag-star">★</span>');
  if(s.s2) st.push('<span class="tag tag-s2">盈利</span>');
  if(s.s3) st.push('<span class="tag tag-s3">加速</span>');
  if(s.s4) st.push('<span class="tag tag-s4">机构</span>');
  if(s.s4_sub) st.push('<span class="tag tag-star">★</span>');
  html += '<td>' + st.join('') + '</td>';
  html += '<td>' + (s.roe!=null?s.roe.toFixed(2)+'%':'—') + '</td>';
  html += '<td>' + (s.净利!=null?(s.净利/1e8).toFixed(2)+'亿':'—') + '</td>';
  html += '</tr>';
  document.getElementById('tbody').innerHTML += html;
});

function showDetail(code) {
  window.location.href = 'stock_detail.html?code=' + code;
}

function exportAll() {
  var csv = '\\uFEFF代码,名称,行业,策略,ROE25,净利25\\n';
  DATA.forEach(function(s) {
    var row = s.code + ',' + s.name + ',' + (s.industry||'');
    var st = [];
    if(s.s1) st.push('持股增长');
    if(s.s1_sub) st.push('持股★');
    if(s.s2) st.push('盈利质量');
    if(s.s3) st.push('全速前进');
    if(s.s4) st.push('机构持股');
    if(s.s4_sub) st.push('机构★');
    row += ',' + st.join('|');
    row += ',' + (s.roe!=null?s.roe.toFixed(2)+'%':'');
    row += ',' + (s.净利!=null?(s.净利/1e8).toFixed(2)+'亿':'');
    csv += row + '\\n';
  });
  var blob = new Blob([csv], {type:'text/csv;charset=utf-8'});
  var a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = '命中股票_' + new Date().toISOString().slice(0,10) + '.csv';
  a.click();
}
</script>
</body></html>'''

with open(os.path.join(OUTPUT_DIR, '选股策略_命中股票.html'), 'w', encoding='utf-8') as f:
    f.write(html_all)
print("✅ 选股策略_命中股票.html")

print("\n🎉 全部完成！")
