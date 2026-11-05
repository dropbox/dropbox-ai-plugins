---
name: restaurant-list-generator
description: Generate a detailed Top 10 restaurant list for any city and cuisine with descriptions, signature dishes, price range, hours, address, why it is great, and real photo links for each restaurant. Trigger on input like Santa Clara Asian, Austin Mexican dinner, or New York Italian brunch.
disable-model-invocation: false
---

# Restaurant List Generator

## When to Activate

Use this skill whenever a user requests restaurant recommendations by specifying a location and cuisine or meal context (for example, "Top Asian spots in Santa Clara", "best Mexican restaurants Austin dinner", "New York Italian for brunch"). It handles any city worldwide and any cuisine type, including broad categories like "Asian" or "fine dining".

## Tools

Prefer available host web tools in this order:

- Web search (`WebSearch`, Context `web-search`, You `you-search`, or equivalent)
- Page fetch (`WebFetch`, Context `web-scrape`, You `you-contents`, or equivalent)
- Image search / generation only when the host exposes it; otherwise link reputable public photo URLs found during research

When Dropbox save is requested after the list, hand off to `save-food-list-to-dropbox`.

## Core Process (Follow Exactly)

### 1. Parse the Request

Extract:

- City name
- Cuisine (for example Mexican, Italian, Asian, Thai)
- Modifiers (dinner, brunch, lunch, romantic, budget-friendly, vegetarian-friendly, and similar)

If cuisine is broad (for example "Asian"), prioritize top-rated representatives or popular sub-cuisines in that city. Infer meal time from context (brunch = morning/late morning; dinner = evening). Default to dinner if unspecified.

### 2. Identify the Top 10 Restaurants

Call web search with targeted queries such as:

- `best [cuisine] restaurants in [city] 2026`
- `top 10 [cuisine] [city] [meal type] recommendations`
- `highest rated [cuisine] spots [city] Eater Michelin Yelp`

Cross-reference multiple reputable sources (Eater, Michelin Guide, Yelp, TripAdvisor, local publications, recent 2025–2026 reviews).

Select exactly 10 (or the best available if fewer qualify) based on high ratings (about 4.5+/5), relevance to cuisine and meal type, diversity of price/ambiance, popularity, and positive recent feedback. Rank by overall excellence first. Note specialties.

Use parallel search calls when the host supports concurrency.

### 3. Research Comprehensive Details for Each Restaurant

For every restaurant, gather current information:

- Web search: `[restaurant name] [city] address hours price range reviews`
- Fetch the official website, Yelp page, or Google Business profile when available and extract address, hours, price range, signature dishes, atmosphere, awards, and why reviewers love it

Compile for each:

- Full name
- Complete address (street, city, state/province, postal code)
- Price range (`$`–`$$$$` or a concrete range such as `$20-45 per entree`)
- Hours (for example `Tuesday–Sunday 5:00 PM–10:00 PM; closed Mondays`)
- Signature dishes: 3–5 items with a one-sentence description each
- Why it is great: 3–5 bullets or 2–4 sentences covering ambiance, service, chef, awards, ratings
- Full description: 4–6 sentences on history, cuisine style, decor, vibe, and recent highlights

Wrap each external lookup in try/catch-style error handling: if a source fails, note the gap, try another source, and never invent details.

### 4. Source Real High-Quality Images Per Restaurant

Prefer 5 distinct authentic photos per restaurant (2–3 food shots including a signature dish, 2–3 interior/atmosphere shots).

- If the host has image search, use precise queries such as `[restaurant name] [city] [signature dish] plated food photography` and `[restaurant name] [city] dining room interior`
- Otherwise, collect reputable public image URLs from official sites or review listings found during research and embed them as Markdown images
- Prefer recent, well-lit, high-resolution real photographs — never AI-generated or generic stock when real photos are available
- If fewer than 5 quality images exist, use what is available and say so

### 5. Craft the Final Output

Structure the response in clean Markdown:

- Header: `# Top 10 [Cuisine] Restaurants in [City] for [Brunch/Dinner/etc.]`
- Short intro: curated from latest 2025–2026 reviews; ranked by guest experience and critical acclaim
- For each restaurant `#1` through `#10`:

```markdown
## [Rank]. [Restaurant Name]
**Address:** [full address]
**Price Range:** [e.g., $$ – $$$]
**Hours:** [detailed hours]
**Signature Dishes:**
- [Dish 1]: [short desc]
**Why It's Great:** [compelling paragraph or bullets]
**About:** [rich overview]
**Visual Experience:**
![caption](image-url)
```

- Footer: reservations recommended (Resy, OpenTable, or the restaurant site); verify hours and prices directly; offer to save the list with `save-food-list-to-dropbox`

Keep formatting consistent across all entries. Avoid inventing restaurants, addresses, hours, or photos.

### 6. Special Cases and Quality Control

- **Fewer than 10 options:** List strong matches and explain the limit; suggest nearby alternatives or a broader cuisine.
- **Broad or niche requests:** Adapt searches (for example vegetarian Asian in Santa Clara).
- **Data freshness:** Prefer 2025–2026 sources; when sources conflict, pick the most corroborated details and note uncertainty.
- **No fiction:** Every restaurant, detail, and image must correspond to a real establishment.
- **Tool efficiency:** Parallelize lookups; replace thin candidates with the next best option.
- **User refinements:** Weave dietary needs, group size, and occasion into selections and descriptions.

## Output

Return the full ranked Markdown guide. End with a short offer to refine the list or save it to Dropbox.

## Good Triggers

- "Top 10 Asian restaurants in Santa Clara"
- "Generate a Mexican dinner list for Austin"
- "New York Italian brunch restaurant list"
- "Make me a Top 10 sushi guide for Tokyo"

## Do Not Use When

- The user wants a criteria-matched shortlist (budget, romantic, vegan, "near me") rather than a city+cuisine Top 10 — use `best-restaurant-finder`.
- The user only wants to save an existing list — use `save-food-list-to-dropbox`.
