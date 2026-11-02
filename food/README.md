# Food Mission Cursor Plugin

Unified Cursor plugin for the food project. It merges the Grok restaurant skills into one local plugin and adds Dropbox save support.

## Skills

| Skill | Purpose |
| --- | --- |
| `restaurant-list-generator` | Build a Top 10 restaurant list for a city + cuisine with details and photo links |
| `best-restaurant-finder` | Find the best restaurants for any mix of location, cuisine, diet, budget, ambiance, or occasion |
| `save-food-list-to-dropbox` | Save a curated Markdown food/restaurant list to Dropbox after confirmation |

## Install (local Cursor plugin)

```bash
mkdir -p ~/.cursor/plugins/local
rm -rf ~/.cursor/plugins/local/food-mission
cp -a food ~/.cursor/plugins/local/food-mission
```

Then reload Cursor plugins / restart the agent session so `food-mission` appears under local plugins.

## Usage examples

**Top 10 list**

> Generate a Top 10 Asian restaurants list for Santa Clara dinner

**Best-match finder**

> Best romantic Italian dinner under $80 in Santa Clara

**Save to Dropbox**

> Save this restaurant list to Dropbox under `/06_AI_Notes/Food_Mission/`

The save skill confirms destination path and filename before calling Dropbox `create_file`.

## Inputs / outputs

### `restaurant-list-generator`

- **Inputs:** city, cuisine, optional meal/modifiers
- **Outputs:** ranked Markdown Top 10 with address, price, hours, dishes, why-great, about, and visuals
- **Tools:** host web search + page fetch; image URLs when available

### `best-restaurant-finder`

- **Inputs:** location (defaults Gardena/Santa Clara CA for "near me"), criteria, count
- **Outputs:** ranked Markdown shortlist tailored to the criteria
- **Tools:** host web search + page fetch; image URLs when available

### `save-food-list-to-dropbox`

- **Inputs:** Markdown list content, optional Dropbox folder/filename
- **Outputs:** created Dropbox path, file ID, optional open-in-Dropbox link
- **Tools:** Dropbox MCP `create_file`, `create_folder`, `list_folder`, `search`, `get_file_metadata`, `file_preview`
- **Default folder:** `/06_AI_Notes/Food_Mission/`

## Relationship to Dropbox AI plugins

This package lives under `food/` and is **not** part of the public Dropbox MCP Host marketplace package (`cursor/`, `claude/`, `codex/`, `antigravity/`). It is a personal/local food-mission plugin that can use the Dropbox MCP connection when saving lists.

## Version

1.0.0
