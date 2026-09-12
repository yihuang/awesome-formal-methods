# References and citation conventions

This wiki makes factual claims about real systems, real papers, and real numbers. Every one of them
should be traceable. This page defines how.

---

## The three-layer system

| Layer | Where | Purpose |
|---|---|---|
| **1. Inline link** | in the sentence that makes the claim | the claim and its source are inseparable |
| **2. Page references** | a `## References` section at the end of the page | the complete source list for that page, with enough detail to find it offline |
| **3. Master bibliography** | [bibliography.md](bibliography.md) | the catalogue, grouped by topic, with the highest-value items starred |

**Rule 1: every claim that could be wrong gets an inline link.** If a sentence contains a number, a
date, a quotation, or an attribution, link it at the point of use. A reader should be able to check
any specific claim without reading the whole page.

**Rule 2: every page ends with `## References`.** List the sources the page actually relies on — not
everything tangentially related. If a page has no references, that is a red flag about the page, and
[`tools/check-refs.py`](https://github.com/yihuang/awesome-formal-methods/blob/main/tools/check-refs.py) will say so.

**Rule 3: prefer primary sources.** The paper, not the blog post about the paper. The project's own
repository, not a summary. Where only secondary sources exist, say so.

---

## What to cite, by claim type

| Claim type | Cite |
|---|---|
| A number (scale, cost, line count) | the project's own report or paper, with the date — **and flag it if you can't verify it** |
| A quotation | the original document, linked, with enough context to find the passage |
| A technique's origin | the original paper (Plotkin 1981, Hoare 1969, Cousot & Cousot 1977, …) |
| A tool's capabilities | the tool's own documentation or repository |
| An industry practice | a first-party experience report (e.g. AWS's TLA+ paper), not a vendor blog |
| A historical event | the contemporaneous record, or a standard reference work |

---

## Confidence marking

The wiki distinguishes *cited* from *verified*. Because some claims come from vendor material,
secondary reporting, or a single source, they carry inline flags:

| Marker | Meaning |
|---|---|
| *(no marker)* | sourced to a primary document that was read directly |
| `⚠️` | needs verification before you rely on it — vendor-published, secondary-source, or single-source |
| `~` before a number | order-of-magnitude, not an exact figure |

Every `⚠️` in the wiki is also collected, with an explanation, in the
[confidence ledger](../research-notes.md#4-confidence-ledger). That ledger is the authoritative list;
if you find a claim flagged `⚠️` somewhere with no entry there, that is a bug worth reporting.

**Why mark anything at all?** Because a wiki that states an unverified vendor number with the same
confidence as a machine-checked theorem is worse than useless — it launders uncertainty into
authority. The whole point of formal methods is knowing precisely what is established and what is
assumed. The bibliography should hold itself to the same standard.

---

## Citing this wiki

Prose here is licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); see the
[repository README](https://github.com/yihuang/awesome-formal-methods#license).

When you reuse a specific figure, **cite the primary source rather than this wiki** — the inline
link is right there, and the primary source is the one that carries authority. Cite this wiki for
the synthesis, the framing, and the tooling; cite the paper for the number.

---

## Maintaining references

- [`tools/check-links.py`](https://github.com/yihuang/awesome-formal-methods/blob/main/tools/check-links.py) — internal links resolve
- [`tools/check-site.py`](https://github.com/yihuang/awesome-formal-methods/blob/main/tools/check-site.py) — links in the built site resolve
- [`tools/check-refs.py`](https://github.com/yihuang/awesome-formal-methods/blob/main/tools/check-refs.py) — every page has a `## References` section,
  reference entries are non-empty and linked, and the wiki's reference density is reported

None of these check whether an *external* URL still works — link rot is real, and external hosts
are not reliable enough to gate a build on. If you find a dead link, replace it with an archived
copy or the DOI.

---

## References

This page describes a convention rather than a set of claims, but the convention itself follows
established practice:

- The three-layer split (inline → page → master) is the standard structure of reference
  documentation in technical writing; see e.g. the *Chicago Manual of Style* on notes versus
  bibliography, and the [Diátaxis](https://diataxis.fr/) framing of reference as a distinct
  documentation type.
- The confidence-marking scheme deliberately mirrors what formal methods already does with
  assumptions and trusted bases — see [limits.md § The trusted base](../01-fundamentals/limits.md#the-trusted-base).
