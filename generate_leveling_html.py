import json, re

with open('C:/Users/yodyx/Desktop/POE2/ice-shot-leveling-data.json', encoding='utf-8') as f:
    d = json.load(f)

SLUG_NAME = {
    'supportrapidattacksplayer': 'Rapid Attacks I',
    'supportrapidattacksplayertwo': 'Rapid Attacks II',
    'supportelementalarmamentplayer': 'Elem. Armament I',
    'supportelementalarmamentplayertwo': 'Elem. Armament II',
    'supportconcentratedareaplayer': 'Concentrated Area',
    'supportwindowofopportunityplayer': 'Window of Opp.',
    'supportwindowofopportunityplayertwo': 'Window of Opp. II',
    'supportelementalfocusplayer': 'Elemental Focus',
    'prolongeddurationsupportplayer': 'Prolonged Duration I',
    'prolongeddurationsupportplayertwo': 'Prolonged Duration II',
    'supportmarkofsiphoningplayer': 'Mark of Siphoning I',
    'supportmarkofsiphoningplayertwo': 'Mark of Siphoning II',
    'supporteternalmarkplayer': 'Eternal Mark',
    'supportchargedmarkplayer': 'Charged Mark',
    'supporticebiteplayertwo': 'Ice Bite II',
    'supporticebiteplayer': 'Ice Bite I',
    'supportforkplayer': 'Fork',
    'supportmagnifiedareaplayer': 'Magnified Area',
    'supportmagnifiedareaplayertwo': 'Magnified Area II',
    'supportfreezeplayer': 'Hypothermia',
    'supportshortfuseplayer': 'Short Fuse',
    'supportcooldownrecoveryplayer': 'Cooldown Recovery I',
    'supportcooldownrecoveryplayertwo': 'Cooldown Recovery II',
    'supportchargeprofusionplayer': 'Charge Profusion',
    'supportchargeprofusionplayertwo': 'Charge Profusion II',
    'supportknockbackplayer': 'Knockback',
    'supportincreaselimitplayer': 'Overabundance I',
    'supportincreaselimitplayertwo': 'Overabundance II',
    'supportrapidcastingplayertwo': 'Rapid Casting II',
    'supportaddedlightningdamageplayer': 'Lightning Attunement',
    'iceshotplayer': 'Ice Shot',
}

def sup_name(slug):
    if slug in SLUG_NAME: return SLUG_NAME[slug]
    # auto derive
    n = re.sub(r'^support', '', slug)
    n = re.sub(r'player(two|three)?$', '', n)
    n = re.sub(r'([A-Z])', r' \1', n).strip().title()
    return n

ICE = 'rgba(90,176,255,0.08)'
ICE_BORDER = 'rgba(90,176,255,0.2)'
ICE_TEXT = '#8ecfff'
LA_C = 'rgba(124,200,255,0.08)'
LA_B = 'rgba(124,200,255,0.2)'
LA_T = '#a0d8ff'

def skill_tag(name):
    n = name.lower()
    if 'ice shot' in n or 'lightning arrow' in n: return ('tag-clear', 'Main Clear', 'set1')
    if 'snipe' in n: return ('tag-boss', 'Boss DPS', 'set1')
    if 'barrage' in n: return ('tag-boss', 'Boss Burst', 'set1')
    if 'freezing mark' in n: return ('tag-utility', 'Debuff', 'set2')
    if 'herald' in n: return ('tag-utility', 'Buff', '')
    if 'tornado' in n: return ('tag-utility', 'Utility', 'set1')
    if 'wind dancer' in n: return ('tag-utility', 'Defense', '')
    if 'frost bomb' in n or 'freezing salvo' in n: return ('tag-boss', 'Boss Debuff', '')
    if 'ice-tipped' in n: return ('tag-utility', 'AOE', 'set1')
    if 'combat frenzy' in n: return ('tag-utility', 'Charges', '')
    if 'pounce' in n: return ('tag-utility', 'Mobility', '')
    if 'lightning rod' in n: return ('tag-boss', 'Boss DPS', '')
    return ('tag-utility', 'Utility', '')

def render_skill_row(g, is_ice=False):
    active = g.get('activeSkill', {})
    name = active.get('name', '')
    icon = active.get('iconURL', 'https://cdn.mobalytics.gg/assets/poe-2/images/game/Art/2DItems/Gems/New/BlankGem.avif')
    sups = g.get('supportGems', []) or []
    wset = g.get('weaponSet', '') or ''
    tag_cls, tag_label, tag_set = skill_tag(name)

    bg_style = ''
    if is_ice:
        bg_style = 'border-color:#1a3050;background:rgba(0,20,40,0.3);'

    set2_badge = ''
    if tag_set == 'set2':
        set2_badge = '<span class="weapon-set-badge" style="color:#e05050;border-color:rgba(224,80,80,0.3);background:rgba(224,80,80,0.12);">SET 2</span>'
    elif tag_set == 'set1':
        set2_badge = '<span class="weapon-set-badge">SET 1</span>'

    chips = ''
    if sups:
        chips = '<span class="plus">+</span>'
        for s in sups:
            slug = s.get('gemSlug','')
            s_icon = s.get('iconURL','')
            s_name = sup_name(slug)
            if is_ice:
                chip_style = f'background:{ICE};border-color:{ICE_BORDER};color:{ICE_TEXT};'
            else:
                chip_style = ''
            chips += f'<div class="support-chip" style="{chip_style}"><img class="gem-icon small" src="{s_icon}" alt="">{s_name}</div>'

    return f'''      <div class="skill-row" style="{bg_style}">
        <img class="gem-icon" src="{icon}" alt="{name}">
        <div class="skill-name">{name}</div>
        <div class="support-chips">{chips}</div>
        <span class="skill-tag {tag_cls}">{tag_label}</span>{set2_badge}
      </div>'''

def notes_to_html(text):
    if not text: return ''
    text = re.sub(r'\[([^\]]+)\]', r'<span class="gem-ref">\1</span>', text)
    paragraphs = [p.strip() for p in re.split(r'\n\n+', text.strip()) if p.strip()]
    lines = []
    for p in paragraphs:
        p_lines = p.split('\n')
        for line in p_lines:
            line = line.strip()
            if line:
                lines.append(f'<p>{line}</p>')
    return '\n'.join(lines)

def equip_card(slot_label, item):
    if not item: return ''
    name = item.get('name', '')
    icon = item.get('iconURL', '')
    is_unique = item.get('isUnique', False)
    mods = item.get('explicitMods', []) or []
    mod_text = '<br>'.join(mods[:2]) if mods else ''
    unique_cls = ' is-unique' if is_unique else ''
    return f'''      <div class="equip-card{unique_cls}">
        <img class="equip-img" src="{icon}" alt="{name}" onerror="this.style.opacity='0.3'">
        <div class="equip-slot">{slot_label}</div>
        <div class="equip-name">{name}</div>
        <div class="equip-mods">{mod_text}</div>
      </div>'''

VARIANT_COLORS = {
    'lvl 1-14':  {'bg': '#0d1320', 'border': '#1a2540', 'is_ice': False},
    'lvl 15-23': {'bg': '#0d1320', 'border': '#1a2540', 'is_ice': False},
    'lvl 24-30': {'bg': '#0d1520', 'border': '#1a2d40', 'is_ice': False},
    'lvl 31-41': {'bg': '#0d1420', 'border': '#1a3045', 'is_ice': True},
    'lvl 42-59': {'bg': '#0d141f', 'border': '#1a2d45', 'is_ice': True},
    'lvl 60+':   {'bg': '#0d141f', 'border': '#1a2d45', 'is_ice': True},
}

VARIANT_DESC = {
    'lvl 1-14':  'ใช้ Lightning Arrow clear · Frost Bomb กับ boss · เน้น flat damage + movement speed',
    'lvl 15-23': 'ยัง Lightning Arrow · เพิ่ม Pounce สำหรับ mobility · Recurve Bow ที่ lvl 16',
    'lvl 24-30': 'เพิ่ม Snipe + Freezing Mark · ใช้ Freezing Salvo กับ boss · ยังใช้ LA',
    'lvl 31-41': '⚡→❄️ <strong style="color:#5ab0ff;">Swap ไป Ice Shot ที่ lvl 31!</strong> · ตั้ง Weapon Set 2 สำหรับ Freezing Mark · Dualstring/Cultist Bow ที่ lvl 33',
    'lvl 42-59': 'Ice Shot full setup · เพิ่ม Wind Dancer + Tornado Shot · Artillery Bow ที่ lvl 46',
    'lvl 60+':   'Setup เหมือน 42-59 · เตรียม transition ไป endgame build',
}

# Build tab HTMLs
tabs_html = []
panels_html = []

for i, v in enumerate(d['variants']):
    title = v['title']
    tab_id = f'il{i+1}'
    active_cls = ' active' if i == 0 else ''
    tab_cls = 'ice-tab-btn' if VARIANT_COLORS[title]['is_ice'] else ''
    tabs_html.append(f'    <button class="tab-btn {tab_cls}" onclick="switchLevelTab(\'{tab_id}\', this)">{title}</button>')

    color = VARIANT_COLORS[title]
    is_ice = color['is_ice']
    sec_title_cls = 'ice-section-title' if is_ice else 'section-title'
    notes_box_cls = 'ice-notes-box' if is_ice else 'notes-box'

    # Skills
    skills_rows = '\n'.join(render_skill_row(g, is_ice) for g in v['skillGems'])

    # Notes
    gem_notes = notes_to_html(v['notes'].get('descriptionPoeSkillGems',''))
    equip_notes = notes_to_html(v['notes'].get('descriptionPoeEquipment',''))
    tree_notes = notes_to_html(v['notes'].get('descriptionPoe2PassiveTree',''))

    # Equipment
    slots_order = [
        ('mainHand', 'Bow ⭐'),
        ('helmet', 'Helmet'),
        ('body', 'Body'),
        ('gloves', 'Gloves'),
        ('boots', 'Boots'),
        ('belt', 'Belt'),
        ('amulet', 'Amulet'),
        ('leftRing', 'Ring x2'),
        ('flask1', 'Flask'),
        ('charm1', 'Charm'),
        ('charm2', 'Charm 2'),
    ]
    equip_cards = '\n'.join(equip_card(label, v['equipment'].get(slot)) for slot, label in slots_order if v['equipment'].get(slot))

    panel = f'''  <div id="{tab_id}" class="tab-panel{active_cls}" style="background:{color['bg']};border-color:{color['border']};">
    <div class="ice-variant-desc">{VARIANT_DESC[title]}</div>

    <div class="{sec_title_cls}">⚔️ Skills &amp; Gems</div>
    <div class="skills-grid">
{skills_rows}
    </div>

    <div class="divider"></div>
    <div class="{sec_title_cls}">📋 Skill Gem Notes</div>
    <div class="{notes_box_cls}">{gem_notes}</div>

    <div class="divider"></div>
    <div class="{sec_title_cls}">🎒 Equipment</div>
    <div class="equip-grid">
{equip_cards}
    </div>

    <div class="divider"></div>
    <div class="{sec_title_cls}">📋 Equipment Notes</div>
    <div class="{notes_box_cls}">{equip_notes}</div>

    <div class="divider"></div>
    <div class="{sec_title_cls}">🌳 Passive Tree</div>
    <div class="passive-note" style="{'border-left-color:#5ab0ff;background:rgba(90,176,255,0.04);' if is_ice else ''}">{tree_notes}</div>
  </div>'''

    panels_html.append(panel)

overview_html = '''<div class="overview" style="margin-top:24px;">
  <div class="overview-grid">
    <div class="overview-card">
      <h3>❄️ Build Overview</h3>
      <ul class="tip-list">
        <li>เริ่มด้วย <span class="highlight">Lightning Arrow</span> lvl 1–30 — ง่ายและ SSF viable</li>
        <li>Swap ไป <span class="highlight-blue">Ice Shot</span> ที่ <strong>lvl 31</strong> — main skill endgame</li>
        <li>ตั้ง <span class="highlight">Weapon Set 2</span> สำหรับ Freezing Mark ตั้งแต่ lvl 31</li>
        <li>สามารถ transition ไป endgame Ice Shot build ได้ทันทีหลัง campaign</li>
      </ul>
    </div>
    <div class="overview-card">
      <h3>🏹 Bow Progression</h3>
      <div class="asc-chain">
        <div class="asc-step"><div class="asc-num">1</div><div class="asc-node">Any Bow (lvl 1–15)</div></div>
        <div class="asc-down">↓</div>
        <div class="asc-step"><div class="asc-num" style="background:rgba(90,176,255,0.15);border-color:rgba(90,176,255,0.3);color:#5ab0ff;">2</div><div class="asc-node" style="background:rgba(90,176,255,0.08);border-color:rgba(90,176,255,0.25);color:#a0d8ff;">Recurve Bow (lvl 16)</div></div>
        <div class="asc-down" style="color:rgba(90,176,255,0.4);">↓</div>
        <div class="asc-step"><div class="asc-num" style="background:rgba(90,176,255,0.15);border-color:rgba(90,176,255,0.3);color:#5ab0ff;">3</div><div class="asc-node" style="background:rgba(90,176,255,0.08);border-color:rgba(90,176,255,0.25);color:#a0d8ff;">Dualstring/Cultist (lvl 33)</div></div>
        <div class="asc-down" style="color:rgba(90,176,255,0.4);">↓</div>
        <div class="asc-step"><div class="asc-num" style="background:rgba(90,176,255,0.15);border-color:rgba(90,176,255,0.3);color:#5ab0ff;">4</div><div class="asc-node" style="background:rgba(90,176,255,0.08);border-color:rgba(90,176,255,0.25);color:#a0d8ff;">Artillery Bow (lvl 46)</div></div>
      </div>
    </div>
    <div class="overview-card">
      <h3>💀 ลำดับ Boss (Act 1)</h3>
      <div class="boss-chain">
        <div class="boss-step"><div class="boss-num">1</div><div class="boss-node">Devourer (Mud Barrow)</div></div>
        <div class="boss-down">↓</div>
        <div class="boss-step"><div class="boss-num">2</div><div class="boss-node">Cold Witch (Clearfell)</div></div>
        <div class="boss-down">↓</div>
        <div class="boss-step"><div class="boss-num">3</div><div class="boss-node">Hut Witch (Grelwood)</div></div>
        <div class="boss-down">↓</div>
        <div class="boss-step"><div class="boss-num">4</div><div class="boss-node">Rust King (Redvale)</div></div>
      </div>
    </div>
    <div class="overview-card">
      <h3>💡 Tips สำคัญ</h3>
      <ul class="tip-list">
        <li>Salvage weapons ที่มี quality → ได้ <strong>Whetstone</strong></li>
        <li>Salvage items ที่มี socket → ได้ <strong>Artificer's Orb</strong></li>
        <li>รองเท้า <span class="highlight">Movement Speed</span> — ห้ามถอด</li>
        <li>Flat damage to attacks บน ถุงมือ + แหวน = สำคัญที่สุด</li>
        <li>Craft bow ใหม่ทุกครั้งที่ถึง lvl ที่กำหนด อย่าตามใจตัวเอง</li>
        <li>ตั้ง Weapon Set 2 ที่ <span class="highlight-blue">lvl 31</span> ก่อน swap skills</li>
      </ul>
    </div>
  </div>
</div>'''

tab_nav_html = '\n'.join(tabs_html)
panels_combined = '\n'.join(panels_html)

result = f'''{overview_html}

<!-- ICE SHOT LEVELING TABS -->
<div class="tabs-container">
  <div class="tab-nav" id="level-tab-nav">
{tab_nav_html}
  </div>

{panels_combined}

</div><!-- end level tabs -->'''

with open('C:/Users/yodyx/Desktop/POE2/leveling_section.html', 'w', encoding='utf-8') as f:
    f.write(result)

print(f'Generated {len(result):,} chars')
print(f'Saved to leveling_section.html')
