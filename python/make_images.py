# Draws the 26 simple pictures used by the game (one example word per letter).
# The pictures are already included in java/images, so you only need to run this
# if you want to recreate them. You can also replace any picture with your own PNG
# (keep the same file name, for example java/images/apple.png).
#   pip install pillow
#   python make_images.py

import math
import os
from PIL import Image, ImageDraw

K = 2           # everything is drawn at double size and then reduced (smooth edges)
SIZE = 400

RED = (226, 60, 60)
ORANGE = (250, 150, 40)
YELLOW = (255, 215, 60)
GREEN = (80, 180, 90)
BLUE = (70, 130, 220)
PURPLE = (150, 90, 200)
PINK = (250, 170, 190)
BROWN = (140, 90, 50)
GRAY = (150, 150, 160)
WHITE = (255, 255, 255)
BLACK = (40, 40, 40)
OUT = (70, 50, 40)


class Pic:
    def __init__(self, background=None):
        self.img = Image.new("RGBA", (SIZE * K, SIZE * K), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.img)
        if background:
            self.d.rounded_rectangle(self.box((8, 8, 392, 392)), radius=40 * K, fill=background)

    def box(self, b):
        return tuple(v * K for v in b)

    def pt(self, p):
        return (p[0] * K, p[1] * K)

    def ellipse(self, b, fill=None, outline=None, width=4):
        self.d.ellipse(self.box(b), fill=fill, outline=outline, width=width * K if outline else 0)

    def rect(self, b, fill=None, outline=None, width=4, radius=0):
        self.d.rounded_rectangle(self.box(b), radius=radius * K, fill=fill,
                                 outline=outline, width=width * K if outline else 0)

    def poly(self, points, fill=None, outline=None, width=4):
        pts = [self.pt(p) for p in points]
        self.d.polygon(pts, fill=fill)
        if outline:
            self.d.line(pts + [pts[0]], fill=outline, width=width * K, joint="curve")

    def line(self, points, fill, width=4):
        self.d.line([self.pt(p) for p in points], fill=fill, width=int(width * K), joint="curve")

    def pie(self, b, start, end, fill):
        self.d.pieslice(self.box(b), start, end, fill=fill)

    def arc(self, b, start, end, fill, width=4):
        self.d.arc(self.box(b), start, end, fill=fill, width=int(width * K))

    def save(self, name):
        folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "java", "images")
        os.makedirs(folder, exist_ok=True)
        small = self.img.resize((SIZE, SIZE), Image.LANCZOS)
        small.save(os.path.join(folder, name + ".png"))


def star_points(cx, cy, r_out, r_in):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def apple(p):
    p.ellipse((70, 100, 330, 350), RED, OUT, 5)
    p.line([(200, 110), (212, 55)], BROWN, 12)
    p.ellipse((215, 40, 295, 95), GREEN, OUT, 4)
    p.ellipse((110, 150, 150, 220), (255, 255, 255, 150))


def ball(p):
    colors = [RED, YELLOW, BLUE, GREEN, ORANGE, PURPLE]
    for i, c in enumerate(colors):
        p.pie((60, 60, 340, 340), i * 60, i * 60 + 60, c)
    p.ellipse((60, 60, 340, 340), None, OUT, 5)
    p.ellipse((172, 172, 228, 228), WHITE, OUT, 4)


def cat(p):
    fur = (245, 160, 70)
    p.poly([(95, 170), (105, 60), (185, 140)], fur, OUT)
    p.poly([(305, 170), (295, 60), (215, 140)], fur, OUT)
    p.poly([(115, 150), (118, 95), (160, 138)], PINK)
    p.poly([(285, 150), (282, 95), (240, 138)], PINK)
    p.ellipse((80, 120, 320, 340), fur, OUT, 5)
    for x in (185, 200, 215):
        p.line([(x, 135), (x, 160)], (200, 110, 40), 6)
    p.ellipse((135, 190, 185, 250), WHITE, OUT, 4)
    p.ellipse((215, 190, 265, 250), WHITE, OUT, 4)
    p.ellipse((150, 205, 175, 240), BLACK)
    p.ellipse((230, 205, 255, 240), BLACK)
    p.poly([(188, 262), (212, 262), (200, 278)], (230, 100, 120))
    p.line([(200, 278), (200, 295)], OUT, 4)
    p.line([(200, 295), (180, 308)], OUT, 4)
    p.line([(200, 295), (220, 308)], OUT, 4)
    for dy in (-8, 8):
        p.line([(130, 285 + dy), (60, 285 + dy * 2)], OUT, 3)
        p.line([(270, 285 + dy), (340, 285 + dy * 2)], OUT, 3)


def dog(p):
    ear = (110, 70, 40)
    p.ellipse((65, 110, 145, 270), ear, OUT, 4)
    p.ellipse((255, 110, 335, 270), ear, OUT, 4)
    p.ellipse((105, 90, 295, 330), (200, 140, 80), OUT, 5)
    p.ellipse((145, 190, 255, 305), (250, 225, 190), OUT, 4)
    p.ellipse((135, 150, 175, 195), WHITE, OUT, 3)
    p.ellipse((225, 150, 265, 195), WHITE, OUT, 3)
    p.ellipse((148, 162, 166, 188), BLACK)
    p.ellipse((234, 162, 252, 188), BLACK)
    p.ellipse((175, 205, 225, 240), BLACK)
    p.line([(200, 240), (200, 265)], OUT, 4)
    p.arc((170, 245, 200, 285), 0, 180, OUT, 4)
    p.arc((200, 245, 230, 285), 0, 180, OUT, 4)
    p.ellipse((188, 272, 212, 300), (240, 110, 130), OUT, 3)


def egg(p):
    p.ellipse((105, 60, 295, 345), (250, 240, 215), OUT, 5)
    for x, y in [(160, 150), (230, 190), (180, 250), (240, 280), (150, 300), (215, 110)]:
        p.ellipse((x - 7, y - 5, x + 7, y + 5), (190, 150, 100))
    p.ellipse((135, 105, 165, 160), (255, 255, 255, 170))


def fish(p):
    p.poly([(285, 205), (365, 130), (365, 280)], (240, 120, 40), OUT)
    p.poly([(150, 155), (210, 90), (250, 160)], (240, 120, 40), OUT)
    p.ellipse((45, 130, 310, 285), ORANGE, OUT, 5)
    for x in (190, 225, 260):
        p.line([(x, 160), (x - 10, 255)], (230, 110, 30), 5)
    p.ellipse((85, 175, 125, 215), WHITE, OUT, 3)
    p.ellipse((97, 186, 115, 206), BLACK)
    p.line([(55, 230), (85, 240)], OUT, 4)


def grapes(p):
    rows = [(125, [110, 170, 230, 290]), (180, [140, 200, 260]), (235, [170, 230]), (290, [200])]
    p.line([(200, 100), (212, 55)], BROWN, 10)
    p.ellipse((215, 35, 305, 90), GREEN, OUT, 4)
    for y, xs in rows:
        for x in xs:
            p.ellipse((x - 31, y - 31, x + 31, y + 31), PURPLE, OUT, 4)
            p.ellipse((x - 18, y - 20, x - 6, y - 8), (255, 255, 255, 170))


def hat(p):
    p.ellipse((70, 235, 330, 305), (50, 50, 60), OUT, 4)
    p.rect((125, 80, 275, 265), (50, 50, 60), OUT, 4, 12)
    p.rect((125, 200, 275, 240), RED, OUT, 3)
    p.ellipse((70, 235, 330, 305), None, OUT, 4)
    p.ellipse((125, 232, 275, 262), (50, 50, 60))


def icecream(p):
    p.poly([(135, 215), (265, 215), (200, 375)], (230, 180, 100), OUT)
    for i in range(1, 5):
        p.line([(135 + i * 20, 215), (200 - (200 - (135 + i * 20)) * 0.2, 330)], (190, 140, 70), 3)
        p.line([(265 - i * 20, 215), (200 + (265 - i * 20 - 200) * 0.2, 330)], (190, 140, 70), 3)
    p.ellipse((120, 125, 280, 240), (250, 170, 200), OUT, 5)
    p.ellipse((145, 60, 255, 155), (150, 100, 70), OUT, 5)
    p.ellipse((180, 28, 220, 68), RED, OUT, 4)


def jam(p):
    p.rect((105, 120, 295, 345), (225, 238, 250), OUT, 5, 25)
    p.rect((115, 190, 285, 335), (170, 40, 90), None, 0, 18)
    p.rect((115, 80, 285, 130), (230, 190, 60), OUT, 5, 8)
    p.rect((145, 235, 255, 305), WHITE, OUT, 3, 8)
    p.ellipse((185, 258, 215, 288), RED)
    p.ellipse((130, 150, 148, 260), (255, 255, 255, 140))


def kite(p):
    c = (200, 170)
    p.poly([(200, 35), (310, 170), c], RED)
    p.poly([(310, 170), (200, 310), c], YELLOW)
    p.poly([(200, 310), (90, 170), c], BLUE)
    p.poly([(90, 170), (200, 35), c], GREEN)
    p.poly([(200, 35), (310, 170), (200, 310), (90, 170)], None, OUT, 5)
    p.line([(200, 35), (200, 310)], OUT, 3)
    p.line([(90, 170), (310, 170)], OUT, 3)
    tail = [(200 + 25 * math.sin(i / 2.0), 310 + i * 7) for i in range(0, 11)]
    p.line(tail, OUT, 3)
    for i in (2, 5, 8):
        x, y = tail[i]
        p.poly([(x, y), (x - 16, y - 10), (x - 16, y + 10)], RED)
        p.poly([(x, y), (x + 16, y - 10), (x + 16, y + 10)], YELLOW)


def leaf(p):
    x0, y0, x1, y1 = 80, 320, 320, 80
    dx, dy = x1 - x0, y1 - y0
    length = math.hypot(dx, dy)
    nx, ny = -dy / length, dx / length
    n = 24
    pts = []
    for i in range(n + 1):
        t = i / n
        w = 75 * math.sin(math.pi * t)
        pts.append((x0 + dx * t + nx * w, y0 + dy * t + ny * w))
    for i in range(n, -1, -1):
        t = i / n
        w = 75 * math.sin(math.pi * t)
        pts.append((x0 + dx * t - nx * w, y0 + dy * t - ny * w))
    p.poly(pts, (90, 190, 80), OUT, 5)
    p.line([(x0, y0), (x1 - 15, y1 + 15)], (50, 130, 50), 5)
    p.line([(x0, y0), (50, 350)], BROWN, 8)
    for t in (0.3, 0.5, 0.7):
        cx, cy = x0 + dx * t, y0 + dy * t
        p.line([(cx, cy), (cx + nx * 35 + dx / length * 20, cy + ny * 35 + dy / length * 20)], (50, 130, 50), 3)
        p.line([(cx, cy), (cx - nx * 35 + dx / length * 20, cy - ny * 35 + dy / length * 20)], (50, 130, 50), 3)


def moon(p):
    night = (35, 45, 100)
    p = p
    p.rect((8, 8, 392, 392), night, None, 0, 40)
    p.ellipse((70, 70, 320, 320), (255, 236, 150))
    p.ellipse((135, 50, 370, 285), night)
    for cx, cy, r in [(300, 110, 18), (330, 230, 12), (90, 330, 14), (250, 340, 10)]:
        p.poly(star_points(cx, cy, r, r * 0.45), (255, 245, 190))


def nut(p):
    p.line([(200, 120), (205, 65)], BROWN, 12)
    p.ellipse((130, 160, 270, 345), (215, 165, 95), OUT, 5)
    p.poly([(185, 335), (215, 335), (200, 360)], (150, 100, 50), OUT, 3)
    p.ellipse((115, 105, 285, 215), (120, 75, 40), OUT, 5)
    for i in range(5):
        p.line([(140 + i * 30, 125), (125 + i * 37, 205)], (90, 55, 30), 3)


def orange(p):
    p.ellipse((65, 90, 335, 360), ORANGE, OUT, 5)
    p.ellipse((205, 45, 290, 100), GREEN, OUT, 4)
    p.line([(200, 95), (205, 70)], BROWN, 8)
    p.ellipse((105, 140, 145, 215), (255, 255, 255, 120))
    for x, y in [(180, 200), (250, 180), (220, 260), (140, 270), (280, 270), (180, 320)]:
        p.ellipse((x - 4, y - 4, x + 4, y + 4), (215, 120, 20))


def pig(p):
    skin = (250, 170, 190)
    p.poly([(95, 180), (85, 80), (170, 125)], (235, 140, 165), OUT)
    p.poly([(305, 180), (315, 80), (230, 125)], (235, 140, 165), OUT)
    p.ellipse((75, 100, 325, 335), skin, OUT, 5)
    p.ellipse((150, 195, 250, 285), (235, 140, 165), OUT, 4)
    p.ellipse((172, 222, 188, 255), (150, 70, 90))
    p.ellipse((212, 222, 228, 255), (150, 70, 90))
    p.ellipse((125, 150, 165, 195), WHITE, OUT, 3)
    p.ellipse((235, 150, 275, 195), WHITE, OUT, 3)
    p.ellipse((138, 162, 156, 188), BLACK)
    p.ellipse((244, 162, 262, 188), BLACK)


def queen(p):
    gold = (250, 200, 50)
    p.poly([(80, 300), (65, 120), (145, 205), (200, 85), (255, 205), (335, 120), (320, 300)], gold, OUT, 5)
    p.rect((80, 275, 320, 330), (230, 170, 30), OUT, 5, 8)
    for x, c in [(65, RED), (200, BLUE), (335, RED)]:
        y = 120 if x != 200 else 85
        p.ellipse((x - 18, y - 18, x + 18, y + 18), c, OUT, 3)
    for x, c in [(130, GREEN), (200, RED), (270, GREEN)]:
        p.ellipse((x - 14, 290, x + 14, 318), c, OUT, 3)


def rainbow(p):
    sky = (200, 230, 255)
    p.rect((8, 8, 392, 392), sky, None, 0, 40)
    colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
    cx, cy = 200, 285
    for i, c in enumerate(colors):
        r = 165 - i * 22
        p.pie((cx - r, cy - r, cx + r, cy + r), 180, 360, c)
    r = 165 - 6 * 22
    p.pie((cx - r, cy - r, cx + r, cy + r), 180, 360, sky)
    for x, y in [(55, 285), (345, 285)]:
        p.ellipse((x - 50, y - 25, x + 30, y + 35), WHITE)
        p.ellipse((x - 20, y - 45, x + 50, y + 25), WHITE)
        p.ellipse((x - 25, y - 5, x + 55, y + 40), WHITE)


def sun(p):
    cx, cy = 200, 200
    for i in range(12):
        a = i * math.pi / 6
        a1, a2 = a - 0.14, a + 0.14
        p.poly([(cx + 105 * math.cos(a1), cy + 105 * math.sin(a1)),
                (cx + 175 * math.cos(a), cy + 175 * math.sin(a)),
                (cx + 105 * math.cos(a2), cy + 105 * math.sin(a2))], ORANGE, OUT, 3)
    p.ellipse((100, 100, 300, 300), YELLOW, OUT, 5)
    p.ellipse((150, 165, 175, 200), BLACK)
    p.ellipse((225, 165, 250, 200), BLACK)
    p.arc((150, 190, 250, 260), 20, 160, OUT, 6)


def tree(p):
    p.rect((172, 220, 228, 365), BROWN, OUT, 5)
    for box in [(70, 130, 220, 275), (180, 130, 330, 275), (115, 50, 285, 210)]:
        p.ellipse(box, (60, 160, 70), OUT, 5)
    p.ellipse((115, 50, 285, 210), (60, 160, 70))
    p.ellipse((70, 130, 220, 275), (60, 160, 70))
    p.ellipse((180, 130, 330, 275), (60, 160, 70))
    for x, y in [(160, 110), (240, 150), (120, 200), (270, 210), (200, 190)]:
        p.ellipse((x - 10, y - 10, x + 10, y + 10), RED, OUT, 2)


def umbrella(p):
    colors = [RED, WHITE, RED, WHITE, RED]
    for i, c in enumerate(colors):
        p.pie((45, 40, 355, 350), 180 + i * 36, 216 + i * 36, c)
    p.arc((45, 40, 355, 350), 180, 360, OUT, 5)
    p.line([(45, 195), (355, 195)], OUT, 5)
    p.line([(200, 195), (200, 325)], OUT, 8)
    p.arc((168, 300, 200, 345), 0, 180, OUT, 8)


def van(p):
    p.rect((40, 150, 360, 295), BLUE, OUT, 5, 25)
    p.rect((60, 175, 160, 245), (200, 230, 250), OUT, 4, 8)
    p.rect((175, 175, 245, 245), (200, 230, 250), OUT, 4, 8)
    p.poly([(260, 175), (330, 175), (345, 245), (260, 245)], (200, 230, 250), OUT, 4)
    p.line([(165, 150), (165, 295)], OUT, 4)
    for x in (110, 290):
        p.ellipse((x - 42, 255, x + 42, 339), BLACK, OUT, 3)
        p.ellipse((x - 18, 279, x + 18, 315), GRAY)
    p.ellipse((338, 255, 356, 275), YELLOW, OUT, 2)


def watch(p):
    strap = (90, 110, 150)
    p.rect((145, 15, 255, 125), strap, OUT, 4, 10)
    p.rect((145, 275, 255, 385), strap, OUT, 4, 10)
    p.ellipse((80, 85, 320, 315), WHITE, (60, 60, 80), 10)
    for i in range(12):
        a = i * math.pi / 6
        p.line([(200 + 95 * math.cos(a), 200 + 95 * math.sin(a)),
                (200 + 82 * math.cos(a), 200 + 82 * math.sin(a))], OUT, 4)
    p.line([(200, 200), (200, 135)], OUT, 7)
    p.line([(200, 200), (245, 225)], RED, 5)
    p.ellipse((190, 190, 210, 210), OUT)


def xylophone(p):
    p.line([(40, 150), (360, 150)], BROWN, 12)
    p.line([(40, 250), (360, 250)], BROWN, 12)
    colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, (230, 90, 170)]
    for i, c in enumerate(colors):
        h = 230 - i * 22
        x = 52 + i * 42
        p.rect((x, 200 - h / 2, x + 36, 200 + h / 2), c, OUT, 3, 6)
    p.line([(340, 60), (290, 130)], BROWN, 8)
    p.ellipse((330, 40, 365, 75), (220, 60, 60), OUT, 3)
    p.line([(60, 60), (110, 130)], BROWN, 8)
    p.ellipse((35, 40, 70, 75), (220, 60, 60), OUT, 3)


def yoyo(p):
    p.line([(200, 250), (200, 60)], OUT, 4)
    p.ellipse((178, 15, 222, 75), None, OUT, 5)
    p.ellipse((95, 145, 305, 355), RED, OUT, 5)
    p.ellipse((130, 180, 270, 320), (240, 110, 110), OUT, 3)
    p.ellipse((170, 220, 230, 280), YELLOW, OUT, 4)


def zipper(p):
    tape = (60, 140, 200)
    gold = (230, 190, 60)
    p.rect((105, 25, 195, 375), tape, OUT, 4, 8)
    p.rect((205, 25, 295, 375), tape, OUT, 4, 8)
    for i, y in enumerate(range(150, 365, 22)):
        p.rect((178, y, 200, y + 12), gold, OUT, 2)
        p.rect((200, y + 11, 222, y + 23), gold, OUT, 2)
    p.rect((165, 80, 235, 150), (110, 110, 120), OUT, 4, 12)
    p.rect((185, 150, 215, 225), (140, 140, 150), OUT, 4, 10)
    p.ellipse((192, 195, 208, 215), WHITE, OUT, 2)


PICTURES = [
    ("apple", apple, None), ("ball", ball, None), ("cat", cat, None), ("dog", dog, None),
    ("egg", egg, None), ("fish", fish, None), ("grapes", grapes, None), ("hat", hat, None),
    ("icecream", icecream, None), ("jam", jam, None), ("kite", kite, None), ("leaf", leaf, None),
    ("moon", moon, None), ("nut", nut, None), ("orange", orange, None), ("pig", pig, None),
    ("queen", queen, None), ("rainbow", rainbow, None), ("sun", sun, None), ("tree", tree, None),
    ("umbrella", umbrella, None), ("van", van, None), ("watch", watch, None),
    ("xylophone", xylophone, None), ("yoyo", yoyo, None), ("zipper", zipper, None),
]

for name, draw, background in PICTURES:
    pic = Pic(background)
    draw(pic)
    pic.save(name)
    print("saved", name + ".png")
