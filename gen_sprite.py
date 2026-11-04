from PIL import Image, ImageDraw
from pathlib import Path

from config import SPRITE_SIZE, ASSETS
from states import STATES

COLS = max(s["frame_count"] for s in STATES.values())
ROWS = max(s["row"] for s in STATES.values()) + 1
ROW_STATE = {spec["row"]: name for name, spec in STATES.items()}

OUTLINE = (38, 34, 54, 255)

CAT_FUR = (255, 238, 218, 255)
CAT_SHADOW = (232, 202, 178, 255)
CAT_HIGHLIGHT = (255, 250, 245, 255)
CAT_EAR_PINK = (255, 168, 185, 255)
CAT_CHEEK = (255, 140, 165, 200)
CAT_EYE = (45, 42, 74, 255)
CAT_GLINT = (255, 255, 255, 255)
CAT_NOSE = (245, 120, 150, 255)
CAT_MOUTH = (210, 75, 110, 255)
CAT_BELL = (255, 205, 55, 255)
CAT_COLLAR = (235, 65, 85, 255)

DOG_FUR = (226, 162, 102, 255)
DOG_SHADOW = (186, 126, 74, 255)
DOG_HIGHLIGHT = (248, 196, 145, 255)
DOG_EAR = (150, 92, 50, 255)
DOG_EAR_SHADOW = (120, 70, 36, 255)
DOG_CHEEK = (240, 130, 120, 200)
DOG_EYE = (35, 30, 48, 255)
DOG_NOSE = (40, 35, 45, 255)
DOG_TONGUE = (255, 120, 145, 255)
DOG_COLLAR = (65, 140, 245, 255)
DOG_TAG = (255, 220, 70, 255)

ALIEN_SKIN = (145, 225, 95, 255)
ALIEN_SHADOW = (105, 180, 65, 255)
ALIEN_HIGHLIGHT = (185, 245, 145, 255)
ALIEN_BLUSH = (120, 210, 160, 200)
ALIEN_ORB = (70, 230, 245, 255)
ALIEN_ORB_GLOW = (160, 245, 255, 255)
ALIEN_EYE = (28, 20, 48, 255)
ALIEN_GLINT1 = (255, 255, 255, 255)
ALIEN_GLINT2 = (180, 120, 255, 255)
ALIEN_SUIT = (120, 105, 185, 255)
ALIEN_SUIT_DARK = (85, 72, 145, 255)
ALIEN_BELT = (255, 205, 65, 255)

ROBOT_METAL = (195, 205, 220, 255)
ROBOT_SHADOW = (145, 155, 175, 255)
ROBOT_HIGHLIGHT = (235, 242, 250, 255)
ROBOT_DARK = (55, 62, 78, 255)
ROBOT_SCREEN = (25, 32, 45, 255)
ROBOT_CYAN = (60, 235, 245, 255)
ROBOT_CYAN_OFF = (30, 110, 125, 255)
ROBOT_LIGHT_RED = (255, 85, 95, 255)
ROBOT_LIGHT_YELLOW = (255, 215, 65, 255)
ROBOT_ANTENNA = (255, 95, 105, 255)


def draw_cat(p, ox, oy, state, col):
    def set_px(x, y, color):
        if 0 <= x < SPRITE_SIZE and 0 <= y < SPRITE_SIZE and color:
            p[ox + x, oy + y] = color

    def fill_rect(x1, y1, x2, y2, color):
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                set_px(x, y, color)

    bob = [0, 1, 0, -1][col % 4] if state in ("idle", "talk") else 0
    tail_phase = col % 4

    if state == "idle":
        by = 13 + bob
        tail_x = 21 + (1 if tail_phase in (1, 2) else 0)
        tail_y = 20 + bob
        set_px(tail_x + 1, tail_y - 2, OUTLINE)
        set_px(tail_x + 2, tail_y - 1, OUTLINE)
        set_px(tail_x + 2, tail_y, CAT_FUR)
        set_px(tail_x + 1, tail_y + 1, CAT_FUR)
        set_px(tail_x + 3, tail_y - 1, CAT_SHADOW)

        fill_rect(10, by + 7, 21, by + 12, CAT_FUR)
        fill_rect(11, by + 11, 21, by + 12, CAT_SHADOW)
        for x in range(10, 22):
            set_px(x, by + 13, OUTLINE)
        set_px(9, by + 8, OUTLINE)
        set_px(9, by + 9, OUTLINE)
        set_px(9, by + 10, OUTLINE)
        set_px(22, by + 8, OUTLINE)
        set_px(22, by + 9, OUTLINE)
        set_px(22, by + 10, OUTLINE)

        set_px(11, by + 12, CAT_HIGHLIGHT)
        set_px(12, by + 12, CAT_HIGHLIGHT)
        set_px(19, by + 12, CAT_HIGHLIGHT)
        set_px(20, by + 12, CAT_HIGHLIGHT)

        fill_rect(12, by + 7, 19, by + 7, CAT_COLLAR)
        set_px(15, by + 8, CAT_BELL)
        set_px(16, by + 8, CAT_BELL)

        fill_rect(8, by, 23, by + 6, CAT_FUR)
        fill_rect(9, by - 1, 22, by, CAT_FUR)
        fill_rect(8, by + 5, 23, by + 6, CAT_SHADOW)

        for x in range(11, 21):
            set_px(x, by - 2, OUTLINE)
        for y in range(by, by + 6):
            set_px(7, y, OUTLINE)
            set_px(24, y, OUTLINE)
        set_px(8, by + 6, OUTLINE)
        set_px(23, by + 6, OUTLINE)

        set_px(8, by - 3, OUTLINE)
        set_px(9, by - 4, OUTLINE)
        set_px(10, by - 5, OUTLINE)
        set_px(11, by - 4, OUTLINE)
        fill_rect(9, by - 3, 10, by - 2, CAT_FUR)
        set_px(10, by - 3, CAT_EAR_PINK)

        set_px(23, by - 3, OUTLINE)
        set_px(22, by - 4, OUTLINE)
        set_px(21, by - 5, OUTLINE)
        set_px(20, by - 4, OUTLINE)
        fill_rect(21, by - 3, 22, by - 2, CAT_FUR)
        set_px(21, by - 3, CAT_EAR_PINK)

        set_px(9, by + 4, CAT_CHEEK)
        set_px(10, by + 4, CAT_CHEEK)
        set_px(21, by + 4, CAT_CHEEK)
        set_px(22, by + 4, CAT_CHEEK)

        if col == 3:
            set_px(11, by + 2, OUTLINE)
            set_px(12, by + 1, OUTLINE)
            set_px(13, by + 2, OUTLINE)
            set_px(18, by + 2, OUTLINE)
            set_px(19, by + 1, OUTLINE)
            set_px(20, by + 2, OUTLINE)
        else:
            fill_rect(11, by + 1, 13, by + 3, CAT_EYE)
            set_px(11, by + 1, CAT_GLINT)
            fill_rect(18, by + 1, 20, by + 3, CAT_EYE)
            set_px(18, by + 1, CAT_GLINT)

        set_px(15, by + 3, CAT_NOSE)
        set_px(16, by + 3, CAT_NOSE)
        set_px(15, by + 4, OUTLINE)
        set_px(16, by + 4, OUTLINE)

    elif state == "talk":
        by = 13 + bob
        fill_rect(10, by + 7, 21, by + 12, CAT_FUR)
        fill_rect(11, by + 11, 21, by + 12, CAT_SHADOW)
        for x in range(10, 22):
            set_px(x, by + 13, OUTLINE)
        set_px(9, by + 8, OUTLINE)
        set_px(22, by + 8, OUTLINE)

        fill_rect(12, by + 7, 19, by + 7, CAT_COLLAR)
        set_px(15, by + 8, CAT_BELL)
        set_px(16, by + 8, CAT_BELL)

        fill_rect(8, by, 23, by + 6, CAT_FUR)
        fill_rect(9, by - 1, 22, by, CAT_FUR)
        fill_rect(8, by + 5, 23, by + 6, CAT_SHADOW)

        for x in range(11, 21):
            set_px(x, by - 2, OUTLINE)
        for y in range(by, by + 6):
            set_px(7, y, OUTLINE)
            set_px(24, y, OUTLINE)

        set_px(8, by - 3, OUTLINE)
        set_px(9, by - 4, OUTLINE)
        set_px(10, by - 5, OUTLINE)
        set_px(11, by - 4, OUTLINE)
        fill_rect(9, by - 3, 10, by - 2, CAT_FUR)
        set_px(10, by - 3, CAT_EAR_PINK)

        set_px(23, by - 3, OUTLINE)
        set_px(22, by - 4, OUTLINE)
        set_px(21, by - 5, OUTLINE)
        set_px(20, by - 4, OUTLINE)
        fill_rect(21, by - 3, 22, by - 2, CAT_FUR)
        set_px(21, by - 3, CAT_EAR_PINK)

        set_px(15, by + 3, CAT_NOSE)
        set_px(16, by + 3, CAT_NOSE)
        if col % 2 == 1:
            fill_rect(14, by + 4, 17, by + 6, CAT_MOUTH)
            set_px(14, by + 4, OUTLINE)
            set_px(17, by + 4, OUTLINE)
            set_px(15, by + 6, OUTLINE)
            set_px(16, by + 6, OUTLINE)
        else:
            set_px(14, by + 4, OUTLINE)
            set_px(15, by + 5, OUTLINE)
            set_px(16, by + 5, OUTLINE)
            set_px(17, by + 4, OUTLINE)

        set_px(11, by + 2, OUTLINE)
        set_px(12, by + 1, OUTLINE)
        set_px(13, by + 2, OUTLINE)
        set_px(18, by + 2, OUTLINE)
        set_px(19, by + 1, OUTLINE)
        set_px(20, by + 2, OUTLINE)

        set_px(9, by + 4, CAT_CHEEK)
        set_px(10, by + 4, CAT_CHEEK)
        set_px(21, by + 4, CAT_CHEEK)
        set_px(22, by + 4, CAT_CHEEK)

    elif state == "grabbed":
        by = 8
        set_px(15, by - 3, OUTLINE)
        set_px(16, by - 3, OUTLINE)

        fill_rect(9, by, 22, by + 6, CAT_FUR)
        for x in range(11, 21):
            set_px(x, by - 2, OUTLINE)
        for y in range(by, by + 6):
            set_px(8, y, OUTLINE)
            set_px(23, y, OUTLINE)

        set_px(7, by - 1, OUTLINE)
        set_px(6, by - 2, OUTLINE)
        set_px(7, by - 3, OUTLINE)
        set_px(8, by - 2, CAT_EAR_PINK)

        set_px(24, by - 1, OUTLINE)
        set_px(25, by - 2, OUTLINE)
        set_px(24, by - 3, OUTLINE)
        set_px(23, by - 2, CAT_EAR_PINK)

        fill_rect(10, by + 1, 13, by + 4, CAT_EYE)
        set_px(11, by + 1, CAT_GLINT)
        fill_rect(18, by + 1, 21, by + 4, CAT_EYE)
        set_px(19, by + 1, CAT_GLINT)

        set_px(15, by + 3, CAT_NOSE)
        set_px(16, by + 3, CAT_NOSE)
        set_px(15, by + 5, CAT_MOUTH)
        set_px(16, by + 5, CAT_MOUTH)

        fill_rect(11, by + 7, 20, by + 16, CAT_FUR)
        fill_rect(12, by + 14, 19, by + 16, CAT_SHADOW)
        for y in range(by + 7, by + 17):
            set_px(10, y, OUTLINE)
            set_px(21, y, OUTLINE)
        for x in range(11, 21):
            set_px(x, by + 17, OUTLINE)

        paw_wobble = -1 if col % 2 == 0 else 1
        set_px(12 + paw_wobble, by + 18, CAT_HIGHLIGHT)
        set_px(13 + paw_wobble, by + 18, OUTLINE)
        set_px(18 - paw_wobble, by + 18, CAT_HIGHLIGHT)
        set_px(19 - paw_wobble, by + 18, OUTLINE)

    elif state == "falling":
        by = 7
        set_px(10, by - 5, OUTLINE)
        set_px(11, by - 6, OUTLINE)
        set_px(12, by - 5, OUTLINE)
        set_px(11, by - 4, CAT_EAR_PINK)

        set_px(21, by - 5, OUTLINE)
        set_px(20, by - 6, OUTLINE)
        set_px(19, by - 5, OUTLINE)
        set_px(20, by - 4, CAT_EAR_PINK)

        fill_rect(9, by - 1, 22, by + 6, CAT_FUR)
        for y in range(by, by + 6):
            set_px(8, y, OUTLINE)
            set_px(23, y, OUTLINE)

        fill_rect(10, by + 1, 13, by + 4, CAT_EYE)
        fill_rect(18, by + 1, 21, by + 4, CAT_EYE)
        set_px(10, by + 1, CAT_GLINT)
        set_px(18, by + 1, CAT_GLINT)

        set_px(7, by + 2, (120, 200, 255, 255))
        set_px(24, by + 2, (120, 200, 255, 255))

        fill_rect(14, by + 4, 17, by + 7, CAT_MOUTH)
        set_px(14, by + 4, OUTLINE)
        set_px(17, by + 4, OUTLINE)
        set_px(15, by + 7, OUTLINE)
        set_px(16, by + 7, OUTLINE)

        fill_rect(10, by + 8, 21, by + 15, CAT_FUR)
        if col % 2 == 0:
            set_px(7, by + 8, CAT_HIGHLIGHT)
            set_px(6, by + 7, OUTLINE)
            set_px(24, by + 8, CAT_HIGHLIGHT)
            set_px(25, by + 7, OUTLINE)
        else:
            set_px(7, by + 10, CAT_HIGHLIGHT)
            set_px(6, by + 11, OUTLINE)
            set_px(24, by + 10, CAT_HIGHLIGHT)
            set_px(25, by + 11, OUTLINE)


def draw_dog(p, ox, oy, state, col):
    def set_px(x, y, color):
        if 0 <= x < SPRITE_SIZE and 0 <= y < SPRITE_SIZE and color:
            p[ox + x, oy + y] = color

    def fill_rect(x1, y1, x2, y2, color):
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                set_px(x, y, color)

    bob = [0, 1, 0, -1][col % 4] if state in ("idle", "talk") else 0
    tail_wag = [-2, 0, 2, 0][col % 4]

    if state == "idle":
        by = 13 + bob
        tail_x = 21 + tail_wag
        set_px(tail_x + 1, by + 8, OUTLINE)
        set_px(tail_x + 2, by + 7, DOG_EAR)
        set_px(tail_x + 3, by + 6, OUTLINE)
        set_px(tail_x + 2, by + 6, DOG_FUR)

        fill_rect(10, by + 7, 21, by + 12, DOG_FUR)
        fill_rect(11, by + 11, 21, by + 12, DOG_SHADOW)
        for x in range(10, 22):
            set_px(x, by + 13, OUTLINE)
        set_px(9, by + 8, OUTLINE)
        set_px(9, by + 9, OUTLINE)
        set_px(9, by + 10, OUTLINE)
        set_px(22, by + 8, OUTLINE)
        set_px(22, by + 9, OUTLINE)
        set_px(22, by + 10, OUTLINE)

        set_px(11, by + 12, DOG_HIGHLIGHT)
        set_px(12, by + 12, DOG_HIGHLIGHT)
        set_px(19, by + 12, DOG_HIGHLIGHT)
        set_px(20, by + 12, DOG_HIGHLIGHT)

        fill_rect(12, by + 7, 19, by + 7, DOG_COLLAR)
        set_px(15, by + 8, DOG_TAG)
        set_px(16, by + 8, DOG_TAG)

        fill_rect(8, by, 23, by + 6, DOG_FUR)
        fill_rect(9, by - 1, 22, by, DOG_FUR)
        fill_rect(8, by + 5, 23, by + 6, DOG_SHADOW)

        fill_rect(13, by + 2, 18, by + 5, DOG_HIGHLIGHT)

        for x in range(11, 21):
            set_px(x, by - 2, OUTLINE)
        for y in range(by, by + 6):
            set_px(7, y, OUTLINE)
            set_px(24, y, OUTLINE)
        set_px(8, by + 6, OUTLINE)
        set_px(23, by + 6, OUTLINE)

        ear_bob = 1 if col % 2 == 1 else 0
        fill_rect(6, by - 1 + ear_bob, 8, by + 3 + ear_bob, DOG_EAR)
        set_px(5, by + ear_bob, OUTLINE)
        set_px(5, by + 1 + ear_bob, OUTLINE)
        set_px(5, by + 2 + ear_bob, OUTLINE)
        set_px(6, by + 4 + ear_bob, OUTLINE)
        set_px(7, by + 4 + ear_bob, OUTLINE)

        fill_rect(23, by - 1 + ear_bob, 25, by + 3 + ear_bob, DOG_EAR)
        set_px(26, by + ear_bob, OUTLINE)
        set_px(26, by + 1 + ear_bob, OUTLINE)
        set_px(26, by + 2 + ear_bob, OUTLINE)
        set_px(24, by + 4 + ear_bob, OUTLINE)
        set_px(25, by + 4 + ear_bob, OUTLINE)

        if col == 3:
            set_px(10, by + 2, OUTLINE)
            set_px(11, by + 1, OUTLINE)
            set_px(12, by + 2, OUTLINE)
            set_px(19, by + 2, OUTLINE)
            set_px(20, by + 1, OUTLINE)
            set_px(21, by + 2, OUTLINE)
        else:
            fill_rect(10, by + 1, 12, by + 3, DOG_EYE)
            set_px(10, by + 1, (255, 255, 255, 255))
            fill_rect(19, by + 1, 21, by + 3, DOG_EYE)
            set_px(19, by + 1, (255, 255, 255, 255))

        set_px(15, by + 3, DOG_NOSE)
        set_px(16, by + 3, DOG_NOSE)
        set_px(15, by + 4, OUTLINE)
        set_px(16, by + 4, OUTLINE)
        set_px(9, by + 4, DOG_CHEEK)
        set_px(22, by + 4, DOG_CHEEK)

    elif state == "talk":
        by = 13 + bob
        fill_rect(10, by + 7, 21, by + 12, DOG_FUR)
        fill_rect(11, by + 11, 21, by + 12, DOG_SHADOW)
        for x in range(10, 22):
            set_px(x, by + 13, OUTLINE)
        set_px(9, by + 8, OUTLINE)
        set_px(22, by + 8, OUTLINE)

        fill_rect(12, by + 7, 19, by + 7, DOG_COLLAR)
        set_px(15, by + 8, DOG_TAG)
        set_px(16, by + 8, DOG_TAG)

        fill_rect(8, by, 23, by + 6, DOG_FUR)
        fill_rect(9, by - 1, 22, by, DOG_FUR)
        fill_rect(8, by + 5, 23, by + 6, DOG_SHADOW)
        fill_rect(13, by + 2, 18, by + 5, DOG_HIGHLIGHT)

        for x in range(11, 21):
            set_px(x, by - 2, OUTLINE)
        for y in range(by, by + 6):
            set_px(7, y, OUTLINE)
            set_px(24, y, OUTLINE)

        ear_bob = 0 if col % 2 == 1 else 1
        fill_rect(6, by - 1 + ear_bob, 8, by + 3 + ear_bob, DOG_EAR)
        fill_rect(23, by - 1 + ear_bob, 25, by + 3 + ear_bob, DOG_EAR)

        set_px(15, by + 3, DOG_NOSE)
        set_px(16, by + 3, DOG_NOSE)

        if col % 2 == 1:
            fill_rect(14, by + 4, 17, by + 5, (180, 50, 70, 255))
            set_px(15, by + 6, DOG_TONGUE)
            set_px(16, by + 6, DOG_TONGUE)
            set_px(15, by + 7, OUTLINE)
            set_px(16, by + 7, OUTLINE)
        else:
            set_px(14, by + 4, OUTLINE)
            set_px(15, by + 5, OUTLINE)
            set_px(16, by + 5, OUTLINE)
            set_px(17, by + 4, OUTLINE)

        set_px(10, by + 2, OUTLINE)
        set_px(11, by + 1, OUTLINE)
        set_px(12, by + 2, OUTLINE)
        set_px(19, by + 2, OUTLINE)
        set_px(20, by + 1, OUTLINE)
        set_px(21, by + 2, OUTLINE)
        set_px(9, by + 4, DOG_CHEEK)
        set_px(22, by + 4, DOG_CHEEK)

    elif state == "grabbed":
        by = 8
        set_px(15, by - 3, OUTLINE)
        set_px(16, by - 3, OUTLINE)

        fill_rect(9, by, 22, by + 6, DOG_FUR)
        for x in range(11, 21):
            set_px(x, by - 2, OUTLINE)
        for y in range(by, by + 6):
            set_px(8, y, OUTLINE)
            set_px(23, y, OUTLINE)

        fill_rect(6, by + 1, 8, by + 6, DOG_EAR)
        fill_rect(23, by + 1, 25, by + 6, DOG_EAR)

        fill_rect(10, by + 1, 13, by + 4, DOG_EYE)
        set_px(11, by + 1, (255, 255, 255, 255))
        fill_rect(18, by + 1, 21, by + 4, DOG_EYE)
        set_px(19, by + 1, (255, 255, 255, 255))

        set_px(15, by + 3, DOG_NOSE)
        set_px(16, by + 3, DOG_NOSE)
        set_px(15, by + 5, DOG_TONGUE)
        set_px(16, by + 5, DOG_TONGUE)

        fill_rect(11, by + 7, 20, by + 16, DOG_FUR)
        fill_rect(12, by + 14, 19, by + 16, DOG_SHADOW)
        for y in range(by + 7, by + 17):
            set_px(10, y, OUTLINE)
            set_px(21, y, OUTLINE)
        for x in range(11, 21):
            set_px(x, by + 17, OUTLINE)

        paw_wobble = -1 if col % 2 == 0 else 1
        set_px(12 + paw_wobble, by + 18, DOG_HIGHLIGHT)
        set_px(13 + paw_wobble, by + 18, OUTLINE)
        set_px(18 - paw_wobble, by + 18, DOG_HIGHLIGHT)
        set_px(19 - paw_wobble, by + 18, OUTLINE)

    elif state == "falling":
        by = 7
        set_px(6, by - 4, OUTLINE)
        fill_rect(7, by - 4, 8, by, DOG_EAR)
        set_px(25, by - 4, OUTLINE)
        fill_rect(23, by - 4, 24, by, DOG_EAR)

        fill_rect(9, by - 1, 22, by + 6, DOG_FUR)
        for y in range(by, by + 6):
            set_px(8, y, OUTLINE)
            set_px(23, y, OUTLINE)

        fill_rect(10, by + 1, 13, by + 4, DOG_EYE)
        fill_rect(18, by + 1, 21, by + 4, DOG_EYE)
        set_px(10, by + 1, (255, 255, 255, 255))
        set_px(18, by + 1, (255, 255, 255, 255))

        set_px(7, by + 2, (120, 200, 255, 255))
        set_px(24, by + 2, (120, 200, 255, 255))

        fill_rect(14, by + 4, 17, by + 7, (180, 50, 70, 255))
        set_px(15, by + 8, DOG_TONGUE)
        set_px(16, by + 8, DOG_TONGUE)

        fill_rect(10, by + 8, 21, by + 15, DOG_FUR)
        if col % 2 == 0:
            set_px(7, by + 8, DOG_HIGHLIGHT)
            set_px(6, by + 7, OUTLINE)
            set_px(24, by + 8, DOG_HIGHLIGHT)
            set_px(25, by + 7, OUTLINE)
        else:
            set_px(7, by + 10, DOG_HIGHLIGHT)
            set_px(6, by + 11, OUTLINE)
            set_px(24, by + 10, DOG_HIGHLIGHT)
            set_px(25, by + 11, OUTLINE)


def draw_alien(p, ox, oy, state, col):
    def set_px(x, y, color):
        if 0 <= x < SPRITE_SIZE and 0 <= y < SPRITE_SIZE and color:
            p[ox + x, oy + y] = color

    def fill_rect(x1, y1, x2, y2, color):
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                set_px(x, y, color)

    bob = [0, 1, 0, -1][col % 4] if state in ("idle", "talk") else 0

    if state == "idle":
        by = 13 + bob
        orb_color = ALIEN_ORB if col % 2 == 0 else ALIEN_ORB_GLOW
        fill_rect(14, by - 6, 17, by - 4, orb_color)
        set_px(15, by - 5, (255, 255, 255, 255))
        set_px(15, by - 3, OUTLINE)
        set_px(16, by - 3, OUTLINE)
        set_px(15, by - 2, ALIEN_SKIN)
        set_px(16, by - 2, ALIEN_SKIN)

        fill_rect(8, by, 23, by + 6, ALIEN_SKIN)
        fill_rect(9, by - 1, 22, by, ALIEN_SKIN)
        fill_rect(8, by + 5, 23, by + 6, ALIEN_SHADOW)

        for x in range(11, 21):
            set_px(x, by - 2, OUTLINE)
        for y in range(by, by + 6):
            set_px(7, y, OUTLINE)
            set_px(24, y, OUTLINE)
        set_px(8, by + 6, OUTLINE)
        set_px(23, by + 6, OUTLINE)

        fill_rect(10, by + 1, 13, by + 4, ALIEN_EYE)
        fill_rect(18, by + 1, 21, by + 4, ALIEN_EYE)
        set_px(10, by + 1, ALIEN_GLINT1)
        set_px(11, by + 2, ALIEN_GLINT2)
        set_px(18, by + 1, ALIEN_GLINT1)
        set_px(19, by + 2, ALIEN_GLINT2)

        set_px(15, by + 5, OUTLINE)
        set_px(16, by + 5, OUTLINE)
        set_px(9, by + 4, ALIEN_BLUSH)
        set_px(22, by + 4, ALIEN_BLUSH)

        fill_rect(10, by + 7, 21, by + 12, ALIEN_SUIT)
        fill_rect(11, by + 11, 21, by + 12, ALIEN_SUIT_DARK)
        fill_rect(12, by + 9, 19, by + 9, ALIEN_BELT)
        set_px(15, by + 9, ALIEN_ORB)
        set_px(16, by + 9, ALIEN_ORB)

        for x in range(10, 22):
            set_px(x, by + 13, OUTLINE)
        set_px(9, by + 8, OUTLINE)
        set_px(22, by + 8, OUTLINE)

        set_px(12, by + 13, ALIEN_HIGHLIGHT)
        set_px(19, by + 13, ALIEN_HIGHLIGHT)

    elif state == "talk":
        by = 13 + bob
        orb_color = ALIEN_ORB_GLOW if col % 2 == 1 else ALIEN_ORB
        fill_rect(14, by - 6, 17, by - 4, orb_color)
        set_px(15, by - 3, OUTLINE)
        set_px(16, by - 3, OUTLINE)

        fill_rect(8, by, 23, by + 6, ALIEN_SKIN)
        fill_rect(9, by - 1, 22, by, ALIEN_SKIN)
        fill_rect(8, by + 5, 23, by + 6, ALIEN_SHADOW)

        for x in range(11, 21):
            set_px(x, by - 2, OUTLINE)
        for y in range(by, by + 6):
            set_px(7, y, OUTLINE)
            set_px(24, y, OUTLINE)

        if col % 2 == 1:
            fill_rect(10, by + 1, 13, by + 3, ALIEN_EYE)
            fill_rect(18, by + 1, 21, by + 3, ALIEN_EYE)
            set_px(10, by + 1, ALIEN_GLINT1)
            set_px(18, by + 1, ALIEN_GLINT1)
            fill_rect(14, by + 4, 17, by + 6, (40, 110, 80, 255))
            set_px(15, by + 5, (160, 255, 180, 255))
        else:
            set_px(10, by + 2, OUTLINE)
            set_px(11, by + 1, OUTLINE)
            set_px(12, by + 1, OUTLINE)
            set_px(13, by + 2, OUTLINE)
            set_px(18, by + 2, OUTLINE)
            set_px(19, by + 1, OUTLINE)
            set_px(20, by + 1, OUTLINE)
            set_px(21, by + 2, OUTLINE)
            set_px(15, by + 5, OUTLINE)
            set_px(16, by + 5, OUTLINE)

        fill_rect(10, by + 7, 21, by + 12, ALIEN_SUIT)
        fill_rect(12, by + 9, 19, by + 9, ALIEN_BELT)
        for x in range(10, 22):
            set_px(x, by + 13, OUTLINE)
        set_px(9, by + 8, OUTLINE)
        set_px(22, by + 8, OUTLINE)

    elif state == "grabbed":
        by = 8
        set_px(15, by - 3, OUTLINE)
        set_px(16, by - 3, OUTLINE)

        fill_rect(14, by - 6, 17, by - 4, (255, 245, 100, 255))
        fill_rect(9, by, 22, by + 6, ALIEN_SKIN)
        for x in range(11, 21):
            set_px(x, by - 2, OUTLINE)
        for y in range(by, by + 6):
            set_px(8, y, OUTLINE)
            set_px(23, y, OUTLINE)

        fill_rect(10, by + 1, 13, by + 4, ALIEN_EYE)
        set_px(11, by + 1, ALIEN_GLINT1)
        fill_rect(18, by + 1, 21, by + 4, ALIEN_EYE)
        set_px(19, by + 1, ALIEN_GLINT1)

        set_px(15, by + 5, (40, 110, 80, 255))
        set_px(16, by + 5, (40, 110, 80, 255))

        fill_rect(11, by + 7, 20, by + 16, ALIEN_SUIT)
        fill_rect(12, by + 14, 19, by + 16, ALIEN_SUIT_DARK)
        fill_rect(12, by + 11, 19, by + 11, ALIEN_BELT)
        for y in range(by + 7, by + 17):
            set_px(10, y, OUTLINE)
            set_px(21, y, OUTLINE)
        for x in range(11, 21):
            set_px(x, by + 17, OUTLINE)

        tentacle_wobble = -1 if col % 2 == 0 else 1
        set_px(12 + tentacle_wobble, by + 18, ALIEN_HIGHLIGHT)
        set_px(18 - tentacle_wobble, by + 18, ALIEN_HIGHLIGHT)

    elif state == "falling":
        by = 7
        fill_rect(14, by - 6, 17, by - 4, (255, 120, 100, 255))
        fill_rect(9, by - 1, 22, by + 6, ALIEN_SKIN)
        for y in range(by, by + 6):
            set_px(8, y, OUTLINE)
            set_px(23, y, OUTLINE)

        fill_rect(10, by + 1, 13, by + 4, ALIEN_EYE)
        fill_rect(18, by + 1, 21, by + 4, ALIEN_EYE)
        set_px(10, by + 1, ALIEN_GLINT1)
        set_px(18, by + 1, ALIEN_GLINT1)

        set_px(7, by + 2, (120, 200, 255, 255))
        set_px(24, by + 2, (120, 200, 255, 255))

        fill_rect(14, by + 4, 17, by + 7, (40, 110, 80, 255))

        fill_rect(10, by + 8, 21, by + 15, ALIEN_SUIT)
        if col % 2 == 0:
            set_px(7, by + 8, ALIEN_HIGHLIGHT)
            set_px(6, by + 7, OUTLINE)
            set_px(24, by + 8, ALIEN_HIGHLIGHT)
            set_px(25, by + 7, OUTLINE)
        else:
            set_px(7, by + 10, ALIEN_HIGHLIGHT)
            set_px(6, by + 11, OUTLINE)
            set_px(24, by + 10, ALIEN_HIGHLIGHT)
            set_px(25, by + 11, OUTLINE)


def draw_robot(p, ox, oy, state, col):
    def set_px(x, y, color):
        if 0 <= x < SPRITE_SIZE and 0 <= y < SPRITE_SIZE and color:
            p[ox + x, oy + y] = color

    def fill_rect(x1, y1, x2, y2, color):
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                set_px(x, y, color)

    bob = [0, 1, 0, -1][col % 4] if state in ("idle", "talk") else 0

    if state == "idle":
        by = 13 + bob
        set_px(15, by - 5, ROBOT_ANTENNA)
        set_px(16, by - 5, ROBOT_ANTENNA)
        set_px(15, by - 4, OUTLINE)
        set_px(16, by - 4, OUTLINE)
        set_px(15, by - 3, ROBOT_SHADOW)
        set_px(16, by - 3, ROBOT_SHADOW)

        fill_rect(8, by - 2, 23, by + 5, ROBOT_METAL)
        fill_rect(8, by + 4, 23, by + 5, ROBOT_SHADOW)
        set_px(8, by - 2, OUTLINE)
        set_px(23, by - 2, OUTLINE)
        for x in range(9, 23):
            set_px(x, by - 3, OUTLINE)
        for y in range(by - 2, by + 6):
            set_px(7, y, OUTLINE)
            set_px(24, y, OUTLINE)

        set_px(6, by + 1, ROBOT_HIGHLIGHT)
        set_px(25, by + 1, ROBOT_HIGHLIGHT)

        fill_rect(10, by, 21, by + 3, ROBOT_SCREEN)

        if col == 3:
            fill_rect(11, by + 2, 13, by + 2, ROBOT_CYAN)
            fill_rect(18, by + 2, 20, by + 2, ROBOT_CYAN)
        else:
            fill_rect(11, by + 1, 13, by + 2, ROBOT_CYAN)
            fill_rect(18, by + 1, 20, by + 2, ROBOT_CYAN)

        fill_rect(9, by + 7, 22, by + 12, ROBOT_METAL)
        fill_rect(10, by + 11, 21, by + 12, ROBOT_SHADOW)
        for x in range(9, 23):
            set_px(x, by + 13, OUTLINE)
        set_px(8, by + 7, OUTLINE)
        set_px(23, by + 7, OUTLINE)

        set_px(12, by + 8, ROBOT_LIGHT_RED if col % 2 == 0 else ROBOT_DARK)
        set_px(14, by + 8, ROBOT_LIGHT_YELLOW if col % 2 == 1 else ROBOT_DARK)
        fill_rect(17, by + 8, 20, by + 9, ROBOT_SCREEN)
        set_px(18, by + 8, ROBOT_CYAN)

        fill_rect(11, by + 13, 13, by + 13, ROBOT_DARK)
        fill_rect(18, by + 13, 20, by + 13, ROBOT_DARK)

    elif state == "talk":
        by = 13 + bob
        set_px(15, by - 5, ROBOT_ANTENNA)
        set_px(16, by - 5, ROBOT_ANTENNA)
        set_px(15, by - 3, ROBOT_SHADOW)
        set_px(16, by - 3, ROBOT_SHADOW)

        fill_rect(8, by - 2, 23, by + 5, ROBOT_METAL)
        for y in range(by - 2, by + 6):
            set_px(7, y, OUTLINE)
            set_px(24, y, OUTLINE)

        fill_rect(10, by, 21, by + 4, ROBOT_SCREEN)

        if col % 2 == 1:
            set_px(11, by + 2, ROBOT_CYAN)
            set_px(12, by + 1, ROBOT_CYAN)
            set_px(13, by + 2, ROBOT_CYAN)
            set_px(18, by + 2, ROBOT_CYAN)
            set_px(19, by + 1, ROBOT_CYAN)
            set_px(20, by + 2, ROBOT_CYAN)
            fill_rect(13, by + 3, 18, by + 3, ROBOT_CYAN)
        else:
            fill_rect(11, by + 1, 13, by + 2, ROBOT_CYAN)
            fill_rect(18, by + 1, 20, by + 2, ROBOT_CYAN)
            set_px(15, by + 3, ROBOT_CYAN)
            set_px(16, by + 3, ROBOT_CYAN)

        fill_rect(9, by + 7, 22, by + 12, ROBOT_METAL)
        for x in range(9, 23):
            set_px(x, by + 13, OUTLINE)
        set_px(8, by + 7, OUTLINE)
        set_px(23, by + 7, OUTLINE)

    elif state == "grabbed":
        by = 8
        set_px(15, by - 3, OUTLINE)
        set_px(16, by - 3, OUTLINE)

        fill_rect(8, by - 2, 23, by + 5, ROBOT_METAL)
        for y in range(by - 2, by + 6):
            set_px(7, y, OUTLINE)
            set_px(24, y, OUTLINE)

        fill_rect(10, by, 21, by + 3, ROBOT_SCREEN)
        fill_rect(11, by + 1, 13, by + 2, ROBOT_LIGHT_YELLOW)
        fill_rect(18, by + 1, 20, by + 2, ROBOT_LIGHT_YELLOW)

        fill_rect(9, by + 7, 22, by + 15, ROBOT_METAL)
        fill_rect(10, by + 13, 21, by + 15, ROBOT_SHADOW)
        for y in range(by + 7, by + 16):
            set_px(8, y, OUTLINE)
            set_px(23, y, OUTLINE)
        for x in range(9, 23):
            set_px(x, by + 16, OUTLINE)

        wobble = -1 if col % 2 == 0 else 1
        set_px(11 + wobble, by + 17, ROBOT_DARK)
        set_px(20 - wobble, by + 17, ROBOT_DARK)

    elif state == "falling":
        by = 7
        set_px(15, by - 5, (255, 230, 80, 255))
        set_px(16, by - 5, (255, 230, 80, 255))

        fill_rect(8, by - 2, 23, by + 5, ROBOT_METAL)
        for y in range(by - 2, by + 6):
            set_px(7, y, OUTLINE)
            set_px(24, y, OUTLINE)

        fill_rect(10, by, 21, by + 3, ROBOT_SCREEN)
        set_px(11, by + 1, ROBOT_LIGHT_RED)
        set_px(13, by + 1, ROBOT_LIGHT_RED)
        set_px(12, by + 2, ROBOT_LIGHT_RED)
        set_px(18, by + 1, ROBOT_LIGHT_RED)
        set_px(20, by + 1, ROBOT_LIGHT_RED)
        set_px(19, by + 2, ROBOT_LIGHT_RED)

        fill_rect(9, by + 7, 22, by + 15, ROBOT_METAL)
        for x in range(9, 23):
            set_px(x, by + 15, OUTLINE)

        set_px(11, by + 16, (255, 160, 50, 255))
        set_px(12, by + 17, (255, 80, 40, 255))
        set_px(19, by + 16, (255, 160, 50, 255))
        set_px(20, by + 17, (255, 80, 40, 255))


DRAWERS = {
    "cat": draw_cat,
    "dog": draw_dog,
    "alien": draw_alien,
    "robot": draw_robot,
}


def generate_spritesheet(name):
    drawer = DRAWERS.get(name, draw_cat)
    sheet = Image.new("RGBA", (COLS * SPRITE_SIZE, ROWS * SPRITE_SIZE), (0, 0, 0, 0))
    p = sheet.load()
    for row in range(ROWS):
        state = ROW_STATE[row]
        for col in range(STATES[state]["frame_count"]):
            drawer(p, col * SPRITE_SIZE, row * SPRITE_SIZE, state, col)
    return sheet


def generate_all():
    ASSETS.mkdir(parents=True, exist_ok=True)
    for name in DRAWERS:
        sheet = generate_spritesheet(name)
        out_path = ASSETS / f"spritesheet_{name}.png"
        sheet.save(out_path)
    default_sheet = generate_spritesheet("cat")
    default_sheet.save(ASSETS / "spritesheet.png")


def main():
    generate_all()


if __name__ == "__main__":
    main()
