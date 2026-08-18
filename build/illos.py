# Pen-and-ink style SVG illustrations. All drawn in a 200x140 box, stroke = currentColor.
S = 'fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"'
T = 'fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"'

def wrap(body, w=200, h=140):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" class="illo" aria-hidden="true">{body}</svg>'

ILLOS = {}

# Farmhouse with barn and silo — cover / title
ILLOS['farm'] = wrap(f'''
<g {S}>
 <!-- ground line -->
 <path d="M6 118 Q100 112 194 118"/>
 <!-- barn -->
 <path d="M112 116 V70 L142 48 L172 70 V116"/>
 <path d="M112 70 L142 48 L172 70" />
 <path d="M106 72 L142 44 L178 72"/>
 <path d="M130 116 V90 H154 V116"/>
 <path d="M130 90 L154 116 M154 90 L130 116"/>
 <path d="M136 62 h12 v10 h-12z"/>
 <!-- silo -->
 <path d="M178 116 V60 Q186 50 194 60 V116"/>
 <path d="M178 76 H194 M178 92 H194"/>
 <!-- house -->
 <path d="M28 116 V78 L58 52 L88 78 V116"/>
 <path d="M22 80 L58 48 L94 80"/>
 <path d="M50 116 V94 H66 V116"/>
 <path d="M34 86 h10 v10 h-10z M72 86 h10 v10 h-10z"/>
 <path d="M70 62 V50 h8 v20"/>
 <!-- tree -->
 <path d="M12 116 V96"/>
 <path d="M12 96 Q-2 90 4 78 Q2 66 14 66 Q26 60 26 74 Q34 84 22 92 Q22 98 12 96"/>
 <!-- fence -->
 <path d="M96 116 V102 M104 116 V102 M96 106 H108 M96 112 H108"/>
 <!-- sun -->
 <path d="M160 26 a8 8 0 1 0 0.1 0 M160 8 V12 M160 40 V44 M142 26 H146 M174 26 H178 M147 13 l3 3 M170 36 l3 3 M173 13 l-3 3 M150 36 l-3 3"/>
</g>''')


# Wheat sheaf
ILLOS['wheat'] = wrap(f'''
<g {S}>
 <path d="M100 130 V40"/>
 <path d="M100 40 q-8 -6 -8 -16 q8 6 8 16 q8 -6 8 -16 q-8 6 -8 16"/>
 <path d="M100 52 q-9 -5 -10 -16 q9 5 10 16 q9 -5 10 -16 q-9 5 -10 16"/>
 <path d="M100 64 q-9 -5 -10 -16 q9 5 10 16 q9 -5 10 -16 q-9 5 -10 16"/>
 <path d="M100 76 q-9 -5 -10 -16 q9 5 10 16 q9 -5 10 -16 q-9 5 -10 16"/>
 <path d="M76 130 Q80 90 84 60"/>
 <path d="M84 60 q-8 -6 -8 -16 q8 6 8 16 q8 -6 8 -16 q-8 6 -8 16"/>
 <path d="M83 72 q-9 -5 -10 -16 q9 5 10 16 q9 -5 10 -16 q-9 5 -10 16"/>
 <path d="M82 84 q-9 -5 -10 -16 q9 5 10 16 q9 -5 10 -16 q-9 5 -10 16"/>
 <path d="M124 130 Q120 90 116 60"/>
 <path d="M116 60 q-8 -6 -8 -16 q8 6 8 16 q8 -6 8 -16 q-8 6 -8 16"/>
 <path d="M117 72 q-9 -5 -10 -16 q9 5 10 16 q9 -5 10 -16 q-9 5 -10 16"/>
 <path d="M118 84 q-9 -5 -10 -16 q9 5 10 16 q9 -5 10 -16 q-9 5 -10 16"/>
 <path d="M84 104 q16 -8 32 0 q4 4 0 8 q-16 -6 -32 0 q-4 -4 0 -8z"/>
</g>''')

# Milk can
ILLOS['milkcan'] = wrap(f'''
<g {S}>
 <path d="M76 128 H124 Q130 128 130 122 V72 Q130 58 116 54 V44 H84 V54 Q70 58 70 72 V122 Q70 128 76 128z"/>
 <path d="M84 44 Q84 34 100 34 Q116 34 116 44"/>
 <path d="M84 50 H116"/>
 <path d="M70 68 Q60 66 58 78 Q60 88 70 86 M130 68 Q140 66 142 78 Q140 88 130 86"/>
 <path d="M76 100 H124"/>
 <path d="M96 30 H104"/>
</g>''')

# Pie
ILLOS['pie'] = wrap(f'''
<g {S}>
 <path d="M30 88 Q100 72 170 88 Q176 96 168 100 Q100 116 32 100 Q24 96 30 88z"/>
 <path d="M34 90 Q100 78 166 90"/>
 <path d="M42 84 Q100 62 158 84"/>
 <path d="M60 78 Q66 68 72 78 M88 72 Q94 62 100 72 M116 74 Q122 64 128 74"/>
 <path d="M52 76 q-2 -12 4 -20 M78 70 q-2 -12 4 -20 M104 68 q-2 -12 4 -20 M130 72 q-2 -12 4 -20" stroke-width="1.6"/>
 <path d="M40 100 Q100 122 160 100 Q160 116 100 122 Q40 116 40 100" stroke-width="1.6"/>
 <path d="M18 128 H182" stroke-width="1.6"/>
</g>''')

# Mixing bowl with spoon
ILLOS['bowl'] = wrap(f'''
<g {S}>
 <path d="M40 66 H160 Q162 118 100 120 Q38 118 40 66z"/>
 <path d="M34 66 H166"/>
 <path d="M52 100 Q100 112 148 100" stroke-width="1.6"/>
 <path d="M112 66 L150 22 Q158 14 164 22 Q168 30 160 34 L118 66"/>
 <path d="M64 66 q6 -10 12 0 q6 -10 12 0" stroke-width="1.6"/>
 <path d="M18 128 H182" stroke-width="1.6"/>
</g>''')

# Mason jars
ILLOS['jars'] = wrap(f'''
<g {S}>
 <path d="M52 44 h44 v10 q8 4 8 12 v50 q0 8 -8 8 h-44 q-8 0 -8 -8 v-50 q0 -8 8 -12z"/>
 <path d="M50 44 h48 v-8 h-48z"/>
 <path d="M52 92 h52" stroke-width="1.4"/>
 <path d="M60 78 a4 4 0 1 0 0.1 0 M74 84 a3 3 0 1 0 0.1 0 M84 74 a3.5 3.5 0 1 0 0.1 0 M64 100 a3 3 0 1 0 0.1 0 M88 104 a3 3 0 1 0 0.1 0" stroke-width="1.4"/>
 <path d="M124 60 h30 v8 q6 3 6 9 v40 q0 7 -6 7 h-30 q-6 0 -6 -7 v-40 q0 -6 6 -9z"/>
 <path d="M122 60 h34 v-7 h-34z"/>
 <path d="M124 90 h36" stroke-width="1.4"/>
 <path d="M126 96 h30 v18 h-30z" stroke-width="1.4"/>
 <path d="M18 128 H182" stroke-width="1.6"/>
</g>''')

# Apple
ILLOS['apple'] = wrap(f'''
<g {S}>
 <path d="M100 48 Q84 32 64 42 Q40 56 48 88 Q56 118 82 118 Q92 118 100 112 Q108 118 118 118 Q144 118 152 88 Q160 56 136 42 Q116 32 100 48z"/>
 <path d="M100 48 Q102 34 110 26"/>
 <path d="M104 40 Q120 24 138 32 Q126 46 104 40z"/>
 <path d="M64 60 Q56 70 58 84" stroke-width="1.6"/>
 <path d="M18 128 H182" stroke-width="1.6"/>
</g>''')


# Basket of eggs
ILLOS['eggs'] = wrap(f'''
<g {S}>
 <path d="M44 84 H156 L146 118 H54z"/>
 <path d="M40 84 H160"/>
 <path d="M60 84 Q60 40 100 32 Q140 40 140 84"/>
 <path d="M60 84 Q80 62 100 60 Q120 62 140 84" stroke-width="1.6"/>
 <path d="M76 82 q0 -12 10 -12 q10 0 10 12 M100 82 q0 -12 10 -12 q10 0 10 12 M88 74 q0 -12 10 -12 q10 0 10 12" stroke-width="1.8"/>
 <path d="M52 96 H148 M50 106 H150" stroke-width="1.4"/>
 <path d="M18 128 H182" stroke-width="1.6"/>
</g>''')

# Cast iron skillet
ILLOS['skillet'] = wrap(f'''
<g {S}>
 <path d="M30 76 H126 Q128 116 78 116 Q28 116 30 76z"/>
 <path d="M26 76 H130"/>
 <path d="M126 82 L184 70 Q192 68 190 76 L128 90"/>
 <path d="M50 96 Q78 104 106 96" stroke-width="1.6"/>
 <path d="M60 60 q4 -8 0 -16 M78 58 q4 -8 0 -16 M96 60 q4 -8 0 -16" stroke-width="1.4"/>
 <path d="M18 128 H182" stroke-width="1.6"/>
</g>''')

# Loaf of bread
ILLOS['bread'] = wrap(f'''
<g {S}>
 <path d="M40 116 H150 Q166 116 166 100 V84 Q166 68 150 68 H40 Q30 68 30 80 V106 Q30 116 40 116z"/>
 <path d="M40 68 Q40 46 62 46 H84 Q92 60 100 46 H124 Q132 60 140 46 H150 Q166 46 166 68"/>
 <path d="M52 62 Q60 50 70 62 M78 62 Q86 50 96 62 M104 62 Q112 50 122 62 M130 62 Q138 50 148 62" stroke-width="1.6"/>
 <path d="M18 128 H182" stroke-width="1.6"/>
</g>''')

# Cake on stand
ILLOS['cake'] = wrap(f'''
<g {S}>
 <path d="M50 96 H150 V72 Q100 84 50 72z"/>
 <path d="M50 72 Q100 60 150 72 Q100 84 50 72z"/>
 <path d="M50 84 Q100 96 150 84" stroke-width="1.6"/>
 <path d="M60 78 q4 8 8 0 q4 8 8 0 q4 8 8 0 q4 8 8 0 q4 8 8 0 q4 8 8 0 q4 8 8 0 q4 8 8 0 q4 8 8 0" stroke-width="1.6"/>
 <path d="M96 66 a4 4 0 1 0 0.1 0" stroke-width="1.6"/>
 <path d="M96 62 V54"/>
 <path d="M36 100 H164 Q166 100 166 102 Q166 106 100 106 Q34 106 34 102 Q34 100 36 100z"/>
 <path d="M100 106 V120 M78 122 H122"/>
 <path d="M18 128 H182" stroke-width="1.6"/>
</g>''')


# Soup pot
ILLOS['pot'] = wrap(f'''
<g {S}>
 <path d="M44 66 H156 V106 Q156 116 146 116 H54 Q44 116 44 106z"/>
 <path d="M40 66 H160"/>
 <path d="M52 66 Q52 58 60 58 H140 Q148 58 148 66"/>
 <path d="M100 58 V50 M92 50 h16"/>
 <path d="M44 84 Q30 82 30 92 Q30 100 44 98 M156 84 Q170 82 170 92 Q170 100 156 98"/>
 <path d="M70 46 q4 -8 0 -16 M92 44 q4 -8 0 -16 M114 46 q4 -8 0 -16" stroke-width="1.4"/>
 <path d="M18 128 H182" stroke-width="1.6"/>
</g>''')

# Fish
ILLOS['fish'] = wrap(f'''
<g {S}>
 <path d="M30 80 Q60 44 108 48 Q146 52 166 80 Q146 108 108 112 Q60 116 30 80z"/>
 <path d="M166 80 L190 60 Q186 80 190 100z"/>
 <path d="M60 60 Q56 74 62 88" />
 <path d="M96 52 Q104 40 118 44 M100 110 Q108 122 122 116" stroke-width="1.6"/>
 <path d="M50 74 a2 2 0 1 0 0.1 0" stroke-width="3"/>
 <path d="M80 62 q6 6 0 12 M96 60 q6 6 0 12 M112 62 q6 6 0 12 M128 66 q6 6 0 12 M88 76 q6 6 0 12 M104 76 q6 6 0 12 M120 78 q6 6 0 12" stroke-width="1.4"/>
 <path d="M18 128 H182" stroke-width="1.6"/>
</g>''')

# Salad bowl with tongs / greens
ILLOS['salad'] = wrap(f'''
<g {S}>
 <path d="M36 74 H164 Q166 118 100 120 Q34 118 36 74z"/>
 <path d="M30 74 H170"/>
 <path d="M52 74 Q60 52 78 60 Q86 44 100 56 Q112 42 124 58 Q140 50 148 74" />
 <path d="M70 66 q6 -8 12 -2 M110 62 q6 -8 12 -2" stroke-width="1.4"/>
 <path d="M96 66 a4 4 0 1 0 0.1 0" stroke-width="1.6"/>
 <path d="M18 128 H182" stroke-width="1.6"/>
</g>''')

# Casserole dish
ILLOS['casserole'] = wrap(f'''
<g {S}>
 <path d="M40 76 H160 V108 Q160 114 154 114 H46 Q40 114 40 108z"/>
 <path d="M40 76 Q40 68 48 68 H152 Q160 68 160 76"/>
 <path d="M92 68 Q92 60 100 60 Q108 60 108 68"/>
 <path d="M40 90 Q28 88 28 96 Q28 104 40 102 M160 90 Q172 88 172 96 Q172 104 160 102"/>
 <path d="M48 96 H152" stroke-width="1.4"/>
 <path d="M18 128 H182" stroke-width="1.6"/>
</g>''')



# Spice / mustard jar & spoon for sauces
ILLOS['sauce'] = wrap(f'''
<g {S}>
 <path d="M76 116 H124 Q130 116 130 110 V72 Q130 64 122 62 H78 Q70 64 70 72 V110 Q70 116 76 116z"/>
 <path d="M84 62 V50 H116 V62"/>
 <path d="M80 50 H120"/>
 <path d="M84 84 h32 v18 h-32z" stroke-width="1.4"/>
 <path d="M112 62 L146 30 Q152 26 156 30 Q158 36 152 40 L118 66"/>
 <path d="M18 128 H182" stroke-width="1.6"/>
</g>''')

# Children / crafts — kite? use scissors & paper star
ILLOS['crafts'] = wrap(f'''
<g {S}>
 <path d="M60 60 L70 82 L94 84 L76 100 L82 124 L60 112 L38 124 L44 100 L26 84 L50 82z"/>
 <path d="M130 118 L160 62 M118 116 L154 60"/>
 <path d="M126 122 a8 8 0 1 0 0.1 0 M116 120 a8 8 0 1 0 0.1 0" stroke-width="1.8"/>
 <path d="M18 128 H182" stroke-width="1.6"/>
</g>''')

# Broom & bucket — household hints
ILLOS['broom'] = wrap(f'''
<g {S}>
 <path d="M60 24 L84 92"/>
 <path d="M76 88 Q64 96 60 116 L110 116 Q106 96 92 84z"/>
 <path d="M70 100 L74 116 M80 98 L84 116 M90 100 L94 116" stroke-width="1.4"/>
 <path d="M126 82 H166 L160 116 H132z"/>
 <path d="M124 82 H168"/>
 <path d="M132 82 Q146 60 160 82"/>
 <path d="M18 128 H182" stroke-width="1.6"/>
</g>''')

# Small ornaments / dividers
ILLOS['spoonrule'] = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 20" class="rule" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"><path d="M10 10 H170"/><path d="M230 10 H390"/><path d="M186 10 h10 M204 10 h10"/><path d="M200 5 a5 5 0 1 0 0.1 0" /></g></svg>'

# Rooster (cleaner)
ILLOS['rooster'] = wrap(f"""
<g {S}>
 <path d="M70 112 Q48 100 52 78 Q58 58 84 58 Q106 60 112 78 L118 100 Q110 114 88 116z"/>
 <path d="M112 78 Q112 56 126 50 Q136 46 138 56 L136 66 Q130 72 118 70"/>
 <path d="M126 50 q0 -10 6 -10 q2 -8 8 -6 q4 -8 8 -2 q-6 4 -8 10 q-4 2 -6 8"/>
 <path d="M138 56 l10 2 -10 4"/>
 <path d="M134 62 q4 4 2 10"/>
 <path d="M130 54 a1.6 1.6 0 1 0 0.1 0" stroke-width="2.6"/>
 <path d="M52 78 Q34 64 30 40 M54 86 Q30 78 18 58 M58 96 Q30 96 22 84" />
 <path d="M84 116 V126 M84 126 l-6 6 M84 126 l6 6 M84 126 v7 M100 114 V126 M100 126 l-6 6 M100 126 l6 6 M100 126 v7"/>
 <path d="M64 100 q10 -6 20 0" stroke-width="1.4"/>
 <path d="M12 134 H188" stroke-width="1.6"/>
</g>""")

# Teapot & cup
ILLOS['teapot'] = wrap(f"""
<g {S}>
 <path d="M52 64 Q40 76 40 92 Q42 116 82 116 Q122 116 124 92 Q124 76 112 64z"/>
 <path d="M50 64 H114"/>
 <path d="M66 64 Q66 52 82 52 Q98 52 98 64"/>
 <path d="M82 52 V44 M77 44 h10"/>
 <path d="M114 74 Q136 70 142 50 M120 88 Q142 84 148 52 M140 48 h10"/>
 <path d="M40 78 Q22 78 24 92 Q26 106 42 104"/>
 <path d="M144 118 h28 q0 -20 -4 -28 h-20 q-4 8 -4 28z"/>
 <path d="M172 96 q10 -2 10 8 q0 10 -12 12"/>
 <path d="M152 78 q4 -6 0 -12 M162 80 q4 -6 0 -12" stroke-width="1.4"/>
 <path d="M18 128 H182" stroke-width="1.6"/>
</g>""")



# Vegetables: carrot, onion, pea pod
ILLOS['veg'] = wrap(f"""
<g {S}>
 <path d="M30 116 Q60 80 96 60 Q104 56 106 64 Q100 74 60 100 Q40 112 30 116z"/>
 <path d="M96 60 q4 -14 14 -18 q-2 12 -14 18 M100 58 q12 -6 22 -2 q-10 8 -22 2" stroke-width="1.6"/>
 <path d="M52 100 l6 4 M64 90 l6 4 M76 82 l6 4" stroke-width="1.4"/>
 <path d="M126 116 Q104 110 108 90 Q112 72 130 70 Q148 72 152 90 Q156 110 134 116z"/>
 <path d="M130 70 q-4 -10 2 -16 q6 6 2 16 M124 74 q-6 -8 -4 -14 M136 74 q6 -8 4 -14" stroke-width="1.6"/>
 <path d="M120 88 Q118 104 126 114 M140 88 Q142 104 134 114" stroke-width="1.2"/>
 <path d="M150 116 Q160 96 184 88 Q188 104 168 116z"/>
 <path d="M158 110 a3 3 0 1 0 0.1 0 M166 104 a3 3 0 1 0 0.1 0 M174 98 a3 3 0 1 0 0.1 0" stroke-width="1.4"/>
 <path d="M18 128 H182" stroke-width="1.6"/>
</g>""")

# Cookies on a plate
ILLOS['cookies'] = wrap(f"""
<g {S}>
 <path d="M30 108 Q100 124 170 108 Q170 116 100 118 Q30 116 30 108z"/>
 <circle cx="62" cy="88" r="17"/><circle cx="100" cy="84" r="19"/><circle cx="140" cy="88" r="17"/>
 <path d="M56 82 h1 M68 86 h1 M60 94 h1 M94 78 h1 M106 84 h1 M98 92 h1 M134 82 h1 M146 86 h1 M138 94 h1" stroke-width="3.4"/>
 <path d="M18 128 H182" stroke-width="1.6"/>
</g>""")

# Platter with cheese ball & crackers
ILLOS['platter'] = wrap(f"""
<g {S}>
 <path d="M20 100 Q100 78 180 100 Q100 122 20 100z"/>
 <path d="M30 100 Q100 84 170 100" stroke-width="1.3"/>
 <circle cx="70" cy="82" r="17"/>
 <path d="M62 76 h1 M76 74 h1 M78 88 h1 M64 90 h1 M70 82 h1" stroke-width="3"/>
 <circle cx="112" cy="94" r="9" stroke-width="1.6"/><circle cx="132" cy="90" r="9" stroke-width="1.6"/><circle cx="150" cy="96" r="9" stroke-width="1.6"/>
 <path d="M109 91 h1 M115 96 h1 M129 87 h1 M135 92 h1 M147 93 h1 M153 98 h1" stroke-width="2.4"/>
 <path d="M18 128 H182" stroke-width="1.6"/>
</g>""")
