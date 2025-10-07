SCALE_PATTERNS = {
    "major": [2, 2, 1, 2, 2, 2, 1],
    "minor": [2, 1, 2, 2, 1, 2, 2],
    "dorian": [2, 1, 2, 2, 2, 1, 2],
    "phrygian": [1, 2, 2, 2, 1, 2, 2],
    "lydian": [2, 2, 2, 1, 2, 2, 1],
    "mixolydian": [2, 2, 1, 2, 2, 1, 2],
    "locrian": [1, 2, 2, 1, 2, 2, 2],
}

CHORD_PATTERNS = {
    "major": [0, 4, 7],
    "minor": [0, 3, 7],
    "major7": [0, 4, 7, 11],
    "minor7": [0, 3, 7, 10],
    "major9": [0, 4, 7, 11, 14],
    "minor9": [0, 3, 7, 10, 14],
    "add9": [0, 4, 7, 14],
    "major11": [0, 4, 7, 11, 14, 17],
    "minor11": [0, 3, 7, 10, 14, 17],
    "sus4": [0, 5, 7],
    "sus2": [0, 2, 7],
    "dim": [0, 3, 6],
    "aug": [0, 4, 8],
}

def get_chord(note: str, chord_type: str) -> list[str]:
    """
    Calculates the notes of a chord, starting from the given root note.

    Args:
        note: The root note of the chord (e.g., "C", "G#", "Ab").
        chord_type: The type of chord to generate ("major" or "minor").

    Returns:
        A list of strings representing the notes in the chord.
    """
    sharps = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    flats = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

    chord_type_lower = chord_type.lower()
    if chord_type_lower not in CHORD_PATTERNS:
        raise ValueError(f"Invalid chord type: '{chord_type}'. Please use one of {list(CHORD_PATTERNS.keys())}.")

    # Simplified chromatic scale selection for chords
    if note.endswith("b") or note in ("F", "Bb", "Eb", "Ab", "Db", "Gb"):
        chromatic_scale = flats
    else:
        chromatic_scale = sharps

    if note not in chromatic_scale:
        # Attempt to find the note in the other chromatic scale (e.g. C# in flats)
        if note.endswith("#"):
            try:
                note_index = sharps.index(note)
                note = flats[note_index] # convert to flat equivalent
                chromatic_scale = flats
            except ValueError:
                 raise ValueError(f"Invalid note: '{note}' is not in the chromatic scale.")
        elif note.endswith("b"):
            try:
                note_index = flats.index(note)
                note = sharps[note_index] # convert to sharp equivalent
                chromatic_scale = sharps
            except ValueError:
                raise ValueError(f"Invalid note: '{note}' is not in the chromatic scale.")

    try:
        start_index = chromatic_scale.index(note)
    except ValueError:
        raise ValueError(f"Invalid note: '{note}' is not in the chromatic scale.")

    chord_pattern = CHORD_PATTERNS[chord_type_lower]
    chord = []
    for step in chord_pattern:
        current_index = (start_index + step) % 12
        chord.append(chromatic_scale[current_index])

    return chord

def _get_chromatic_scale(note: str, scale_type: str, flats: list[str], sharps: list[str]) -> list[str]:
    scale_type_lower = scale_type.lower()
    if scale_type_lower == "major":
        if note.endswith("b") or note in ("F"):
            return flats
        else:
            return sharps
    elif scale_type_lower == "minor":
        if note in ("D", "G", "C", "F", "Bb", "Eb", "Ab") or note.endswith("b"):
            return flats
        else:
            return sharps
    elif scale_type_lower == "dorian":
        if note in ("D", "G", "C", "F", "Bb", "Eb") or note.endswith("b"):
            return flats
        else:
            return sharps
    elif scale_type_lower == "phrygian":
        if note in ("A", "D", "G", "C", "F", "Bb", "Eb") or note.endswith("b"):
            return flats
        else:
            return sharps
    elif scale_type_lower == "lydian":
        if note in ("F"):
            return flats
        else:
            return sharps
    elif scale_type_lower == "mixolydian":
        if note in ("C", "F", "Bb", "Eb", "Ab", "Db", "Gb") or note.endswith("b"):
            return flats
        else:
            return sharps
    elif scale_type_lower == "locrian":
        if note in ("B"):
            return sharps
        else:
            return flats
    return sharps # Default to sharps

def get_scale(note: str, scale_type: str) -> list[str]:
    """
    Calculates the notes of a scale, starting from the given root note.

    Args:
        note: The root note of the scale (e.g., "C", "G#", "Ab").
        scale_type: The type of scale to generate ("major", "minor", "mixolydian", or "phrygian").

    Returns:
        A list of strings representing the notes in the scale.
    """
    sharps = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    flats = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

    scale_type_lower = scale_type.lower()
    if scale_type_lower not in SCALE_PATTERNS:
        raise ValueError(f"Invalid scale type: '{scale_type}'. Please use one of {list(SCALE_PATTERNS.keys())}.")

    scale_pattern = SCALE_PATTERNS[scale_type_lower]
    chromatic_scale = _get_chromatic_scale(note, scale_type, flats, sharps)

    if note not in chromatic_scale:
        if note.endswith("#"):
            try:
                note_index = sharps.index(note)
                note = flats[note_index]
                chromatic_scale = flats
            except ValueError:
                raise ValueError(f"Invalid note: '{note}' is not in the chromatic scale.")
        elif note.endswith("b"):
            try:
                note_index = flats.index(note)
                note = sharps[note_index]
                chromatic_scale = sharps
            except ValueError:
                raise ValueError(f"Invalid note: '{note}' is not in the chromatic scale.")

    try:
        start_index = chromatic_scale.index(note)
    except ValueError:
        raise ValueError(f"Invalid note: '{note}' is not in the chromatic scale.")

    scale = [chromatic_scale[start_index]]
    current_index = start_index
    for step in scale_pattern:
        current_index = (current_index + step) % 12
        scale.append(chromatic_scale[current_index])

    return scale

if __name__ == '__main__':
    while True:
        try:
            note = input("Enter a note (or 'exit' to quit): ")
            if note.lower() == 'exit':
                break
            scale_type = input(f"Enter scale type {list(SCALE_PATTERNS.keys())}: ")
            scale = get_scale(note, scale_type)
            print(f"{note} {scale_type.capitalize()} Scale: {scale}")
        except (ValueError, IndexError) as e:
            print(e)