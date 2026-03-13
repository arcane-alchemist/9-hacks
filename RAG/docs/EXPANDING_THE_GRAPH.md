# How to Expand the Statute Graph

The beauty of hand-coded relationships is that adding new connections is a 30-second task.

## Adding a New Statute Chunk

### 1. Create the .txt file

```
e:\Sidelines\RAG\statutes\your_new_statute.txt
```

With content:
```
YOUR ACT NAME, YEAR

Section X: Your Section Title
[Content of statute section - max 300 words]
```

### 2. Add to statute_graph.json

Edit `data/statute_graph.json` and add your statute to `statute_relationships`:

```json
{
  "statute_relationships": {
    ...existing statutes...,
    "your_new_statute_section_x": {
      "title": "Your Act Name - Section X: Your Section Title",
      "related": [
        "existing_statute_1",
        "existing_statute_2"
      ],
      "process_flow": ["step1", "step2"],
      "remedy_type": "labour_complaint|criminal_complaint|protection_order|information_request|legal_aid",
      "next_step": "file_with_authority"
    }
  }
}
```

### 3. Update the domain map (if new type)

If this statue covers a new domain, add it to `domain_statute_map`:

```json
{
  "domain_statute_map": {
    "your_new_domain": ["your_new_statute_section_x"],
    ...
  }
}
```

### 4. Update process flows (if new procedure)

If this creates a new legal procedure, add to `process_flows`:

```json
{
  "process_flows": {
    "your_new_process": {
      "steps": ["statute1", "statute2", "statute3"],
      "description": "What the user should do",
      "timeline": "How long it takes"
    }
  }
}
```

## Example: Adding Labour Law Amendments

Let's say you want to add Industrial Disputes Act, 1947 Section 25U (termination rules):

### File: `statutes/industrial_disputes_section_25u.txt`
```
INDUSTRIAL DISPUTES ACT, 1947

Section 25U: Conditions for Retrenchment
[Add statute text...]
```

### Update `data/statute_graph.json`:
```json
{
  "statute_relationships": {
    "industrial_disputes_section_25u": {
      "title": "Industrial Disputes Act 1947 - Section 25U: Conditions for Retrenchment",
      "related": [
        "payment_of_wages_section_5",
        "payment_of_wages_section_15",
        "minimum_wages_section_3",
        "nalsa_scheme"
      ],
      "process_flow": ["industrial_disputes_section_25u", "payment_of_wages_section_15"],
      "remedy_type": "labour_complaint",
      "next_step": "file_with_labour_tribunal"
    },
    "payment_of_wages_section_5": {
      "title": "...",
      "related": [
        "payment_of_wages_section_15",
        "minimum_wages_section_3",
        "industrial_disputes_section_25u"  // ADD THIS LINE
      ],
      ...
    }
  }
}
```

Now when a user asks about termination:
1. Similarity search finds `industrial_disputes_section_25u`
2. Graph expansion adds `payment_of_wages_*`, `minimum_wages_*`, `nalsa_scheme`
3. Gemini sees all related labour provisions

## Batch Adding Multiple Statutes

If adding 5-10 statutes at once, here's the pattern:

### 1. Identify relationships between new statutes
```
Looking at SC/ST Atrocities Act amendments...

- Atrocities Act Section 3 → enforcement, penalties
- Atrocities Act Section 14 → procedure
- Atrocities Act Section 15 → bail conditions

Relationships:
- Sec 3 → Sec 14, Sec 15, nalsa_scheme
- Sec 14 → Sec 3, Sec 15
- Sec 15 → Sec 3, Sec 14
```

### 2. Create all .txt files first
```
statutes/atrocities_act_section_14.txt
statutes/atrocities_act_section_15.txt
```

### 3. Update statute_graph.json with all nodes and edges
```json
{
  "statute_relationships": {
    "atrocities_act_section_3": {
      "title": "...",
      "related": [
        "atrocities_act_section_14",
        "atrocities_act_section_15",
        "nalsa_scheme"
      ],
      ...
    },
    "atrocities_act_section_14": {
      "title": "...",
      "related": [
        "atrocities_act_section_3",
        "atrocities_act_section_15"
      ],
      ...
    },
    "atrocities_act_section_15": {
      "title": "...",
      "related": [
        "atrocities_act_section_3",
        "atrocities_act_section_14"
      ],
      ...
    }
  }
}
```

### 4. Update domain map
```json
{
  "domain_statute_map": {
    "scst": [
      "atrocities_act_section_3",
      "atrocities_act_section_14",
      "atrocities_act_section_15"
    ]
  }
}
```

### 5. Test with `test_graph_expansion.py`
```bash
python test_graph_expansion.py

# You should see:
# ✓ Loaded statute relationship graph with X nodes
# Graph should show your new statutes in expansions
```

## Relationship Design Principles

When adding relationships, follow these rules:

### ✅ DO Add Related Edges For:

1. **Procedural flow**: Section 3 → Section 12 (problem → remedy)
2. **Legal interaction**: DV Act + IPC (same case filed under multiple laws)
3. **Precedent/override**: When one law takes precedence over another
4. **Appeal path**: Lower court law → Appeal court law
5. **Enforcement**: Substantive law → Enforcement/penalty law
6. **Cross-domain**: NALSA applies to all domains

### ❌ DON'T Add Random Edges For:

- Statutes that coincidentally mention the same word
- Outdated versions (keep only current law)
- Related but too distant (e.g., don't link DV Act to Traffic Act)

### 📏 Keep Related Lists Reasonable

- 2-5 edges per node is ideal
- Max 7-8 edges (too many dilutes context)
- If you have 10+ related items, you probably need to group them

## Validation Checklist

After adding new statutes:

```
☐ Created .txt file in statutes/ directory
☐ Added node to statute_graph.json["statute_relationships"]
☐ Set title, related[], process_flow[], remedy_type
☐ Updated domain_statute_map if new domain
☐ Updated process_flows if new procedure
☐ Verified no orphaned statutes (should have ≥1 connection)
☐ Tested with: python test_graph_expansion.py
☐ Tested with: python main.py + query endpoint
```

## Git Workflow

When growing the graph:

```bash
# Branch for new statute additions
git checkout -b add/industrial-disputes-law

# Add statute text file
# Update statute_graph.json
# Test locally

git add statutes/industrial_disputes_*.txt data/statute_graph.json
git commit -m "Add Industrial Disputes Act Sections 25U, 25F regarding retrenchment"

git push origin add/industrial-disputes-law
# Create pull request, review, merge
```

## Performance Impact

Adding statutes to the graph has NO performance impact:

- **Indexing**: +1 second per new statute (loads new .txt file at startup)
- **Query time**: Same (~40ms retrieval). Graph expansion is O(n) but n ≤ 8
- **Memory**: +500KB per statute (text + embedding)

You can safely scale to 100+ statutes with negligible performance change.

## Example: Full Cycle

Let's walk through adding a new statute:

### Step 1: Create statute file
```
statutes/maternity_benefit_act_section_5.txt
```

### Step 2: Add to graph
```json
"maternity_benefit_act_section_5": {
  "title": "Maternity Benefit Act 1961 - Section 5: Entitlement to Maternity Benefit",
  "related": [
    "payment_of_wages_section_5",
    "labour_laws_general",
    "nalsa_scheme"
  ],
  "process_flow": ["maternity_benefit_act_section_5"],
  "remedy_type": "labour_complaint",
  "next_step": "apply_with_employer"
}
```

### Step 3: Test
```bash
python test_graph_expansion.py

# Output should show:
# ✓ Loaded statute relationship graph with 12 nodes  (11 + 1 new)
```

### Step 4: Query
```bash
python main.py

# Test: "Pregnancy ke baad mujhe naukri se nikaal diya"
# Should return maternity benefit act + related labour statutes
```

Done! System automatically discovered and contextualized the new statute via relationships.

## When to Refactor the Graph

After reaching 50+ statutes, consider:

1. **Grouping by Act**: Instead of individual sections, group sections of the same Act
2. **Hierarchy**: Use `"parent"` field to organize sections under Acts
3. **Tags**: Add `"tags": ["labour_standard", "worker_protection"]` for better filtering

But for now (5-30 statutes), flat structure is perfect.

---

**Key Principle**: The statute graph IS your legal knowledge base. Growing it is as simple as writing JSON.
