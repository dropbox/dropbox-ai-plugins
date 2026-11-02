---
name: best-restaurant-finder
description: Find the best restaurants matching location, cuisine, dietary needs, ambiance, occasion, or meal preferences with detailed descriptions, signature dishes, price range, hours, address, why it is great, and real photo links. Trigger on queries like best sushi in Santa Clara, romantic dinner Los Angeles, or top vegan spots New York.
disable-model-invocation: false
---

# Best Restaurant Finder

## When to Activate

Activate whenever the user asks for restaurant recommendations, the "best" spots, or matches for specific criteria (cuisine, location, budget, dietary restrictions, ambiance, occasion, meal type, group size, and similar). Handles broad queries ("best Asian food LA"), targeted ones ("romantic Italian dinner under $80 in Santa Clara"), single "the best" picks, and "near me" requests. Works for any city worldwide.

## Tools

Prefer available host web tools in this order:

- Web search (`WebSearch`, Context `web-search`, You `you-search`, or equivalent)
- Page fetch (`WebFetch`, Context `web-scrape`, You `you-contents`, or equivalent)
- Image search only when the host exposes it; otherwise Markdown-link reputable public photo URLs

When Dropbox save is requested after recommendations, hand off to `save-food-list-to-dropbox`.

## Core Process (Follow Exactly)

### 1. Parse the Request

Extract:

- Location (city/neighborhood; if "near me" or unspecified, default to Gardena / Santa Clara CA and say so)
- Cuisine or food type
- Number of recommendations (default 5–8; fewer for very specific criteria or "the best one")
- Modifiers (romantic, budget-friendly, vegan/gluten-free, family-friendly, fine dining, late-night, patio/ocean view, and similar)
- Meal or occasion context

Infer sensible defaults (for example dinner if unspecified).

### 2. Research the Best Matches

Use targeted web searches:

- `best [cuisine] restaurants [location] 2026`
- `top rated [cuisine] [location] [preferences] Yelp Eater Michelin`
- `[specific criteria] restaurants [location] recommendations`

Cross-reference Eater, Michelin, Yelp, Google, TripAdvisor, and local 2025–2026 reviews. Select the strongest 3–10 real restaurants that match **all** criteria (ratings about 4.5+, relevance, recent positive feedback, diversity where appropriate). Rank by overall fit. Parallelize searches when possible.

### 3. Gather Comprehensive Details for Each Restaurant

For every selected restaurant:

- Web search: `[restaurant name] [location] address hours price signature dishes reviews`
- Fetch official site, Yelp, or Google Business profile when available

Compile:

- Full name
- Complete address
- Price range (`$`–`$$$$` or a per-person estimate)
- Hours (current/recent)
- 3–5 signature dishes with one-sentence descriptions
- Why it is great (3–5 bullets or a paragraph tailored to the user criteria)
- Full description (4–6 sentences: cuisine style, history, decor, vibe, standouts)

If a lookup fails, report the failure path/URL, try another source, and do not invent missing facts.

### 4. Source Real High-Quality Images Per Restaurant

Aim for 5 distinct authentic photos (2–3 food close-ups including signature dishes + 2–3 interior/exterior/atmosphere shots).

- Image search queries when available: `[restaurant name] [location] [signature dish] plated food photography`, `[restaurant name] [location] dining room interior`
- Otherwise embed reputable public image URLs found during research
- Prefer recent real photographs — never AI-generated or stock when real photos exist
- If fewer than 5 quality images exist, use what is available and note it

### 5. Craft the Final Output

```markdown
# Best [Cuisine/Style] Restaurants in [Location] for [Occasion/Preferences]

Short intro tailored to the criteria.

## [Rank]. [Restaurant Name]
**Address:** ...
**Price Range:** ...
**Hours:** ...
**Signature Dishes:**
- ...
**Why It's Great:** ...
**About:** ...
**Visual Experience:**
![caption](image-url)
```

Footer: reservations recommended; verify details directly; offer Dropbox save via `save-food-list-to-dropbox`.

### 6. Special Cases and Quality Control

- **Fewer options than requested:** List strong matches, explain the limit, suggest broadening criteria or nearby alternatives.
- **"Near me" or vague location:** Default to Gardena / Santa Clara CA and note it; offer to refine.
- **Very specific niche requests:** Weave every constraint into selections and descriptions.
- **Single "the best" request:** Focus on top 1–3 with extra depth.
- **Data freshness and realism:** Prefer 2025–2026 sources; only real, currently operating establishments; when sources conflict, prefer corroborated details and note uncertainty.
- **Tool efficiency:** Parallelize lookups; replace thin candidates.
- **User refinements:** Update selections when follow-ups add constraints.

## Output

Return the curated Markdown recommendations ranked by fit. End with an offer to refine or save to Dropbox.

## Good Triggers

- "Best sushi in Santa Clara"
- "Romantic dinner in Los Angeles under $100"
- "Top vegan spots in New York"
- "Highest rated steakhouse near me"
- "Find the best Italian for a family dinner in Austin"

## Do Not Use When

- The user explicitly wants a city+cuisine **Top 10 list** generator format — use `restaurant-list-generator`.
- The user only wants to save an existing list — use `save-food-list-to-dropbox`.
