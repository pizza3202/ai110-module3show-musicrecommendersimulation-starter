# 🎧 Model Card: Music Recommender Simulation

## 1. Model name

**VibeFinder 1.0** (also called **Catalog Vibe Scorer** in the repo—a small, explainable classroom recommender.)

---

## 2. Goal / task

The model **predicts which songs in a fixed list best match a listener sketch** and returns a **ranked short list** (for example the top five). It does not predict whether someone will press play in real life; it only **scores and sorts** rows from a CSV using tags and a few numeric “audio style” fields.

---

## 3. Data used

The data file is **`data/songs.csv`** with **18 songs**. Each song has **title**, **artist**, **genre**, **mood**, **energy** (about 0–1), **tempo_bpm**, **valence**, **danceability**, and **acousticness**. Genres include pop, lofi, rock, jazz, edm, metal, and others; moods include happy, chill, intense, moody, and more.

The set is **tiny and hand-built** for teaching. It is **not** balanced like real streaming data, and it **does not** include lyrics, language, charts, listening history, or social context. Any conclusion about “all music” would overreach.

---

## 4. Algorithm summary (plain language)

Each song starts at zero points. If the user’s **genre** word matches the song’s genre tag, the song gets a **larger** bonus than a **mood** match. **Energy** works differently: the song gets more points when its energy number is **close** to the user’s target, not simply when it is “louder.” **Acousticness** adds a small tilt toward either **acoustic** or **produced** tracks, depending on a yes/no switch. Optional targets (like valence or tempo) can add more “closeness” points if the user supplies them.

After every song has a total score, the program **sorts** from highest to lowest and reads off the top slots. The printed **reason lines** are the same ingredients added up, so you can see why one row beat another without reading code.

---

## 5. Observed behavior / biases

During CLI stress tests, the system behaved like a **strict librarian**: if the spreadsheet does not contain your exact mood word inside your genre, the big mood bonus often **never turns on**, and loud rows with the right genre can float up anyway—**Gym Hero** appeared first for a **“moody pop + very high energy”** profile even though that track is tagged **intense**, not moody, because there is almost no **pop + moody** inventory.

That creates a **filter-bubble** feeling: you mostly see what the tags allow. **Genre is weighted above mood**, so listeners who care more about vibe than genre may still see genre-first results. **Numeric energy** can also feel “right” on paper but wrong in the ears, because closeness on a scale is not the same as emotional fit.

---

## 6. Evaluation process

Evaluation mixed **automation** and **manual runs**. `pytest` checks a two-song toy case so the ranking logic does not silently regress. For the real catalog, **`python -m src.main`** ran **four taste profiles** (high-energy pop, chill lofi, intense rock, and a deliberately awkward edge case) and printed **top five** lists with **scores and reason bullets**. A **weight experiment** (double energy importance, half genre importance) was run on the same pop profile to see whether the order changed in an explainable way. Notes comparing profiles live in **`reflection.md`**.

---

## 7. Intended use and non-intended use

**Intended:** learning how **user fields → scores → ranked list** works, practicing documentation, and discussing **bias and transparency** in a controlled sandbox.

**Not intended:** real product recommendations, medical or mood “diagnosis,” fairness claims about artists or cultures, or use with private or large-scale user data. It should not be mistaken for Spotify-, YouTube-, or Apple-scale personalization.

---

## 8. Ideas for improvement

1. **Softer matching** for genre and mood (synonyms, hierarchies, or partial credit) so rare combos do not collapse to a single loud default.  
2. A **diversity rule** so the top five are not almost the same sub-genre when scores tie closely.  
3. A **tiny feedback loop** (thumbs up/down) stored in a file to show how real systems update—still small, but closer to practice.

---

## 9. Personal reflection

**Biggest learning moment:** seeing the **edge-case profile** return a plausible-but-wrong “mood” winner drove home that **missing data reads as preference** if you are not careful. The math was honest; the catalog was not complete for that ask.

**AI tools:** they sped up **boilerplate** (CSV loading, sorting, wording drafts) and suggested **edge profiles** I might have skipped. I still had to **verify** weights against the README recipe, re-run the CLI after each change, and catch places where a suggestion would have **broken tests** or overstated what the CSV contains.

**Surprise:** even a **handful of if-then-style rules** can produce an ordered list that **feels** like a recommendation feed, because humans also lean on shortcuts (“same genre, same mood”). The “magic” was mostly **transparent arithmetic**, which is both reassuring and a little deflating.

**Next if I extended this:** I would prototype **one** soft-mood or synonym layer and measure whether the **moody pop** style edge case stops defaulting to **intense** gym pop without hurting the simple profiles that already work.
