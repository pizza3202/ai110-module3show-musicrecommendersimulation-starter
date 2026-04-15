"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from typing import Any, Dict, List, Optional, Tuple

from src.recommender import (
    ScoreWeights,
    experiment_energy_double_genre_half_weights,
    load_songs,
    recommend_songs,
    score_song,
)

# Stress-test profiles (Step 1): diverse tastes + one edge-style profile.
PROFILE_RUNS: List[Tuple[str, Dict[str, Any]]] = [
    (
        "High-Energy Pop",
        {"genre": "pop", "mood": "happy", "energy": 0.88, "likes_acoustic": False},
    ),
    (
        "Chill Lofi",
        {"genre": "lofi", "mood": "chill", "energy": 0.38, "likes_acoustic": True},
    ),
    (
        "Deep Intense Rock",
        {"genre": "rock", "mood": "intense", "energy": 0.92, "likes_acoustic": False},
    ),
    (
        "Edge case: high energy + moody (conflicting vibe)",
        {"genre": "pop", "mood": "moody", "energy": 0.93, "likes_acoustic": False},
    ),
]


def _print_recommendations_block(
    label: str,
    user_prefs: Dict[str, Any],
    songs: List[Dict[str, Any]],
    k: int = 5,
    weights: Optional[ScoreWeights] = None,
) -> None:
    """Print top-k titles, scores, and per-reason lines for one profile."""
    width = 72
    bar = "=" * width
    rule = "-" * width

    print(bar)
    print(f" {label}")
    print(bar)
    print(
        "Profile: "
        f"genre={user_prefs.get('genre')!r}, mood={user_prefs.get('mood')!r}, "
        f"energy={user_prefs.get('energy')}, "
        f"likes_acoustic={user_prefs.get('likes_acoustic', False)}"
    )
    if weights is not None:
        print(
            "Weights: "
            f"genre={weights.genre_match:.2f}, mood={weights.mood_match:.2f}, "
            f"energy_scale={weights.energy_similarity:.2f}"
        )
    print(rule)

    recommendations = recommend_songs(user_prefs, songs, k=k, weights=weights)

    print("\nTop recommendations (highest score first)\n")
    for rank, rec in enumerate(recommendations, start=1):
        song, score, _ = rec
        _, reasons = score_song(user_prefs, song, weights=weights)
        print(f"#{rank}  {song['title']}")
        print(f"     Artist:  {song['artist']}")
        print(f"     Score:   {score:.2f}")
        print("     Reasons:")
        for r in reasons:
            print(f"       • {r}")
        print()

    print(bar)
    print()


def main() -> None:
    """Load CSV, run baseline stress tests, then a weight sensitivity experiment."""
    songs = load_songs("data/songs.csv")
    width = 72
    bar = "=" * width

    print(bar)
    print(" Music Recommender — CLI-first simulation (evaluation runs)")
    print(bar)
    print(f"Loaded songs: {len(songs)}\n")

    for label, prefs in PROFILE_RUNS:
        _print_recommendations_block(label, prefs, songs, k=5, weights=None)

    # Step 3: sensitivity — double energy weight, halve genre weight; same pop profile.
    pop_prefs = PROFILE_RUNS[0][1]
    exp_w = experiment_energy_double_genre_half_weights()
    _print_recommendations_block(
        "EXPERIMENT: same High-Energy Pop profile, energy×2 & genre×0.5 weights",
        pop_prefs,
        songs,
        k=5,
        weights=exp_w,
    )

    print(bar)
    print(" Notes")
    print(bar)
    print(
        "• High-Energy Pop: expect Sunrise City at #1 (genre+mood+energy line up).\n"
        "• Chill Lofi: expect lofi/chill rows near the top (Library Rain, Midnight Coding).\n"
        "• Deep Intense Rock: expect Storm Runner / Granite Echo high (rock+intense).\n"
        "• Edge case: no pop+moody row; expect pop + perfect/near energy (e.g. Gym Hero) ahead of mood-only fits.\n"
        "• Experiment: top order may shift toward very high-energy tracks vs baseline.\n"
    )
    print(bar)


if __name__ == "__main__":
    main()
