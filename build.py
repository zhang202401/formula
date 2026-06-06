#!/usr/bin/env python3
"""构建：模块化卡片 → 单文件 gongshi.html"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(BASE, 'index.html')
OUTPUT = os.path.join(BASE, 'gongshi.html')

CARDS = {
    'sec1': ['01-中点坐标公式/card01.html','01-中点坐标公式/card02.html','01-中点坐标公式/card03.html'],
    'sec2': ['02-倾斜角与斜率/card01.html','02-倾斜角与斜率/card02.html','02-倾斜角与斜率/card03.html'],
    'sec3': ['03-直线方程/card01.html','03-直线方程/card02.html','03-直线方程/card03.html','03-直线方程/card04.html'],
    'sec4': ['04-两直线位置关系/card01.html','04-两直线位置关系/card02.html'],
    'sec5': ['05-距离公式/card01.html','05-距离公式/card02.html'],
    'sec6': ['06-圆的方程/card01.html','06-圆的方程/card02.html','06-圆的方程/card03.html'],
    'sec7': ['07-直线与圆位置关系/card01.html','07-直线与圆位置关系/card02.html'],
    'sec8': ['08-圆的切线/card01.html','08-圆的切线/card02.html','08-圆的切线/card03.html'],
}

SEC_META = [
    (1,'中点坐标公式','已知两点坐标，可求出它们连线的中点坐标——这是一切对称问题的基础。'),
    (2,'倾斜角与斜率','直线的倾斜程度由倾斜角和斜率描述，是学习直线方程的基础。'),
    (3,'直线方程','直线有三种常见的方程形式，每种适用于不同的已知条件。'),
    (4,'两直线位置关系','设直线 \\(l_1: y = k_1x + b_1\\) 或 \\(l_1: A_1x + B_1y + C_1 = 0\\)。'),
    (5,'距离公式','距离计算是解析几何的基本运算，两种距离公式对应不同场景。'),
    (6,'圆的方程','圆的标准式直接看出圆心和半径，一般式便于运算，两者可互化。'),
    (7,'直线与圆的位置关系','判断直线与圆的位置关系，核心是比较圆心到直线的距离 d 与半径 r 的大小。'),
    (8,'圆的切线','求圆的切线方程是常考题型，关键在于切点与圆心连线垂直于切线。'),
]

def rc(path):
    with open(os.path.join(BASE, 'modules', path), 'r', encoding='utf-8') as f:
        return f.read()

def build():
    with open(INDEX, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. 插入 sections 到 main 标签之间
    ms = '<main class="content" id="formulaContent">'
    me = '</main>'
    msi = html.find(ms)
    mei = html.find(me, msi)
    if -1 in (msi, mei): return print('❌ main not found')

    body = ''
    for num, title, intro in SEC_META:
        sid = f'sec{num}'
        cards_html = '\n'.join('          ' + rc(c) for c in CARDS[sid])
        sep = '=' * 60
        body += f'''      <!-- 第 {num} 节：{title} -->
      <!-- {sep} -->
      <section class="formula-section" id="{sid}">
        <div class="section-header">
          <div class="section-number">{num}</div>
          <h2>{title}</h2>
        </div>
        <p class="section-intro">{intro}</p>
        <div class="section-cards" id="cards-{sid}">
          {cards_html}
        </div>
      </section>

'''
    body += '      <footer class="content-footer"><p>中职数学 · 直线与圆 公式要点 · 可打印参考</p></footer>\n'
    html = html[:msi + len(ms)] + '\n' + body + html[mei:]

    # 2. 替换主 JS（从 'const MODULES' 往前找到最近的 <script>）
    mod_pos = html.find('const MODULES')
    main_script = html[:mod_pos].rfind('<script>')
    if main_script == -1: main_script = html.find('<script>', html.find('KaTeX</script>'))
    script_end = html.find('</script>', main_script + 1)
    if -1 in (main_script, script_end): return print('❌ script block not found')

    new_script = '''  <script>
    document.addEventListener('DOMContentLoaded',function(){
      if(typeof renderMathInElement!=='undefined'){
        renderMathInElement(document.getElementById('formulaContent'),{
          delimiters:[{left:'$$',right:'$$',display:true},{left:'\\\\(',right:'\\\\)',display:false},{left:'\\\\[',right:'\\\\]',display:true}],
          throwOnError:false,errorColor:'#D97706'
        });
      }
    });
    var t=function(){var s=document.getElementById('sidebar'),b=document.getElementById('sidebarBackdrop'),h=document.getElementById('hamburger');if(window.innerWidth<=900){var o='flex'===s.style.display;s.style.display=o?'none':'flex';b.style.display=o?'none':'block';o?b.classList.remove('show'):requestAnimationFrame(function(){b.classList.add('show')});h.classList.toggle('open');h.setAttribute('aria-expanded',!o);}};
    var r=function(){var s=document.getElementById('sidebar'),b=document.getElementById('sidebarBackdrop'),h=document.getElementById('hamburger');if(window.innerWidth>900){s.style.display='flex';b.style.display='none';b.classList.remove('show');h.classList.remove('open');h.setAttribute('aria-expanded','false');}else if(!s.classList.contains('show'))s.style.display='none';};
    window.addEventListener('resize',r);
    var u=function(){var s=document.querySelectorAll('.formula-section'),n=document.querySelectorAll('.sidebar-nav a'),i='sec1';s.forEach(function(x){var q=x.getBoundingClientRect();if(q.top<=window.innerHeight*0.35)i=x.id;});n.forEach(function(l){l.classList.toggle('active',l.getAttribute('data-target')===i);});};
    window.addEventListener('scroll',u,{passive:true});
    document.querySelectorAll('.sidebar-nav a').forEach(function(l){l.addEventListener('click',function(){if(window.innerWidth<=900)t();});});
    document.addEventListener('keydown',function(e){if('Escape'===e.key&&window.innerWidth<=900){var s=document.getElementById('sidebar');if('flex'===s.style.display)t();}});
    r();u();
  </script>'''

    html = html[:main_script] + new_script + html[script_end + 9:]

    # 3. 清理动态加载痕迹
    html = html.replace('<span class="loading-spinner" id="mobileSpinner"></span>', '')
    html = html.replace('加载中...', '8 组核心公式')
    html = html.replace('<p id="sidebarStatus" style="font-size:0.75rem;color:#94A3B8;margin-top:0.125rem;">加载中...</p>', '<p style="font-size:0.75rem;color:#94A3B8;margin-top:0.125rem;">8 组核心公式</p>')
    html = html.replace('<span class="loading-dot"></span>', '')

    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'✅ gongshi.html ({len(html)/1024:.1f} KB)')

if __name__ == '__main__':
    build()
