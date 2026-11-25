#!/usr/bin/env python3
"""Draw the magazine-cover image for make.fun news-image-20261125.

Layout: masthead -> big dark cover panel for the lead story (Nvidia) ->
five numbered cover-line rows -> source footer. Pure PIL, real text only.
Output: entry.png, 1024x1024, deterministic (no timestamps, fixed PNG).
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PAPER = (250, 247, 240)      # warm off-white
INK = (17, 24, 39)           # near-black
PANEL = (17, 24, 39)         # dark navy panel
RED = (185, 28, 28)          # cover red
GOLD = (180, 83, 9)          # accent gold
GREY = (75, 85, 99)          # muted grey
LIGHT = (226, 232, 240)      # light grey on dark panel
RULE = (17, 24, 39)

M = 44  # side margin


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap measured with the real font; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.line([(M, 24), (W - M, 24)], fill=INK, width=4)
    f_date = font(BOLD, 86)
    d.text((W // 2, 34), "25 NOVEMBER 2026", font=f_date, fill=INK, anchor="ma")
    f_sub = font(BOLD, 25)
    d.text((W // 2, 132), "WEDNESDAY  \u2022  SIX STORIES FROM AROUND THE GLOBE",
           font=f_sub, fill=RED, anchor="ma")
    d.line([(M, 168), (W - M, 168)], fill=INK, width=4)

    # ---------- lead cover panel (dark) ----------
    px0, py0, px1, py1 = M, 182, W - M, 514
    d.rounded_rectangle([px0, py0, px1, py1], radius=10, fill=PANEL)
    pad = 34
    x = px0 + pad
    max_w = px1 - pad - x
    y = py0 + 22
    f_kick = font(BOLD, 26)
    d.text((x, y), "1  \u2022  MARKETS  |  USA", font=f_kick, fill=(252, 211, 77))
    y += 42
    f_head = font(BOLD, 47)
    headline = "NVIDIA SLIDES 7% AS LAWMAKERS DEMAND ANSWERS ON TRUMP'S ROLE"
    for line in wrap(d, headline, f_head, max_w):
        d.text((x, y), line, font=f_head, fill=(255, 255, 255))
        y += 54
    y += 6
    f_sum = font(FONT, 24)
    summary = ("Shares slid after both parties in Congress questioned President "
               "Trump's role in bringing back CEO Jensen Huang, reinstated days "
               "after resigning over an affair with a suspected Chinese spy.")
    for line in wrap(d, summary, f_sum, max_w):
        d.text((x, y), line, font=f_sum, fill=LIGHT)
        y += 30
    assert y <= py1 - 8, f"lead panel overflow: text ends y={y}, panel ends {py1}"

    # ---------- five numbered cover lines ----------
    rows = [
        ("2", "WHITE HOUSE  |  USA",
         "Freedom and Feathers Get the Presidential Pardon",
         "Trump spares the two turkeys; Feathers fled into the bushes first."),
        ("3", "MIDDLE EAST  |  YEMEN",
         "Houthis 60 km From Aden, Army Vows City Will Hold",
         "Government forces dig in as the Houthis close in on the capital."),
        ("4", "DIPLOMACY  |  INDIA\u2013NEPAL",
         "Nepal PM Shah Wraps First State Visit to India",
         "Modi and Shah agree a joint vision for the two neighbours."),
        ("5", "POLITICS  |  INDIA",
         "BJP and Akali Dal Reunite for Punjab 2027",
         "Six years after the farm-laws split, the old allies reunite."),
        ("6", "SAFETY  |  USA",
         "Army to Blast 9,500 lb of Lead Azide in Iowa",
         "Middletown residents told to evacuate before Wednesday's blast."),
    ]
    f_num = font(BOLD, 46)
    f_rkick = font(BOLD, 21)
    f_rhead = font(BOLD, 27)
    f_rsum = font(FONT, 21)
    row_y = 530
    row_h = 88
    for i, (num, kicker, head, summ) in enumerate(rows):
        d.text((M + 4, row_y + 4), num, font=f_num, fill=RED)
        tx = M + 78
        tw = W - M - tx
        d.text((tx, row_y), kicker, font=f_rkick, fill=GOLD)
        assert d.textlength(head, font=f_rhead) <= tw, f"row {num} headline too wide"
        d.text((tx, row_y + 25), head, font=f_rhead, fill=INK)
        # summary: wrap to at most 2 lines, assert it fits one row
        slines = wrap(d, summ, f_rsum, tw)
        assert len(slines) <= 1, f"row {num} summary wraps to {len(slines)} lines: {slines}"
        d.text((tx, row_y + 54), slines[0], font=f_rsum, fill=GREY)
        row_y += row_h
        if i < len(rows) - 1:
            d.line([(M, row_y - 6), (W - M, row_y - 6)], fill=(203, 213, 225), width=1)
    assert row_y <= 972, f"rows overflow: end y={row_y}"

    # ---------- footer ----------
    d.line([(M, 978), (W - M, 978)], fill=INK, width=2)
    f_foot = font(FONT, 20)
    d.text((W // 2, 988),
           "Sources: Reuters, AP, Bloomberg  \u2022  All events of 25 November 2026",
           font=f_foot, fill=GREY, anchor="ma")

    img.save("entry.png", "PNG", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    draw()
