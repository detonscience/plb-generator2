import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QLabel, QTabWidget, QComboBox, QSpinBox, QMessageBox, QFileDialog, QGridLayout
)
from mido import Message, MidiFile, MidiTrack

# ===============================
# GLOBAL SETTINGS / SCALES
# ===============================
SCALES = {
    # Basic
    "major": [0, 2, 4, 5, 7, 9, 11],
    "minor": [0, 2, 3, 5, 7, 8, 10],

    # Modes
    "dorian": [0, 2, 3, 5, 7, 9, 10],
    "phrygian": [0, 1, 3, 5, 7, 8, 10],
    "lydian": [0, 2, 4, 6, 7, 9, 11],
    "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "locrian": [0, 1, 3, 5, 6, 8, 10],

    # Minor variations
    "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
    "melodic_minor": [0, 2, 3, 5, 7, 9, 11],

    # Pentatonic
    "major_pentatonic": [0, 2, 4, 7, 9],
    "minor_pentatonic": [0, 3, 5, 7, 10],

    # Blues
    "blues": [0, 3, 5, 6, 7, 10],

    # Exotic / dark vibes
    "phrygian_dominant": [0, 1, 4, 5, 7, 8, 10],
    "double_harmonic": [0, 1, 4, 5, 7, 8, 11],
    "enigmatic": [0, 1, 4, 6, 8, 10, 11],

    # Ambient / cinematic
    "whole_tone": [0, 2, 4, 6, 8, 10],
    "chromatic": list(range(12)),

    # Japanese / modal textures
    "hirajoshi": [0, 2, 3, 7, 8],
    "in_sen": [0, 1, 5, 7, 10],
}

# ===============================
# SMART KEY DISPLAY
# ===============================
def get_display_keys(scale_name):
    # flat-friendly keys
    flat_scales = ["minor", "dorian", "phrygian"]

    if scale_name in flat_scales:
        return [
            "C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B"
        ]
    else:
        return [
            "C","C#","D","D#","E","F","F#","G","G#","A","A#","B"
        ]

NOTE_MAP = {
    "C": 60,
    "C#": 61, "Db": 61,
    "D": 62,
    "D#": 63, "Eb": 63,
    "E": 64, "Fb": 64,
    "E#": 65, "F": 65,
    "F#": 66, "Gb": 66,
    "G": 67,
    "G#": 68, "Ab": 68,
    "A": 69,
    "A#": 70, "Bb": 70,
    "B": 71, "Cb": 71,
    "B#": 60
}

# ===============================
# CHORD PROGRESSIONS
# ===============================
# ===============================
# CHORD PROGRESSIONS
# ===============================
PROGRESSIONS = {
    "standard": [[0, 5, 6, 4], [0, 3, 4, 6]],
    "ambient": [[0, 2, 5, 3], [0, 4, 2, 6]],
    "weird": [[0, 1, 6, 3], [2, 6, 1, 5]],

    "dark": [
        [0, 6, 5, 4],
        [0, 3, 6, 2],
        [0, 5, 3, 2],
    ],

    "dystopian": [
        [0, 1, 6, 2],
        [0, 6, 1, 5],
        [2, 1, 6, 0],
    ],

    "jazz": [
        [0, 2, 5, 1],
        [0, 4, 1, 5],
        [2, 5, 1, 4],
    ],

    "emotional": [
        [0, 4, 5, 3],
        [0, 3, 5, 4],
        [0, 5, 4, 3],
    ],

    "uplifting": [
        [0, 4, 5, 6],
        [0, 3, 4, 5],
        [0, 5, 6, 4],
    ],

    "sad": [
        [0, 3, 4, 3],
        [0, 5, 3, 4],
        [0, 2, 3, 1],
    ],

    "introspective": [
        [0, 3, 2, 3],
        [0, 5, 2, 4],
        [0, 2, 4, 3],
    ],

    "spacey": [
        [0, 2, 1, 5],
        [0, 6, 2, 5],
        [0, 1, 2, 6],
    ],

    "techno": [
        [0, 5, 3, 4],
        [0, 3, 5, 2],
        [0, 6, 5, 3],
    ],

    "dub_techno": [
        [0, 5, 3, 2],
        [0, 3, 2, 5],
        [0, 2, 5, 3],
    ],

    "minimal": [
        [0, 0, 5, 0],
        [0, 3, 0, 5],
        [0, 2, 0, 4],
    ],

    "idm": [
        [0, 1, 4, 6],
        [2, 5, 1, 6],
        [0, 6, 2, 1],
    ],

    "cinematic": [
        [0, 5, 4, 3],
        [0, 3, 4, 5],
        [0, 4, 2, 5],
    ],

    "drone": [
        [0, 0, 0, 0],
        [0, 5, 0, 5],
        [0, 3, 0, 3],
    ],

    "floating": [
        [0, 2, 4, 2],
        [0, 4, 2, 6],
        [0, 6, 4, 2],
    ],

    "chaotic": [
        [0, 1, 2, 3],
        [6, 5, 4, 3],
        [0, 6, 1, 5],
    ],

    "atonalish": [
        [0, 1, 6, 5],
        [2, 3, 1, 6],
        [0, 6, 3, 1],
    ],

    "am/fmhead": [
        [0, 5, 2, 6],
        [0, 3, 5, 4],
        [0, 1, 5, 2],
        [0, 3, 2, 6],
    ],
}

# ===============================
# PAD PROGRESSIONS (FOCUSED SET)
# ===============================
PAD_PROGRESSIONS = {
    "standard": [[0, 5, 6, 4], [0, 3, 4, 6]],
    "ambient": [[0, 2, 5, 3], [0, 4, 2, 6]],
    "weird": [[0, 1, 6, 3], [2, 6, 1, 5]],

    "dark": [
        [0, 6, 5, 4],
        [0, 3, 6, 2],
        [0, 5, 3, 2],
    ],

    "dystopian": [
        [0, 1, 6, 2],
        [0, 6, 1, 5],
        [2, 1, 6, 0],
    ],

    "jazz": [
        [0, 2, 5, 1],
        [0, 4, 1, 5],
        [2, 5, 1, 4],
    ],

    "emotional": [
        [0, 4, 5, 3],
        [0, 3, 5, 4],
        [0, 5, 4, 3],
    ],

    "uplifting": [
        [0, 4, 5, 6],
        [0, 3, 4, 5],
        [0, 5, 6, 4],
    ],

    "sad": [
        [0, 3, 4, 3],
        [0, 5, 3, 4],
        [0, 2, 3, 1],
    ],

    "introspective": [
        [0, 3, 2, 3],
        [0, 5, 2, 4],
        [0, 2, 4, 3],
    ],

    "spacey": [
        [0, 2, 1, 5],
        [0, 6, 2, 5],
        [0, 1, 2, 6],
    ],

    "am/fmhead": [
        [0, 5, 2, 6],
        [0, 3, 5, 4],
        [0, 1, 5, 2],
        [0, 3, 2, 6],
    ],
}

# ===============================
# MIDI EXPORT
# ===============================
def export_midi(notes, filename="output.mid"):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    i = 0
    while i < len(notes):
        base_duration = notes[i][1]
        chord_notes = []

        j = i
        while j < len(notes) and notes[j][1] == base_duration:
            chord_notes.append(notes[j])
            j += 1

        for note, duration, velocity in chord_notes:
            track.append(Message('note_on', note=note, velocity=velocity, time=0))

        for k, (note, duration, velocity) in enumerate(chord_notes):
            track.append(Message('note_off', note=note, velocity=velocity, time=duration if k == 0 else 0))

        i = j

    mid.save(filename)

# ===============================
# GENERATORS
# ===============================
def generate_bass(settings):
    root = NOTE_MAP[settings["key"]] - settings.get("bass_octave", 2) * 12
    scale = SCALES[settings["scale"]]
    notes = []

    pattern = settings.get("bass_pattern", "four_on_floor")
    steps = settings["bars"] * 16

    for step in range(steps):

        if pattern == "four_on_floor":
            if step % 4 != 0:
                continue

        elif pattern == "offbeat":
            if step % 4 != 2:
                continue

        elif pattern == "rolling":
            if random.random() < 0.5:
                continue

        elif pattern == "driving":
            if step % 2 != 0:
                continue

        elif pattern == "funky_dark":
            if step % 4 == 0:
                pass
            elif step % 4 == 3 and random.random() > 0.4:
                pass
            elif random.random() > 0.7:
                pass
            else:
                continue

        note = root + random.choice(scale)
        mood = settings.get("mood", "dark")
        genre = settings.get("genre", "techno")

        if settings.get("velocity_mode") == "fixed":
            velocity = settings.get("velocity", 90)
        else:
            if mood == "dark":
                velocity = random.randint(70, 100)
            elif mood == "hypnotic":
                velocity = random.randint(80, 110)
            elif mood == "dreamy":
                velocity = random.randint(60, 90)
            else:
                velocity = random.randint(75, 105)

        if genre == "techno":
            duration = 120
        elif genre == "house":
            duration = 180
        elif genre == "dub_techno":
            duration = 240
        else:
            duration = 120

        notes.append((note, duration, velocity))

    return notes


def generate_chords(settings):
    root = NOTE_MAP[settings["key"]]
    scale = SCALES[settings["scale"]]
    notes = []

    style = settings.get("chord_style", "sustain")
    mood = settings.get("mood", "dark")

    # extend scale for proper stacking
    extended_scale = scale + [n+12 for n in scale] + [n+24 for n in scale]

    for bar in range(settings["bars"]):
        progression_type = settings.get("genre", "standard")
        if progression_type not in PROGRESSIONS:
            progression_type = "standard"

        progression = random.choice(PROGRESSIONS[progression_type])
        degree = progression[bar % len(progression)]

        chord_type = settings.get("chord_type", "7th")

        if chord_type == "triad":
            chord = [
                root + extended_scale[degree],
                root + extended_scale[degree + 2],
                root + extended_scale[degree + 4]
            ]
        elif chord_type == "extended":
            chord = [
                root + extended_scale[degree],
                root + extended_scale[degree + 2],
                root + extended_scale[degree + 4],
                root + extended_scale[degree + 6],
                root + extended_scale[degree + 8]
            ]
        else:
            chord = [
                root + extended_scale[degree],
                root + extended_scale[degree + 2],
                root + extended_scale[degree + 4],
                root + extended_scale[degree + 6]
            ]

        if settings.get("chord_inversion") == "random":
            inversion = random.choice([0, 1, 2])
        else:
            inversion = 0
        for _ in range(inversion):
            note = chord.pop(0)
            chord.append(note + 12)

        if settings.get("chord_spread") == "wide":
            if len(chord) > 1:
                chord[1] += 12
            if len(chord) > 2:
                chord[2] += 12

        duration = 960 if style == "sustain" else 240

        for i, note in enumerate(chord):
            if settings.get("velocity_mode") == "fixed":
                velocity = settings.get("velocity", 90)
            else:
                if mood == "dark":
                    velocity = random.randint(50, 70)
                elif mood == "dreamy":
                    velocity = random.randint(70, 100)
                else:
                    velocity = random.randint(60, 90)

            # slight humanization (optional strum feel)
            offset = i * 5 if style == "stabs" else 0
            notes.append((note, duration, velocity))

    return notes

def generate_pads(settings):
    root = NOTE_MAP[settings["key"]]
    scale = SCALES[settings["scale"]]
    notes = []

    mood = settings.get("mood", "dreamy")

    for bar in range(settings["bars"]):
        progression_type = settings.get("mood", "ambient")
        if progression_type not in PAD_PROGRESSIONS:
            progression_type = "ambient"

        progression = random.choice(PAD_PROGRESSIONS[progression_type])
        degree = progression[bar % len(progression)]

        root_note = root + scale[degree]
        third = root + scale[(degree + 2) % len(scale)]
        fifth = root + scale[(degree + 4) % len(scale)]

        chord = [root_note, third, fifth]

        # pads = long sustained
        duration = 1920  # 2 bars feel

        for note in chord:
            if mood == "dreamy":
                velocity = random.randint(70, 100)
            elif mood == "dark":
                velocity = random.randint(50, 70)
            else:
                velocity = random.randint(60, 90)

            notes.append((note, duration, velocity))

    return notes


def generate_lead(settings):
    root = NOTE_MAP[settings["key"]] + settings.get("lead_octave", 1) * 12
    scale = SCALES[settings["scale"]]
    notes = []

    pattern = settings.get("lead_pattern", "random")
    mood = settings.get("mood", "dark")
    genre = settings.get("genre", "techno")

    steps = settings["bars"] * 16

    last_note = None

    for step in range(steps):
        if pattern == "skip" and random.random() < 0.5:
            continue

        if pattern == "repeat" and last_note:
            note = last_note
        else:
            note = root + random.choice(scale)

        if settings.get("velocity_mode") == "fixed":
            velocity = settings.get("velocity", 90)
        else:
            if mood == "dark":
                velocity = random.randint(60, 100)
            elif mood == "dreamy":
                velocity = random.randint(80, 120)
            else:
                velocity = random.randint(70, 110)

        if genre == "techno":
            duration = 120
        elif genre == "house":
            duration = random.choice([120, 240])
        elif genre == "dub_techno":
            duration = random.choice([240, 480])
        elif genre == "idm":
            duration = random.choice([60, 120, 240])
        elif genre == "drum_and_bass":
            duration = random.choice([60, 90, 120])
        else:
            duration = 120

        notes.append((note, duration, velocity))
        last_note = note

    return notes


# ===============================
# MAIN APP
# ===============================
class GeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Track Generator")

        self.setStyleSheet("""
        QWidget {
            background-color: #121212;
            color: #eeeeee;
            font-size: 12px;
        }
        QPushButton {
            background-color: #1f1f1f;
            border: 1px solid #333;
            padding: 6px;
        }
        QPushButton:hover {
            background-color: #2a2a2a;
        }
        QComboBox, QSpinBox {
            background-color: #1a1a1a;
            border: 1px solid #333;
            padding: 4px;
        }
        QTabWidget::pane {
            border: 1px solid #333;
        }
        QTabBar::tab {
            background: #111;
            color: #bbbbbb;
            padding: 10px;
            border: 1px solid #222;
            min-width: 100px;
            font-size: 14px;
            letter-spacing: 1px;
        }
        QTabBar::tab:selected {
            background: #00ccff;
            color: black;
            font-weight: bold;
            font-size: 15px;
            border: 2px solid #00ccff;
        }
        QTabBar::tab:hover {
            background: #222;
            color: #ffffff;
        }
        """)

        layout = QVBoxLayout()
        self.arp_steps = [True] * 16

        top_btn = QPushButton("⬢  GENERATE TRACK")
        top_btn.clicked.connect(self.generate_full)
        top_btn.setStyleSheet("background-color:#00cc88; color:black; font-weight:bold;")

        random_btn = QPushButton("◉  RANDOMIZE")
        random_btn.clicked.connect(self.randomize_all)

        layout.addWidget(top_btn)
        layout.addWidget(random_btn)

        # GLOBAL CONTROLS
        self.key_select = QComboBox()

        self.scale_select = QComboBox()
        self.scale_select.addItems(SCALES.keys())

        self.update_keys()

        self.bars_select = QSpinBox()
        self.bars_select.setRange(1, 32)
        self.bars_select.setValue(8)

        # ADVANCED CONTROLS
        self.velocity_mode = QComboBox()
        self.velocity_mode.addItems(["fixed", "random"])

        self.velocity_value = QSpinBox()
        self.velocity_value.setRange(1, 127)
        self.velocity_value.setValue(90)

        self.length_mode = QComboBox()
        self.length_mode.addItems(["short", "long", "random"])

        self.mood = QComboBox()
        self.mood.addItems(["dark", "hypnotic", "dreamy", "dubby"])

        self.genre = QComboBox()
        self.genre.addItems(["techno", "house", "dub_techno", "electro", "idm", "drum_and_bass"])

        layout.addWidget(QLabel("◼  KEY"))
        layout.addWidget(self.key_select)
        layout.addWidget(QLabel("▲  SCALE"))
        layout.addWidget(self.scale_select)
        layout.addWidget(QLabel("◆  BARS"))
        layout.addWidget(self.bars_select)
        layout.addWidget(QLabel("⬟  VELOCITY MODE"))
        layout.addWidget(self.velocity_mode)
        layout.addWidget(QLabel("Velocity"))
        layout.addWidget(self.velocity_value)
        layout.addWidget(QLabel("Length Mode"))
        layout.addWidget(self.length_mode)
        layout.addWidget(QLabel("◉  MOOD"))
        layout.addWidget(self.mood)
        layout.addWidget(QLabel("⬢  GENRE"))
        layout.addWidget(self.genre)

        self.scale_select.currentTextChanged.connect(self.update_keys)

        # ===============================
        # BASS SETTINGS
        # ===============================
        self.bass_density = QSpinBox()
        self.bass_density.setRange(1, 16)
        self.bass_density.setValue(4)

        self.bass_pattern = QComboBox()
        self.bass_pattern.addItems([
            "four_on_floor",
            "offbeat",
            "rolling",
            "driving",
            "funky_dark"
        ])

        self.bass_octave = QSpinBox()
        self.bass_octave.setRange(1, 4)
        self.bass_octave.setValue(2)

        # ===============================
        # CHORD SETTINGS
        # ===============================
        self.chord_density = QSpinBox()
        self.chord_density.setRange(1, 8)
        self.chord_density.setValue(1)

        self.chord_style = QComboBox()
        self.chord_style.addItems(["sustain", "stabs"])

        self.chord_type = QComboBox()
        self.chord_type.addItems(["triad", "7th", "extended"])

        self.chord_spread = QComboBox()
        self.chord_spread.addItems(["tight", "wide"])

        self.chord_inversion = QComboBox()
        self.chord_inversion.addItems(["root", "random"])

        # ===============================
        # LEAD SETTINGS
        # ===============================
        self.lead_density = QSpinBox()
        self.lead_density.setRange(1, 16)
        self.lead_density.setValue(8)

        self.lead_pattern = QComboBox()
        self.lead_pattern.addItems(["random", "repeat", "skip"])

        self.lead_octave = QSpinBox()
        self.lead_octave.setRange(0, 3)
        self.lead_octave.setValue(1)

        layout.addWidget(QLabel("Bass Density"))
        layout.addWidget(self.bass_density)

        # TABS
        tabs = QTabWidget()

        # Bass Tab
        bass_tab = QWidget()
        bass_layout = QVBoxLayout()
        bass_layout.addWidget(QLabel("Pattern"))
        bass_layout.addWidget(self.bass_pattern)
        bass_layout.addWidget(QLabel("Octave"))
        bass_layout.addWidget(self.bass_octave)
        bass_btn = QPushButton("◼  GENERATE BASS")
        bass_btn.clicked.connect(self.generate_bass)
        bass_layout.addWidget(bass_btn)
        bass_tab.setLayout(bass_layout)

        # Chords Tab
        chords_tab = QWidget()
        chords_layout = QVBoxLayout()
        chords_layout.addWidget(QLabel("Style"))
        chords_layout.addWidget(self.chord_style)
        chords_layout.addWidget(QLabel("Chord Type"))
        chords_layout.addWidget(self.chord_type)

        chords_layout.addWidget(QLabel("Spread"))
        chords_layout.addWidget(self.chord_spread)

        chords_layout.addWidget(QLabel("Inversion"))
        chords_layout.addWidget(self.chord_inversion)
        chords_btn = QPushButton("▲  GENERATE CHORDS")
        chords_btn.clicked.connect(self.generate_chords)
        chords_layout.addWidget(chords_btn)
        chords_tab.setLayout(chords_layout)

        # Pads Tab
        pads_tab = QWidget()
        pads_layout = QVBoxLayout()
        pads_layout.addWidget(QLabel("Pads = long sustained atmospheres"))

        # PAD CONTROLS
        self.pad_progression = QComboBox()
        self.pad_progression.addItems(list(PAD_PROGRESSIONS.keys()))

        self.pad_density = QComboBox()
        self.pad_density.addItems(["triad", "7th", "cluster"])

        self.pad_evolve = QComboBox()
        self.pad_evolve.addItems(["off", "slow", "medium"])

        pads_layout.addWidget(QLabel("Pad Progression"))
        pads_layout.addWidget(self.pad_progression)

        pads_layout.addWidget(QLabel("Pad Density"))
        pads_layout.addWidget(self.pad_density)

        pads_layout.addWidget(QLabel("Pad Evolution"))
        pads_layout.addWidget(self.pad_evolve)

        pads_btn = QPushButton("◆  GENERATE PADS")
        pads_btn.clicked.connect(self.generate_pads)
        pads_layout.addWidget(pads_btn)

        pads_tab.setLayout(pads_layout)

        # Lead Tab
        lead_tab = QWidget()
        lead_layout = QVBoxLayout()
        lead_layout.addWidget(QLabel("Pattern"))
        lead_layout.addWidget(self.lead_pattern)
        lead_layout.addWidget(QLabel("Octave"))
        lead_layout.addWidget(self.lead_octave)
        lead_btn = QPushButton("⬟  GENERATE LEAD")
        lead_btn.clicked.connect(self.generate_lead)
        lead_layout.addWidget(lead_btn)
        lead_tab.setLayout(lead_layout)

        # ARP TAB
        arp_tab = QWidget()
        arp_layout = QVBoxLayout()

        self.arp_pattern = QComboBox()
        self.arp_pattern.addItems(["up", "down", "up_down", "random", "chord"])

        arp_layout.addWidget(QLabel("Pattern"))
        arp_layout.addWidget(self.arp_pattern)

        # 🔥 STEP GRID (Elektron style)
        grid = QGridLayout()
        self.arp_buttons = []

        for i in range(16):
            btn = QPushButton(str(i+1))
            btn.setCheckable(True)
            btn.setChecked(True)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #1a1a1a;
                    border: 2px solid #333;
                    min-width: 30px;
                    min-height: 30px;
                }
                QPushButton:checked {
                    background-color: #00ccff;
                    color: black;
                }
            """)

            btn.clicked.connect(lambda checked, idx=i: self.toggle_arp_step(idx, checked))

            self.arp_buttons.append(btn)
            grid.addWidget(btn, i // 8, i % 8)

        arp_layout.addLayout(grid)

        # velocity controls
        self.arp_velocity_mode = QComboBox()
        self.arp_velocity_mode.addItems(["random", "fixed"])

        self.arp_velocity = QSpinBox()
        self.arp_velocity.setRange(1, 127)
        self.arp_velocity.setValue(90)

        arp_layout.addWidget(QLabel("Velocity Mode"))
        arp_layout.addWidget(self.arp_velocity_mode)

        arp_layout.addWidget(QLabel("Velocity"))
        arp_layout.addWidget(self.arp_velocity)

        arp_btn = QPushButton("◉  GENERATE ARP")
        arp_btn.clicked.connect(self.generate_arp)
        arp_layout.addWidget(arp_btn)

        arp_tab.setLayout(arp_layout)

        # Full Track Tab
        full_tab = QWidget()
        full_layout = QVBoxLayout()
        full_btn = QPushButton("⬢  GENERATE FULL")
        full_btn.clicked.connect(self.generate_full)
        full_layout.addWidget(full_btn)
        full_tab.setLayout(full_layout)

        tabs.addTab(bass_tab, "◼  BASS")
        tabs.addTab(chords_tab, "▲  CHORDS")
        tabs.addTab(pads_tab, "◆  PADS")
        tabs.addTab(lead_tab, "⬟  LEAD")
        tabs.addTab(arp_tab, "◉  ARPS")
        tabs.addTab(full_tab, "⬢  FULL")

        layout.addWidget(tabs)
        self.setLayout(layout)

    def save_file_dialog(self, default_name):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save MIDI File",
            default_name,
            "MIDI Files (*.mid)",
            options=options
        )
        return file_path

    def get_settings(self):
        return {
            "key": self.key_select.currentText(),
            "scale": self.scale_select.currentText(),
            "bars": self.bars_select.value(),
            "bass_density": self.bass_density.value(),
            "chord_density": self.chord_density.value(),
            "lead_density": self.lead_density.value(),
            "velocity_mode": self.velocity_mode.currentText(),
            "velocity": self.velocity_value.value(),
            "length_mode": self.length_mode.currentText(),
            "bass_pattern": self.bass_pattern.currentText(),
            "lead_pattern": self.lead_pattern.currentText(),
            "chord_style": self.chord_style.currentText(),
            "chord_type": self.chord_type.currentText(),
            "chord_spread": self.chord_spread.currentText(),
            "chord_inversion": self.chord_inversion.currentText(),
            "bass_octave": self.bass_octave.value(),
            "lead_octave": self.lead_octave.value(),
            "mood": self.mood.currentText(),
            "genre": self.genre.currentText(),
            "pad_progression": self.pad_progression.currentText(),
            "pad_density": self.pad_density.currentText(),
            "pad_evolve": self.pad_evolve.currentText(),
            "arp_pattern": self.arp_pattern.currentText(),
            "arp_velocity_mode": self.arp_velocity_mode.currentText(),
            "arp_velocity": self.arp_velocity.value(),
            "arp_steps": self.arp_steps,
        }
    def update_keys(self):
        current_scale = self.scale_select.currentText()
        self.key_select.clear()
        self.key_select.addItems(get_display_keys(current_scale))

    def randomize_all(self):
        self.key_select.setCurrentIndex(random.randint(0, self.key_select.count()-1))
        self.scale_select.setCurrentIndex(random.randint(0, self.scale_select.count()-1))
        self.bars_select.setValue(random.randint(2, 16))

        self.mood.setCurrentIndex(random.randint(0, self.mood.count()-1))
        self.genre.setCurrentIndex(random.randint(0, self.genre.count()-1))

        self.velocity_mode.setCurrentIndex(random.randint(0, 1))
        self.velocity_value.setValue(random.randint(60, 110))

        self.bass_pattern.setCurrentIndex(random.randint(0, self.bass_pattern.count()-1))
        self.lead_pattern.setCurrentIndex(random.randint(0, self.lead_pattern.count()-1))
        self.arp_pattern.setCurrentIndex(random.randint(0, self.arp_pattern.count()-1))

    def toggle_arp_step(self, idx, state):
        self.arp_steps[idx] = state

    def generate_arp(self):
        file_path = self.save_file_dialog("arp.mid")
        if file_path:
            notes = generate_arp(self.get_settings())
            export_midi(notes, file_path)
            QMessageBox.information(self, "Success", f"Saved to {file_path}")

    def generate_bass(self):
        file_path = self.save_file_dialog("bass.mid")
        if file_path:
            notes = generate_bass(self.get_settings())
            export_midi(notes, file_path)
            QMessageBox.information(self, "Success", f"Saved to {file_path}")

    def generate_chords(self):
        file_path = self.save_file_dialog("chords.mid")
        if file_path:
            notes = generate_chords(self.get_settings())
            export_midi(notes, file_path)
            QMessageBox.information(self, "Success", f"Saved to {file_path}")

    def generate_pads(self):
        file_path = self.save_file_dialog("pads.mid")
        if not file_path:
            return

        settings = self.get_settings()

        root = NOTE_MAP[settings["key"]]
        scale = SCALES[settings["scale"]]
        notes = []

        mood = settings.get("mood", "dreamy")
        density = settings.get("pad_density", "triad")
        evolve = settings.get("pad_evolve", "off")

        progression_type = settings.get("pad_progression", "ambient")
        if progression_type not in PAD_PROGRESSIONS:
            progression_type = "ambient"

        progression = random.choice(PAD_PROGRESSIONS[progression_type])

        for bar in range(settings["bars"]):
            degree = progression[bar % len(progression)]
            base = root + scale[degree]

            if density == "triad":
                chord = [
                    base,
                    root + scale[(degree + 2) % len(scale)],
                    root + scale[(degree + 4) % len(scale)],
                ]
            elif density == "7th":
                chord = [
                    base,
                    root + scale[(degree + 2) % len(scale)],
                    root + scale[(degree + 4) % len(scale)],
                    root + scale[(degree + 6) % len(scale)],
                ]
            else:
                chord = [
                    base,
                    root + scale[(degree + 1) % len(scale)],
                    root + scale[(degree + 2) % len(scale)],
                    root + scale[(degree + 4) % len(scale)],
                    base + 12,
                ]

            if evolve != "off":
                if evolve == "slow" and bar % 2 == 0:
                    chord = [n + random.choice([0, 12]) for n in chord]
                elif evolve == "medium":
                    chord = [n + random.choice([0, 12, -12]) for n in chord]

            duration = 1920

            for note in chord:
                if settings.get("velocity_mode") == "fixed":
                    velocity = settings.get("velocity", 90)
                else:
                    if mood == "dreamy":
                        base_vel = 80
                    elif mood == "dark":
                        base_vel = 60
                    else:
                        base_vel = 70

                    velocity = int(base_vel + (bar * 2) % 20)
                    velocity = max(40, min(110, velocity))

                notes.append((note, duration, velocity))

        export_midi(notes, file_path)
        QMessageBox.information(self, "Success", f"Pads saved to {file_path}")

    def generate_lead(self):
        file_path = self.save_file_dialog("lead.mid")
        if file_path:
            notes = generate_lead(self.get_settings())
            export_midi(notes, file_path)
            QMessageBox.information(self, "Success", f"Saved to {file_path}")

    def generate_full(self):
        file_path = self.save_file_dialog("full_track.mid")
        if file_path:
            settings = self.get_settings()

            mid = MidiFile()

            bass_track = MidiTrack()
            chords_track = MidiTrack()
            pads_track = MidiTrack()
            lead_track = MidiTrack()

            mid.tracks.append(bass_track)
            mid.tracks.append(chords_track)
            mid.tracks.append(pads_track)
            mid.tracks.append(lead_track)

            for note, duration, velocity in generate_bass(settings):
                bass_track.append(Message('note_on', note=note, velocity=velocity, time=0))
                bass_track.append(Message('note_off', note=note, velocity=velocity, time=duration))

            chord_notes = generate_chords(settings)

            i = 0
            while i < len(chord_notes):
                base_duration = chord_notes[i][1]
                group = []

                j = i
                while j < len(chord_notes) and chord_notes[j][1] == base_duration:
                    group.append(chord_notes[j])
                    j += 1

                for note, duration, velocity in group:
                    chords_track.append(Message('note_on', note=note, velocity=velocity, time=0))

                for k, (note, duration, velocity) in enumerate(group):
                    chords_track.append(Message('note_off', note=note, velocity=velocity, time=duration if k == 0 else 0))

                i = j

            for note, duration, velocity in generate_pads(settings):
                pads_track.append(Message('note_on', note=note, velocity=velocity, time=0))
                pads_track.append(Message('note_off', note=note, velocity=velocity, time=duration))

            for note, duration, velocity in generate_lead(settings):
                lead_track.append(Message('note_on', note=note, velocity=velocity, time=0))
                lead_track.append(Message('note_off', note=note, velocity=velocity, time=duration))

            mid.save(file_path)

            QMessageBox.information(self, "Success", f"Full track saved to {file_path}")

# ===============================
# RUN
# ===============================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GeneratorApp()
    window.show()
    sys.exit(app.exec_())
# ===============================
# ARP GENERATOR (UPGRADED)
# ===============================
def generate_arp(settings):
    step_mask = settings.get("arp_steps", [True]*16)
    root = NOTE_MAP[settings["key"]] + 12
    scale = SCALES[settings["scale"]]

    pattern = settings.get("arp_pattern", "up")
    velocity_mode = settings.get("arp_velocity_mode", "random")
    fixed_velocity = settings.get("arp_velocity", 90)

    notes = []
    steps = settings["bars"] * 16

    # 🔥 chord progression follow (same logic as chords)
    progression_type = settings.get("genre", "standard")
    if progression_type not in PROGRESSIONS:
        progression_type = "standard"

    progression = random.choice(PROGRESSIONS[progression_type])

    for step in range(steps):
        if not step_mask[step % 16]:
            continue
        bar = step // 16
        degree_root = progression[bar % len(progression)]

        # build chord per step
        chord = [
            root + scale[degree_root % len(scale)],
            root + scale[(degree_root + 2) % len(scale)],
            root + scale[(degree_root + 4) % len(scale)]
        ]

        if pattern == "random":
            note = root + random.choice(scale)

        elif pattern == "chord":
            note = chord[step % len(chord)]

        else:
            degree = step % len(scale)

            if pattern == "down":
                degree = (-step) % len(scale)
            elif pattern == "up_down":
                cycle = step % (len(scale) * 2)
                if cycle < len(scale):
                    degree = cycle
                else:
                    degree = len(scale) - (cycle - len(scale)) - 1

            note = root + scale[degree]

        # velocity control
        if velocity_mode == "fixed":
            velocity = int(fixed_velocity)
        else:
            velocity = random.randint(70, 110)

        duration = random.choice([60, 120])

        notes.append((note, duration, velocity))

    return notes

