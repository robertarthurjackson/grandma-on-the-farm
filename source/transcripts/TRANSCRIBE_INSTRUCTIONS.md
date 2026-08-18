# Transcription task

You are transcribing photographs of handwritten recipe cards from a late grandmother's recipe box ("Grandma Harris", known to the family as "Grandma on the Farm"). The photos are in
`/private/tmp/claude-501/-Users-RobRoth-projects-grandma-cooking/ac6eeaec-944b-4fff-8b2a-27efd50fc85c/scratchpad/photos/NNN.jpg` (NNN is a zero-padded 3-digit number, 000–633).

Photos are in album order, which is the order the cards were photographed. IMPORTANT: many cards were photographed front and then back, so a photo is often a CONTINUATION of the previous photo (the text starts mid-sentence, e.g. "add a little warm H2O to make meat soft" or "Bake @ 350° for 35–40 min"). Some photos contain two or three small cards or clippings at once. Some are non-recipe (children's crafts, household/cleaning tips, home remedies, notes, lists of names, a photo of the recipe box itself). Some are newspaper/magazine clippings.

## Your range
Read EVERY photo in your assigned range with the Read tool, one at a time (you may read several per turn). Look carefully — read the whole card, including margins and anything written sideways. Also read the ONE photo just before your range (if it exists) so you can tell whether your first photo continues it, and the ONE photo just after your range so you can tell whether your last photo continues onto it. Do not transcribe those two context photos.

## Output
Write ONE JSON file: the path given in your task. It must be a JSON array with one object per photo in your range (in order), each with exactly these keys:

- "photo": integer photo number
- "kind": one of "recipe" (a recipe or the start of one), "continuation" (this photo continues the previous photo's card), "non-recipe" (crafts, cleaning tips, remedies, notes, name lists, etc.), "clipping" (printed newspaper/magazine/package recipe), "photo-of-box" (a photo of the recipe box/cards not text), "blank-or-unreadable"
- "title": the recipe/card title as written (null if none). If a continuation, repeat the title of the card it continues if you can tell, else null.
- "attribution": who the recipe is from if written on the card, e.g. "Jean Lavender", "Margaret F.", "Mrs. Joe Harris" (null if none)
- "category": your best guess, one of: "Breads & Buns", "Breakfast", "Soups & Salads", "Main Dishes", "Vegetables & Sides", "Cookies & Bars", "Cakes & Frostings", "Pies & Pastry", "Desserts & Sweets", "Candy & Treats", "Preserves, Pickles & Sauces", "Beverages", "Kids' Crafts & Fun", "Household Hints & Remedies", "Other". Use null for continuation photos.
- "ingredients": array of strings, one per ingredient line, transcribed as written but with quantity first if that reads naturally, e.g. "1 c + 2 tbsp warm water", "2 tbsp margarine". If the card has multiple sub-sections (e.g. "Cinnamon paste:"), include a header string like "— Cinnamon paste —" before those lines. Empty array if none.
- "directions": array of strings, one per step/sentence group, transcribed faithfully in Grandma's own words (keep her voice, abbreviations like V.G., "H2O", "oleo", pan sizes, temps). Empty array if none.
- "notes": array of strings for marginalia, cross-references ("see back", "over"), ratings ("V.G."), dates, who liked it, yield, etc.
- "continues_from_previous": true/false
- "continues_to_next": true/false (the card clearly runs off the end / says "over" / next photo continues it)
- "multiple_cards": true if the photo shows more than one separate card/recipe (in that case put ALL recipes' text in the fields, separated by a header line "=== Second card: <title> ===" etc. in ingredients/directions, and list all titles in title separated by " / ")
- "raw_text": a faithful line-by-line transcription of everything on the photo (use "\n" for line breaks). Mark words you can't read as [?] and uncertain readings as [word?].
- "confidence": "high", "medium", or "low"

Do not invent ingredients or steps that aren't on the card. Do not "improve" recipes. Preserve unusual spellings only if they're clearly intentional; otherwise use normal spelling. Fractions: write as "1/2", "1 1/2", "3/4".

Return, as your final message, only a 2–3 line summary: how many photos, how many recipes/continuations/non-recipes, and any photos you found genuinely unreadable. Do NOT paste the JSON into the message. Make sure the JSON file is valid (verify with `python3 -c "import json;json.load(open('...'))"`).
