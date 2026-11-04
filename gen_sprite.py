from PIL import Image, ImageDraw

from config import SPRITE_SIZE, SPRITESHEET, ASSETS
from states import STATES

COLS = max(s["frame_count"] for s in STATES.values())
ROWS = max(s["row"] for s in STATES.values()) + 1
ROW_STATE = {spec["row"]: name for name, spec in STATES.items()}

# Palette
OUTLINE = (42, 38, 62, 255)
FUR_BASE = (255, 238, 218, 255)       # warm cream
FUR_SHADOW = (232, 202, 178, 255)     # soft shading
FUR_HIGHLIGHT = (255, 250, 245, 255)  # highlight
EAR_PINK = (255, 168, 185, 255)       # rosy inner ear
CHEEK = (255, 140, 165, 200)          # blush
EYE_DARK = (45, 42, 74, 255)          # rich dark indigo
EYE_GLINT = (255, 255, 255, 255)
NOSE_PINK = (245, 120, 150, 255)
MOUTH_INNER = (210, 75, 110, 255)
ACCENT_BELL = (255, 205, 55, 255)     # gold collar bell
COLLAR_RED = (235, 65, 85, 255)       # red ribbon


def draw_kitten(img, ox, oy, state, col):
    """Render a detailed pixel-art companion into a 32x32 cell at (ox, oy)."""
    p = img.load()

    def set_px(x, y, color):
        if 0 <= x < SPRITE_SIZE and 0 <= y < SPRITE_SIZE and color:
            p[ox + x, oy + y] = color

    def fill_rect(x1, y1, x2, y2, color):
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                set_px(x, y, color)

    # Bob offsets
    bob = [0, 1, 0, -1][col % 4] if state in ("idle", "talk") else 0
    tail_phase = col % 4

    if state == "idle":
        by = 13 + bob
        # Tail
        tail_x = 21 + (1 if tail_phase in (1, 2) else 0)
        tail_y = 20 + bob
        set_px(tail_x + 1, tail_y - 2, OUTLINE)
        set_px(tail_x + 2, tail_y - 1, OUTLINE)
        set_px(tail_x + 2, tail_y, FUR_BASE)
        set_px(tail_x + 1, tail_y + 1, FUR_BASE)
        set_px(tail_x + 3, tail_y - 1, FUR_SHADOW)

        # Body
        fill_rect(10, by + 7, 21, by + 12, FUR_BASE)
        fill_rect(11, by + 11, 21, by + 12, FUR_SHADOW)
        # Outline body
        for x in range(10, 22):
            set_px(x, by + 13, OUTLINE)
        set_px(9, by + 8, OUTLINE)
        set_px(9, by + 9, OUTLINE)
        set_px(9, by + 10, OUTLINE)
        set_px(22, by + 8, OUTLINE)
        set_px(22, by + 9, OUTLINE)
        set_px(22, by + 10, OUTLINE)

        # Tiny Paws
        set_px(11, by + 12, FUR_HIGHLIGHT)
        set_px(12, by + 12, FUR_HIGHLIGHT)
        set_px(19, by + 12, FUR_HIGHLIGHT)
        set_px(20, by + 12, FUR_HIGHLIGHT)

        # Collar + Bell
        fill_rect(12, by + 7, 19, by + 7, COLLAR_RED)
        set_px(15, by + 8, ACCENT_BELL)
        set_px(16, by + 8, ACCENT_BELL)

        # Head base
        fill_rect(8, by, 23, by + 6, FUR_BASE)
        fill_rect(9, by - 1, 22, by, FUR_BASE)
        fill_rect(8, by + 5, 23, by + 6, FUR_SHADOW)

        # Head outline
        for x in range(11, 21):
            set_px(x, by - 2, OUTLINE)
        for y in range(by, by + 6):
            set_px(7, y, OUTLINE)
            set_px(24, y, OUTLINE)
        set_px(8, by + 6, OUTLINE)
        set_px(23, by + 6, OUTLINE)

        # Ears (twitch slightly)
        # Left ear
        set_px(8, by - 3, OUTLINE)
        set_px(9, by - 4, OUTLINE)
        set_px(10, by - 5, OUTLINE)
        set_px(11, by - 4, OUTLINE)
        fill_rect(9, by - 3, 10, by - 2, FUR_BASE)
        set_px(10, by - 3, EAR_PINK)

        # Right ear
        set_px(23, by - 3, OUTLINE)
        set_px(22, by - 4, OUTLINE)
        set_px(21, by - 5, OUTLINE)
        set_px(20, by - 4, OUTLINE)
        fill_rect(21, by - 3, 22, by - 2, FUR_BASE)
        set_px(21, by - 3, EAR_PINK)

        # Cheeks
        set_px(9, by + 4, CHEEK)
        set_px(10, by + 4, CHEEK)
        set_px(21, by + 4, CHEEK)
        set_px(22, by + 4, CHEEK)

        # Eyes (blinking on col == 3)
        if col == 3:
            # Happy sleeping/blinking line eyes ^ ^
            set_px(11, by + 2, OUTLINE)
            set_px(12, by + 1, OUTLINE)
            set_px(13, by + 2, OUTLINE)

            set_px(18, by + 2, OUTLINE)
            set_px(19, by + 1, OUTLINE)
            set_px(20, by + 2, OUTLINE)
        else:
            # Big sparkling dark anime eyes
            fill_rect(11, by + 1, 13, by + 3, EYE_DARK)
            set_px(11, by + 1, EYE_GLINT)
            fill_rect(18, by + 1, 20, by + 3, EYE_DARK)
            set_px(18, by + 1, EYE_GLINT)

        # Cute Nose & Mouth
        set_px(15, by + 3, NOSE_PINK)
        set_px(16, by + 3, NOSE_PINK)
        set_px(15, by + 4, OUTLINE)
        set_px(16, by + 4, OUTLINE)

    elif state == "talk":
        by = 13 + bob
        # Body
        fill_rect(10, by + 7, 21, by + 12, FUR_BASE)
        fill_rect(11, by + 11, 21, by + 12, FUR_SHADOW)
        for x in range(10, 22):
            set_px(x, by + 13, OUTLINE)
        set_px(9, by + 8, OUTLINE)
        set_px(22, by + 8, OUTLINE)

        # Collar + Bell
        fill_rect(12, by + 7, 19, by + 7, COLLAR_RED)
        set_px(15, by + 8, ACCENT_BELL)
        set_px(16, by + 8, ACCENT_BELL)

        # Head
        fill_rect(8, by, 23, by + 6, FUR_BASE)
        fill_rect(9, by - 1, 22, by, FUR_BASE)
        fill_rect(8, by + 5, 23, by + 6, FUR_SHADOW)

        # Head outline
        for x in range(11, 21):
            set_px(x, by - 2, OUTLINE)
        for y in range(by, by + 6):
            set_px(7, y, OUTLINE)
            set_px(24, y, OUTLINE)

        # Ears
        set_px(8, by - 3, OUTLINE)
        set_px(9, by - 4, OUTLINE)
        set_px(10, by - 5, OUTLINE)
        set_px(11, by - 4, OUTLINE)
        fill_rect(9, by - 3, 10, by - 2, FUR_BASE)
        set_px(10, by - 3, EAR_PINK)

        set_px(23, by - 3, OUTLINE)
        set_px(22, by - 4, OUTLINE)
        set_px(21, by - 5, OUTLINE)
        set_px(20, by - 4, OUTLINE)
        fill_rect(21, by - 3, 22, by - 2, FUR_BASE)
        set_px(21, by - 3, EAR_PINK)

        # Animated talking mouth (open on odd frames)
        set_px(15, by + 3, NOSE_PINK)
        set_px(16, by + 3, NOSE_PINK)
        if col % 2 == 1:
            fill_rect(14, by + 4, 17, by + 6, MOUTH_INNER)
            set_px(14, by + 4, OUTLINE)
            set_px(17, by + 4, OUTLINE)
            set_px(15, by + 6, OUTLINE)
            set_px(16, by + 6, OUTLINE)
        else:
            set_px(14, by + 4, OUTLINE)
            set_px(15, by + 5, OUTLINE)
            set_px(16, by + 5, OUTLINE)
            set_px(17, by + 4, OUTLINE)

        # Happy eyes
        set_px(11, by + 2, OUTLINE)
        set_px(12, by + 1, OUTLINE)
        set_px(13, by + 2, OUTLINE)
        set_px(18, by + 2, OUTLINE)
        set_px(19, by + 1, OUTLINE)
        set_px(20, by + 2, OUTLINE)

        # Cheeks
        set_px(9, by + 4, CHEEK)
        set_px(10, by + 4, CHEEK)
        set_px(21, by + 4, CHEEK)
        set_px(22, by + 4, CHEEK)

    elif state == "grabbed":
        # Stretched dangling body when lifted
        by = 8
        # Scruff pinch indicator
        set_px(15, by - 3, OUTLINE)
        set_px(16, by - 3, OUTLINE)

        # Head
        fill_rect(9, by, 22, by + 6, FUR_BASE)
        for x in range(11, 21):
            set_px(x, by - 2, OUTLINE)
        for y in range(by, by + 6):
            set_px(8, y, OUTLINE)
            set_px(23, y, OUTLINE)

        # Ears pinned slightly sideways
        set_px(7, by - 1, OUTLINE)
        set_px(6, by - 2, OUTLINE)
        set_px(7, by - 3, OUTLINE)
        set_px(8, by - 2, EAR_PINK)

        set_px(24, by - 1, OUTLINE)
        set_px(25, by - 2, OUTLINE)
        set_px(24, by - 3, OUTLINE)
        set_px(23, by - 2, EAR_PINK)

        # Big surprised round eyes O . O
        fill_rect(10, by + 1, 13, by + 4, EYE_DARK)
        set_px(11, by + 1, EYE_GLINT)
        fill_rect(18, by + 1, 21, by + 4, EYE_DARK)
        set_px(19, by + 1, EYE_GLINT)

        # Surprised small round mouth 'o'
        set_px(15, by + 3, NOSE_PINK)
        set_px(16, by + 3, NOSE_PINK)
        set_px(15, by + 5, MOUTH_INNER)
        set_px(16, by + 5, MOUTH_INNER)

        # Stretched Body
        fill_rect(11, by + 7, 20, by + 16, FUR_BASE)
        fill_rect(12, by + 14, 19, by + 16, FUR_SHADOW)
        for y in range(by + 7, by + 17):
            set_px(10, y, OUTLINE)
            set_px(21, y, OUTLINE)
        for x in range(11, 21):
            set_px(x, by + 17, OUTLINE)

        # Dangling paws
        paw_wobble = -1 if col % 2 == 0 else 1
        set_px(12 + paw_wobble, by + 18, FUR_HIGHLIGHT)
        set_px(13 + paw_wobble, by + 18, OUTLINE)
        set_px(18 - paw_wobble, by + 18, FUR_HIGHLIGHT)
        set_px(19 - paw_wobble, by + 18, OUTLINE)

    elif state == "falling":
        # Falling flail animation
        by = 7
        # Ears swept up by wind
        set_px(10, by - 5, OUTLINE)
        set_px(11, by - 6, OUTLINE)
        set_px(12, by - 5, OUTLINE)
        set_px(11, by - 4, EAR_PINK)

        set_px(21, by - 5, OUTLINE)
        set_px(20, by - 6, OUTLINE)
        set_px(19, by - 5, OUTLINE)
        set_px(20, by - 4, EAR_PINK)

        # Head
        fill_rect(9, by - 1, 22, by + 6, FUR_BASE)
        for y in range(by, by + 6):
            set_px(8, y, OUTLINE)
            set_px(23, y, OUTLINE)

        # Big funny shocked eyes > < or wide open with tears
        fill_rect(10, by + 1, 13, by + 4, EYE_DARK)
        fill_rect(18, by + 1, 21, by + 4, EYE_DARK)
        set_px(10, by + 1, EYE_GLINT)
        set_px(18, by + 1, EYE_GLINT)

        # Little tear drop at edge of eye
        set_px(7, by + 2, (120, 200, 255, 255))
        set_px(24, by + 2, (120, 200, 255, 255))

        # Open screaming / falling mouth
        fill_rect(14, by + 4, 17, by + 7, MOUTH_INNER)
        set_px(14, by + 4, OUTLINE)
        set_px(17, by + 4, OUTLINE)
        set_px(15, by + 7, OUTLINE)
        set_px(16, by + 7, OUTLINE)

        # Body flailing
        fill_rect(10, by + 8, 21, by + 15, FUR_BASE)
        # Flailing paws
        if col % 2 == 0:
            set_px(7, by + 8, FUR_HIGHLIGHT)
            set_px(6, by + 7, OUTLINE)
            set_px(24, by + 8, FUR_HIGHLIGHT)
            set_px(25, by + 7, OUTLINE)
        else:
            set_px(7, by + 10, FUR_HIGHLIGHT)
            set_px(6, by + 11, OUTLINE)
            set_px(24, by + 10, FUR_HIGHLIGHT)
            set_px(25, by + 11, OUTLINE)


def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    sheet = Image.new("RGBA", (COLS * SPRITE_SIZE, ROWS * SPRITE_SIZE), (0, 0, 0, 0))
    for row in range(ROWS):
        state = ROW_STATE[row]
        for col in range(STATES[state]["frame_count"]):
            draw_kitten(sheet, col * SPRITE_SIZE, row * SPRITE_SIZE, state, col)
    sheet.save(SPRITESHEET)
    print(f"Wrote {SPRITESHEET} ({sheet.width}x{sheet.height}, {ROWS} rows: {', '.join(ROW_STATE[r] for r in range(ROWS))})")


if __name__ == "__main__":
    main()
