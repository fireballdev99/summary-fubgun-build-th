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
}

NOTES_TH = {
    'lvl 1-14': {
        'gems': [
            '⚔️ ลำดับ boss ช่วงต้น (Act 1): <span class="gem-ref">Devourer</span> (Mud Barrow) → <span class="gem-ref">Cold Witch</span> (Clearfell) → <span class="gem-ref">Hut Witch</span> (Grelwood) → <span class="gem-ref">Rust King</span> (Redvale)',
            'รับ <span class="gem-ref">Rapid Attacks I</span> หลังฆ่า Devourer · รับ <span class="gem-ref">Elemental Armament I</span> หลังฆ่า Hut Witch',
            'ลำดับ support gem ช่วงต้น: <span class="gem-ref">Rapid Attacks I</span> → <span class="gem-ref">Elemental Armament I</span> → <span class="gem-ref">Concentrated Area</span> → <span class="gem-ref">Elem. Armament I</span> ที่ 2',
            'ถ้า support gems ยังไม่ครบ ต้อง swap <span class="gem-ref">Elemental Armament I</span> จาก LA ไปใส่ Lightning Rod ตอนสู้ boss — สำคัญมากสำหรับ boss damage',
            'รับ <span class="gem-ref">Lightning Rod</span> ก่อน แล้วค่อยรับ <span class="gem-ref">Frost Bomb</span> (ควรมีทั้งคู่ก่อนสู้ Devourer/Cold Witch — มีหีบใน Clearfell ที่ drop skill gem lvl 1 เสมอ)',
            '<span class="gem-ref">Herald of Thunder</span> คือ spirit gem ที่ดีที่สุดตอนนี้ เพราะยัง swap ไป <span class="gem-ref">Ice Shot</span> ไม่ได้จนถึง lvl 31',
            '<span class="gem-ref">Pounce</span> ใช้เคลื่อนที่ได้ (optional) — ต้องมี talisman ใน offhand · มักจะ drop ช่วง Act 2-3 เมื่อ skill slot เต็ม',
            '⚠️ <strong style="color:var(--red);">สำคัญ!</strong> เนื่องจากมี skill swap ที่ lvl 24 ให้เก็บ uncut gems ไว้ — <strong>อย่าใช้ lvl 6-7 uncut gems ก่อน swap</strong>',
        ],
        'equip': [
            'ใน Act 1 gear ที่มี <strong>flat damage to attacks</strong> สำคัญที่สุด — ไม่ว่าจะเป็น phys/cold/fire/lightning',
            'ที่ lvl 11 หา <span class="gem-ref">Warden Bow</span> DPS สูงจาก vendor/drop — <strong>อย่าใช้ resource กับ bow นี้!</strong> เพราะจะทำ Recurve Bow 6 mod ที่ lvl 16 เก็บ Artificers Orb, Exalt, Regal ไว้',
            'ที่ Redvale หา <span class="gem-ref">Shortbow</span> และ level ให้ถึง 5 ก่อนสู้ Rust King · Trans/aug bow+quiver ทุกครั้งที่หามาได้',
            '🧪 Flask: อัปเกรดตลอด campaign — ซื้อ tier ใหม่ที่ vendor ทุกครั้งที่ถึง lvl 10, 16, 23, 30, 40, 50, 60',
            '🏹 Quiver: ต้องการ +levels + flat damage สูง · base ไม่สำคัญมาก',
            '🧤 Gloves: ดู vendor ทุก 1-2 lvl สำหรับ flat damage gloves — ทุก flat damage มีผลมากใน Act 1-2',
            '👟 Boots: Movement speed สำคัญมาก — ห้ามถอดเว้นแต่ของใหม่มี MS ด้วย',
            'เน้น Evasion หรือ Evasion/ES hybrid · Helmet/belt ดีสำหรับหา attribute (STR บน belt, DEX/INT บน helmet)',
            '⚠️ <strong style="color:var(--red);">สำคัญ!</strong> Salvage อาวุธที่มี quality → <strong>Whetstone</strong> · Salvage items ที่มี socket → <strong>Artificer\'s Orb</strong> — จำเป็นมากตลอด campaign',
            'Vendor ของ rare ทั้งหมดเป็น gold เพื่อ Gamble ใน Act 3-4',
        ],
        'tree': [
            'ใช้ <strong>Dexterity</strong> เป็น attribute node default · ใช้ STR/INT เฉพาะตามที่ gear ต้องการ',
            'หา amulet ที่มี attribute หรือ belt ที่มี STR เพื่อรองรับ requirement gear ช่วงหลัง',
            '⚡ Ascendancy (ตามลำดับ): <span class="gem-ref">Point Blank</span> → <span class="gem-ref">Endless Munitions</span> → <span class="gem-ref">Gathering Winds</span>',
        ],
    },
    'lvl 15-23': {
        'gems': [
            '<span class="gem-ref">Pounce</span> ใช้สำหรับ mobility — ต้องมี talisman ใน offhand (ใช้ low level สำหรับ STR requirement ต่ำ) · optional',
            '<span class="gem-ref">Ice-Tipped Arrows</span> ใช้ <span class="gem-ref">Magnified Area</span> หรือ <span class="gem-ref">Elem. Armament I</span> ก็ได้ — ขึ้นอยู่กับ attribute ที่มี (Mag Area ดีกว่าถ้าเลือกได้)',
            '⚠️ <strong style="color:var(--red);">สำคัญ!</strong> มี skill swap ที่ lvl 22-24 — <strong>อย่าใช้ lvl 6-7 uncut gems ก่อน swap!</strong>',
            'เก็บ Lesser Jeweller\'s Orb แรกไว้สำหรับ <span class="gem-ref">Snipe</span> (swap ที่ lvl 24) · อันที่ 2 สำหรับ <span class="gem-ref">Ice Shot</span> (lvl 31)',
        ],
        'equip': [
            '🏹 <strong>Bow ที่ lvl 16:</strong> ทำ <span class="gem-ref">Recurve Bow</span> ให้ดีที่สุด — bow นี้ใช้ถึง lvl 33 ดังนั้น <strong>ลงทุนเต็มที่!</strong>',
            'Craft bow: ใช้ Alchemy/Regal/Exalt ให้ได้ 6 mod · ลอง transmute/aug หลายๆ base ถ้าได้ prefix tier สูง → Regal แล้ว triple Exalt slam (หรือ Essence แทน Regal)',
            'ลำดับ bow upgrade: lvl 16 → <span class="gem-ref">Recurve Bow</span> · lvl 33 → <span class="gem-ref">Dualstring/Cultist Bow</span> (ilvl 33+) · lvl 46 → <span class="gem-ref">Artillery Bow</span> (ilvl 46+)',
            '⚠️ <strong>ตรวจ ilvl ของ bow ก่อน craft เสมอ</strong> (กด Alt บน item) — ต้องเป็น ilvl 33+ ก่อนทำ Cultist/Dualstring',
            '🧪 Flask: อัปเกรดที่ vendor ทุก lvl 10, 16, 23, 30, 40, 50, 60',
            '🏹 Quiver + 🧤 Gloves: flat damage สำคัญตลอด Act 1-2 · ดู vendor ทุก 1-2 lvl',
            '👟 Boots: Movement Speed ห้ามถอด',
            '⚠️ Salvage weapons (quality) → Whetstone · Salvage items (socket) → Artificer\'s Orb',
        ],
        'tree': [
            'ใช้ <strong>Dexterity</strong> default · ใช้ STR/INT ตาม requirement',
            '⚡ Ascendancy: <span class="gem-ref">Point Blank</span> → <span class="gem-ref">Endless Munitions</span> → <span class="gem-ref">Gathering Winds</span>',
        ],
    },
    'lvl 24-30': {
        'gems': [
            'ลำดับ Lesser Jeweller\'s Orb: <span class="gem-ref">Snipe</span> → <span class="gem-ref">Ice Shot</span> → <span class="gem-ref">Freezing Mark</span> → <span class="gem-ref">Herald of Ice</span>',
            'Quality priority: <span class="gem-ref">Freezing Mark</span> → <span class="gem-ref">Herald of Ice</span> → <span class="gem-ref">Snipe</span>',
            'นี่คือ <strong>skill swap ใหญ่ครั้งเดียวใน campaign</strong> (lvl 31 จะ swap LA → Ice Shot) ต้องการ gems: lvl 7 x1 (ต้องเป็น Freezing Mark!) + lvl 5-6 x2-3 + support gems 4-5 ชิ้น',
            'ให้ <span class="gem-ref">Snipe</span> อยู่ที่ level สูงสุดเสมอ · ให้ <span class="gem-ref">Lightning Arrow</span> ถึง lvl 7 แล้วหยุด (จะ swap เป็น Ice Shot ที่ lvl 9 ใน Act 3)',
            '<span class="gem-ref">Frost Bomb</span>: lvl 3 ใช้กับ boss ≤25, lvl 4 ใช้ ≤29, lvl 5 ใช้ ≤32 — จะ drop ช่วง Act 2-3 เมื่อขาด INT',
            '❄️ Boss rotation: วาง <span class="gem-ref">Ice-Tipped Arrows</span> → cast <span class="gem-ref">Freezing Mark</span> → ยิง <span class="gem-ref">Lightning Arrow</span> 3-4 ครั้ง → cast <span class="gem-ref">Freezing Salvo</span> → รอ freeze → กด <span class="gem-ref">Barrage</span> → <span class="gem-ref">Snipe</span>',
            'ถ้า Snipe ยาก: เปลี่ยน <span class="gem-ref">Window of Opportunity</span> เป็น <span class="gem-ref">Elemental Focus</span>',
        ],
        'equip': [
            '🏹 <strong>Bow ที่ lvl 16:</strong> ทำ <span class="gem-ref">Recurve Bow</span> ดีสุด ใช้ถึง lvl 33 — ลงทุนเต็มที่',
            'lvl 33: ทำ <span class="gem-ref">Dualstring Bow</span> หรือ <span class="gem-ref">Cultist Bow</span> (ilvl 33+) · lvl 46: <span class="gem-ref">Artillery Bow</span> (ilvl 46+)',
            '⚠️ ตรวจ ilvl ก่อน craft เสมอ (Alt + hover)',
            '🧪 Flask อัปเกรดที่ vendor lvl 10, 16, 23, 30, 40, 50, 60',
            '🏹 Quiver: +levels + flat damage สูง · 🧤 Gloves: flat damage จาก vendor ทุก 1-2 lvl',
            '👟 Boots: Movement Speed ห้ามถอด · เน้น Evasion/ES hybrid gear',
            '⚠️ Salvage weapons (quality) → Whetstone · Salvage items (socket) → Artificer\'s Orb',
        ],
        'tree': [
            'ใช้ <strong>Dexterity</strong> default · ใช้ STR/INT ตาม requirement',
            '⚡ Ascendancy: <span class="gem-ref">Point Blank</span> → <span class="gem-ref">Endless Munitions</span> → <span class="gem-ref">Gathering Winds</span>',
        ],
    },
    'lvl 31-41': {
        'gems': [
            '❄️ <strong style="color:#5ab0ff;">ที่ lvl 31 swap จาก Lightning Arrow ไป Ice Shot!</strong> และเปลี่ยน <span class="gem-ref">Herald of Thunder</span> เป็น <span class="gem-ref">Herald of Ice</span>',
            'ลำดับ Lesser Jeweller\'s Orb: <span class="gem-ref">Snipe</span> → <span class="gem-ref">Ice Shot</span> → <span class="gem-ref">Freezing Mark</span> → <span class="gem-ref">Herald of Ice</span>',
            '❄️ Boss rotation: วาง <span class="gem-ref">Ice-Tipped Arrows</span> → cast <span class="gem-ref">Freezing Mark</span> → ยิง <span class="gem-ref">Ice Shot</span> จนบอส freeze → กด <span class="gem-ref">Barrage</span> → <span class="gem-ref">Snipe</span>',
            '<span class="gem-ref">Freezing Salvo</span> กลายเป็น optional ช่วงนี้ — <span class="gem-ref">Ice Shot</span> freeze เร็วกว่าเดิมมาก',
            'Clear: ใช้ <span class="gem-ref">Ice-Tipped Arrows</span> + <span class="gem-ref">Freezing Mark</span> buff + <span class="gem-ref">Ice Shot</span> — ต้องการ Ice-Tipped เฉพาะ rares หรือ pack ใหญ่',
        ],
        'equip': [
            '🏹 <strong>Bow ที่ lvl 33:</strong> ทำ <span class="gem-ref">Dualstring Bow</span> หรือ <span class="gem-ref">Cultist Bow</span> (ilvl 33+) — ใช้ถึง lvl 46 ดังนั้น <strong>ลงทุนเต็มที่!</strong>',
            'Craft: Alchemy/Regal/Exalt ให้ได้ 6 mod · <span class="gem-ref">Cultist Bow</span> พบบ่อยกว่าใน Act 3 ก็ใช้ได้',
            'เก็บ Iron Rune ไว้ 1 ชิ้นสำหรับ <span class="gem-ref">Artillery Bow</span> ที่ lvl 46',
            '⚠️ ตรวจ ilvl ก่อน craft (Alt + hover) — ต้องเป็น ilvl 33+',
            '🧪 Flask อัปเกรดที่ vendor lvl 10, 16, 23, 30, 40, 50, 60',
            '🏹 Quiver: +levels + flat damage · 👟 Boots: Movement Speed ห้ามถอด',
            '⚠️ Salvage weapons (quality) → Whetstone · Salvage items (socket) → Artificer\'s Orb',
        ],
        'tree': [
            '⚠️ <strong style="color:#5ab0ff;">ที่ lvl 31 ตั้ง Weapon Set</strong> — ได้ 10 points หลังฆ่า monkey ใน Jungle Ruins (Act 3)',
            'วิธีตั้ง: ใส่ <span class="gem-ref">Freezing Mark</span> ใน <strong>Weapon Set 2</strong> · skills อื่นทั้งหมดอยู่ใน Set 1',
            'เปิด skill menu → กด details ของแต่ละ skill → กำหนด weapon set',
            '⚡ Ascendancy: <span class="gem-ref">Point Blank</span> → <span class="gem-ref">Endless Munitions</span> → <span class="gem-ref">Gathering Winds</span>',
        ],
    },
    'lvl 42-59': {
        'gems': [
            'ลำดับ Lesser Jeweller\'s Orb: <span class="gem-ref">Snipe</span> → <span class="gem-ref">Ice Shot</span> → <span class="gem-ref">Freezing Mark</span> → <span class="gem-ref">Herald of Ice</span>',
            'ถ้าได้ Greater Jeweller\'s Orb ที่ 2 ใส่ใน <span class="gem-ref">Ice Shot</span> เพื่อ <span class="gem-ref">Fork</span> (อันแรกไปที่ Snipe)',
            'lvl 5 support gem แรกควรเป็น <span class="gem-ref">Charged Mark</span> สำหรับ <span class="gem-ref">Freezing Mark</span> — ทำให้ shock boss อย่างสม่ำเสมอ เพิ่ม damage มาก',
            '❄️ Boss rotation: วาง <span class="gem-ref">Ice-Tipped Arrows</span> → cast <span class="gem-ref">Freezing Mark</span> → ยิง <span class="gem-ref">Ice Shot</span> จน freeze → กด <span class="gem-ref">Barrage</span> → <span class="gem-ref">Snipe</span>',
            '<span class="gem-ref">Tornado Shot</span>: วางก่อน boss spawn สำหรับ extra damage · ใช้ clear pack ได้ด้วย',
        ],
        'equip': [
            '🏹 <strong>Bow ที่ lvl 46:</strong> <span class="gem-ref">Artillery Bow</span> — upgrade ใหญ่ที่สุด! เน้น <strong>%phys สูง</strong> เพราะ base phys สูงมาก',
            'ถ้าหา %phys ไม่ได้ ใช้ flat damage สูงแทนได้ — สำคัญคือ DPS รวมสูง',
            '⚠️ ตรวจ ilvl 46+ ก่อน craft (Alt + hover)',
            '🧪 Flask อัปเกรดที่ vendor lvl 50, 60',
            '🏹 Quiver: +levels + flat damage · 👟 Boots: Movement Speed ห้ามถอด',
            '⚠️ Salvage weapons (quality) → Whetstone · Salvage items (socket) → Artificer\'s Orb',
        ],
        'tree': [
            'Weapon Set ยังเหมือนเดิม: <span class="gem-ref">Freezing Mark</span> ใน Set 2 · ทุก skill อื่นใน Set 1',
            '⚡ Ascendancy: <span class="gem-ref">Point Blank</span> → <span class="gem-ref">Endless Munitions</span> → <span class="gem-ref">Gathering Winds</span>',
        ],
    },
    'lvl 60+': {
        'gems': [
            'ลำดับ Lesser Jeweller\'s Orb: <span class="gem-ref">Snipe</span> → <span class="gem-ref">Ice Shot</span> → <span class="gem-ref">Freezing Mark</span> → <span class="gem-ref">Herald of Ice</span>',
            'ถ้าได้ Greater Jeweller\'s Orb ที่ 2 ใส่ใน <span class="gem-ref">Ice Shot</span> เพื่อ <span class="gem-ref">Fork</span>',
            'lvl 5 support แรก: <span class="gem-ref">Charged Mark</span> สำหรับ <span class="gem-ref">Freezing Mark</span> — shock boss สม่ำเสมอ',
            '❄️ Boss rotation: วาง <span class="gem-ref">Ice-Tipped Arrows</span> → cast <span class="gem-ref">Freezing Mark</span> → ยิง <span class="gem-ref">Ice Shot</span> จน freeze → <span class="gem-ref">Barrage</span> → <span class="gem-ref">Snipe</span>',
            'Setup นี้เหมือน lvl 42-59 — พร้อม transition ไป endgame Ice Shot build ได้เลย',
        ],
        'equip': [
            '🏹 Bow: ยังใช้ <span class="gem-ref">Artillery Bow</span> จาก lvl 46 ต่อ — ถ้าไม่ได้ %phys ดีใช้ flat damage สูงแทน',
            'เตรียมตัว transition ไป endgame — focus life + resist ให้ครบ · เก็บ currency ไว้สำหรับ endgame gear',
            '🧪 Flask อัปเกรดที่ vendor lvl 60 (tier สุดท้าย)',
            '⚠️ Salvage weapons (quality) → Whetstone · Salvage items (socket) → Artificer\'s Orb',
        ],
        'tree': [
            'Weapon Set: <span class="gem-ref">Freezing Mark</span> ใน Set 2 · ทุก skill ใน Set 1',
            '⚡ Ascendancy: <span class="gem-ref">Point Blank</span> → <span class="gem-ref">Endless Munitions</span> → <span class="gem-ref">Gathering Winds</span>',
            'เมื่อจบ campaign สามารถ respec passive tree เพื่อ transition ไป endgame build ได้เลย',
        ],
    },
}

def sup_name(slug):
    if slug in SLUG_NAME: return SLUG_NAME[slug]
    n = re.sub(r'^support', '', slug)
    n = re.sub(r'player(two|three)?$', '', n)
    n = re.sub(r'([A-Z])', r' \1', n).strip().title()
    return n

ICE = 'rgba(90,176,255,0.08)'
ICE_BORDER = 'rgba(90,176,255,0.2)'
ICE_TEXT = '#8ecfff'

def skill_tag(name):
    n = name.lower()
    if 'ice shot' in n or 'lightning arrow' in n: return ('tag-clear', 'Main Clear')
    if 'snipe' in n: return ('tag-boss', 'Boss DPS')
    if 'barrage' in n: return ('tag-boss', 'Boss Burst')
    if 'freezing mark' in n: return ('tag-utility', 'Debuff')
    if 'herald' in n: return ('tag-utility', 'Buff')
    if 'tornado' in n: return ('tag-utility', 'AOE Utility')
    if 'wind dancer' in n: return ('tag-utility', 'Defense')
    if 'frost bomb' in n or 'freezing salvo' in n: return ('tag-boss', 'Boss Debuff')
    if 'ice-tipped' in n: return ('tag-utility', 'AOE')
    if 'combat frenzy' in n: return ('tag-utility', 'Charges')
    if 'pounce' in n: return ('tag-utility', 'Mobility')
    if 'lightning rod' in n: return ('tag-boss', 'Boss DPS')
    return ('tag-utility', 'Utility')

def weapon_set_badge(name, wset):
    n = name.lower()
    if 'freezing mark' in n:
        return '<span class="weapon-set-badge" style="color:#e05050;border-color:rgba(224,80,80,0.3);background:rgba(224,80,80,0.12);">SET 2</span>'
    if wset == 'set1':
        return '<span class="weapon-set-badge">SET 1</span>'
    return ''

def render_skill_row(g, is_ice=False):
    active = g.get('activeSkill', {})
    name = active.get('name', '')
    icon = active.get('iconURL', 'https://cdn.mobalytics.gg/assets/poe-2/images/game/Art/2DItems/Gems/New/BlankGem.avif')
    sups = g.get('supportGems', []) or []
    wset = g.get('weaponSet', '') or ''
    tag_cls, tag_label = skill_tag(name)

    bg_style = 'border-color:#1a3050;background:rgba(0,20,40,0.3);' if is_ice else ''
    badge = weapon_set_badge(name, wset)

    chips = ''
    if sups:
        chips = '<span class="plus">+</span>'
        for s in sups:
            slug = s.get('gemSlug', '')
            s_icon = s.get('iconURL', '')
            s_name = sup_name(slug)
            chip_style = f'background:{ICE};border-color:{ICE_BORDER};color:{ICE_TEXT};' if is_ice else ''
            chips += f'<div class="support-chip" style="{chip_style}"><img class="gem-icon small" src="{s_icon}" alt="">{s_name}</div>'

    return f'''      <div class="skill-row" style="{bg_style}">
        <img class="gem-icon" src="{icon}" alt="{name}">
        <div class="skill-name">{name}</div>
        <div class="support-chips">{chips}</div>
        <span class="skill-tag {tag_cls}">{tag_label}</span>{badge}
      </div>'''

def render_notes(lines, is_ice=False):
    cls = 'ice-notes-box' if is_ice else 'notes-box'
    inner = '\n'.join(f'<p>{line}</p>' for line in lines)
    return f'<div class="{cls}">{inner}</div>'

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
    'lvl 1-14':  'ใช้ <strong>Lightning Arrow</strong> clear · Frost Bomb กับ boss · เน้น flat damage + movement speed',
    'lvl 15-23': 'ยัง LA · เพิ่ม Pounce mobility (optional) · <strong>Recurve Bow ที่ lvl 16</strong> — ลงทุนเต็มที่',
    'lvl 24-30': 'เพิ่ม <strong>Snipe + Freezing Mark</strong> · Freezing Salvo boss · เตรียมพร้อมสำหรับ swap ที่ lvl 31',
    'lvl 31-41': '⚡→❄️ <strong style="color:#5ab0ff;">Swap ไป Ice Shot ที่ lvl 31!</strong> · ตั้ง Weapon Set 2 สำหรับ Freezing Mark · Dualstring/Cultist Bow ที่ lvl 33',
    'lvl 42-59': 'Ice Shot full setup · Wind Dancer + Tornado Shot · <strong>Artillery Bow ที่ lvl 46</strong>',
    'lvl 60+':   'Setup ครบ · พร้อม transition ไป endgame Ice Shot Deadeye build ได้เลย',
}

tabs_html = []
panels_html = []

for i, v in enumerate(d['variants']):
    title = v['title']
    tab_id = f'il{i+1}'
    active_cls = ' active' if i == 0 else ''
    color = VARIANT_COLORS[title]
    is_ice = color['is_ice']
    tab_cls = 'ice-tab-btn' if is_ice else ''
    tabs_html.append(f'    <button class="tab-btn {tab_cls}" onclick="switchLevelTab(\'{tab_id}\', this)">{title}</button>')

    sec_cls = 'ice-section-title' if is_ice else 'section-title'
    tree_style = 'border-left-color:#5ab0ff;background:rgba(90,176,255,0.04);' if is_ice else ''

    skills_rows = '\n'.join(render_skill_row(g, is_ice) for g in v['skillGems'])

    th = NOTES_TH[title]
    gems_notes_html = render_notes(th['gems'], is_ice)
    equip_notes_html = render_notes(th['equip'], is_ice)
    tree_notes_html = render_notes(th['tree'], is_ice)

    slots_order = [
        ('mainHand', 'Bow ⭐'), ('helmet', 'Helmet'), ('body', 'Body'),
        ('gloves', 'Gloves'), ('boots', 'Boots'), ('belt', 'Belt'),
        ('amulet', 'Amulet'), ('leftRing', 'Ring'), ('flask1', 'Flask'),
        ('charm1', 'Charm 1'), ('charm2', 'Charm 2'),
    ]
    equip_cards = '\n'.join(equip_card(label, v['equipment'].get(slot)) for slot, label in slots_order if v['equipment'].get(slot))

    panel = f'''  <div id="{tab_id}" class="tab-panel{active_cls}" style="background:{color['bg']};border-color:{color['border']};">
    <div class="ice-variant-desc">{VARIANT_DESC[title]}</div>

    <div class="{sec_cls}">⚔️ Skills &amp; Gems</div>
    <div class="skills-grid">
{skills_rows}
    </div>

    <div class="divider"></div>
    <div class="{sec_cls}">📋 คำแนะนำ Skill Gems</div>
    {gems_notes_html}

    <div class="divider"></div>
    <div class="{sec_cls}">🎒 Equipment</div>
    <div class="equip-grid">
{equip_cards}
    </div>

    <div class="divider"></div>
    <div class="{sec_cls}">📋 คำแนะนำ Equipment</div>
    {equip_notes_html}

    <div class="divider"></div>
    <div class="{sec_cls}">🌳 Passive Tree</div>
    <div class="passive-note" style="{tree_style}">{tree_notes_html}</div>
  </div>'''

    panels_html.append(panel)

overview_html = '''<div class="overview" style="margin-top:24px;">
  <div class="overview-grid">
    <div class="overview-card">
      <h3>❄️ Build Overview</h3>
      <ul class="tip-list">
        <li>เริ่มด้วย <span class="highlight">Lightning Arrow</span> lvl 1–30 — ง่าย, SSF viable</li>
        <li>Swap ไป <span class="highlight-blue">Ice Shot</span> ที่ <strong>lvl 31</strong> — main skill endgame</li>
        <li>ตั้ง <span class="highlight">Weapon Set 2</span> สำหรับ Freezing Mark ที่ lvl 31</li>
        <li>Transition ไป endgame ได้ทันทีหลัง campaign จบ</li>
      </ul>
    </div>
    <div class="overview-card">
      <h3>🏹 Bow Progression</h3>
      <div class="asc-chain">
        <div class="asc-step"><div class="asc-num">1</div><div class="asc-node">Any Bow (lvl 1–15)</div></div>
        <div class="asc-down">↓</div>
        <div class="asc-step"><div class="asc-num" style="background:rgba(90,176,255,0.15);border-color:rgba(90,176,255,0.3);color:#5ab0ff;">2</div><div class="asc-node" style="background:rgba(90,176,255,0.08);border-color:rgba(90,176,255,0.25);color:#a0d8ff;">Recurve Bow (lvl 16) ⭐</div></div>
        <div class="asc-down" style="color:rgba(90,176,255,0.4);">↓</div>
        <div class="asc-step"><div class="asc-num" style="background:rgba(90,176,255,0.15);border-color:rgba(90,176,255,0.3);color:#5ab0ff;">3</div><div class="asc-node" style="background:rgba(90,176,255,0.08);border-color:rgba(90,176,255,0.25);color:#a0d8ff;">Dualstring/Cultist (lvl 33) ⭐</div></div>
        <div class="asc-down" style="color:rgba(90,176,255,0.4);">↓</div>
        <div class="asc-step"><div class="asc-num" style="background:rgba(90,176,255,0.15);border-color:rgba(90,176,255,0.3);color:#5ab0ff;">4</div><div class="asc-node" style="background:rgba(90,176,255,0.08);border-color:rgba(90,176,255,0.25);color:#a0d8ff;">Artillery Bow (lvl 46) ⭐</div></div>
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
        <li>Salvage weapons (quality) → <strong>Whetstone</strong></li>
        <li>Salvage items (socket) → <strong>Artificer\'s Orb</strong></li>
        <li>รองเท้า <span class="highlight">Movement Speed</span> — ห้ามถอด</li>
        <li><span class="highlight">Flat damage to attacks</span> บน ถุงมือ + แหวน</li>
        <li><strong>Craft bow ทุก milestone</strong>: lvl 16 / 33 / 46</li>
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

print(f'Generated {len(result):,} chars -> leveling_section.html')
