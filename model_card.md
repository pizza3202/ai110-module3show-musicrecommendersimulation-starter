# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**Catalog Vibe Scorer (Module 3 simulation)**

---

## 2. Intended Use

This system suggests a small number of songs from a fixed CSV catalog by comparing each track’s metadata to a short list of user preferences. It is intended for **classroom exploration and documentation practice**: you can read the scoring recipe, run the CLI demo, and run automated tests to see how deterministic rules produce an ordered list.

It assumes the user can state a **favorite genre**, **favorite mood**, a **target energy** level on a zero-to-one style scale, and whether they **lean acoustic or produced** tracks. It is **not** for real listeners, commercial deployment, or personalization at scale.

---

## 3. How the Model Works

Think of each song as a row of musical “stats” and tags. The model gives **+2 points** when the genre tag matches the user’s favorite genre, and **+1 point** when the mood tag matches. Genre is therefore a stronger signal than mood, which matches a simple classroom weighting strategy before tuning.

For energy—and, if you supply them, valence, danceability, or tempo—the model does **not** simply reward “more.” It rewards **being close** to the number the user asked for. That mirrors the idea that someone who wants a calm evening does not always want the *lowest* possible energy score; they want energy **near** their comfort zone.

Acousticness is interpreted with one bit of taste: if the user says they like acoustic material, higher acousticness helps the score; if not, more electronic or produced-sounding tracks score better. After every song has a total score, the system **sorts** the catalog from highest score to lowest and returns the first few rows. That final sort is what turns individual numbers into a ranked playlist.

Compared to the starter code, the project now **loads real rows from the CSV**, implements the **full scoring and ranking path**, and returns **short natural-language reasons** so results are explainable rather than mysterious.

---

## 4. Data

The catalog is `data/songs.csv` with **18 songs** (10 from the starter plus **8** added rows for broader coverage). Each row includes identifiers and human-readable names plus **genre**, **mood**, **energy** (roughly 0.0–1.0), **tempo in BPM**, **valence**, **danceability**, and **acousticness**.

Genres now include **pop**, **lofi**, **rock**, **ambient**, **jazz**, **synthwave**, **indie pop**, **metal**, **folk**, **edm**, **hip hop**, **reggae**, and **classical**. Moods include **happy**, **chill**, **intense**, **relaxed**, **moody**, and **focused**. The extra rows are **synthetic teaching examples**, not a real streaming export.

The dataset is **not** a statistically representative sample of global music. It is a teaching mix, so conclusions about “what people like” in general should not be drawn from it. Important taste dimensions such as **language, lyrics, cultural context, era, popularity, and social signals** are missing.

---

## 5. Strengths

The recommender is **transparent**: given the same inputs, it always produces the same ordering, and the explanation strings tie back to concrete matches and similarity phrases.

For users who state preferences in the **same vocabulary as the CSV** (for example “pop” and “happy” with a high energy target), the top results tend to **feel coherent** because the model is doing exactly what a human curator might do at a glance: check genre, mood, and intensity.

The design is also **easy to audit** in a course setting: weights and features can be discussed without reading a large machine-learning stack, which helps when the learning goal is to understand **scoring versus ranking** and the limits of hand-crafted rules.

---

## 6. Limitations and Bias

The system only knows what is in the table. **Underrepresented genres or moods** will rarely win, not because listeners dislike them, but because the catalog is small and uneven. **String equality** on genre and mood punishes harmless variation in wording.

Because the approach is **content-only**, it cannot discover “hidden gems” from listening patterns, and it cannot correct for bad or subjective tags. If two songs share a label but feel very different in real life, the model cannot tell.

If this logic were dropped into a real product unchanged, **allocation harm** is easy to imagine: artists outside the favored tag set would almost never surface, and the scoring recipe would amplify whatever cultural assumptions were baked into the tags and weights. Users who do not fit a single genre-mood-energy description get a **flattened** version of their taste.

---

## 7. Evaluation

Checks included:

- **Automated tests** in `tests/test_recommender.py` that verify the higher-scoring song for a pop / happy / high-energy profile is the expected track, and that explanations are non-empty strings.
- **Manual CLI run** (`python -m src.main`) to confirm the pipeline loads the CSV, scores each row, sorts, and prints titles with reasons that match the stated demo preferences.

No separate offline accuracy metric was used; the catalog is too small for meaningful statistical rates. Evaluation here is primarily **face validity** and **regression tests** on a couple of controlled examples.

---

## 8. Future Work

Reasonable next steps without turning this into a large product would include: **synonym or hierarchy handling** for genres, a **diversity penalty** so the top five are not almost the same vibe, optional **soft mood** matches, and a second tiny dataset or user study to discuss **fairness** with more than anecdotal examples.

If the scope were allowed to grow, hybrid signals (even a toy collaborative layer) and logging of skips or replays would illustrate how production systems close the loop.

---

## 9. Personal Reflection

Building a recommender from scratch—even a toy one—makes it obvious that **“the algorithm” is mostly choices**: which fields exist, how strongly genre outweighs mood, and what we pretend “energy” means for a person’s evening.

It also sharpened the contrast between **transparent rules** and the opaque feeds people use daily. A real platform adds data volume, personalization, and business goals on top of similar bones. Human judgment still matters in deciding what belongs in the catalog, how labels are applied, and what outcomes we are willing to call success.
