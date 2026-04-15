"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs, score_song


def main() -> None:
    """Load the catalog, score with a demo profile, and print ranked results to the terminal."""
    songs = load_songs("data/songs.csv")
    width = 72
    bar = "=" * width
    rule = "-" * width

    print(bar)
    print(" Music Recommender — CLI-first simulation")
    print(bar)
    print(f"Loaded songs: {len(songs)}")

    # Default profile: pop + happy + high energy (matches course verification)
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    print(
        "Profile: "
        f"genre={user_prefs['genre']!r}, mood={user_prefs['mood']!r}, "
        f"energy={user_prefs['energy']}"
    )
    print(rule)

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations (highest score first)\n")
    for rank, rec in enumerate(recommendations, start=1):
        song, score, _ = rec
        _, reasons = score_song(user_prefs, song)
        print(f"#{rank}  {song['title']}")
        print(f"     Artist:  {song['artist']}")
        print(f"     Score:   {score:.2f}")
        print("     Reasons:")
        for r in reasons:
            print(f"       • {r}")
        print()

    print(bar)
    print("Expected for this profile: #1 should be a pop + happy match (Sunrise City).")
    print(bar)


if __name__ == "__main__":
    main()
