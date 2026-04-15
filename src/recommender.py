import csv
from typing import Any, Dict, List, Tuple

from dataclasses import dataclass

# Content-based weights (genre/mood are categorical; numerics reward closeness to taste).
# Course starting point: +2 genre, +1 mood, plus energy similarity (see README).
WEIGHT_GENRE_MATCH = 2.0
WEIGHT_MOOD_MATCH = 1.0
WEIGHT_ENERGY_SIMILARITY = 2.0  # scaled by (1 - |song_energy - target|)
WEIGHT_ACOUSTIC_PREFERENCE = 1.0
WEIGHT_VALENCE_SIMILARITY = 0.75  # used only if user_prefs includes "valence"
WEIGHT_DANCEABILITY_SIMILARITY = 0.75  # used only if user_prefs includes "danceability"
WEIGHT_TEMPO_SIMILARITY = 0.5  # used only if user_prefs includes "tempo_bpm"


def _float(row: Dict[str, Any], key: str) -> float:
    """Coerce ``row[key]`` to float for numeric CSV fields."""
    return float(row[key])


def _similarity_01(a: float, b: float) -> float:
    """Return 1 minus absolute difference, clamped at zero (closer values score higher)."""
    return max(0.0, 1.0 - abs(a - b))


def _tempo_similarity(song_bpm: float, target_bpm: float) -> float:
    """Return similarity in [0, 1] from BPM distance using a fixed span of 60 BPM."""
    span = 60.0
    return max(0.0, 1.0 - abs(song_bpm - target_bpm) / span)


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """

    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """

    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return up to ``k`` songs with highest scores for the given user profile."""
        prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        ranked: List[Tuple[Song, float]] = []
        for song in self.songs:
            d = _song_to_dict(song)
            score, _ = score_song(prefs, d)
            ranked.append((song, score))
        ranked = sorted(ranked, key=lambda x: x[1], reverse=True)
        return [s for s, _ in ranked[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a single-line explanation string built from scoring reasons."""
        prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        _, reasons = score_song(prefs, _song_to_dict(song))
        return " ".join(reasons) if reasons else "No strong matches to your stated preferences."


def _song_to_dict(song: Song) -> Dict[str, Any]:
    """Map a ``Song`` instance to the dict shape expected by ``score_song``."""
    return {
        "id": song.id,
        "title": song.title,
        "artist": song.artist,
        "genre": song.genre,
        "mood": song.mood,
        "energy": song.energy,
        "tempo_bpm": song.tempo_bpm,
        "valence": song.valence,
        "danceability": song.danceability,
        "acousticness": song.acousticness,
    }


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file using the standard-library csv module.
    Returns a list of dicts; ``id`` is an int, all other numeric fields are floats
    so scoring can use them directly.
    Required by src/main.py
    """
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append(
                {
                    "id": int(row["id"]),
                    "title": row["title"],
                    "artist": row["artist"],
                    "genre": row["genre"],
                    "mood": row["mood"],
                    "energy": _float(row, "energy"),
                    "tempo_bpm": _float(row, "tempo_bpm"),
                    "valence": _float(row, "valence"),
                    "danceability": _float(row, "danceability"),
                    "acousticness": _float(row, "acousticness"),
                }
            )
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py

    Scoring rule (content-based):
    - Genre/mood: binary match with genre weighted higher than mood.
    - Energy, valence, danceability, tempo: reward closeness to targets, not "higher is better".
    - Acousticness: if likes_acoustic, reward higher acousticness; otherwise reward lower.

    Returns ``(total_score, reasons)`` where each reason string includes the points
    added for that component (for example ``"genre match (+2.0) [pop]"``).
    """
    score = 0.0
    reasons: List[str] = []

    ug = str(user_prefs.get("genre", "")).strip().lower()
    um = str(user_prefs.get("mood", "")).strip().lower()
    sg = str(song.get("genre", "")).strip().lower()
    sm = str(song.get("mood", "")).strip().lower()

    if ug and sg == ug:
        score += WEIGHT_GENRE_MATCH
        reasons.append(f"genre match (+{WEIGHT_GENRE_MATCH:.1f}) [{sg}]")
    if um and sm == um:
        score += WEIGHT_MOOD_MATCH
        reasons.append(f"mood match (+{WEIGHT_MOOD_MATCH:.1f}) [{sm}]")

    target_energy = float(user_prefs["energy"])
    e = _float(song, "energy")
    energy_sim = _similarity_01(e, target_energy)
    energy_pts = WEIGHT_ENERGY_SIMILARITY * energy_sim
    score += energy_pts
    reasons.append(
        f"energy similarity (+{energy_pts:.2f}) (song {e:.2f} vs target {target_energy:.2f})"
    )

    likes_acoustic = bool(user_prefs.get("likes_acoustic", False))
    ac = _float(song, "acousticness")
    if likes_acoustic:
        ac_pts = WEIGHT_ACOUSTIC_PREFERENCE * ac
        score += ac_pts
        reasons.append(f"acoustic preference (+{ac_pts:.2f}) (favor acoustic)")
    else:
        ac_pts = WEIGHT_ACOUSTIC_PREFERENCE * (1.0 - ac)
        score += ac_pts
        reasons.append(f"acoustic preference (+{ac_pts:.2f}) (favor produced)")

    if "valence" in user_prefs:
        tv = float(user_prefs["valence"])
        v = _float(song, "valence")
        vs = _similarity_01(v, tv)
        v_pts = WEIGHT_VALENCE_SIMILARITY * vs
        score += v_pts
        reasons.append(f"valence similarity (+{v_pts:.2f})")

    if "danceability" in user_prefs:
        td = float(user_prefs["danceability"])
        d = _float(song, "danceability")
        ds = _similarity_01(d, td)
        d_pts = WEIGHT_DANCEABILITY_SIMILARITY * ds
        score += d_pts
        reasons.append(f"danceability similarity (+{d_pts:.2f})")

    if "tempo_bpm" in user_prefs:
        tb = float(user_prefs["tempo_bpm"])
        bpm = _float(song, "tempo_bpm")
        ts = _tempo_similarity(bpm, tb)
        t_pts = WEIGHT_TEMPO_SIMILARITY * ts
        score += t_pts
        reasons.append(f"tempo similarity (+{t_pts:.2f})")

    return score, reasons


def recommend_songs(
    user_prefs: Dict, songs: List[Dict], k: int = 5
) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py

    Ranking rule: compute per-song scores, sort descending by score, return top k.

    Uses ``sorted(..., reverse=True)`` so we return a **new** ordered list. That avoids
    mutating anything the caller passed in. (``list.sort()`` sorts in place, returns
    ``None``, and would reorder a list if we appended tuples then sorted that list.)
    """
    ranked: List[Tuple[Dict, float, str]] = []
    for song in songs:
        s, reasons = score_song(user_prefs, song)
        explanation = " ".join(reasons)
        ranked.append((song, s, explanation))
    ranked = sorted(ranked, key=lambda x: x[1], reverse=True)
    return ranked[:k]
