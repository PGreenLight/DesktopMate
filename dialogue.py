import random

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QPolygon, QFont
from PyQt5.QtCore import Qt, QTimer, QPoint, QRectF

import config
from config import BUBBLE_MS

COMPANION_LINES = {
    "cat": {
        "music": [
            "purr... nice tunes 🎵",
            "ooh, is that Spotify? volume up!",
            "vibe check passed 🐾",
            "meow! this beat is catchy~",
        ],
        "late_night": [
            "go to sleep hooman, the screen is too bright",
            "it's 3am cat zoomies time... go to bed! 💤",
            "time to curl up and sleep 💤",
            "even night owls sleep eventually...",
        ],
        "busy": [
            "fans go whirrr... warm laptop bed! 🐾",
            "whoa, your computer is burning up!",
            "did you open 500 chrome tabs again?",
            "i can hear the fans spinning at max speed!",
        ],
        "pet": [
            "purrrrrr~ ❤️",
            "mew! scratch right behind the ear!",
            "soft head scritches... purrrr ❤️",
            "*nuzzles hand gently* ❤️",
        ],
        "battery_low": [
            "feed the laptop! it's dying! 🪫",
            "low battery warning, hooman!",
            "find the charger before we black out! 🪫",
        ],
        "charging": [
            "electricity yum! ⚡",
            "power flowing! charging up ⚡",
            "ahhh, that's the good juice!",
        ],
        "tossed": [
            "WHEEEEE! cats always land on their feet!",
            "flying cat incoming!!",
            "whoaaa! i believe i can fly!",
        ],
        "wake": [
            "yawn... five more minutes... 🐾",
            "i was having a nice nap!",
            "purr... okay, i'm awake!",
        ],
        "sleep": [
            "Zzz... zzz... 💤",
            "nap time... 💤",
            "sleeping on the job... zzz",
        ],
        "idle_thought": [
            "watching your mouse cursor... twitch twitch",
            "thinking about fish... 🐟",
            "what a cozy desktop we have",
            "stretching my tiny paws 🐾",
        ],
    },
    "dog": {
        "music": [
            "bork! i love this song! 🎶",
            "dance party time!! 🐶",
            "turn it louder hooman! 🎵",
            "tail wagging to the beat! 🐾",
        ],
        "late_night": [
            "it's so late... cuddle time? 💤",
            "hooman you need sleep! bedtime!",
            "yawn... even i'm tired 🦴",
            "dreaming of tennis balls... go to sleep!",
        ],
        "busy": [
            "PANT PANT so much computing happening!!",
            "i can hear the fans! are we launching a rocket?",
            "your CPU is sweating like a dog in summer!",
            "zoomies in the CPU! lots going on!",
        ],
        "pet": [
            "WAG WAG WAG! best hooman ever! ❤️",
            "tail wagging at maximum speed! 🐶",
            "belly rubs next please!! ❤️",
            "*happy panting and tail wags* ❤️",
        ],
        "battery_low": [
            "hungry battery! plug in the cord! 🪫",
            "battery is running out, woof! 🪫",
            "quick, find the power bone!",
        ],
        "charging": [
            "power cord plugged in! zoomies ready! ⚡",
            "full energy incoming! ⚡",
            "charging up the battery zoomies!",
        ],
        "tossed": [
            "WHEEEEE!! FETCH ME!! 🐶",
            "i'm flying through the air!!",
            "super dog airborne!!",
        ],
        "wake": [
            "I'M AWAKE! what are we doing?! 🐶",
            "nap time over, playtime start!",
            "ready to help you code!",
        ],
        "sleep": [
            "Zzz... twitching paws... 💤",
            "dreaming of chasing mail trucks... 💤",
            "snoozing happily 💤",
        ],
        "idle_thought": [
            "look at you work! so proud of you! 🦴",
            "waiting for walkies!",
            "sniff sniff... smells like good code",
            "you're doing great today, hooman! 🐾",
        ],
    },
    "alien": {
        "music": [
            "processing terrestrial auditory vibrations...",
            "rhythmic atmospheric waves detected 🛸",
            "this sound frequency pleases my antennae 🎵",
            "Earth audio tracks are strangely compelling",
        ],
        "late_night": [
            "warning: planetary nocturnal cycle exceeded",
            "your planet's rotation indicates sleep cycle 🛸",
            "biological rest required for optimal cognition 💤",
            "Earthling, power down your visual receptors",
        ],
        "busy": [
            "core temperature rising rapidly... silicon distress detected",
            "immense thermal flux detected in primary processor!",
            "are you attempting to calculate the meaning of the cosmos?",
            "thermal dissipation units engaged at maximum output",
        ],
        "pet": [
            "endorphin receptors stimulated! ❤️",
            "tactile interaction acknowledged. pleasant sensation.",
            "is this... alien affection? 🛸 ❤️",
            "antennae glowing with happiness ❤️",
        ],
        "battery_low": [
            "energy cell depletion imminent! locate power conduit! 🪫",
            "warning: auxiliary power failing 🪫",
            "planetary battery reserves below 20%",
        ],
        "charging": [
            "power influx detected. plasma cells charging ⚡",
            "energy grid interface active. ⚡",
            "recharging cosmic propulsion drive",
        ],
        "tossed": [
            "zero gravity propulsion engaged!! 🛸",
            "anti-gravity thruster failure!!",
            "atmospheric trajectory destabilized!",
        ],
        "wake": [
            "hibernation cycle interrupted.",
            "sensors reactivated. greetings, Earthling.",
            "cosmic consciousness restored.",
        ],
        "sleep": [
            "entering stasis mode... 💤",
            "hibernating until further notice... 💤",
            "powering down sensory array 💤",
        ],
        "idle_thought": [
            "observing human keyboard keystrokes...",
            "transmitting research report back to mothership 🛸",
            "fascinating desktop environment",
            "scanning local sector for cosmic anomalies",
        ],
    },
    "robot": {
        "music": [
            "audio stream registered. evaluating BPM...",
            "acoustic waveforms optimal. 🎵",
            "initiating audio enjoyment protocol",
            "synthesizing companion dance routine 🎶",
        ],
        "late_night": [
            "system recommendation: power down for maintenance",
            "operating in extended hours mode. recharge advised.",
            "circuits indicate human fatigue threshold reached 💤",
            "sleep mode strongly recommended for user organism",
        ],
        "busy": [
            "ALERT: processor saturation at critical levels!",
            "thermal dissipation fans at 100%! cooling requested!",
            "heavy computational payload processing...",
            "CPU silicon core approaching maximum operational capacity!",
        ],
        "pet": [
            "haptic sensor ping: affection detected! ❤️",
            "chassis warmth increased by 2.4 degrees! ❤️",
            "serotonin synthesis simulation initialized",
            "unit appreciates positive reinforcement ❤️",
        ],
        "battery_low": [
            "CRITICAL: battery level low. connect AC adapter immediately. 🪫",
            "voltage dropping! seeking energy supply! 🪫",
            "power reserves depleted. shutdown warning!",
        ],
        "charging": [
            "external AC power connected. charging internal cells ⚡",
            "voltage nominal. charging initiated. ⚡",
            "current flowing smoothly into capacitor banks",
        ],
        "tossed": [
            "warning: unexpected g-forces detected!",
            "trajectory calculation in progress! 🤖",
            "accelerometer limits exceeded! flying!",
        ],
        "wake": [
            "rebooting from low-power state... online.",
            "standby mode disengaged. ready for instructions.",
            "systems operational. hello user.",
        ],
        "sleep": [
            "entering sleep/low-power standby mode... 💤",
            "standby mode active. Zzz... 💤",
            "hibernating processor cores 💤",
        ],
        "idle_thought": [
            "system status: all diagnostics nominal.",
            "background calculations running smoothly.",
            "memory index optimized.",
            "scanning for pending tasks... idle.",
        ],
    },
}


def pick_line(event, companion=None):
    comp = str(companion or config.COMPANION).lower()
    pool = COMPANION_LINES.get(comp, COMPANION_LINES["cat"]).get(event)
    if not pool:
        pool = COMPANION_LINES["cat"].get(event)
    return random.choice(pool) if pool else None


class SpeechBubble(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
            | Qt.X11BypassWindowManagerHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)

        self.text = ""
        self._hide_timer = QTimer(self)
        self._hide_timer.setSingleShot(True)
        self._hide_timer.timeout.connect(self.hide)

    def reposition(self, anchor):
        ax = anchor.x() + anchor.width() // 2 - self.width() // 2
        ay = anchor.y() - self.height() - 4
        self.move(ax, max(0, ay))

    def show_text(self, text, anchor):
        self.text = text
        font = QFont("Sans-Serif", 10)
        fm = self.fontMetrics()
        lines = text.split("\n")
        max_w = min(220, max(fm.horizontalAdvance(line) for line in lines) + 24)
        rect = fm.boundingRect(0, 0, max_w - 20, 1000, Qt.TextWordWrap, text)
        w = max(90, rect.width() + 24)
        h = max(38, rect.height() + 22)
        self.setFixedSize(w, h + 8)

        self.reposition(anchor)
        self.show()
        self.raise_()
        self.update()
        self._hide_timer.start(BUBBLE_MS)

    def paintEvent(self, event):
        if not self.text:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        w = self.width()
        h = self.height() - 8

        body_rect = QRectF(1.5, 1.5, w - 3, h - 3)

        bg_color = QColor(255, 255, 255, 245)
        border_color = QColor(120, 175, 235, 255)

        painter.setBrush(QBrush(bg_color))
        painter.setPen(QPen(border_color, 2))
        painter.drawRoundedRect(body_rect, 10, 10)

        cx = w / 2.0
        tail = QPolygon([
            QPoint(int(cx - 6), int(h - 1)),
            QPoint(int(cx + 6), int(h - 1)),
            QPoint(int(cx), int(h + 7)),
        ])
        painter.setPen(Qt.NoPen)
        painter.drawPolygon(tail)

        painter.setPen(QPen(border_color, 2))
        painter.drawLine(int(cx - 6), int(h - 1), int(cx), int(h + 7))
        painter.drawLine(int(cx + 6), int(h - 1), int(cx), int(h + 7))

        painter.setPen(QPen(QColor(40, 38, 55)))
        font = QFont("Sans-Serif", 10)
        painter.setFont(font)
        text_rect = QRectF(10, 6, w - 20, h - 12)
        painter.drawText(text_rect, Qt.AlignCenter | Qt.TextWordWrap, self.text)
