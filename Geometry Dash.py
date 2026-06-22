import sys
import random
import math
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# ─── Translations ────────────────────────────────────────────────────────────────
TRANSLATIONS = {
    "en": {
        "title": "Geometry Dash",
        "score": "Score",
        "best": "Best",
        "speed": "Speed",
        "start": "Start Game",
        "restart": "Restart",
        "settings": "Settings",
        "theme": "Theme",
        "language": "Language",
        "light": "Light",
        "dark": "Dark",
        "game_over": "GAME OVER",
        "press_space": "Press SPACE or Click to Jump",
        "level": "Level",
        "attempts": "Attempts",
        "percent": "Progress",
        "normal": "Normal",
        "practice": "Practice",
        "mode": "Mode",
        "paused": "PAUSED",
        "resume": "Resume",
        "controls": "SPACE / Click to Jump  |  Double Jump allowed",
        "new_best": "NEW BEST!",
    },
    "zh": {
        "title": "几何冲刺",
        "score": "分数",
        "best": "最佳",
        "speed": "速度",
        "start": "开始游戏",
        "restart": "重新开始",
        "settings": "设置",
        "theme": "主题",
        "language": "语言",
        "light": "浅色",
        "dark": "深色",
        "game_over": "游戏结束",
        "press_space": "按空格或点击跳跃",
        "level": "关卡",
        "attempts": "尝试",
        "percent": "进度",
        "normal": "普通",
        "practice": "练习",
        "mode": "模式",
        "paused": "已暂停",
        "resume": "继续",
        "controls": "空格/点击跳跃 | 允许二段跳",
        "new_best": "新纪录！",
    },
    "fa": {
        "title": "جهش هندسی",
        "score": "امتیاز",
        "best": "بهترین",
        "speed": "سرعت",
        "start": "شروع بازی",
        "restart": "شروع مجدد",
        "settings": "تنظیمات",
        "theme": "تم",
        "language": "زبان",
        "light": "روشن",
        "dark": "تاریک",
        "game_over": "بازی تمام شد",
        "press_space": "فاصله یا کلیک برای پرش",
        "level": "مرحله",
        "attempts": "تلاش",
        "percent": "پیشرفت",
        "normal": "عادی",
        "practice": "تمرین",
        "mode": "حالت",
        "paused": "مکث",
        "resume": "ادامه",
        "controls": "فاصله/کلیک برای پرش | پرش دوگانه مجاز",
        "new_best": "رکورد جدید!",
    },
}

# ─── Themes ──────────────────────────────────────────────────────────────────────
THEMES = {
    "light": {
        "name": "light",
        "window_bg": "#F0F4FF",
        "panel_bg": "#FFFFFF",
        "panel_border": "#C8D8F0",
        "text": "#0A0A2E",
        "text_sub": "#5060A0",
        "accent": "#FF6B35",
        "accent2": "#4FC3F7",
        "accent3": "#A8E063",
        "btn_primary": "#5C6BC0",
        "btn_primary_h": "#3F51B5",
        "btn_success": "#43A047",
        "btn_success_h": "#2E7D32",
        "btn_danger": "#E53935",
        "btn_danger_h": "#B71C1C",
        "btn_text": "#FFFFFF",
        # Game colors
        "sky1": "#1A1A4E",
        "sky2": "#0D0D2B",
        "ground": "#1A1A3A",
        "ground_line": "#4040AA",
        "ground_glow": "#6060FF",
        "player1": "#FFD700",
        "player2": "#FFA500",
        "player_glow": "#FFFF00",
        "spike": "#FF4444",
        "spike2": "#FF0000",
        "block": "#5C6BC0",
        "block2": "#3F51B5",
        "block_glow": "#7986CB",
        "portal": "#00E5FF",
        "star": "#FFFFFF",
        "trail": "#FFD700",
        "progress_bg": "#2A2A5A",
        "progress_fill": "#FFD700",
        "hud_bg": "#FFFFFF",
        "hud_text": "#0A0A2E",
        "orb": "#00FF88",
        "pad": "#FF44FF",
    },
    "dark": {
        "name": "dark",
        "window_bg": "#050510",
        "panel_bg": "#0D0D1E",
        "panel_border": "#1A1A3A",
        "text": "#E8E8FF",
        "text_sub": "#7080C0",
        "accent": "#FF6B35",
        "accent2": "#4FC3F7",
        "accent3": "#A8E063",
        "btn_primary": "#16213E",
        "btn_primary_h": "#0F3460",
        "btn_success": "#1B5E20",
        "btn_success_h": "#2E7D32",
        "btn_danger": "#7F0000",
        "btn_danger_h": "#B71C1C",
        "btn_text": "#E8E8FF",
        # Game colors
        "sky1": "#050518",
        "sky2": "#080828",
        "ground": "#0A0A20",
        "ground_line": "#2020AA",
        "ground_glow": "#4040FF",
        "player1": "#FFD700",
        "player2": "#FFA500",
        "player_glow": "#FFFF00",
        "spike": "#FF3333",
        "spike2": "#CC0000",
        "block": "#1A237E",
        "block2": "#0D1557",
        "block_glow": "#3F51B5",
        "portal": "#00E5FF",
        "star": "#FFFFFF",
        "trail": "#FFD700",
        "progress_bg": "#0A0A20",
        "progress_fill": "#FFD700",
        "hud_bg": "#0D0D1E",
        "hud_text": "#E8E8FF",
        "orb": "#00FF88",
        "pad": "#FF44FF",
    },
}

# ─── Constants ───────────────────────────────────────────────────────────────────
GW, GH = 900, 480
FPS = 60
GROUND_Y = GH - 80
GRAVITY = 0.7
JUMP_V = -15.5
DOUBLE_JUMP_V = -14.0
BASE_SPEED = 5.5
PLAYER_SIZE = 36
TILE = 40


# ─── Particle ────────────────────────────────────────────────────────────────────
class Particle:
    def __init__(self, x, y, color, vx=None, vy=None, size=None, life=None, shape="circle"):
        self.x = x
        self.y = y
        self.color = color
        self.vx = vx if vx is not None else random.uniform(-4, 4)
        self.vy = vy if vy is not None else random.uniform(-6, -1)
        self.size = size if size is not None else random.uniform(3, 8)
        self.life = life if life is not None else random.randint(20, 45)
        self.max_life = self.life
        self.shape = shape
        self.rot = random.uniform(0, 360)
        self.rot_v = random.uniform(-8, 8)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.25
        self.vx *= 0.96
        self.life -= 1
        self.rot += self.rot_v

    def draw(self, p: QPainter):
        alpha = int(255 * self.life / self.max_life)
        c = QColor(self.color)
        c.setAlpha(max(0, alpha))
        p.setBrush(QBrush(c))
        p.setPen(Qt.PenStyle.NoPen)
        if self.shape == "rect":
            p.save()
            p.translate(self.x, self.y)
            p.rotate(self.rot)
            p.drawRect(QRectF(-self.size / 2, -self.size / 2, self.size, self.size))
            p.restore()
        else:
            p.drawEllipse(QRectF(self.x - self.size / 2, self.y - self.size / 2,
                                 self.size, self.size))


# ─── Obstacle Types ───────────────────────────────────────────────────────────────
class Spike:
    def __init__(self, x, y, count=1, inverted=False):
        self.x = x
        self.y = y
        self.count = count
        self.inverted = inverted
        self.w = count * 28
        self.h = 36

    def get_rects(self):
        rects = []
        for i in range(self.count):
            sx = self.x + i * 28
            rects.append(QRectF(sx + 4, self.y - self.h + 6, 20, self.h - 6))
        return rects

    def draw(self, painter: QPainter, t: dict):
        for i in range(self.count):
            sx = self.x + i * 28
            path = QPainterPath()
            if not self.inverted:
                path.moveTo(sx, self.y)
                path.lineTo(sx + 14, self.y - self.h)
                path.lineTo(sx + 28, self.y)
            else:
                path.moveTo(sx, self.y)
                path.lineTo(sx + 14, self.y + self.h)
                path.lineTo(sx + 28, self.y)
            path.closeSubpath()
            grad = QLinearGradient(sx, self.y, sx + 14, self.y - self.h)
            grad.setColorAt(0, QColor(t["spike"]))
            grad.setColorAt(1, QColor(t["spike2"]).lighter(150))
            painter.setBrush(QBrush(grad))
            painter.setPen(QPen(QColor(t["spike2"]), 1.5))
            painter.drawPath(path)
            # Glow
            glow_c = QColor(t["spike"])
            glow_c.setAlpha(60)
            painter.setBrush(QBrush(glow_c))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawPath(path)


class Block:
    def __init__(self, x, y, w=TILE, h=TILE):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.anim = random.uniform(0, 360)

    def rect(self):
        return QRectF(self.x, self.y, self.w, self.h)

    def update(self):
        self.anim = (self.anim + 1.5) % 360

    def draw(self, painter: QPainter, t: dict):
        r = self.rect()
        grad = QLinearGradient(self.x, self.y, self.x + self.w, self.y + self.h)
        grad.setColorAt(0, QColor(t["block_glow"]))
        grad.setColorAt(0.5, QColor(t["block"]))
        grad.setColorAt(1, QColor(t["block2"]))
        painter.setBrush(QBrush(grad))
        painter.setPen(QPen(QColor(t["block_glow"]), 1.5))
        painter.drawRoundedRect(r, 4, 4)
        # Inner pattern
        painter.setPen(QPen(QColor(t["block_glow"]).lighter(120), 0.8))
        painter.drawLine(QPointF(self.x + 5, self.y + 5), QPointF(self.x + self.w - 5, self.y + 5))
        painter.drawLine(QPointF(self.x + 5, self.y + 5), QPointF(self.x + 5, self.y + self.h - 5))
        # Glow pulse
        gv = abs(math.sin(math.radians(self.anim))) * 40 + 20
        glow = QColor(t["block_glow"])
        glow.setAlpha(int(gv))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(glow, 3))
        painter.drawRoundedRect(r.adjusted(-2, -2, 2, 2), 6, 6)


class YellowOrb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 14
        self.anim = 0
        self.collected = False

    def rect(self):
        return QRectF(self.x - self.r, self.y - self.r, self.r * 2, self.r * 2)

    def update(self):
        self.anim = (self.anim + 3) % 360

    def draw(self, painter: QPainter, t: dict):
        if self.collected:
            return
        pulse = abs(math.sin(math.radians(self.anim))) * 4
        r = self.r + pulse
        grad = QRadialGradient(self.x, self.y, r)
        grad.setColorAt(0, QColor("#FFFFFF"))
        grad.setColorAt(0.4, QColor(t["orb"]))
        grad.setColorAt(1, QColor(t["orb"]).darker(180))
        painter.setBrush(QBrush(grad))
        painter.setPen(QPen(QColor(t["orb"]), 1.5))
        painter.drawEllipse(QRectF(self.x - r, self.y - r, r * 2, r * 2))


# ─── Player ───────────────────────────────────────────────────────────────────────
class Player:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.vy = 0.0
        self.on_ground = False
        self.jumps_left = 2
        self.alive = True
        self.rotation = 0.0
        self.rot_speed = 0.0
        self.trail: list[dict] = []
        self.size = PLAYER_SIZE
        self.glow_anim = 0

    def rect(self):
        return QRectF(self.x - self.size / 2, self.y - self.size / 2,
                      self.size, self.size)

    def jump(self):
        if self.jumps_left > 0:
            v = JUMP_V if self.jumps_left == 2 else DOUBLE_JUMP_V
            self.vy = v
            self.jumps_left -= 1
            self.rot_speed = -12 if self.jumps_left == 1 else -10
            return True
        return False

    def update(self, ground_y):
        self.vy += GRAVITY
        self.y += self.vy

        if not self.on_ground:
            self.rotation = (self.rotation + self.rot_speed) % 360
        else:
            self.rotation = round(self.rotation / 90) * 90

        # Trail
        self.trail.append({"x": self.x, "y": self.y,
                            "rot": self.rotation, "alpha": 200})
        if len(self.trail) > 12:
            self.trail.pop(0)
        for tr in self.trail:
            tr["alpha"] = max(0, tr["alpha"] - 18)

        self.glow_anim = (self.glow_anim + 4) % 360

        if self.y >= ground_y - self.size / 2:
            self.y = ground_y - self.size / 2
            self.vy = 0
            self.on_ground = True
            self.jumps_left = 2
            self.rot_speed = 0
        else:
            self.on_ground = False

    def draw(self, painter: QPainter, t: dict):
        # Trail
        for i, tr in enumerate(self.trail):
            alpha = int(tr["alpha"] * (i / len(self.trail)))
            if alpha <= 0:
                continue
            c = QColor(t["trail"])
            c.setAlpha(alpha)
            painter.save()
            painter.translate(tr["x"], tr["y"])
            painter.rotate(tr["rot"])
            s = self.size * 0.6 * (i / len(self.trail))
            painter.setBrush(QBrush(c))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(QRectF(-s / 2, -s / 2, s, s), 3, 3)
            painter.restore()

        painter.save()
        painter.translate(self.x, self.y)
        painter.rotate(self.rotation)

        s = self.size
        h = s / 2

        # Outer glow
        gv = abs(math.sin(math.radians(self.glow_anim))) * 60 + 30
        for gi in range(3, 0, -1):
            gc = QColor(t["player_glow"])
            gc.setAlpha(int(gv / gi))
            painter.setBrush(QBrush(gc))
            painter.setPen(Qt.PenStyle.NoPen)
            gs = s + gi * 5
            painter.drawRoundedRect(QRectF(-gs / 2, -gs / 2, gs, gs), 6, 6)

        # Body gradient
        grad = QLinearGradient(-h, -h, h, h)
        grad.setColorAt(0, QColor(t["player1"]))
        grad.setColorAt(0.5, QColor(t["player2"]))
        grad.setColorAt(1, QColor(t["player1"]).darker(150))
        painter.setBrush(QBrush(grad))
        painter.setPen(QPen(QColor(t["player2"]).darker(120), 2))
        painter.drawRoundedRect(QRectF(-h, -h, s, s), 5, 5)

        # Inner design - star/cross
        painter.setPen(QPen(QColor(t["player1"]).lighter(180), 2))
        painter.drawLine(QPointF(0, -h + 6), QPointF(0, h - 6))
        painter.drawLine(QPointF(-h + 6, 0), QPointF(h - 6, 0))

        # Center dot
        painter.setBrush(QBrush(QColor("#FFFFFF")))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QRectF(-5, -5, 10, 10))

        painter.restore()


# ─── Level Generator ──────────────────────────────────────────────────────────────
def gen_chunk(start_x: float, difficulty: float) -> list:
    objects = []
    x = start_x
    chunk_end = x + random.randint(600, 1000)

    while x < chunk_end:
        gap = random.randint(60, 140)
        roll = random.random()

        if roll < 0.35:
            # Single or double spike
            n = random.randint(1, min(3, int(1 + difficulty * 2)))
            objects.append(Spike(x, GROUND_Y, n))
            x += n * 28 + gap

        elif roll < 0.55:
            # Block stack
            stack = random.randint(1, min(3, int(1 + difficulty)))
            bx = x
            for s in range(stack):
                by = GROUND_Y - s * TILE - TILE
                objects.append(Block(bx, by))
                if s == stack - 1 and random.random() < 0.4 * difficulty:
                    objects.append(Spike(bx, by, 1))
            x += TILE + gap

        elif roll < 0.70 and difficulty > 0.3:
            # Floating block with spike below
            fy = GROUND_Y - random.randint(100, 180)
            objects.append(Block(x, fy))
            if random.random() < 0.5:
                objects.append(Spike(x + 5, GROUND_Y, 1))
            objects.append(YellowOrb(x + TILE / 2, fy - 35))
            x += TILE + gap

        elif roll < 0.80:
            # Orb
            oy = GROUND_Y - random.randint(80, 200)
            objects.append(YellowOrb(x, oy))
            x += gap

        else:
            x += gap + 40

    return objects


# ─── Game Widget ─────────────────────────────────────────────────────────────────
class GameWidget(QWidget):
    sig_score = pyqtSignal(int)
    sig_best = pyqtSignal(int)
    sig_percent = pyqtSignal(int)
    sig_speed = pyqtSignal(float)
    sig_dead = pyqtSignal(int)
    sig_attempts = pyqtSignal(int)

    def __init__(self, theme: dict, parent=None):
        super().__init__(parent)
        self.theme = theme
        self.setFixedSize(GW, GH)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.state = "idle"
        self.score = 0
        self.best = 0
        self.attempts = 0
        self.distance = 0.0
        self.speed = BASE_SPEED
        self.particles: list[Particle] = []

        self.player = Player(160, GROUND_Y - PLAYER_SIZE / 2)
        self.objects: list = []
        self.camera_x = 0.0
        self.level_length = 8000.0

        self.bg_stars = [(random.randint(0, GW * 3), random.randint(0, GH - 100),
                          random.uniform(0.5, 2.5), random.uniform(0, 360))
                         for _ in range(120)]
        self.bg_layers = [
            {"shapes": self._gen_bg_layer(GW * 3, i), "speed": 0.1 + i * 0.15}
            for i in range(3)
        ]
        self.ground_tiles = list(range(0, GW + TILE * 2, TILE))
        self.anim_tick = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._loop)
        self.timer.setInterval(1000 // FPS)

    def _gen_bg_layer(self, w, depth):
        shapes = []
        for _ in range(20 + depth * 10):
            shapes.append({
                "x": random.randint(0, w),
                "y": random.randint(20, GH - 120),
                "w": random.randint(20, 60 - depth * 15),
                "h": random.randint(40, 100 - depth * 20),
                "alpha": random.randint(10, 30 - depth * 5),
            })
        return shapes

    def set_theme(self, theme):
        self.theme = theme
        self.update()

    def start(self):
        self.attempts += 1
        self.sig_attempts.emit(self.attempts)
        self.score = 0
        self.distance = 0.0
        self.speed = BASE_SPEED
        self.camera_x = 0.0
        self.particles.clear()
        self.player = Player(160, GROUND_Y - PLAYER_SIZE / 2)

        # Generate level
        self.objects.clear()
        x = 400.0
        diff = 0.0
        while x < self.level_length:
            chunk = gen_chunk(x, diff)
            self.objects.extend(chunk)
            x += 700
            diff = min(1.0, diff + 0.08)

        self.state = "playing"
        self.timer.start()
        self.setFocus()

    def stop(self):
        self.timer.stop()
        self.state = "idle"

    def _loop(self):
        if self.state != "playing":
            return

        t = self.theme
        self.anim_tick += 1
        self.speed = min(BASE_SPEED + self.distance / 2000, BASE_SPEED * 2.2)

        # Move world
        self.distance += self.speed
        self.camera_x += self.speed

        # Score
        self.score = int(self.distance / 10)
        pct = min(100, int(self.distance / self.level_length * 100))
        self.sig_score.emit(self.score)
        self.sig_percent.emit(pct)
        self.sig_speed.emit(self.speed)

        # Update player
        self.player.update(GROUND_Y)

        # Update objects
        for obj in self.objects:
            if hasattr(obj, "update"):
                obj.update()

        # Orb collection
        pr = self.player.rect()
        pr_screen = QRectF(self.player.x, self.player.y - self.player.size / 2,
                           self.player.size, self.player.size)

        for obj in self.objects:
            if isinstance(obj, YellowOrb) and not obj.collected:
                orb_x = obj.x - self.camera_x + 160
                orb_r = QRectF(orb_x - obj.r, obj.y - obj.r, obj.r * 2, obj.r * 2)
                if pr_screen.intersects(orb_r):
                    obj.collected = True
                    self.player.jump()
                    self.score += 50
                    self._burst(orb_x, obj.y, t["orb"], 16)

        # Collision
        for obj in self.objects:
            ox = self._obj_x(obj)
            if ox < -100 or ox > GW + 100:
                continue

            if isinstance(obj, Spike):
                for sr in obj.get_rects():
                    sr2 = QRectF(sr.x() - self.camera_x + 160,
                                 sr.y(), sr.width(), sr.height())
                    if pr_screen.intersects(sr2):
                        self._die()
                        return

            elif isinstance(obj, Block):
                br = QRectF(obj.x - self.camera_x + 160, obj.y, obj.w, obj.h)
                if pr_screen.intersects(br):
                    self._die()
                    return

        if self.distance >= self.level_length:
            self._die()

        # Particles
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.life > 0]

        self.update()

    def _obj_x(self, obj):
        if isinstance(obj, (Spike, Block)):
            return obj.x - self.camera_x + 160
        if isinstance(obj, YellowOrb):
            return obj.x - self.camera_x + 160
        return -9999

    def _die(self):
        self.state = "dead"
        self.timer.stop()
        if self.score > self.best:
            self.best = self.score
        self.sig_dead.emit(self.score)
        self.sig_best.emit(self.best)
        # burst
        self._burst(self.player.x, self.player.y, self.theme["player1"], 30)

    def _burst(self, x, y, color, count):
        for _ in range(count):
            self.particles.append(Particle(x, y, color))

    def mousePressEvent(self, e):
        if self.state == "playing":
            self.player.jump()

    def keyPressEvent(self, e):
        if e.key() in (Qt.Key.Key_Space, Qt.Key.Key_Up, Qt.Key.Key_W):
            if self.state == "playing":
                self.player.jump()

    def paintEvent(self, e):
        p = QPainter(self)
        t = self.theme

        # Sky gradient
        grad = QLinearGradient(0, 0, 0, GH)
        grad.setColorAt(0, QColor(t["sky1"]))
        grad.setColorAt(1, QColor(t["sky2"]))
        p.fillRect(self.rect(), grad)

        # Stars
        for i, (sx, sy, ss, rot) in enumerate(self.bg_stars):
            x = (sx - self.camera_x * 0.1) % (GW * 3)
            c = QColor(t["star"])
            c.setAlpha(140)
            p.setBrush(QBrush(c))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(QRectF(x, sy, ss, ss))

        # BG layers
        for layer in self.bg_layers:
            for shp in layer["shapes"]:
                lx = (shp["x"] - self.camera_x * layer["speed"]) % (GW * 3)
                c = QColor(255, 255, 255, shp["alpha"])
                p.setBrush(QBrush(c))
                p.setPen(Qt.PenStyle.NoPen)
                p.drawRect(QRectF(lx, shp["y"], shp["w"], shp["h"]))

        # Ground
        grad_g = QLinearGradient(0, GROUND_Y, 0, GH)
        grad_g.setColorAt(0, QColor(t["ground_line"]))
        grad_g.setColorAt(0.2, QColor(t["ground_glow"]))
        grad_g.setColorAt(1, QColor(t["ground"]))
        p.setBrush(QBrush(grad_g))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRect(0, GROUND_Y, GW, GH - GROUND_Y)

        # Ground tiles
        p.setPen(QPen(QColor(t["ground_line"]), 1))
        for i in range(-2, GW // TILE + 4):
            x = (i * TILE - (self.camera_x % TILE))
            p.drawLine(x, GROUND_Y, x, GH)

        # Objects
        for obj in self.objects:
            ox = self._obj_x(obj)
            if ox < -80 or ox > GW + 80:
                continue
            p.save()
            p.translate(ox - obj.x, 0)
            if isinstance(obj, Spike):
                obj.draw(p, t)
            elif isinstance(obj, Block):
                obj.draw(p, t)
            elif isinstance(obj, YellowOrb):
                obj.draw(p, t)
            p.restore()

        # Player
        self.player.draw(p, t)

        # Particles
        for pa in self.particles:
            pa.draw(p)

        # Messages
        if self.state == "idle":
            p.setPen(QPen(QColor(t["text"]), 3))
            p.setFont(QFont("Arial", 36, QFont.Weight.Bold))
            p.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Press SPACE to Start")

        if self.state == "dead":
            p.setPen(QPen(QColor(t["accent"]), 4))
            p.setFont(QFont("Arial", 40, QFont.Weight.Bold))
            p.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "GAME OVER")


# ─── UI Window ────────────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.lang = "en"
        self.theme_name = "dark"

        self.theme = THEMES[self.theme_name]
        self.t = TRANSLATIONS[self.lang]

        self.setWindowTitle(self.t["title"])
        self.setFixedSize(GW, GH + 120)

        self.game = GameWidget(self.theme)
        self.game.sig_score.connect(self.update_score)
        self.game.sig_best.connect(self.update_best)
        self.game.sig_percent.connect(self.update_percent)
        self.game.sig_speed.connect(self.update_speed)
        self.game.sig_dead.connect(self.on_dead)
        self.game.sig_attempts.connect(self.update_attempts)

        self.lbl_score = QLabel()
        self.lbl_best = QLabel()
        self.lbl_percent = QLabel()
        self.lbl_speed = QLabel()
        self.lbl_attempts = QLabel()
        self.btn_start = QPushButton()
        self.btn_restart = QPushButton()
        self.cmb_theme = QComboBox()
        self.cmb_lang = QComboBox()

        self._build_ui()
        self._update_texts()
        self._apply_theme()

    def _build_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        top = QHBoxLayout()
        mid = QHBoxLayout()
        bottom = QHBoxLayout()

        layout.addLayout(top)
        layout.addWidget(self.game)
        layout.addLayout(mid)
        layout.addLayout(bottom)
        self.setCentralWidget(widget)

        top.addWidget(self.lbl_score)
        top.addWidget(self.lbl_best)
        top.addWidget(self.lbl_percent)
        top.addWidget(self.lbl_speed)
        top.addWidget(self.lbl_attempts)
        top.addStretch()

        self.btn_start.clicked.connect(self.game.start)
        self.btn_restart.clicked.connect(self.game.start)

        mid.addWidget(self.btn_start)
        mid.addWidget(self.btn_restart)

        self.cmb_theme.addItems(["light", "dark"])
        self.cmb_theme.currentTextChanged.connect(self.change_theme)
        bottom.addWidget(QLabel("Theme:"))
        bottom.addWidget(self.cmb_theme)

        self.cmb_lang.addItems(["en", "zh", "fa"])
        self.cmb_lang.currentTextChanged.connect(self.change_lang)
        bottom.addWidget(QLabel("Language:"))
        bottom.addWidget(self.cmb_lang)

    def _update_texts(self):
        t = self.t
        self.setWindowTitle(t["title"])
        self.btn_start.setText(t["start"])
        self.btn_restart.setText(t["restart"])
        self.lbl_score.setText(f"{t['score']}: 0")
        self.lbl_best.setText(f"{t['best']}: 0")
        self.lbl_percent.setText(f"{t['percent']}: 0%")
        self.lbl_speed.setText(f"{t['speed']}: 0")
        self.lbl_attempts.setText(f"{t['attempts']}: 0")

    def _apply_theme(self):
        t = self.theme
        pal = self.palette()
        pal.setColor(QPalette.ColorRole.Window, QColor(t["window_bg"]))
        pal.setColor(QPalette.ColorRole.WindowText, QColor(t["text"]))
        self.setPalette(pal)

    def change_theme(self, th):
        self.theme_name = th
        self.theme = THEMES[th]
        self.game.set_theme(self.theme)
        self._apply_theme()

    def change_lang(self, lang):
        self.lang = lang
        self.t = TRANSLATIONS[lang]
        self._update_texts()

    def update_score(self, v):
        self.lbl_score.setText(f"{self.t['score']}: {v}")

    def update_best(self, v):
        self.lbl_best.setText(f"{self.t['best']}: {v}")

    def update_percent(self, v):
        self.lbl_percent.setText(f"{self.t['percent']}: {v}%")

    def update_speed(self, v):
        self.lbl_speed.setText(f"{self.t['speed']}: {v:.1f}")

    def update_attempts(self, v):
        self.lbl_attempts.setText(f"{self.t['attempts']}: {v}")

    def on_dead(self, v):
        pass


# ─── Main ─────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
