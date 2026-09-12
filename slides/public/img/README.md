# Optional portraits

**The deck does not need these.** Every visual in `slides.md` is authored SVG, CSS, or typography, so
the deck renders completely — and identically offline — with this directory empty. That is
deliberate: a broken image in a live talk is worse than no image.

Drop files here to add portraits to the "heroes of the fundamentals" slides. Slidev serves this
directory at `/img/`, so a file named `turing.jpg` is referenced as:

```markdown
<img src="/img/turing.jpg" class="portrait" alt="Alan Turing" />
```

## Suggested set

Chosen to match the deck's philosophical arc — each one owns a beat in the talk:

| File | Person | The beat they carry |
|---|---|---|
| `lovelace.jpg` | Ada Lovelace | the opening: "the engine can only do what we order it to" |
| `godel.jpg` | Kurt Gödel | 1931 — incompleteness |
| `turing.jpg` | Alan Turing | 1936 — undecidability, and the 1949 program-correctness paper |
| `hoare.jpg` | Tony Hoare | 1969 — the triple; also the humblest famous apology in CS |
| `dijkstra.jpg` | Edsger Dijkstra | weakest preconditions; "testing shows the presence, not the absence, of bugs" |
| `lamport.jpg` | Leslie Lamport | TLA+, and stuttering invariance |
| `liskov.jpg` | Barbara Liskov | abstraction, and why specifications outlive implementations |

## Getting them

Use Wikimedia Commons images — they are freely licensed, but **check the licence and record the
attribution** for each file you add.

```bash
# one at a time, with a pause: Commons rate-limits aggressively
curl -L -H 'User-Agent: your-talk-slides/1.0' -o turing.jpg \
  'https://commons.wikimedia.org/wiki/Special:FilePath/Alan_turing_header.jpg'
```

The thumbnail service gives small files, which is what you want for a deck:

```
https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/Alan_turing_header.jpg/520px-Alan_turing_header.jpg
```

## Attribution

Record the source and licence of anything you add, here:

| File | Source | Licence |
|---|---|---|
| *(none yet)* | | |

**Note from the wiki's author:** fetching these was attempted while building the deck and abandoned —
the environment was rate-limited to roughly one Commons request per session, and no other image host
was a reliable substitute. The deck was therefore designed to be complete without them. If you do add
portraits, add the licence rows above in the same commit.
