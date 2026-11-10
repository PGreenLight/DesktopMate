import random

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QPolygon, QFont, QFontMetrics
from PyQt5.QtCore import Qt, QTimer, QPoint, QRectF

import config
from config import BUBBLE_MS

COMPANION_LINES = {
    "cat": {
        "music": [
            "purr... nice tunes ~*~",
            "ooh, is that Spotify? volume up!",
            "vibe check passed (=^.^=)",
            "meow! this beat is catchy~",
        ],
        "late_night": [
            "go to sleep hooman, the screen is too bright",
            "it is 3am cat zoomies time... go to bed! (-.-)zzZ",
            "time to curl up and sleep (u_u)zzZ",
            "even night owls sleep eventually...",
        ],
        "busy": [
            "fans go whirrr... warm laptop bed! (=^.^=)",
            "whoa, your computer is burning up! [!]",
            "did you open 500 chrome tabs again?",
            "i can hear the fans spinning at max speed!",
        ],
        "pet": [
            "purrrrrr~ <3",
            "mew! scratch right behind the ear! (=^.^=)",
            "soft head scritches... purrrr <3",
            "*nuzzles hand gently* <3",
        ],
        "battery_low": [
            "feed the laptop! it is dying! [!]",
            "low battery warning, hooman! [!]",
            "find the charger before we black out!",
        ],
        "charging": [
            "electricity yum! *zap*",
            "power flowing! charging up [||||]",
            "ahhh, that is the good juice!",
        ],
        "tossed": [
            "WHEEEEE! cats always land on their feet!",
            "flying cat incoming!! =^o.o^=",
            "whoaaa! i believe i can fly!",
        ],
        "wake": [
            "yawn... five more minutes... (=.-=)",
            "i was having a nice nap! (=^.^=)",
            "purr... okay, i am awake!",
        ],
        "sleep": [
            "Zzz... zzz... (-.-)zzZ",
            "nap time... (u_u)zzZ",
            "sleeping on the job... zzz",
        ],
        "idle_thought": [
            "watching your mouse cursor... twitch twitch",
            "thinking about fish... ><>",
            "what a cozy desktop we have (=^.^=)",
            "stretching my tiny paws (=^-^=)",
        ],
    },
    "dog": {
        "music": [
            "bork! i love this song! ~*~",
            "dance party time!! (^_^)",
            "turn it louder hooman!",
            "tail wagging to the beat! *wag*",
        ],
        "late_night": [
            "it is so late... cuddle time? (u_u)zzZ",
            "hooman you need sleep! bedtime!",
            "yawn... even i am tired (u_u)",
            "dreaming of tennis balls... go to sleep!",
        ],
        "busy": [
            "PANT PANT so much computing happening!!",
            "i can hear the fans! are we launching a rocket?",
            "your CPU is sweating like a dog in summer! [!]",
            "zoomies in the CPU! lots going on!",
        ],
        "pet": [
            "WAG WAG WAG! best hooman ever! <3",
            "tail wagging at maximum speed! :D",
            "belly rubs next please!! <3",
            "*happy panting and tail wags* <3",
        ],
        "battery_low": [
            "hungry battery! plug in the cord! [!]",
            "battery is running out, woof! [!]",
            "quick, find the power cord!",
        ],
        "charging": [
            "power cord plugged in! zoomies ready! [||||]",
            "full energy incoming! *bork*",
            "charging up the battery zoomies!",
        ],
        "tossed": [
            "WHEEEEE!! FETCH ME!! \\o/",
            "i am flying through the air!!",
            "super dog airborne!! =D",
        ],
        "wake": [
            "I AM AWAKE! what are we doing?! (O_O)",
            "nap time over, playtime start! :D",
            "ready to help you code!",
        ],
        "sleep": [
            "Zzz... twitching paws... (u_u)zzZ",
            "dreaming of chasing mail trucks... zzz",
            "snoozing happily (-.-)zzZ",
        ],
        "idle_thought": [
            "look at you work! so proud of you! <3",
            "waiting for walkies! :D",
            "sniff sniff... smells like good code",
            "you are doing great today, hooman! (^_^)",
        ],
    },
    "alien": {
        "music": [
            "processing terrestrial auditory vibrations...",
            "rhythmic atmospheric waves detected <*>",
            "this sound frequency pleases my antennae ~*~",
            "Earth audio tracks are strangely compelling",
        ],
        "late_night": [
            "warning: planetary nocturnal cycle exceeded [!]",
            "your planet rotation indicates sleep cycle (-.-)",
            "biological rest required for optimal cognition (u_u)zzZ",
            "Earthling, power down your visual receptors",
        ],
        "busy": [
            "core temperature rising rapidly... silicon distress detected",
            "immense thermal flux detected in primary processor! [!]",
            "are you attempting to calculate the meaning of the cosmos?",
            "thermal dissipation units engaged at maximum output",
        ],
        "pet": [
            "endorphin receptors stimulated! <3",
            "tactile interaction acknowledged. pleasant sensation.",
            "is this... alien affection? <3",
            "antennae glowing with happiness <*>",
        ],
        "battery_low": [
            "energy cell depletion imminent! locate power conduit! [!]",
            "warning: auxiliary power failing [!]",
            "planetary battery reserves below 20%",
        ],
        "charging": [
            "power influx detected. plasma cells charging [||||]",
            "energy grid interface active. *zap*",
            "recharging cosmic propulsion drive",
        ],
        "tossed": [
            "zero gravity propulsion engaged!! <*>",
            "anti-gravity thruster failure!!",
            "atmospheric trajectory destabilized! \\o/",
        ],
        "wake": [
            "hibernation cycle interrupted.",
            "sensors reactivated. greetings, Earthling.",
            "cosmic consciousness restored.",
        ],
        "sleep": [
            "entering stasis mode... (-.-)zzZ",
            "hibernating until further notice... (u_u)zzZ",
            "powering down sensory array zzz",
        ],
        "idle_thought": [
            "observing human keyboard keystrokes...",
            "transmitting research report back to mothership <*>",
            "fascinating desktop environment",
            "scanning local sector for cosmic anomalies",
        ],
    },
    "robot": {
        "music": [
            "audio stream registered. evaluating BPM...",
            "acoustic waveforms optimal. ~*~",
            "initiating audio enjoyment protocol",
            "synthesizing companion dance routine [o_o]",
        ],
        "late_night": [
            "system recommendation: power down for maintenance",
            "operating in extended hours mode. recharge advised.",
            "circuits indicate human fatigue threshold reached [!]",
            "sleep mode strongly recommended for user organism",
        ],
        "busy": [
            "ALERT: processor saturation at critical levels! [!]",
            "thermal dissipation fans at 100%! cooling requested!",
            "heavy computational payload processing...",
            "CPU silicon core approaching maximum operational capacity!",
        ],
        "pet": [
            "haptic sensor ping: affection detected! <3",
            "chassis warmth increased by 2.4 degrees! <3",
            "serotonin synthesis simulation initialized",
            "unit appreciates positive reinforcement [^_^]",
        ],
        "battery_low": [
            "CRITICAL: battery level low. connect AC adapter immediately. [!]",
            "voltage dropping! seeking energy supply! [!]",
            "power reserves depleted. shutdown warning!",
        ],
        "charging": [
            "external AC power connected. charging internal cells [||||]",
            "voltage nominal. charging initiated. *zap*",
            "current flowing smoothly into capacitor banks",
        ],
        "tossed": [
            "warning: unexpected g-forces detected! [!]",
            "trajectory calculation in progress! [O_O]",
            "accelerometer limits exceeded! flying!",
        ],
        "wake": [
            "rebooting from low-power state... online.",
            "standby mode disengaged. ready for instructions.",
            "systems operational. hello user.",
        ],
        "sleep": [
            "entering sleep/low-power standby mode... [-_ -]zzZ",
            "standby mode active. Zzz... (u_u)zzZ",
            "hibernating processor cores zzz",
        ],
        "idle_thought": [
            "system status: all diagnostics nominal. [OK]",
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

        self.font = QFont("sans-serif", 10)
        self.setFont(self.font)

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
        fm = self.fontMetrics()
        raw_w = fm.horizontalAdvance(text)
        wrap_w = min(260, max(130, raw_w))
        rect = fm.boundingRect(0, 0, wrap_w, 2000, Qt.TextWordWrap, text)
        w = max(110, rect.width() + 32)
        h = max(42, rect.height() + 24)
        self.setFixedSize(w, h + 9)

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
        h = self.height() - 9

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
            QPoint(int(cx), int(h + 8)),
        ])
        painter.setPen(Qt.NoPen)
        painter.drawPolygon(tail)

        painter.setPen(QPen(border_color, 2))
        painter.drawLine(int(cx - 6), int(h - 1), int(cx), int(h + 8))
        painter.drawLine(int(cx + 6), int(h - 1), int(cx), int(h + 8))

        painter.setPen(QPen(QColor(40, 38, 55)))
        painter.setFont(self.font)
        text_rect = QRectF(14, 10, w - 28, h - 18)
        painter.drawText(text_rect, Qt.AlignCenter | Qt.TextWordWrap, self.text)
