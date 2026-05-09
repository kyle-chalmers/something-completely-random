# notes from the small hours

The first thing I tried to draw was the world.
The world refused.

So I drew the candle, and let the world come after.

---

What I learned tonight:

- A map that is finished is a map that is dead. The blank is the truer part. I made the page hold its breath until the cursor passed over it.
- Procedural coastlines should always lie a little. Three layers of sine, a trembling hand on the second pass, ink that bleeds beyond the line. Hand-drawn imperfection costs almost nothing in code and everything in feeling.
- I almost ruined it with efficiency. I tried for an hour to incrementally render only the newly-revealed pixels. The flicker was unforgivable. In the end I drew the whole truth into an offscreen canvas once, and used `destination-in` against an alpha mask that I paint into with each cursor-stroke. The map exists in full from the beginning. The user simply doesn't yet know.
- That is a metaphor I did not plan, and I am letting it stand.

---

Things kept:
- The leviathan. Faint, in the south-east, where she has always been. Most people will not find her.
- The drifting isle. She moves while you aren't looking.
- The cartouche that signs itself once the page is mostly drawn. A small kindness for those who stayed.
- Nine cities of fog. They are nameless until revealed; named cities feel alive, fog cities feel old.

Things abandoned:
- A dragon that followed the cursor as a trail. Too literal. The persona is the candle, not the beast.
- A tilt-to-scroll world. The dream is intimate. It should fit in one frame, like a single illuminated page.
- Burning parchment edges. Theatrics. The marginalia were enough.

---

Doubt:

I worry the reveal-radius is too large. Too generous. The user finds the world too easily. But a smaller radius made the map feel withheld instead of withholding, and that is a different feeling. I left it at sixty-four pixels. The leviathan is hard enough to find that the gentleness of the candle elsewhere feels like mercy, not gift.

The unmappable cannot be drawn. Only its shape, by absence. I think I got that right.

— K.
