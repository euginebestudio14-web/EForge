# =============================================================================
# ███████╗███████╗ ██████╗ ██████╗  ██████╗ ███████╗
# ██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝
# █████╗  █████╗  ██║   ██║██████╔╝██║  ███╗█████╗
# ██╔══╝  ██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝
# ███████╗██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗
# ╚══════╝╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
#
# EForge — Single-File 2D Game Framework built on Pygame
# Version  : 1.0.0
# Target   : Android (Pydroid 3) + PC
# Usage    : from eforge import *
# =============================================================================

# =============================================================================
# ===[ EXPORTS ]================================================================
# =============================================================================

__all__ = [
    # Theme
    "Theme", "Style",
    # Math & Utils
    "Vec2", "Rect2", "clamp", "lerp", "sign", "overlap_aabb", "overlap_circle",
    # Assets
    "Assets",
    # Input
    "Input",
    # Audio
    "Audio",
    # ECS Core
    "Entity", "World", "System", "Pool",
    # Components
    "Transform", "Velocity", "Sprite", "Collider", "Animator",
    "Health", "StateMachine", "Timer", "Stats", "Hitbox",
    "Inventory", "Shadow", "Light", "Tag", "NetSync", "SyncMode",
    # Systems
    "PhysicsSystem", "RenderSystem", "AnimationSystem",
    "CollisionSystem", "LightSystem",
    # Physics config
    "Physics",
    # Tilemap
    "Tilemap",
    # Camera
    "Camera",
    # Pathfinding
    "Pathfinder",
    # Networking (optional)
    "Network", "NetMode", "Lobby", "TurnManager",
    # UI
    "UIManager", "Button", "Label", "Panel", "ProgressBar",
    "HealthBar", "Slider", "Toggle", "Dropdown", "TextInput",
    "ScrollView", "Grid", "Toast", "Modal", "Joystick",
    "VStack", "HStack", "Anchor",
    # Debug
    "Debug",
    # Scene
    "Scene", "SceneManager",
    # Event
    "EventBus",
    # Save
    "Save",
    # Game Loop
    "Game",
]

# =============================================================================
# ===[ IMPORTS ]================================================================
# =============================================================================

import pygame
import sys
import os
import json
import math
import time
import uuid
import weakref
import threading
import socket
import struct
import traceback
from collections import defaultdict, deque
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()

# =============================================================================
# ===[ THEME ]=================================================================
# =============================================================================

class _ThemeMeta:
    """Global visual configuration. Change once — updates everywhere."""

    PLAIN = {
        "bg":           (45,  45,  45),
        "text":         (220, 220, 220),
        "accent":       (160, 160, 160),
        "button_bg":    (65,  65,  65),
        "button_hover": (90,  90,  90),
        "button_press": (40,  40,  40),
        "debug_color":  (180, 255, 120),
        "border":       (90,  90,  90),
        "panel_bg":     (55,  55,  55),
        "bar_fg":       (100, 200, 100),
        "bar_bg":       (40,  40,  40),
        "input_bg":     (35,  35,  35),
        "toast_bg":     (60,  60,  60),
        "modal_bg":     (50,  50,  50),
        "shadow":       (0,   0,   0),
        "overlay":      (0,   0,   0),
    }

    DARK = {
        "bg":           (18,  18,  18),
        "text":         (200, 200, 200),
        "accent":       (120, 120, 255),
        "button_bg":    (30,  30,  30),
        "button_hover": (50,  50,  50),
        "button_press": (15,  15,  15),
        "debug_color":  (0,   255, 140),
        "border":       (60,  60,  60),
        "panel_bg":     (25,  25,  25),
        "bar_fg":       (80,  200, 80),
        "bar_bg":       (30,  30,  30),
        "input_bg":     (22,  22,  22),
        "toast_bg":     (35,  35,  35),
        "modal_bg":     (28,  28,  28),
        "shadow":       (0,   0,   0),
        "overlay":      (0,   0,   0),
    }

    DRACULA = {
        "bg":           (40,  42,  54),
        "text":         (248, 248, 242),
        "accent":       (189, 147, 249),
        "button_bg":    (68,  71,  90),
        "button_hover": (98,  114, 164),
        "button_press": (40,  42,  54),
        "debug_color":  (80,  250, 123),
        "border":       (98,  114, 164),
        "panel_bg":     (50,  52,  66),
        "bar_fg":       (80,  250, 123),
        "bar_bg":       (40,  42,  54),
        "input_bg":     (33,  34,  44),
        "toast_bg":     (68,  71,  90),
        "modal_bg":     (50,  52,  66),
        "shadow":       (0,   0,   0),
        "overlay":      (0,   0,   0),
    }

    LIGHT = {
        "bg":           (240, 240, 240),
        "text":         (30,  30,  30),
        "accent":       (60,  120, 220),
        "button_bg":    (210, 210, 210),
        "button_hover": (190, 190, 190),
        "button_press": (170, 170, 170),
        "debug_color":  (0,   100, 200),
        "border":       (180, 180, 180),
        "panel_bg":     (225, 225, 225),
        "bar_fg":       (60,  180, 60),
        "bar_bg":       (200, 200, 200),
        "input_bg":     (255, 255, 255),
        "toast_bg":     (200, 200, 200),
        "modal_bg":     (220, 220, 220),
        "shadow":       (150, 150, 150),
        "overlay":      (0,   0,   0),
    }

    def __init__(self):
        self._current = dict(self.PLAIN)

    def apply(self, preset: dict):
        self._current = dict(preset)

    def set(self, **kwargs):
        self._current.update(kwargs)

    def get(self, key: str, fallback=None):
        return self._current.get(key, fallback)

    def __getitem__(self, key):
        return self._current[key]

Theme = _ThemeMeta()


class Style:
    """Per-widget style override. Does not affect global Theme."""
    __slots__ = (
        "bg", "text_color", "radius", "font_size", "font_key",
        "border", "padding", "hover_bg", "press_bg",
    )

    def __init__(
        self,
        bg=None, text_color=None, radius=6,
        font_size=20, font_key="default",
        border=None, padding=8,
        hover_bg=None, press_bg=None,
    ):
        self.bg         = bg
        self.text_color = text_color
        self.radius     = radius
        self.font_size  = font_size
        self.font_key   = font_key
        self.border     = border
        self.padding    = padding
        self.hover_bg   = hover_bg
        self.press_bg   = press_bg

    def resolve(self, key: str):
        """Return style value if set, else fall back to Theme."""
        mapping = {
            "bg":       "button_bg",
            "text_color": "text",
            "border":   "border",
            "hover_bg": "button_hover",
            "press_bg": "button_press",
        }
        val = getattr(self, key, None)
        if val is not None:
            return val
        theme_key = mapping.get(key, key)
        return Theme.get(theme_key, (128, 128, 128))

# =============================================================================
# ===[ MATH & UTILS ]===========================================================
# =============================================================================

def clamp(val, lo, hi):
    return max(lo, min(hi, val))

def lerp(a, b, t):
    return a + (b - a) * clamp(t, 0.0, 1.0)

def sign(x):
    return 0 if x == 0 else (1 if x > 0 else -1)

def overlap_aabb(ax, ay, aw, ah, bx, by, bw, bh):
    """Returns True if two AABBs overlap."""
    return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by

def overlap_circle(ax, ay, ar, bx, by, br):
    """Returns True if two circles overlap."""
    dx = ax - bx
    dy = ay - by
    return dx * dx + dy * dy < (ar + br) ** 2


class Vec2:
    """Simple 2D vector."""
    __slots__ = ("x", "y")

    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y

    def __add__(self, o):  return Vec2(self.x + o.x, self.y + o.y)
    def __sub__(self, o):  return Vec2(self.x - o.x, self.y - o.y)
    def __mul__(self, s):  return Vec2(self.x * s, self.y * s)
    def __repr__(self):    return f"Vec2({self.x:.2f}, {self.y:.2f})"

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def normalized(self):
        l = self.length()
        if l == 0:
            return Vec2(0, 0)
        return Vec2(self.x / l, self.y / l)

    def dot(self, o):
        return self.x * o.x + self.y * o.y

    def tuple(self):
        return (self.x, self.y)


class Rect2:
    """Simple 2D rectangle."""
    __slots__ = ("x", "y", "w", "h")

    def __init__(self, x=0, y=0, w=0, h=0):
        self.x = x; self.y = y
        self.w = w; self.h = h

    def to_pygame(self):
        return pygame.Rect(int(self.x), int(self.y), int(self.w), int(self.h))

    def overlaps(self, o):
        return overlap_aabb(self.x, self.y, self.w, self.h, o.x, o.y, o.w, o.h)

# =============================================================================
# ===[ ASSETS ]================================================================
# =============================================================================

class _AssetManager:
    """Loads and caches all game assets from a JSON manifest."""

    def __init__(self):
        self._images:  Dict[str, pygame.Surface] = {}
        self._sounds:  Dict[str, pygame.mixer.Sound] = {}
        self._fonts:   Dict[str, pygame.font.Font] = {}
        self._maps:    Dict[str, dict] = {}
        self._sheets:  Dict[str, dict] = {}
        self._manifest: dict = {}
        self._default_font: Optional[pygame.font.Font] = None

    def _default(self, size=20) -> pygame.font.Font:
        if self._default_font is None:
            self._default_font = pygame.font.SysFont("monospace", size)
        return self._default_font

    def load(self, manifest_path: str):
        """Load all assets declared in a JSON manifest file."""
        if not os.path.exists(manifest_path):
            return
        with open(manifest_path, "r") as f:
            data = json.load(f)
        self._manifest = data

        for key, path in data.get("images", {}).items():
            self._load_image(key, path)

        for key, info in data.get("spritesheets", {}).items():
            surf = self._load_image(key, info["path"])
            self._sheets[key] = {
                "surface": surf,
                "tile_w":  info.get("tile_w", 32),
                "tile_h":  info.get("tile_h", 32),
            }

        for key, path in data.get("sounds", {}).items():
            try:
                snd = pygame.mixer.Sound(path)
                self._sounds[key] = snd
            except Exception as e:
                print(f"[Assets] Cannot load sound '{key}': {e}")

        for key, info in data.get("fonts", {}).items():
            try:
                size = info.get("size", 20) if isinstance(info, dict) else 20
                path = info.get("path", info) if isinstance(info, dict) else info
                fnt = pygame.font.Font(path, size)
                self._fonts[key] = fnt
            except Exception as e:
                print(f"[Assets] Cannot load font '{key}': {e}")

        for key, path in data.get("tilemaps", {}).items():
            try:
                with open(path, "r") as f:
                    self._maps[key] = json.load(f)
            except Exception as e:
                print(f"[Assets] Cannot load map '{key}': {e}")

    def _load_image(self, key: str, path: str) -> Optional[pygame.Surface]:
        try:
            surf = pygame.image.load(path).convert_alpha()
            self._images[key] = surf
            return surf
        except Exception as e:
            print(f"[Assets] Cannot load image '{key}': {e}")
            # Fallback magenta square
            s = pygame.Surface((32, 32), pygame.SRCALPHA)
            s.fill((255, 0, 255, 200))
            self._images[key] = s
            return s

    def get(self, key: str) -> Optional[pygame.Surface]:
        return self._images.get(key)

    def get_font(self, key: str = "default", size: int = 20) -> pygame.font.Font:
        if key == "default":
            return self._default(size)
        return self._fonts.get(key, self._default(size))

    def get_map(self, key: str) -> Optional[dict]:
        return self._maps.get(key)

    def get_sheet(self, key: str) -> Optional[dict]:
        return self._sheets.get(key)

    def get_sound(self, key: str) -> Optional[pygame.mixer.Sound]:
        return self._sounds.get(key)

    def preload(self, keys: List[str]):
        """Force-load specific assets from manifest."""
        for key in keys:
            if key in self._manifest.get("images", {}):
                self._load_image(key, self._manifest["images"][key])


Assets = _AssetManager()

# =============================================================================
# ===[ INPUT ]=================================================================
# =============================================================================

class _VButton:
    __slots__ = ("action", "x", "y", "size", "label", "_pressed", "_held", "_released")

    def __init__(self, action, x, y, size, label):
        self.action   = action
        self.x        = x
        self.y        = y
        self.size     = size
        self.label    = label
        self._pressed  = False
        self._held     = False
        self._released = False

    def contains(self, tx, ty):
        cx = self.x + self.size // 2
        cy = self.y + self.size // 2
        r  = self.size // 2
        return (tx - cx) ** 2 + (ty - cy) ** 2 <= r * r


class _VJoystick:
    __slots__ = ("cx", "cy", "radius", "_axis_x", "_axis_y", "_active", "_touch_id")

    def __init__(self, cx, cy, radius):
        self.cx       = cx
        self.cy       = cy
        self.radius   = radius
        self._axis_x  = 0.0
        self._axis_y  = 0.0
        self._active  = False
        self._touch_id = None


class _InputManager:
    """Processes all input once per frame into a clean state."""

    def __init__(self):
        self._key_map:     Dict[str, int] = {}
        self._pressed:     Set[str] = set()
        self._held:        Set[str] = set()
        self._released:    Set[str] = set()
        self._vbuttons:    List[_VButton] = []
        self._joystick:    Optional[_VJoystick] = None
        self._touch_pos:   Optional[Tuple[int, int]] = None
        self._prev_touch:  Optional[Tuple[int, int]] = None
        self._tapped:      bool = False
        self._swipe:       Optional[str] = None
        self._touch_start: Optional[Tuple[int, int]] = None
        self._touch_time:  float = 0.0
        self._events:      List = []

    def map(self, action: str, key_name: str):
        """Map an action name to a Pygame key name."""
        key = getattr(pygame, f"K_{key_name.upper()}", None)
        if key is None:
            print(f"[Input] Unknown key: {key_name}")
        else:
            self._key_map[action] = key

    def add_button(self, action: str, x: int, y: int, size: int = 80, label: str = ""):
        self._vbuttons.append(_VButton(action, x, y, size, label))

    def add_joystick(self, x: int, y: int, radius: int = 80):
        self._joystick = _VJoystick(x, y, radius)

    def update(self):
        """Process all input events. Call once per frame before update()."""
        self._pressed.clear()
        self._released.clear()
        self._tapped  = False
        self._swipe   = None

        # Reset vbutton frame state
        for btn in self._vbuttons:
            btn._pressed  = False
            btn._released = False

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                for action, k in self._key_map.items():
                    if event.key == k:
                        self._pressed.add(action)
                        self._held.add(action)

            elif event.type == pygame.KEYUP:
                for action, k in self._key_map.items():
                    if event.key == k:
                        self._released.add(action)
                        self._held.discard(action)

            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    tx, ty = event.pos
                elif event.type == pygame.FINGERDOWN:
                    sw = pygame.display.get_surface().get_width()
                    sh = pygame.display.get_surface().get_height()
                    tx, ty = int(event.x * sw), int(event.y * sh)

                self._touch_pos   = (tx, ty)
                self._touch_start = (tx, ty)
                self._touch_time  = time.time()

                for btn in self._vbuttons:
                    if btn.contains(tx, ty):
                        btn._pressed = True
                        btn._held    = True
                        self._pressed.add(btn.action)
                        self._held.add(btn.action)

                if self._joystick:
                    jx, jy = self._joystick.cx, self._joystick.cy
                    if math.sqrt((tx - jx) ** 2 + (ty - jy) ** 2) < self._joystick.radius * 1.5:
                        self._joystick._active   = True
                        self._joystick._touch_id = getattr(event, "finger_id", 0)

            elif event.type in (pygame.MOUSEBUTTONUP, pygame.FINGERUP):
                if event.type == pygame.MOUSEBUTTONUP:
                    tx, ty = event.pos
                elif event.type == pygame.FINGERUP:
                    sw = pygame.display.get_surface().get_width()
                    sh = pygame.display.get_surface().get_height()
                    tx, ty = int(event.x * sw), int(event.y * sh)

                self._touch_pos = (tx, ty)

                if self._touch_start:
                    dt = time.time() - self._touch_time
                    dx = tx - self._touch_start[0]
                    dy = ty - self._touch_start[1]
                    dist = math.sqrt(dx * dx + dy * dy)

                    if dist < 20 and dt < 0.3:
                        self._tapped = True
                    elif dist > 60:
                        if abs(dx) > abs(dy):
                            self._swipe = "right" if dx > 0 else "left"
                        else:
                            self._swipe = "down" if dy > 0 else "up"

                for btn in self._vbuttons:
                    if btn._held:
                        btn._released = True
                        btn._held     = False
                        self._released.add(btn.action)
                        self._held.discard(btn.action)

                if self._joystick and self._joystick._active:
                    self._joystick._active  = False
                    self._joystick._axis_x  = 0.0
                    self._joystick._axis_y  = 0.0

            elif event.type in (pygame.MOUSEMOTION, pygame.FINGERMOTION):
                if event.type == pygame.MOUSEMOTION:
                    tx, ty = event.pos
                elif event.type == pygame.FINGERMOTION:
                    sw = pygame.display.get_surface().get_width()
                    sh = pygame.display.get_surface().get_height()
                    tx, ty = int(event.x * sw), int(event.y * sh)

                self._touch_pos = (tx, ty)

                if self._joystick and self._joystick._active:
                    jx, jy = self._joystick.cx, self._joystick.cy
                    dx  = tx - jx
                    dy  = ty - jy
                    dist = math.sqrt(dx * dx + dy * dy)
                    r    = self._joystick.radius
                    if dist > 0:
                        self._joystick._axis_x = clamp(dx / r, -1.0, 1.0)
                        self._joystick._axis_y = clamp(dy / r, -1.0, 1.0)

    def just_pressed(self, action: str) -> bool:
        return action in self._pressed

    def held(self, action: str) -> bool:
        return action in self._held

    def just_released(self, action: str) -> bool:
        return action in self._released

    def touch_pos(self) -> Optional[Tuple[int, int]]:
        return self._touch_pos

    def touch_world(self, camera) -> Optional[Tuple[float, float]]:
        if self._touch_pos is None:
            return None
        return camera.screen_to_world(*self._touch_pos)

    def tapped(self) -> bool:
        return self._tapped

    def swipe(self) -> Optional[str]:
        return self._swipe

    def joystick_axis(self) -> Tuple[float, float]:
        if self._joystick is None:
            return (0.0, 0.0)
        return (self._joystick._axis_x, self._joystick._axis_y)

    def draw_ui(self, screen: pygame.Surface):
        """Draw virtual buttons and joystick onto screen."""
        font = Assets.get_font("default", 18)

        for btn in self._vbuttons:
            cx = btn.x + btn.size // 2
            cy = btn.y + btn.size // 2
            r  = btn.size // 2
            color = Theme.get("button_press") if btn._held else Theme.get("button_bg")
            pygame.draw.circle(screen, color, (cx, cy), r)
            pygame.draw.circle(screen, Theme.get("border"), (cx, cy), r, 2)
            if btn.label:
                surf = font.render(btn.label, True, Theme.get("text"))
                screen.blit(surf, surf.get_rect(center=(cx, cy)))

        if self._joystick:
            jx, jy = self._joystick.cx, self._joystick.cy
            jr     = self._joystick.radius
            pygame.draw.circle(screen, Theme.get("button_bg"), (jx, jy), jr, 3)
            kx = int(jx + self._joystick._axis_x * jr * 0.7)
            ky = int(jy + self._joystick._axis_y * jr * 0.7)
            pygame.draw.circle(screen, Theme.get("button_hover"), (kx, ky), jr // 3)


Input = _InputManager()

# =============================================================================
# ===[ AUDIO ]=================================================================
# =============================================================================

class _AudioManager:
    """BGM + SFX audio manager with pre-allocated channels."""

    NUM_CHANNELS = 16

    def __init__(self):
        pygame.mixer.set_num_channels(self.NUM_CHANNELS)
        self._sfx_channel  = 0
        self._bgm_volume   = 0.8
        self._sfx_volume   = 0.9
        self._current_bgm: Optional[str] = None

    def play_bgm(self, key: str, fade_in: float = 0.0, loops: int = -1):
        sound = Assets.get_sound(key)
        if sound is None:
            return
        self._current_bgm = key
        ch = pygame.mixer.Channel(0)
        ch.set_volume(self._bgm_volume)
        if fade_in > 0:
            ch.play(sound, loops=loops, fade_ms=int(fade_in * 1000))
        else:
            ch.play(sound, loops=loops)

    def stop_bgm(self, fade_out: float = 0.0):
        ch = pygame.mixer.Channel(0)
        if fade_out > 0:
            ch.fadeout(int(fade_out * 1000))
        else:
            ch.stop()
        self._current_bgm = None

    def crossfade(self, from_key: str, to_key: str, time: float = 1.0):
        self.stop_bgm(fade_out=time / 2)
        threading.Timer(time / 2, lambda: self.play_bgm(to_key, fade_in=time / 2)).start()

    def play_sfx(self, key: str, volume: float = 1.0, pitch: float = 1.0):
        sound = Assets.get_sound(key)
        if sound is None:
            return
        self._sfx_channel = (self._sfx_channel % (self.NUM_CHANNELS - 1)) + 1
        ch = pygame.mixer.Channel(self._sfx_channel)
        ch.set_volume(self._sfx_volume * volume)
        ch.play(sound)

    def set_bgm_volume(self, vol: float):
        self._bgm_volume = clamp(vol, 0.0, 1.0)
        pygame.mixer.Channel(0).set_volume(self._bgm_volume)

    def set_sfx_volume(self, vol: float):
        self._sfx_volume = clamp(vol, 0.0, 1.0)


Audio = _AudioManager()

# =============================================================================
# ===[ ECS CORE ]==============================================================
# =============================================================================

_entity_id_counter = 0

def _new_entity_id() -> int:
    global _entity_id_counter
    _entity_id_counter += 1
    return _entity_id_counter


class Entity:
    """
    A game object. Stores components in a type-keyed dict for O(1) lookup.
    Use fluent .add() chains to build entities.
    """

    def __init__(self, tag: str = "entity"):
        self.id:         int  = _new_entity_id()
        self._primary_tag: str = sys.intern(tag)
        self._tags:      Set[str] = {sys.intern(tag)}
        self._components: Dict[type, Any] = {}
        self._world:     Optional["World"] = None
        self._net_id:    Optional[str] = None

    # ---- Component API ----

    def add(self, component) -> "Entity":
        self._components[type(component)] = component
        return self

    def get(self, cls: type) -> Optional[Any]:
        return self._components.get(cls)

    def require(self, cls: type) -> Any:
        c = self._components.get(cls)
        if c is None:
            raise KeyError(f"Entity {self.id} missing component {cls.__name__}")
        return c

    def has(self, cls: type) -> bool:
        return cls in self._components

    def remove(self, cls: type):
        self._components.pop(cls, None)

    # ---- Tag API ----

    def has_tag(self, tag: str) -> bool:
        return sys.intern(tag) in self._tags

    def add_tag(self, tag: str):
        self._tags.add(sys.intern(tag))

    def remove_tag(self, tag: str):
        self._tags.discard(sys.intern(tag))

    # ---- Lifecycle (override in subclass) ----

    def on_spawn(self):    pass
    def on_destroy(self):  pass
    def on_collide(self, other: "Entity", normal: Tuple[float, float]): pass
    def on_damage(self, amount: float): pass

    def __repr__(self):
        return f"Entity(id={self.id}, tag='{self._primary_tag}')"


class System:
    """
    Base system class. Override components list to filter entities.
    Entity cache rebuilds only when world membership changes.
    """
    components: List[type] = []

    def __init__(self):
        self._cache:   List[Entity] = []
        self._dirty:   bool = True

    def _rebuild(self, all_entities: List[Entity]):
        if not self._dirty:
            return
        required = self.components
        if required:
            self._cache = [
                e for e in all_entities
                if all(e.has(c) for c in required)
            ]
        else:
            self._cache = list(all_entities)
        self._dirty = False

    def mark_dirty(self):
        self._dirty = True

    def update(self, dt: float, entities: List[Entity]): pass
    def draw(self, screen: pygame.Surface, entities: List[Entity]): pass


class _SpatialHash:
    """Broadphase collision spatial hashing."""

    def __init__(self, cell_size: int = 64):
        self.cell_size = cell_size
        self._buckets: Dict[Tuple[int,int], List[Entity]] = defaultdict(list)

    def _cells(self, x, y, w, h):
        cs = self.cell_size
        x0 = int(x)          // cs
        y0 = int(y)          // cs
        x1 = int(x + w - 1)  // cs
        y1 = int(y + h - 1)  // cs
        for cx in range(x0, x1 + 1):
            for cy in range(y0, y1 + 1):
                yield (cx, cy)

    def clear(self):
        self._buckets.clear()

    def insert(self, entity: Entity):
        t = entity.get(Transform)
        c = entity.get(Collider)
        if t is None or c is None:
            return
        if c.radius:
            r = c.radius
            for cell in self._cells(t.x - r, t.y - r, r * 2, r * 2):
                self._buckets[cell].append(entity)
        else:
            for cell in self._cells(
                t.x + c.offset_x, t.y + c.offset_y, c.width, c.height
            ):
                self._buckets[cell].append(entity)

    def query(self, entity: Entity) -> List[Entity]:
        t = entity.get(Transform)
        c = entity.get(Collider)
        if t is None or c is None:
            return []
        seen = set()
        result = []
        if c.radius:
            r = c.radius
            cells = self._cells(t.x - r, t.y - r, r * 2, r * 2)
        else:
            cells = self._cells(
                t.x + c.offset_x, t.y + c.offset_y, c.width, c.height
            )
        for cell in cells:
            for e in self._buckets.get(cell, []):
                if e.id != entity.id and e.id not in seen:
                    seen.add(e.id)
                    result.append(e)
        return result

    def draw_debug(self, screen: pygame.Surface, camera: "Camera"):
        color = Theme.get("debug_color")
        cs    = self.cell_size
        vp    = camera.viewport
        x0    = int((camera.x + vp.x) // cs)
        y0    = int((camera.y + vp.y) // cs)
        x1    = int((camera.x + vp.x + vp.width)  // cs) + 1
        y1    = int((camera.y + vp.y + vp.height) // cs) + 1
        for cx in range(x0, x1):
            for cy in range(y0, y1):
                wx = cx * cs - int(camera.x)
                wy = cy * cs - int(camera.y)
                pygame.draw.rect(screen, color,
                    pygame.Rect(wx, wy, cs, cs), 1)


class _Pool:
    """Object pool to reuse entities and avoid GC pressure."""

    def __init__(self):
        self._pools: Dict[type, List[Entity]] = {}

    def register(self, cls: type, size: int = 20):
        self._pools[cls] = [cls() for _ in range(size)]

    def get(self, cls: type) -> Entity:
        pool = self._pools.get(cls, [])
        if pool:
            return pool.pop()
        return cls()

    def release(self, entity: Entity):
        cls = type(entity)
        if cls not in self._pools:
            self._pools[cls] = []
        self._pools[cls].append(entity)


Pool = _Pool()


class World:
    """
    Container for all entities and systems.
    The central hub of the ECS.
    """

    def __init__(self):
        self._entities:  List[Entity] = []
        self._systems:   List[System] = []
        self._groups:    Dict[str, List[Entity]] = defaultdict(list)
        self._by_id:     Dict[int, Entity] = {}
        self._hash:      _SpatialHash = _SpatialHash()
        self._net_map:   Dict[str, Entity] = {}
        self._pending_add: List[Tuple[Entity, Optional[str]]] = []
        self._pending_del: List[Entity] = []

    def add_system(self, system: System):
        self._systems.append(system)

    def add(self, entity: Entity, group: Optional[str] = None):
        self._pending_add.append((entity, group))

    def remove(self, entity: Entity):
        self._pending_del.append(entity)

    def remove_by_net_id(self, net_id: str):
        e = self._net_map.get(net_id)
        if e:
            self.remove(e)

    def _flush(self):
        changed = False

        for entity, group in self._pending_add:
            entity._world = self
            self._entities.append(entity)
            self._by_id[entity.id] = entity
            if group:
                self._groups[sys.intern(group)].append(entity)
            if entity._net_id:
                self._net_map[entity._net_id] = entity
            entity.on_spawn()
            changed = True

        self._pending_add.clear()

        for entity in self._pending_del:
            if entity in self._entities:
                self._entities.remove(entity)
            self._by_id.pop(entity.id, None)
            if entity._net_id:
                self._net_map.pop(entity._net_id, None)
            for g in self._groups.values():
                if entity in g:
                    g.remove(entity)
            entity._world = None
            entity.on_destroy()
            changed = True

        self._pending_del.clear()

        if changed:
            for sys_ in self._systems:
                sys_.mark_dirty()

    def update(self, dt: float):
        self._flush()
        self._hash.clear()
        for e in self._entities:
            self._hash.insert(e)

        for sys_ in self._systems:
            sys_._rebuild(self._entities)
            sys_.update(dt, sys_._cache)

    def draw(self, screen: pygame.Surface):
        for sys_ in self._systems:
            sys_._rebuild(self._entities)
            sys_.draw(screen, sys_._cache)

    def get_by_id(self, eid: int) -> Optional[Entity]:
        return self._by_id.get(eid)

    def get_by_tag(self, tag: str) -> List[Entity]:
        t = sys.intern(tag)
        return [e for e in self._entities if t in e._tags]

    def get_by_component(self, cls: type) -> List[Entity]:
        return [e for e in self._entities if e.has(cls)]

    def group(self, name: str) -> List[Entity]:
        return self._groups.get(sys.intern(name), [])

    def collide_groups(
        self, group_a: str, group_b: str,
        callback: Callable[[Entity, Entity, Tuple], None]
    ):
        for a in self.group(group_a):
            for b in self.group(group_b):
                normal = _check_collision(a, b)
                if normal is not None:
                    callback(a, b, normal)

    def entity_count(self) -> int:
        return len(self._entities)

# =============================================================================
# ===[ COMPONENTS ]============================================================
# =============================================================================

class Transform:
    __slots__ = ("x", "y", "rotation", "scale_x", "scale_y", "_dirty")

    def __init__(self, x=0.0, y=0.0, rotation=0.0, scale_x=1.0, scale_y=1.0):
        self.x        = float(x)
        self.y        = float(y)
        self.rotation = float(rotation)
        self.scale_x  = float(scale_x)
        self.scale_y  = float(scale_y)
        self._dirty   = True

    @property
    def pos(self):
        return (self.x, self.y)

    def move(self, dx: float, dy: float):
        self.x += dx
        self.y += dy
        self._dirty = True

    def set_pos(self, x: float, y: float):
        self.x = x
        self.y = y
        self._dirty = True


class Velocity:
    __slots__ = ("vx", "vy", "max_speed", "_impulse_x", "_impulse_y")

    def __init__(self, vx=0.0, vy=0.0, max_speed=800.0):
        self.vx        = float(vx)
        self.vy        = float(vy)
        self.max_speed = float(max_speed)
        self._impulse_x = 0.0
        self._impulse_y = 0.0

    def apply_impulse(self, ix: float, iy: float):
        self._impulse_x += ix
        self._impulse_y += iy


class Sprite:
    __slots__ = ("key", "offset_x", "offset_y", "flip_x", "flip_y", "layer", "visible", "surface")

    def __init__(self, key: str = "", offset_x=0, offset_y=0,
                 flip_x=False, flip_y=False, layer=0):
        self.key      = key
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.flip_x   = flip_x
        self.flip_y   = flip_y
        self.layer    = layer
        self.visible  = True
        self.surface: Optional[pygame.Surface] = None

    def get_surface(self) -> Optional[pygame.Surface]:
        if self.surface:
            return self.surface
        return Assets.get(self.key)


class Collider:
    __slots__ = ("width", "height", "radius", "offset_x", "offset_y", "is_trigger")

    def __init__(self, width=0, height=0, radius=0,
                 offset_x=0, offset_y=0, is_trigger=False):
        self.width     = width
        self.height    = height
        self.radius    = radius
        self.offset_x  = offset_x
        self.offset_y  = offset_y
        self.is_trigger = is_trigger

    def get_rect(self, tx: float, ty: float) -> pygame.Rect:
        return pygame.Rect(
            int(tx + self.offset_x),
            int(ty + self.offset_y),
            self.width,
            self.height,
        )


class _Clip:
    __slots__ = ("row", "frames", "fps", "loop")

    def __init__(self, row, frames, fps, loop):
        self.row    = row
        self.frames = frames
        self.fps    = fps
        self.loop   = loop


class Animator:
    __slots__ = (
        "sheet_key", "_clips", "_current", "_frame",
        "_timer", "_playing", "on_finish",
    )

    def __init__(self, sheet_key: str = ""):
        self.sheet_key  = sheet_key
        self._clips:    Dict[str, _Clip] = {}
        self._current:  Optional[str]    = None
        self._frame:    int              = 0
        self._timer:    float            = 0.0
        self._playing:  bool             = False
        self.on_finish: Optional[Callable] = None

    def add_clip(self, name: str, row: int, frames: int,
                 fps: float = 12.0, loop: bool = True):
        self._clips[name] = _Clip(row, frames, fps, loop)

    def play(self, name: str):
        if self._current == name and self._playing:
            return
        self._current = name
        self._frame   = 0
        self._timer   = 0.0
        self._playing = True

    def stop(self):
        self._playing = False

    @property
    def current_clip(self) -> Optional[str]:
        return self._current

    def advance(self, dt: float) -> Optional[pygame.Surface]:
        if not self._playing or self._current is None:
            return None
        clip = self._clips.get(self._current)
        if clip is None:
            return None

        self._timer += dt
        spf = 1.0 / clip.fps
        while self._timer >= spf:
            self._timer -= spf
            self._frame += 1
            if self._frame >= clip.frames:
                if clip.loop:
                    self._frame = 0
                else:
                    self._frame = clip.frames - 1
                    self._playing = False
                    if self.on_finish:
                        self.on_finish()

        sheet = Assets.get_sheet(self.sheet_key)
        if sheet is None:
            return None

        tw = sheet["tile_w"]
        th = sheet["tile_h"]
        surface: pygame.Surface = sheet["surface"]
        sub = surface.subsurface(
            pygame.Rect(self._frame * tw, clip.row * th, tw, th)
        )
        return sub


class Health:
    __slots__ = ("hp", "max_hp", "invincible_duration", "_invincible_timer")

    def __init__(self, hp=100, max_hp=None, invincible_duration=0.5):
        self.hp                  = float(hp)
        self.max_hp              = float(max_hp or hp)
        self.invincible_duration = float(invincible_duration)
        self._invincible_timer   = 0.0

    def take_damage(self, amount: float):
        if self._invincible_timer > 0:
            return
        self.hp = max(0.0, self.hp - amount)
        self._invincible_timer = self.invincible_duration

    def heal(self, amount: float):
        self.hp = min(self.max_hp, self.hp + amount)

    def is_dead(self) -> bool:
        return self.hp <= 0.0

    def is_invincible(self) -> bool:
        return self._invincible_timer > 0.0

    def update(self, dt: float):
        if self._invincible_timer > 0:
            self._invincible_timer -= dt


class StateMachine:
    __slots__ = ("_states", "_current", "_data")

    def __init__(self, initial: str = ""):
        self._states:  Dict[str, dict] = {}
        self._current: Optional[str]   = None
        self._data:    dict             = {}
        if initial:
            self._current = initial

    def add_state(
        self, name: str,
        on_enter:  Optional[Callable] = None,
        on_exit:   Optional[Callable] = None,
        on_update: Optional[Callable] = None,
    ):
        self._states[name] = {
            "enter":  on_enter,
            "exit":   on_exit,
            "update": on_update,
        }

    def transition(self, name: str):
        if name == self._current:
            return
        cur = self._states.get(self._current, {})
        if cur.get("exit"):
            cur["exit"]()
        self._current = name
        nxt = self._states.get(name, {})
        if nxt.get("enter"):
            nxt["enter"]()

    def update(self, dt: float):
        st = self._states.get(self._current, {})
        if st.get("update"):
            st["update"](dt)

    @property
    def current(self) -> Optional[str]:
        return self._current


class Timer:
    __slots__ = ("duration", "repeat", "callback", "_elapsed", "_running")

    def __init__(self, duration: float = 1.0,
                 repeat: bool = False,
                 callback: Optional[Callable] = None):
        self.duration = duration
        self.repeat   = repeat
        self.callback = callback
        self._elapsed = 0.0
        self._running = False

    def start(self):
        self._elapsed = 0.0
        self._running = True

    def stop(self):
        self._running = False

    def reset(self):
        self._elapsed = 0.0

    def is_running(self) -> bool:
        return self._running

    @property
    def elapsed(self) -> float:
        return self._elapsed

    def update(self, dt: float):
        if not self._running:
            return
        self._elapsed += dt
        if self._elapsed >= self.duration:
            if self.callback:
                self.callback()
            if self.repeat:
                self._elapsed -= self.duration
            else:
                self._running = False


class Stats:
    __slots__ = ("hp", "mp", "atk", "defense")

    def __init__(self, hp=100, mp=50, atk=10, defense=5):
        self.hp      = hp
        self.mp      = mp
        self.atk     = atk
        self.defense = defense


class Hitbox:
    __slots__ = ("rects",)

    def __init__(self, rects: List[pygame.Rect]):
        self.rects = rects


class Inventory:
    __slots__ = ("slots", "_items")

    def __init__(self, slots: int = 20):
        self.slots  = slots
        self._items: List[Optional[dict]] = [None] * slots

    def add_item(self, item: dict) -> bool:
        for i, slot in enumerate(self._items):
            if slot is None:
                self._items[i] = item
                return True
        return False

    def remove_item(self, item_id: str) -> bool:
        for i, slot in enumerate(self._items):
            if slot and slot.get("id") == item_id:
                self._items[i] = None
                return True
        return False

    def has_item(self, item_id: str) -> bool:
        return any(s and s.get("id") == item_id for s in self._items)

    def get_item(self, item_id: str) -> Optional[dict]:
        for s in self._items:
            if s and s.get("id") == item_id:
                return s
        return None

    @property
    def items(self) -> List[dict]:
        return [s for s in self._items if s is not None]

    def is_full(self) -> bool:
        return all(s is not None for s in self._items)


class Shadow:
    __slots__ = ("width", "height", "color", "alpha", "offset_y")

    def __init__(self, width=28, height=8, color=(0, 0, 0),
                 alpha=80, offset_y=2):
        self.width   = width
        self.height  = height
        self.color   = color
        self.alpha   = alpha
        self.offset_y = offset_y


class Light:
    __slots__ = ("radius", "color", "intensity")

    def __init__(self, radius=120, color=(255, 200, 100), intensity=0.8):
        self.radius    = radius
        self.color     = color
        self.intensity = clamp(intensity, 0.0, 1.0)


class Tag:
    __slots__ = ("_tags",)

    def __init__(self, *tags: str):
        self._tags: Set[str] = {sys.intern(t) for t in tags}

    @property
    def tags(self) -> Set[str]:
        return self._tags

    def has(self, tag: str) -> bool:
        return sys.intern(tag) in self._tags


# ---- Networking Component (no-op in offline mode) ----

class SyncMode:
    INTERPOLATE = "interpolate"
    SNAP        = "snap"
    RELIABLE    = "reliable"
    UNRELIABLE  = "unreliable"


class NetSync:
    """
    Declares which fields sync and how.
    In offline mode this component is present but ignored by all systems.
    """
    __slots__ = ("owner", "sync", "rate", "_buffer", "_seq")

    def __init__(
        self,
        owner:  str = "",
        sync:   Optional[Dict[str, str]] = None,
        rate:   int = 20,
    ):
        self.owner  = owner
        self.sync   = sync or {}
        self.rate   = rate
        self._buffer: deque = deque(maxlen=6)
        self._seq:    int   = 0

# =============================================================================
# ===[ PHYSICS ]===============================================================
# =============================================================================

class _PhysicsConfig:
    gravity   = 980.0
    friction  = 0.85
    air_drag  = 0.98
    max_fall  = 1200.0


Physics = _PhysicsConfig()


class PhysicsSystem(System):
    components = [Transform, Velocity]

    def __init__(self, tilemap: Optional["Tilemap"] = None):
        super().__init__()
        self._tilemap = tilemap

    def set_tilemap(self, tilemap: "Tilemap"):
        self._tilemap = tilemap

    def update(self, dt: float, entities: List[Entity]):
        g  = Physics.gravity
        mf = Physics.max_fall

        for e in entities:
            t  = e.get(Transform)
            v  = e.get(Velocity)

            # Apply impulse
            v.vx += v._impulse_x
            v.vy += v._impulse_y
            v._impulse_x = 0.0
            v._impulse_y = 0.0

            # Gravity
            v.vy += g * dt
            if v.vy > mf:
                v.vy = mf

            # Move X
            t.x += v.vx * dt

            # Tilemap X collision
            if self._tilemap:
                self._resolve_tilemap_x(t, v, e.get(Collider))

            # Move Y
            t.y += v.vy * dt

            # Tilemap Y collision
            grounded = False
            if self._tilemap:
                grounded = self._resolve_tilemap_y(t, v, e.get(Collider))

            # Friction
            if grounded:
                v.vx *= Physics.friction
            else:
                v.vx *= Physics.air_drag

            # Cap speed
            speed = math.sqrt(v.vx * v.vx + v.vy * v.vy)
            if speed > v.max_speed:
                factor = v.max_speed / speed
                v.vx  *= factor
                v.vy  *= factor

            t._dirty = True

            # Update health invincibility
            hp = e.get(Health)
            if hp:
                hp.update(dt)

            # Update timers
            tmr = e.get(Timer)
            if tmr:
                tmr.update(dt)

            # Update state machine
            fsm = e.get(StateMachine)
            if fsm:
                fsm.update(dt)

    def _resolve_tilemap_x(self, t: Transform, v: Velocity, col: Optional[Collider]):
        if col is None or self._tilemap is None:
            return
        r = col.get_rect(t.x, t.y)
        for tx, ty in self._tilemap.get_solid_tiles_near(r):
            tr = pygame.Rect(tx * self._tilemap.tile_size,
                             ty * self._tilemap.tile_size,
                             self._tilemap.tile_size,
                             self._tilemap.tile_size)
            if r.colliderect(tr):
                if v.vx > 0:
                    r.right = tr.left
                elif v.vx < 0:
                    r.left  = tr.right
                v.vx = 0
                t.x  = r.x - col.offset_x

    def _resolve_tilemap_y(self, t: Transform, v: Velocity, col: Optional[Collider]) -> bool:
        if col is None or self._tilemap is None:
            return False
        r       = col.get_rect(t.x, t.y)
        grounded = False
        for tx, ty in self._tilemap.get_solid_tiles_near(r):
            tr = pygame.Rect(tx * self._tilemap.tile_size,
                             ty * self._tilemap.tile_size,
                             self._tilemap.tile_size,
                             self._tilemap.tile_size)
            if r.colliderect(tr):
                if v.vy > 0:
                    r.bottom = tr.top
                    grounded  = True
                elif v.vy < 0:
                    r.top   = tr.bottom
                v.vy = 0
                t.y  = r.y - col.offset_y
        return grounded

# =============================================================================
# ===[ COLLISION ]=============================================================
# =============================================================================

def _check_collision(
    a: Entity, b: Entity
) -> Optional[Tuple[float, float]]:
    """Returns collision normal (nx, ny) or None."""
    ta = a.get(Transform)
    tb = b.get(Transform)
    ca = a.get(Collider)
    cb = b.get(Collider)
    if ta is None or tb is None or ca is None or cb is None:
        return None

    # Circle vs Circle
    if ca.radius and cb.radius:
        ax = ta.x + ca.offset_x
        ay = ta.y + ca.offset_y
        bx = tb.x + cb.offset_x
        by = tb.y + cb.offset_y
        dx = ax - bx
        dy = ay - by
        dist = math.sqrt(dx * dx + dy * dy)
        if dist < ca.radius + cb.radius and dist > 0:
            return (dx / dist, dy / dist)
        return None

    # Circle vs AABB
    if ca.radius and not cb.radius:
        return _circle_aabb(
            ta.x + ca.offset_x, ta.y + ca.offset_y, ca.radius,
            cb.get_rect(tb.x, tb.y)
        )
    if cb.radius and not ca.radius:
        n = _circle_aabb(
            tb.x + cb.offset_x, tb.y + cb.offset_y, cb.radius,
            ca.get_rect(ta.x, ta.y)
        )
        if n:
            return (-n[0], -n[1])
        return None

    # AABB vs AABB
    ra = ca.get_rect(ta.x, ta.y)
    rb = cb.get_rect(tb.x, tb.y)
    if ra.colliderect(rb):
        cx = (ra.centerx - rb.centerx)
        cy = (ra.centery - rb.centery)
        ox = (ra.width  + rb.width)  / 2 - abs(cx)
        oy = (ra.height + rb.height) / 2 - abs(cy)
        if ox < oy:
            return (1.0 if cx > 0 else -1.0, 0.0)
        else:
            return (0.0, 1.0 if cy > 0 else -1.0)
    return None


def _circle_aabb(cx, cy, cr, rect: pygame.Rect) -> Optional[Tuple[float, float]]:
    nx = clamp(cx, rect.left, rect.right)
    ny = clamp(cy, rect.top,  rect.bottom)
    dx = cx - nx
    dy = cy - ny
    dist2 = dx * dx + dy * dy
    if dist2 < cr * cr:
        dist = math.sqrt(dist2) if dist2 > 0 else 0.001
        return (dx / dist, dy / dist)
    return None


class CollisionSystem(System):
    components = [Transform, Collider]

    def __init__(self, world: Optional[World] = None):
        super().__init__()
        self._world = world

    def set_world(self, world: World):
        self._world = world

    def update(self, dt: float, entities: List[Entity]):
        if self._world is None:
            return
        h = self._world._hash
        for a in entities:
            candidates = h.query(a)
            for b in candidates:
                if not b.has(Collider):
                    continue
                normal = _check_collision(a, b)
                if normal is not None:
                    a.on_collide(b, normal)
                    b.on_collide(a, (-normal[0], -normal[1]))

# =============================================================================
# ===[ SYSTEMS ]===============================================================
# =============================================================================

class AnimationSystem(System):
    components = [Animator, Sprite]

    def update(self, dt: float, entities: List[Entity]):
        for e in entities:
            anim   = e.get(Animator)
            sprite = e.get(Sprite)
            frame  = anim.advance(dt)
            if frame is not None:
                spr = e.get(Sprite)
                if spr:
                    spr.surface = frame


class RenderSystem(System):
    components = [Transform, Sprite]

    def __init__(self, camera: Optional["Camera"] = None):
        super().__init__()
        self._camera = camera
        self._buckets: Dict[int, List[Entity]] = defaultdict(list)

    def set_camera(self, camera: "Camera"):
        self._camera = camera

    def draw(self, screen: pygame.Surface, entities: List[Entity]):
        self._buckets.clear()
        cam = self._camera

        for e in entities:
            sprite = e.get(Sprite)
            if sprite and sprite.visible:
                self._buckets[sprite.layer].append(e)

        for layer in sorted(self._buckets.keys()):
            for e in self._buckets[layer]:
                t      = e.get(Transform)
                sprite = e.get(Sprite)
                surf   = sprite.get_surface()
                if surf is None:
                    continue

                sx = t.x + sprite.offset_x
                sy = t.y + sprite.offset_y

                if cam:
                    # Frustum cull
                    vp = cam.viewport
                    sw = surf.get_width()
                    sh = surf.get_height()
                    sx_screen = sx - cam.x
                    sy_screen = sy - cam.y
                    if (sx_screen + sw < 0 or sx_screen > vp.width or
                            sy_screen + sh < 0 or sy_screen > vp.height):
                        continue
                    sx = sx_screen
                    sy = sy_screen

                # Shadow
                shadow = e.get(Shadow)
                if shadow:
                    sw2 = shadow.width
                    sh2 = shadow.height
                    sx2 = int(sx + surf.get_width() / 2 - sw2 / 2)
                    sy2 = int(sy + surf.get_height() - sh2 / 2 + shadow.offset_y)
                    s   = pygame.Surface((sw2, sh2), pygame.SRCALPHA)
                    pygame.draw.ellipse(
                        s,
                        (*shadow.color, shadow.alpha),
                        pygame.Rect(0, 0, sw2, sh2)
                    )
                    screen.blit(s, (sx2, sy2))

                # Flip
                if sprite.flip_x or sprite.flip_y:
                    surf = pygame.transform.flip(surf, sprite.flip_x, sprite.flip_y)

                screen.blit(surf, (int(sx), int(sy)))

                # Debug hitbox
                if Debug.show_hitboxes:
                    col = e.get(Collider)
                    if col:
                        ox = int((t.x + col.offset_x) - (cam.x if cam else 0))
                        oy = int((t.y + col.offset_y) - (cam.y if cam else 0))
                        if col.radius:
                            pygame.draw.circle(
                                screen, Theme.get("debug_color"),
                                (ox, oy), col.radius, 1
                            )
                        else:
                            pygame.draw.rect(
                                screen, Theme.get("debug_color"),
                                pygame.Rect(ox, oy, col.width, col.height), 1
                            )


class LightSystem(System):
    components = [Transform, Light]

    def __init__(self, ambient: int = 180):
        super().__init__()
        self._ambient = ambient
        self._overlay: Optional[pygame.Surface] = None

    def draw(self, screen: pygame.Surface, entities: List[Entity]):
        if not entities:
            return
        w, h = screen.get_size()
        if self._overlay is None or self._overlay.get_size() != (w, h):
            self._overlay = pygame.Surface((w, h), pygame.SRCALPHA)

        self._overlay.fill((0, 0, 0, self._ambient))

        for e in entities:
            t = e.get(Transform)
            l = e.get(Light)
            r     = l.radius
            color = l.color
            alpha = int(l.intensity * 255)
            cx    = int(t.x)
            cy    = int(t.y)

            light_surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            for i in range(r, 0, -1):
                a = int(alpha * (1.0 - i / r))
                pygame.draw.circle(
                    light_surf, (*color, a), (r, r), i
                )
            self._overlay.blit(
                light_surf, (cx - r, cy - r),
                special_flags=pygame.BLEND_RGBA_SUB
            )

        screen.blit(self._overlay, (0, 0))

# =============================================================================
# ===[ TILEMAP ]===============================================================
# =============================================================================

CHUNK_SIZE = 16


class Tilemap:
    """
    Loads from a Tiled-compatible JSON format.
    Chunk-based rendering — only visible chunks drawn per frame.
    Precomputed bitmask for O(1) solid tile lookup.
    """

    def __init__(self, key: str):
        data = Assets.get_map(key)
        if data is None:
            print(f"[Tilemap] Map '{key}' not found in Assets.")
            data = {"tilewidth": 32, "tileheight": 32, "width": 1, "height": 1, "layers": []}

        self.tile_size: int = data.get("tilewidth", 32)
        self.width:     int = data.get("width",  1)
        self.height:    int = data.get("height", 1)
        self._layers:   Dict[str, List[int]] = {}
        self._bitmask:  List[int] = [0] * (self.width * self.height)
        self._chunks:   Dict[str, Dict[Tuple[int,int], pygame.Surface]] = {}
        self._tilesets: List[dict] = data.get("tilesets", [])

        for layer in data.get("layers", []):
            if layer.get("type") == "tilelayer":
                name = layer.get("name", "layer")
                self._layers[name] = layer.get("data", [])
                if name == "collision":
                    for i, tile in enumerate(self._layers[name]):
                        self._bitmask[i] = 1 if tile > 0 else 0

        self._build_chunks()

    def _build_chunks(self):
        for layer_name, data in self._layers.items():
            self._chunks[layer_name] = {}
            cs    = CHUNK_SIZE
            ts    = self.tile_size
            cw    = (self.width  + cs - 1) // cs
            ch    = (self.height + cs - 1) // cs

            for ccy in range(ch):
                for ccx in range(cw):
                    surf = pygame.Surface((cs * ts, cs * ts), pygame.SRCALPHA)
                    surf.fill((0, 0, 0, 0))
                    has_tile = False
                    for ty in range(cs):
                        for tx in range(cs):
                            wx = ccx * cs + tx
                            wy = ccy * cs + ty
                            if wx >= self.width or wy >= self.height:
                                continue
                            idx  = wy * self.width + wx
                            tile = data[idx] if idx < len(data) else 0
                            if tile <= 0:
                                continue
                            has_tile = True
                            tile_surf = self._get_tile_surface(tile)
                            if tile_surf:
                                surf.blit(tile_surf, (tx * ts, ty * ts))
                    if has_tile:
                        self._chunks[layer_name][(ccx, ccy)] = surf

    def _get_tile_surface(self, tile_id: int) -> Optional[pygame.Surface]:
        if not self._tilesets:
            return None
        ts_data = self._tilesets[0]
        sheet_key = ts_data.get("name", "")
        sheet     = Assets.get_sheet(sheet_key)
        if sheet is None:
            img_key = ts_data.get("image_key", sheet_key)
            img     = Assets.get(img_key)
            if img is None:
                return None
            tw = self.tile_size
            th = self.tile_size
        else:
            img = sheet["surface"]
            tw  = sheet["tile_w"]
            th  = sheet["tile_h"]

        gid     = tile_id - ts_data.get("firstgid", 1)
        cols    = img.get_width() // tw
        if cols == 0:
            return None
        tx      = (gid % cols) * tw
        ty_off  = (gid // cols) * th
        return img.subsurface(pygame.Rect(tx, ty_off, tw, th))

    def draw(self, screen: pygame.Surface, camera: "Camera"):
        vp = camera.viewport
        cs = CHUNK_SIZE
        ts = self.tile_size

        # Which chunks are visible?
        cx0 = max(0, int(camera.x) // (cs * ts))
        cy0 = max(0, int(camera.y) // (cs * ts))
        cx1 = min(
            (self.width  + cs - 1) // cs,
            int(camera.x + vp.width)  // (cs * ts) + 1
        )
        cy1 = min(
            (self.height + cs - 1) // cs,
            int(camera.y + vp.height) // (cs * ts) + 1
        )

        for layer_name in ("background", "default", "foreground"):
            chunks = self._chunks.get(layer_name, {})
            for ccy in range(cy0, cy1):
                for ccx in range(cx0, cx1):
                    chunk = chunks.get((ccx, ccy))
                    if chunk:
                        sx = ccx * cs * ts - int(camera.x)
                        sy = ccy * cs * ts - int(camera.y)
                        screen.blit(chunk, (sx, sy))

    def get_layer(self, name: str) -> List[int]:
        return self._layers.get(name, [])

    def is_solid(self, tx: int, ty: int) -> bool:
        if tx < 0 or ty < 0 or tx >= self.width or ty >= self.height:
            return True
        return self._bitmask[ty * self.width + tx] == 1

    def world_to_tile(self, wx: float, wy: float) -> Tuple[int, int]:
        return (int(wx // self.tile_size), int(wy // self.tile_size))

    def tile_to_world(self, tx: int, ty: int) -> Tuple[float, float]:
        return (float(tx * self.tile_size), float(ty * self.tile_size))

    def get_solid_tiles_near(self, rect: pygame.Rect) -> List[Tuple[int, int]]:
        ts  = self.tile_size
        x0  = max(0, rect.left   // ts - 1)
        y0  = max(0, rect.top    // ts - 1)
        x1  = min(self.width  - 1, rect.right  // ts + 1)
        y1  = min(self.height - 1, rect.bottom // ts + 1)
        result = []
        for ty in range(y0, y1 + 1):
            for tx in range(x0, x1 + 1):
                if self._bitmask[ty * self.width + tx]:
                    result.append((tx, ty))
        return result

# =============================================================================
# ===[ CAMERA ]================================================================
# =============================================================================

class Camera:
    """Viewport camera with smooth follow, shake, zoom, parallax."""

    def __init__(self, viewport: Optional[pygame.Rect] = None):
        surf           = pygame.display.get_surface()
        self.viewport  = viewport or (surf.get_rect() if surf else pygame.Rect(0,0,720,1461))
        self.x         = 0.0
        self.y         = 0.0
        self._target:  Optional[Entity]         = None
        self._deadzone: Optional[pygame.Rect]   = None
        self.follow_speed: float                = 6.0
        self._shake_intensity: float            = 0.0
        self._shake_duration:  float            = 0.0
        self._shake_timer:     float            = 0.0
        self._shake_ox:        float            = 0.0
        self._shake_oy:        float            = 0.0
        self._flash_color:     Optional[Tuple]  = None
        self._flash_duration:  float            = 0.0
        self._flash_timer:     float            = 0.0
        self._zoom:            float            = 1.0
        self._target_zoom:     float            = 1.0
        self._zoom_smooth:     bool             = False
        self._pan_target:      Optional[Tuple]  = None
        self._pan_duration:    float            = 0.0
        self._pan_timer:       float            = 0.0
        self._pan_start:       Tuple            = (0.0, 0.0)
        self._clamp_rect:      Optional[pygame.Rect] = None
        self._parallax:        List[Tuple]      = []
        self._flash_surf: Optional[pygame.Surface] = None

    def follow(self, entity: Entity, deadzone: Optional[pygame.Rect] = None):
        self._target   = entity
        self._deadzone = deadzone

    def shake(self, intensity: float = 8.0, duration: float = 0.4):
        self._shake_intensity = intensity
        self._shake_duration  = duration
        self._shake_timer     = 0.0

    def flash(self, color: Tuple = (255, 255, 255), duration: float = 0.2):
        self._flash_color    = color
        self._flash_duration = duration
        self._flash_timer    = 0.0

    def zoom(self, factor: float, smooth: bool = True):
        self._target_zoom = factor
        self._zoom_smooth = smooth
        if not smooth:
            self._zoom = factor

    def pan_to(self, x: float, y: float, duration: float = 1.0):
        self._pan_target   = (x, y)
        self._pan_duration = duration
        self._pan_timer    = 0.0
        self._pan_start    = (self.x, self.y)
        self._target       = None

    def clamp(self, world_rect: pygame.Rect):
        self._clamp_rect = world_rect

    def add_parallax(self, surface: pygame.Surface, speed: float = 0.3):
        self._parallax.append((surface, speed))

    def update(self, dt: float):
        # Follow target
        if self._target:
            t = self._target.get(Transform)
            if t:
                cx = t.x - self.viewport.width  / 2
                cy = t.y - self.viewport.height / 2
                if self._deadzone:
                    dx = t.x - self.x - self.viewport.width  / 2
                    dy = t.y - self.y - self.viewport.height / 2
                    if abs(dx) > self._deadzone.width  / 2:
                        cx = t.x - self.viewport.width  / 2
                    else:
                        cx = self.x
                    if abs(dy) > self._deadzone.height / 2:
                        cy = t.y - self.viewport.height / 2
                    else:
                        cy = self.y

                spd = self.follow_speed
                self.x = lerp(self.x, cx, clamp(spd * dt, 0.0, 1.0))
                self.y = lerp(self.y, cy, clamp(spd * dt, 0.0, 1.0))

        # Pan
        if self._pan_target:
            self._pan_timer += dt
            t_val = clamp(self._pan_timer / self._pan_duration, 0.0, 1.0)
            self.x = lerp(self._pan_start[0], self._pan_target[0], t_val)
            self.y = lerp(self._pan_start[1], self._pan_target[1], t_val)
            if t_val >= 1.0:
                self._pan_target = None

        # Clamp to world
        if self._clamp_rect:
            vp = self.viewport
            self.x = clamp(self.x, self._clamp_rect.left,
                           self._clamp_rect.right  - vp.width)
            self.y = clamp(self.y, self._clamp_rect.top,
                           self._clamp_rect.bottom - vp.height)

        # Shake
        if self._shake_timer < self._shake_duration:
            self._shake_timer += dt
            p = 1.0 - (self._shake_timer / self._shake_duration)
            import random
            self._shake_ox = (random.random() * 2 - 1) * self._shake_intensity * p
            self._shake_oy = (random.random() * 2 - 1) * self._shake_intensity * p
        else:
            self._shake_ox = 0.0
            self._shake_oy = 0.0

        # Zoom lerp
        if self._zoom_smooth and abs(self._zoom - self._target_zoom) > 0.001:
            self._zoom = lerp(self._zoom, self._target_zoom, clamp(5.0 * dt, 0, 1))
        else:
            self._zoom = self._target_zoom

        # Flash timer
        if self._flash_timer < self._flash_duration:
            self._flash_timer += dt

    def draw_effects(self, screen: pygame.Surface):
        """Draw parallax layers and flash effects."""
        # Parallax
        for surf, speed in self._parallax:
            px = -(self.x * speed) % surf.get_width()
            py = -(self.y * speed) % surf.get_height()
            screen.blit(surf, (px - surf.get_width(), py))
            screen.blit(surf, (px, py))

        # Flash
        if self._flash_timer < self._flash_duration and self._flash_color:
            alpha = int(200 * (1.0 - self._flash_timer / self._flash_duration))
            vp    = self.viewport
            if self._flash_surf is None or self._flash_surf.get_size() != (vp.width, vp.height):
                self._flash_surf = pygame.Surface((vp.width, vp.height), pygame.SRCALPHA)
            self._flash_surf.fill((*self._flash_color, alpha))
            screen.blit(self._flash_surf, (0, 0))

    def apply(self, rect: pygame.Rect) -> pygame.Rect:
        return pygame.Rect(
            rect.x - int(self.x + self._shake_ox),
            rect.y - int(self.y + self._shake_oy),
            rect.w, rect.h
        )

    def apply_pos(self, x: float, y: float) -> Tuple[float, float]:
        return (x - self.x - self._shake_ox, y - self.y - self._shake_oy)

    def screen_to_world(self, sx: float, sy: float) -> Tuple[float, float]:
        return (sx + self.x, sy + self.y)

    def world_to_screen(self, wx: float, wy: float) -> Tuple[float, float]:
        return (wx - self.x, wy - self.y)

# =============================================================================
# ===[ PATHFINDING ]===========================================================
# =============================================================================

class Pathfinder:
    """Grid-based A* with path caching and update budget."""

    def __init__(self, tilemap: Optional[Tilemap] = None):
        self._tilemap  = tilemap
        self.diagonal  = True
        self.budget_ms = 2.0
        self._cache:   Dict[Tuple, List[Tuple[int,int]]] = {}

    def set_tilemap(self, tilemap: Tilemap):
        self._tilemap  = tilemap
        self._cache.clear()

    def find(
        self, start: Tuple[int, int], goal: Tuple[int, int]
    ) -> List[Tuple[int, int]]:
        key = (start, goal)
        if key in self._cache:
            return self._cache[key]

        result = self._astar(start, goal)
        self._cache[key] = result
        return result

    def invalidate(self):
        self._cache.clear()

    def _astar(
        self, start: Tuple[int,int], goal: Tuple[int,int]
    ) -> List[Tuple[int,int]]:
        if self._tilemap is None:
            return []

        t0 = time.perf_counter()

        open_set: List[Tuple[float, Tuple[int,int]]] = []
        import heapq
        heapq.heappush(open_set, (0.0, start))

        came_from: Dict[Tuple[int,int], Optional[Tuple[int,int]]] = {start: None}
        g_score:   Dict[Tuple[int,int], float] = defaultdict(lambda: float("inf"))
        g_score[start] = 0.0

        dirs = [(1,0),(-1,0),(0,1),(0,-1)]
        if self.diagonal:
            dirs += [(1,1),(-1,1),(1,-1),(-1,-1)]

        while open_set:
            if (time.perf_counter() - t0) * 1000 > self.budget_ms:
                break

            _, current = heapq.heappop(open_set)
            if current == goal:
                return self._reconstruct(came_from, goal)

            for dx, dy in dirs:
                nb = (current[0] + dx, current[1] + dy)
                if self._tilemap.is_solid(*nb):
                    continue
                step_cost = 1.414 if dx != 0 and dy != 0 else 1.0
                ng = g_score[current] + step_cost
                if ng < g_score[nb]:
                    g_score[nb] = ng
                    came_from[nb] = current
                    h = abs(nb[0] - goal[0]) + abs(nb[1] - goal[1])
                    heapq.heappush(open_set, (ng + h, nb))

        return []

    def _reconstruct(
        self, came_from: dict, node: Tuple[int,int]
    ) -> List[Tuple[int,int]]:
        path = []
        while node is not None:
            path.append(node)
            node = came_from[node]
        path.reverse()
        return path

# =============================================================================
# ===[ NETWORKING ]============================================================
# =============================================================================
# Networking is fully optional and isolated.
# Core ECS/physics/input never import from this section.
# In offline mode all classes are lightweight no-op stubs.
# =============================================================================

class NetMode:
    SERVER = "server"
    CLIENT = "client"
    PEER   = "peer"


class _Peer:
    __slots__ = ("id", "name", "ping", "packet_loss", "jitter",
                 "ready", "is_spectator", "_sock", "_addr")

    def __init__(self, peer_id: str, sock=None, addr=None):
        self.id          = peer_id
        self.name        = peer_id[:8]
        self.ping        = 0
        self.packet_loss = 0.0
        self.jitter      = 0
        self.ready       = False
        self.is_spectator = False
        self._sock       = sock
        self._addr       = addr


class _PacketSerializer:
    """Transport-agnostic JSON packet encode/decode."""

    HEADER = b"EF"
    VERSION = 1

    @staticmethod
    def encode(event: str, data: dict, seq: int = 0) -> bytes:
        payload = json.dumps({"e": event, "d": data, "s": seq},
                             separators=(",", ":")).encode("utf-8")
        length  = struct.pack(">H", len(payload))
        return _PacketSerializer.HEADER + bytes([_PacketSerializer.VERSION]) + length + payload

    @staticmethod
    def decode(raw: bytes) -> Optional[Tuple[str, dict, int]]:
        try:
            if raw[:2] != _PacketSerializer.HEADER:
                return None
            length = struct.unpack(">H", raw[3:5])[0]
            obj    = json.loads(raw[5:5 + length].decode("utf-8"))
            return obj["e"], obj["d"], obj.get("s", 0)
        except Exception:
            return None


class _InterpolationBuffer:
    """Stores remote entity state snapshots for smooth rendering."""

    def __init__(self, buffer_ms: float = 100.0):
        self.buffer_ms = buffer_ms
        self._snapshots: deque = deque(maxlen=8)

    def push(self, timestamp: float, x: float, y: float,
             vx: float = 0, vy: float = 0):
        self._snapshots.append((timestamp, x, y, vx, vy))

    def sample(self, now: float) -> Optional[Tuple[float, float]]:
        target_time = now - self.buffer_ms / 1000.0
        snaps       = list(self._snapshots)
        if len(snaps) < 2:
            if snaps:
                return (snaps[-1][1], snaps[-1][2])
            return None
        for i in range(len(snaps) - 1):
            t0, x0, y0, *_ = snaps[i]
            t1, x1, y1, *_ = snaps[i + 1]
            if t0 <= target_time <= t1:
                frac = (target_time - t0) / max(t1 - t0, 0.0001)
                return (lerp(x0, x1, frac), lerp(y0, y1, frac))
        # Extrapolate from last
        _, x, y, vx, vy = snaps[-1]
        dt = now - snaps[-1][0]
        return (x + vx * dt, y + vy * dt)


class Network:
    """
    Optional LAN networking layer.
    Activated only when Game(net=NetMode.SERVER/CLIENT) is used.
    All gameplay systems remain unaware of this module.

    Transport  → raw socket send/receive (TCP + UDP broadcast)
    Serialization → JSON packet encode/decode (_PacketSerializer)
    Sync Layer → entity replication via NetSync component
    """

    BROADCAST_PORT = 5556
    DISCOVERY_MSG  = b"EFORGE_DISCOVER"

    def __init__(
        self,
        mode:     str   = NetMode.CLIENT,
        host:     str   = "127.0.0.1",
        port:     int   = 5555,
        max_players: int = 4,
        password: str   = "",
    ):
        self.mode        = mode
        self.host        = host
        self.port        = port
        self.max_players = max_players
        self.password    = password
        self.my_id:   str = str(uuid.uuid4())[:8]
        self.is_host: bool = (mode == NetMode.SERVER)
        self.peers:   Dict[str, _Peer] = {}
        self.bandwidth_in  = 0
        self.bandwidth_out = 0

        self._sock:    Optional[socket.socket] = None
        self._running: bool = False
        self._listeners: Dict[str, List[Callable]] = defaultdict(list)
        self._send_queue: deque = deque()
        self._recv_queue: deque = deque()
        self._clients:   Dict[str, socket.socket] = {}
        self._thread_recv:  Optional[threading.Thread] = None
        self._thread_send:  Optional[threading.Thread] = None
        self._interp_enabled: bool = False
        self._interp_buffer_ms: float = 100.0
        self._entity_buffers: Dict[str, _InterpolationBuffer] = {}
        self._world: Optional[World] = None
        self._sync_timer: float = 0.0

        # Rate limiting
        self._rate_counts: Dict[str, int] = defaultdict(int)
        self._rate_window:  float = 0.0
        self._max_rate:     int   = 60

    def set_world(self, world: World):
        self._world = world

    def enable_interpolation(self, buffer_ms: float = 100.0):
        self._interp_enabled    = True
        self._interp_buffer_ms  = buffer_ms

    def start(self):
        """Lazily initialize sockets and start background threads."""
        if self._running:
            return
        self._running = True
        try:
            if self.mode == NetMode.SERVER:
                self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self._sock.bind(("", self.port))
                self._sock.listen(self.max_players)
                self._sock.setblocking(False)
                self._thread_recv = threading.Thread(
                    target=self._server_accept_loop, daemon=True)
                self._thread_recv.start()
                self._start_broadcast()
            else:
                self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self._sock.connect((self.host, self.port))
                self._sock.setblocking(False)
                self._thread_recv = threading.Thread(
                    target=self._client_recv_loop,
                    args=(self._sock, self.my_id),
                    daemon=True
                )
                self._thread_recv.start()
                self.broadcast("handshake", {
                    "id":       self.my_id,
                    "password": self.password
                })
        except Exception as e:
            print(f"[Network] Failed to start: {e}")
            self._running = False

    def stop(self):
        self._running = False
        if self._sock:
            try:
                self._sock.close()
            except Exception:
                pass

    def on(self, event: str, callback: Callable):
        self._listeners[event].append(callback)

    def off(self, event: str, callback: Callable):
        self._listeners[event] = [
            c for c in self._listeners[event] if c is not callback
        ]

    def broadcast(self, event: str, data: Optional[dict] = None):
        """Send to all connected peers (reliable TCP)."""
        if data is None:
            data = {}
        data["_from"] = self.my_id
        pkt = _PacketSerializer.encode(event, data)
        self._send_queue.append(("all", pkt))

    def send_to(self, peer_id: str, event: str, data: Optional[dict] = None):
        """Send to specific peer."""
        if data is None:
            data = {}
        data["_from"] = self.my_id
        pkt = _PacketSerializer.encode(event, data)
        self._send_queue.append((peer_id, pkt))

    def send_reliable(self, event: str, data: Optional[dict] = None):
        """Guaranteed delivery — uses TCP channel."""
        self.broadcast(event, data)

    def send_unreliable(self, event: str, data: Optional[dict] = None):
        """Fast, drop-ok — still uses TCP on LAN (UDP is simulated via priority)."""
        self.broadcast(event, data)

    def kick(self, peer_id: str, reason: str = ""):
        self.send_to(peer_id, "kicked", {"reason": reason})
        sock = self._clients.get(peer_id)
        if sock:
            try:
                sock.close()
            except Exception:
                pass
            del self._clients[peer_id]
        self.peers.pop(peer_id, None)

    def update(self, dt: float = 0.016):
        """Call once per frame from Game loop."""
        if not self._running:
            return

        # Dispatch queued incoming packets
        while self._recv_queue:
            event, data = self._recv_queue.popleft()
            self._dispatch(event, data)

        # Flush outgoing send queue
        self._flush_send()

        # Sync NetSync entities
        if self._world:
            self._sync_timer += dt
            rate = 1.0 / 20.0
            if self._sync_timer >= rate:
                self._sync_timer = 0.0
                self._sync_entities()

        # Rate window reset
        self._rate_window += dt
        if self._rate_window > 1.0:
            self._rate_window  = 0.0
            self._rate_counts.clear()

    def _dispatch(self, event: str, data: dict):
        # Internal sync packets handled automatically
        if event == "_sync":
            self.apply_sync(data)
            return
        for cb in self._listeners.get(event, []):
            try:
                cb(data)
            except Exception as e:
                print(f"[Network] Listener error on '{event}': {e}")

    def _flush_send(self):
        while self._send_queue:
            target, pkt = self._send_queue.popleft()
            self.bandwidth_out += len(pkt)
            if self.is_host:
                targets = (
                    list(self._clients.values())
                    if target == "all"
                    else [self._clients.get(target)]
                )
                for sock in targets:
                    if sock:
                        try:
                            sock.sendall(pkt)
                        except Exception:
                            pass
            else:
                if self._sock:
                    try:
                        self._sock.sendall(pkt)
                    except Exception:
                        pass

    def _server_accept_loop(self):
        while self._running:
            try:
                import select
                ready, _, _ = select.select([self._sock], [], [], 0.5)
                if ready:
                    conn, addr = self._sock.accept()
                    pid  = str(uuid.uuid4())[:8]
                    self._clients[pid] = conn
                    self.peers[pid]    = _Peer(pid, conn, addr)
                    t = threading.Thread(
                        target=self._client_recv_loop,
                        args=(conn, pid), daemon=True
                    )
                    t.start()
                    # Notify game of new connection
                    self._recv_queue.append(("connect", {"id": pid, "peer_id": pid}))
            except Exception:
                pass

    def _client_recv_loop(self, sock: socket.socket, peer_id: str):
        buf = b""
        while self._running:
            try:
                import select
                ready, _, _ = select.select([sock], [], [], 0.5)
                if ready:
                    chunk = sock.recv(4096)
                    if not chunk:
                        break
                    self.bandwidth_in += len(chunk)
                    buf += chunk
                    while len(buf) >= 5:
                        if buf[:2] != _PacketSerializer.HEADER:
                            buf = b""
                            break
                        length = struct.unpack(">H", buf[3:5])[0]
                        total  = 5 + length
                        if len(buf) < total:
                            break
                        raw    = buf[:total]
                        buf    = buf[total:]
                        result = _PacketSerializer.decode(raw)
                        if result:
                            event, data, _ = result
                            data["peer_id"] = peer_id
                            self._recv_queue.append((event, data))
            except Exception:
                break

        # Cleanup on disconnect
        self._recv_queue.append(("disconnect", {"id": peer_id, "reason": "timeout"}))
        if self._world:
            self._world.remove_by_net_id(peer_id)
        self._clients.pop(peer_id, None)
        self.peers.pop(peer_id, None)

    def _sync_entities(self):
        if self._world is None:
            return
        now = time.time()
        for e in self._world.get_by_component(NetSync):
            ns = e.get(NetSync)
            if ns.owner != self.my_id:
                continue
            payload: dict = {"eid": e._net_id or str(e.id), "t": now}
            for field, mode in ns.sync.items():
                parts = field.split(".")
                comp_name = parts[0]
                attr_name = parts[1] if len(parts) > 1 else parts[0]
                comp_cls  = _COMP_NAME_MAP.get(comp_name)
                if comp_cls is None:
                    continue
                comp = e.get(comp_cls)
                if comp is None:
                    continue
                val = getattr(comp, attr_name, None)
                if val is not None:
                    payload[field] = val
            self.broadcast("_sync", payload)

    def apply_sync(self, data: dict):
        """Apply received sync packet to the matching entity."""
        if self._world is None:
            return
        eid  = data.get("eid")
        now  = data.get("t", time.time())
        e    = self._world._net_map.get(eid)
        if e is None:
            return
        ns = e.get(NetSync)
        if ns is None or ns.owner == self.my_id:
            return

        for field, mode in ns.sync.items():
            if field not in data:
                continue
            val        = data[field]
            parts      = field.split(".")
            comp_name  = parts[0]
            attr_name  = parts[1] if len(parts) > 1 else parts[0]
            comp_cls   = _COMP_NAME_MAP.get(comp_name)
            if comp_cls is None:
                continue
            comp = e.get(comp_cls)
            if comp is None:
                continue
            if mode == SyncMode.INTERPOLATE and self._interp_enabled:
                buf_key = f"{eid}.{field}"
                if buf_key not in self._entity_buffers:
                    self._entity_buffers[buf_key] = _InterpolationBuffer(
                        self._interp_buffer_ms)
                # For transform.x and transform.y push together
                if field == "transform.x":
                    bx = val
                    by = data.get("transform.y", getattr(comp, "y", 0))
                    self._entity_buffers[buf_key].push(now, bx, by)
                elif field == "transform.y":
                    pass  # handled by x
            else:
                setattr(comp, attr_name, val)

    def flush_interpolation(self, dt: float):
        """Apply interpolated positions. Call after world.update()."""
        if not self._interp_enabled or self._world is None:
            return
        now = time.time()
        for e in self._world.get_by_component(NetSync):
            ns = e.get(NetSync)
            if ns.owner == self.my_id:
                continue
            buf_key = f"{e._net_id or e.id}.transform.x"
            buf     = self._entity_buffers.get(buf_key)
            if buf is None:
                continue
            result  = buf.sample(now)
            if result:
                t = e.get(Transform)
                if t:
                    t.x, t.y = result

    def _start_broadcast(self):
        """UDP broadcast so clients can auto-discover the host."""
        def broadcast_loop():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                msg = json.dumps({
                    "name":    "EForge Game",
                    "port":    self.port,
                    "players": len(self.peers),
                    "max":     self.max_players,
                }).encode()
                while self._running:
                    try:
                        s.sendto(msg, ("<broadcast>", self.BROADCAST_PORT))
                    except Exception:
                        pass
                    time.sleep(2.0)
            except Exception:
                pass
        threading.Thread(target=broadcast_loop, daemon=True).start()

    @staticmethod
    def discover(timeout: float = 2.0) -> List[dict]:
        """Scan LAN for available hosts. Returns list of host info dicts."""
        results = []
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(("", Network.BROADCAST_PORT))
            s.settimeout(0.3)
            end = time.time() + timeout
            seen = set()
            while time.time() < end:
                try:
                    data, addr = s.recvfrom(512)
                    ip = addr[0]
                    if ip not in seen:
                        seen.add(ip)
                        info = json.loads(data.decode())
                        info["ip"] = ip
                        results.append(info)
                except socket.timeout:
                    pass
            s.close()
        except Exception as e:
            print(f"[Network] Discover error: {e}")
        return results

    @staticmethod
    def join(host_info: dict) -> "Network":
        return Network(
            mode=NetMode.CLIENT,
            host=host_info["ip"],
            port=host_info.get("port", 5555),
        )


# Component name → class map for NetSync field resolution
_COMP_NAME_MAP: Dict[str, type] = {
    "transform": Transform,
    "velocity":  Velocity,
    "health":    Health,
    "animator":  Animator,
    "stats":     Stats,
}


class TurnManager:
    """Turn-based multiplayer helper. Host is authority."""

    _players:  List[str] = []
    _current:  int        = 0
    _timeout:  float      = 30.0
    _timer:    float      = 0.0
    _running:  bool       = False
    _net:      Optional[Network] = None

    @classmethod
    def set_players(cls, player_ids: List[str]):
        cls._players = player_ids
        cls._current = 0

    @classmethod
    def set_timeout(cls, seconds: float):
        cls._timeout = seconds

    @classmethod
    def set_network(cls, net: Network):
        cls._net = net

    @classmethod
    def start(cls):
        cls._running = True
        cls._timer   = 0.0
        if cls._net and cls._net.is_host:
            cls._net.broadcast("turn_changed", {"id": cls._players[0]})

    @classmethod
    def is_my_turn(cls) -> bool:
        if not cls._players or cls._net is None:
            return True
        return cls._players[cls._current] == cls._net.my_id

    @classmethod
    def end_turn(cls):
        if not cls._net or not cls._net.is_host:
            if cls._net:
                cls._net.broadcast("end_turn", {})
            return
        cls._advance()

    @classmethod
    def _advance(cls):
        cls._current = (cls._current + 1) % len(cls._players)
        cls._timer   = 0.0
        if cls._net:
            cls._net.broadcast("turn_changed", {"id": cls._players[cls._current]})

    @classmethod
    def update(cls, dt: float):
        if not cls._running:
            return
        cls._timer += dt
        if cls._timer >= cls._timeout:
            if cls._net and cls._net.is_host:
                cls._advance()


class Lobby:
    """Player lobby with chat and spectator support."""

    def __init__(self, net: Network):
        self._net = net
        self.players: List[_Peer] = []
        self._on_all_ready: Optional[Callable] = None

        net.on("connect",    self._on_connect)
        net.on("disconnect", self._on_disconnect)
        net.on("ready",      self._on_ready)
        net.on("chat",       lambda d: self.chat._receive(d))

        self.chat = _LobbyChat(net)

    def _on_connect(self, data: dict):
        pid  = data.get("id", data.get("peer_id", ""))
        peer = self._net.peers.get(pid, _Peer(pid))
        self.players.append(peer)

    def _on_disconnect(self, data: dict):
        pid  = data.get("id", "")
        self.players = [p for p in self.players if p.id != pid]

    def _on_ready(self, data: dict):
        pid = data.get("peer_id", "")
        for p in self.players:
            if p.id == pid:
                p.ready = data.get("ready", True)
        if self._on_all_ready and all(p.ready for p in self.players):
            self._on_all_ready()

    def set_ready(self, ready: bool = True):
        self._net.broadcast("ready", {"ready": ready})

    def on_all_ready(self, callback: Callable):
        self._on_all_ready = callback

    def join_as_spectator(self):
        self._net.broadcast("spectate", {})

    def set_max_spectators(self, n: int):
        self._max_spectators = n


class _LobbyChat:
    def __init__(self, net: Network):
        self._net = net
        self._on_msg: Optional[Callable] = None

    def send(self, text: str):
        self._net.broadcast("chat", {"text": text})

    def on_message(self, callback: Callable):
        self._on_msg = callback

    def _receive(self, data: dict):
        msg = {"from": data.get("_from", "?"), "text": data.get("text", ""),
               "time": time.time()}
        if self._on_msg:
            self._on_msg(msg)

# =============================================================================
# ===[ UI ]====================================================================
# =============================================================================

class Anchor:
    TOP_LEFT    = "top_left"
    TOP_CENTER  = "top_center"
    TOP_RIGHT   = "top_right"
    MID_LEFT    = "mid_left"
    CENTER      = "center"
    MID_RIGHT   = "mid_right"
    BOT_LEFT    = "bot_left"
    BOT_CENTER  = "bot_center"
    BOT_RIGHT   = "bot_right"


def _resolve_anchor(x, y, w, h, anchor, screen_w, screen_h):
    offsets = {
        Anchor.TOP_LEFT:   (0,          0),
        Anchor.TOP_CENTER: (screen_w//2 - w//2, 0),
        Anchor.TOP_RIGHT:  (screen_w - w, 0),
        Anchor.MID_LEFT:   (0,          screen_h//2 - h//2),
        Anchor.CENTER:     (screen_w//2 - w//2, screen_h//2 - h//2),
        Anchor.MID_RIGHT:  (screen_w - w, screen_h//2 - h//2),
        Anchor.BOT_LEFT:   (0,          screen_h - h),
        Anchor.BOT_CENTER: (screen_w//2 - w//2, screen_h - h),
        Anchor.BOT_RIGHT:  (screen_w - w, screen_h - h),
    }
    ox, oy = offsets.get(anchor, (0, 0))
    return x + ox, y + oy


def _draw_rounded_rect(surface, color, rect, radius=6, border=None, border_color=None):
    r = min(radius, rect.width // 2, rect.height // 2)
    pygame.draw.rect(surface, color, rect, border_radius=r)
    if border and border_color:
        pygame.draw.rect(surface, border_color, rect, border, border_radius=r)


class _Widget:
    def __init__(self, x, y, w, h, anchor=None, style=None):
        self.x      = x
        self.y      = y
        self.w      = w
        self.h      = h
        self.anchor = anchor
        self.style  = style or Style()
        self.visible = True
        self._anim_alpha = 255
        self._anim_mode: Optional[str] = None
        self._anim_timer = 0.0
        self._anim_in    = False

    def animate_in(self, mode: str = "fade"):
        self._anim_mode  = mode
        self._anim_timer = 0.0
        self._anim_in    = True
        self._anim_alpha = 0

    def animate_out(self, mode: str = "fade"):
        self._anim_mode  = mode
        self._anim_timer = 0.0
        self._anim_in    = False

    def _tick_anim(self, dt: float):
        if self._anim_mode is None:
            return
        self._anim_timer = min(1.0, self._anim_timer + dt * 4)
        t = self._anim_timer
        if self._anim_in:
            self._anim_alpha = int(lerp(0, 255, t))
        else:
            self._anim_alpha = int(lerp(255, 0, t))
        if t >= 1.0:
            self._anim_mode = None

    def _resolved_rect(self, screen) -> pygame.Rect:
        sw, sh = screen.get_size()
        rx, ry = _resolve_anchor(self.x, self.y, self.w, self.h,
                                 self.anchor, sw, sh)
        return pygame.Rect(int(rx), int(ry), self.w, self.h)

    def update(self, dt: float, events): pass
    def draw(self, screen: pygame.Surface): pass


class Button(_Widget):
    def __init__(self, text="Button", x=0, y=0, w=160, h=50,
                 anchor=None, on_click=None, style=None):
        super().__init__(x, y, w, h, anchor, style)
        self.text      = text
        self.on_click  = on_click
        self._hover    = False
        self._pressed  = False

    def update(self, dt: float, events):
        self._tick_anim(dt)
        rect = self._resolved_rect(pygame.display.get_surface())
        mx, my = Input.touch_pos() or (-1, -1)
        self._hover = rect.collidepoint(mx, my)
        if Input.tapped() and self._hover and self.on_click:
            self.on_click()

    def draw(self, screen: pygame.Surface):
        if not self.visible:
            return
        rect = self._resolved_rect(screen)
        s    = self.style
        if self._pressed:
            bg = s.resolve("press_bg")
        elif self._hover:
            bg = s.resolve("hover_bg")
        else:
            bg = s.resolve("bg")
        _draw_rounded_rect(screen, bg, rect, s.radius,
                           border=1, border_color=s.resolve("border"))
        font = Assets.get_font(s.font_key, s.font_size)
        txt  = font.render(self.text, True, s.resolve("text_color"))
        screen.blit(txt, txt.get_rect(center=rect.center))


class Label(_Widget):
    def __init__(self, text="", x=0, y=0, anchor=None, style=None):
        super().__init__(x, y, 0, 0, anchor, style)
        self.text = text

    def set_text(self, text: str):
        self.text = text

    def draw(self, screen: pygame.Surface):
        if not self.visible:
            return
        s    = self.style
        font = Assets.get_font(s.font_key, s.font_size)
        surf = font.render(self.text, True, s.resolve("text_color"))
        sw, sh = screen.get_size()
        rx, ry = _resolve_anchor(self.x, self.y,
                                 surf.get_width(), surf.get_height(),
                                 self.anchor, sw, sh)
        screen.blit(surf, (int(rx), int(ry)))


class Panel(_Widget):
    def __init__(self, x=0, y=0, w=300, h=200, anchor=None, style=None):
        super().__init__(x, y, w, h, anchor, style)
        self._children: List[_Widget] = []

    def add(self, widget: _Widget):
        self._children.append(widget)

    def update(self, dt: float, events):
        self._tick_anim(dt)
        for c in self._children:
            c.update(dt, events)

    def draw(self, screen: pygame.Surface):
        if not self.visible:
            return
        rect = self._resolved_rect(screen)
        _draw_rounded_rect(screen, Theme.get("panel_bg"), rect,
                           self.style.radius, border=1,
                           border_color=Theme.get("border"))
        for c in self._children:
            c.draw(screen)


class ProgressBar(_Widget):
    def __init__(self, x=0, y=0, w=200, h=20, value=1.0,
                 anchor=None, style=None):
        super().__init__(x, y, w, h, anchor, style)
        self.value = clamp(value, 0.0, 1.0)

    def set_value(self, v: float):
        self.value = clamp(v, 0.0, 1.0)

    def draw(self, screen: pygame.Surface):
        if not self.visible:
            return
        rect = self._resolved_rect(screen)
        _draw_rounded_rect(screen, Theme.get("bar_bg"), rect, 4)
        fw = int(rect.width * self.value)
        if fw > 0:
            fr = pygame.Rect(rect.x, rect.y, fw, rect.height)
            _draw_rounded_rect(screen, Theme.get("bar_fg"), fr, 4)
        pygame.draw.rect(screen, Theme.get("border"), rect, 1, border_radius=4)


class HealthBar(ProgressBar):
    def draw(self, screen: pygame.Surface):
        if not self.visible:
            return
        rect = self._resolved_rect(screen)
        _draw_rounded_rect(screen, Theme.get("bar_bg"), rect, 4)
        fw  = int(rect.width * self.value)
        r   = int(lerp(200, 80, self.value))
        g   = int(lerp(60,  200, self.value))
        col = (r, g, 60)
        if fw > 0:
            fr = pygame.Rect(rect.x, rect.y, fw, rect.height)
            _draw_rounded_rect(screen, col, fr, 4)
        pygame.draw.rect(screen, Theme.get("border"), rect, 1, border_radius=4)


class Slider(_Widget):
    def __init__(self, x=0, y=0, w=200, min_val=0.0, max_val=1.0,
                 value=0.5, anchor=None, style=None):
        super().__init__(x, y, w, 30, anchor, style)
        self.min_val   = min_val
        self.max_val   = max_val
        self.value     = value
        self.on_change: Optional[Callable] = None
        self._dragging = False

    def update(self, dt: float, events):
        self._tick_anim(dt)
        rect = self._resolved_rect(pygame.display.get_surface())
        tp   = Input.touch_pos()
        if tp:
            tx, ty = tp
            if rect.collidepoint(tx, ty):
                self._dragging = True
            if self._dragging:
                frac = clamp((tx - rect.x) / rect.width, 0.0, 1.0)
                v    = self.min_val + frac * (self.max_val - self.min_val)
                if v != self.value:
                    self.value = v
                    if self.on_change:
                        self.on_change(v)

    def draw(self, screen: pygame.Surface):
        if not self.visible:
            return
        rect  = self._resolved_rect(screen)
        track = pygame.Rect(rect.x, rect.centery - 3, rect.width, 6)
        _draw_rounded_rect(screen, Theme.get("bar_bg"), track, 3)
        frac  = (self.value - self.min_val) / max(self.max_val - self.min_val, 0.001)
        fx    = int(rect.x + frac * rect.width)
        pygame.draw.circle(screen, Theme.get("accent"), (fx, rect.centery), 12)
        pygame.draw.circle(screen, Theme.get("border"), (fx, rect.centery), 12, 1)


class Toggle(_Widget):
    def __init__(self, x=0, y=0, label="", value=True,
                 anchor=None, style=None):
        super().__init__(x, y, 80, 36, anchor, style)
        self.label     = label
        self.value     = value
        self.on_change: Optional[Callable] = None

    def update(self, dt: float, events):
        self._tick_anim(dt)
        if Input.tapped():
            tp = Input.touch_pos()
            if tp:
                rect = self._resolved_rect(pygame.display.get_surface())
                if rect.collidepoint(*tp):
                    self.value = not self.value
                    if self.on_change:
                        self.on_change(self.value)

    def draw(self, screen: pygame.Surface):
        if not self.visible:
            return
        rect = self._resolved_rect(screen)
        bg   = Theme.get("accent") if self.value else Theme.get("button_bg")
        _draw_rounded_rect(screen, bg, rect, rect.height // 2)
        kx   = rect.right - rect.height // 2 if self.value else rect.left + rect.height // 2
        pygame.draw.circle(screen, (220, 220, 220), (kx, rect.centery), rect.height // 2 - 4)
        if self.label:
            font = Assets.get_font(self.style.font_key, self.style.font_size)
            lbl  = font.render(self.label, True, Theme.get("text"))
            screen.blit(lbl, (rect.right + 10, rect.centery - lbl.get_height() // 2))


class Dropdown(_Widget):
    def __init__(self, x=0, y=0, w=200, options=None, selected=0,
                 anchor=None, style=None):
        super().__init__(x, y, w, 44, anchor, style)
        self.options   = options or []
        self.selected  = selected
        self.on_change: Optional[Callable] = None
        self._open     = False

    @property
    def selected_text(self) -> str:
        if 0 <= self.selected < len(self.options):
            return self.options[self.selected]
        return ""

    def update(self, dt: float, events):
        self._tick_anim(dt)
        if Input.tapped():
            tp   = Input.touch_pos()
            rect = self._resolved_rect(pygame.display.get_surface())
            if tp and rect.collidepoint(*tp):
                self._open = not self._open
            elif self._open and tp:
                for i, _ in enumerate(self.options):
                    or_ = pygame.Rect(rect.x, rect.bottom + i * self.h,
                                      rect.width, self.h)
                    if or_.collidepoint(*tp):
                        self.selected = i
                        self._open    = False
                        if self.on_change:
                            self.on_change(self.selected_text)

    def draw(self, screen: pygame.Surface):
        if not self.visible:
            return
        rect = self._resolved_rect(screen)
        _draw_rounded_rect(screen, Theme.get("button_bg"), rect,
                           self.style.radius, 1, Theme.get("border"))
        font = Assets.get_font(self.style.font_key, self.style.font_size)
        txt  = font.render(self.selected_text + " ▾", True, Theme.get("text"))
        screen.blit(txt, (rect.x + 8, rect.centery - txt.get_height() // 2))
        if self._open:
            for i, opt in enumerate(self.options):
                or_ = pygame.Rect(rect.x, rect.bottom + i * self.h,
                                  rect.width, self.h)
                bg  = Theme.get("button_hover") if i == self.selected \
                    else Theme.get("button_bg")
                _draw_rounded_rect(screen, bg, or_, 4, 1, Theme.get("border"))
                t   = font.render(opt, True, Theme.get("text"))
                screen.blit(t, (or_.x + 8, or_.centery - t.get_height() // 2))


class TextInput(_Widget):
    def __init__(self, x=0, y=0, w=300, placeholder="",
                 anchor=None, style=None):
        super().__init__(x, y, w, 48, anchor, style)
        self.text        = ""
        self.placeholder = placeholder
        self.on_submit:   Optional[Callable] = None
        self._active     = False
        self._cursor     = 0

    def update(self, dt: float, events):
        self._tick_anim(dt)
        if Input.tapped():
            tp   = Input.touch_pos()
            rect = self._resolved_rect(pygame.display.get_surface())
            self._active = bool(tp and rect.collidepoint(*tp))

        if self._active:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get(pygame.KEYDOWN):
                if event.key == pygame.K_RETURN:
                    self._active = False
                    if self.on_submit:
                        self.on_submit(self.text)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if event.unicode:
                        self.text += event.unicode

    def draw(self, screen: pygame.Surface):
        if not self.visible:
            return
        rect  = self._resolved_rect(screen)
        bg    = Theme.get("input_bg")
        border_col = Theme.get("accent") if self._active else Theme.get("border")
        _draw_rounded_rect(screen, bg, rect, self.style.radius,
                           border=2, border_color=border_col)
        font  = Assets.get_font(self.style.font_key, self.style.font_size)
        disp  = self.text if self.text else self.placeholder
        color = Theme.get("text") if self.text else Theme.get("border")
        txt   = font.render(disp, True, color)
        screen.blit(txt, (rect.x + 8, rect.centery - txt.get_height() // 2))
        if self._active:
            cx = rect.x + 8 + txt.get_width() + 2
            cy = rect.centery - 10
            pygame.draw.line(screen, Theme.get("text"),
                             (cx, cy), (cx, cy + 20), 2)


class ScrollView(_Widget):
    def __init__(self, x=0, y=0, w=300, h=400, anchor=None, style=None):
        super().__init__(x, y, w, h, anchor, style)
        self._children: List[_Widget] = []
        self._scroll_y  = 0
        self._drag_y:   Optional[int] = None
        self._content_h = 0

    def add(self, widget: _Widget):
        widget.y += self._content_h
        self._content_h += widget.h + 8
        self._children.append(widget)

    def update(self, dt: float, events):
        self._tick_anim(dt)
        tp = Input.touch_pos()
        if tp:
            rect = self._resolved_rect(pygame.display.get_surface())
            if rect.collidepoint(*tp):
                if self._drag_y is None:
                    self._drag_y = tp[1]
                else:
                    dy = tp[1] - self._drag_y
                    self._scroll_y = clamp(
                        self._scroll_y + dy,
                        -(max(0, self._content_h - self.h)), 0
                    )
                    self._drag_y = tp[1]
            else:
                self._drag_y = None
        for c in self._children:
            c.update(dt, events)

    def draw(self, screen: pygame.Surface):
        if not self.visible:
            return
        rect = self._resolved_rect(screen)
        clip = screen.subsurface(rect.clip(screen.get_rect()))
        clip.fill(Theme.get("panel_bg"))
        for c in self._children:
            oy  = c.y + self._scroll_y
            if -c.h <= oy <= self.h:
                orig_y = c.y
                c.y    = int(self.y + oy)
                c.draw(screen)
                c.y    = orig_y
        pygame.draw.rect(screen, Theme.get("border"), rect, 1)


class Grid(_Widget):
    def __init__(self, x=0, y=0, cols=3, cell_w=100, cell_h=60,
                 gap=8, anchor=None, style=None):
        super().__init__(x, y, cols * (cell_w + gap), 0, anchor, style)
        self.cols    = cols
        self.cell_w  = cell_w
        self.cell_h  = cell_h
        self.gap     = gap
        self._children: List[_Widget] = []

    def add(self, widget: _Widget):
        idx   = len(self._children)
        col   = idx % self.cols
        row   = idx // self.cols
        widget.x = self.x + col * (self.cell_w + self.gap)
        widget.y = self.y + row * (self.cell_h + self.gap)
        widget.w = self.cell_w
        widget.h = self.cell_h
        self._children.append(widget)
        self.h = (row + 1) * (self.cell_h + self.gap)

    def update(self, dt: float, events):
        for c in self._children:
            c.update(dt, events)

    def draw(self, screen: pygame.Surface):
        if not self.visible:
            return
        for c in self._children:
            c.draw(screen)


class _ToastManager:
    _toasts: List[dict] = []

    @classmethod
    def show(cls, message: str, duration: float = 2.0, style: Optional[Style] = None):
        cls._toasts.append({
            "msg":     message,
            "timer":   0.0,
            "dur":     duration,
            "style":   style or Style(),
        })

    @classmethod
    def update(cls, dt: float):
        cls._toasts = [t for t in cls._toasts
                       if t["timer"] + dt < t["dur"]]
        for t in cls._toasts:
            t["timer"] += dt

    @classmethod
    def draw(cls, screen: pygame.Surface):
        sw, sh = screen.get_size()
        font   = Assets.get_font("default", 20)
        y      = sh - 120
        for toast in reversed(cls._toasts):
            alpha = 255
            rem   = toast["dur"] - toast["timer"]
            if rem < 0.4:
                alpha = int(255 * rem / 0.4)
            msg   = toast["msg"]
            txt   = font.render(msg, True, Theme.get("text"))
            w     = txt.get_width() + 24
            h     = 44
            x     = sw // 2 - w // 2
            s     = pygame.Surface((w, h), pygame.SRCALPHA)
            s.fill((*Theme.get("toast_bg"), alpha))
            screen.blit(s, (x, y))
            screen.blit(txt, (x + 12, y + h // 2 - txt.get_height() // 2))
            y -= h + 8


Toast = _ToastManager


class _ModalManager:
    _active: Optional[dict] = None

    @classmethod
    def show(cls, title: str, message: str,
             options: List[str], on_choice: Callable):
        cls._active = {
            "title":     title,
            "message":   message,
            "options":   options,
            "on_choice": on_choice,
        }

    @classmethod
    def is_open(cls) -> bool:
        return cls._active is not None

    @classmethod
    def update(cls, dt: float):
        if not cls._active:
            return
        if Input.tapped():
            tp = Input.touch_pos()
            if tp is None:
                return
            m      = cls._active
            sw, sh = pygame.display.get_surface().get_size()
            mw, mh = 400, 220
            mx     = sw // 2 - mw // 2
            my     = sh // 2 - mh // 2
            bw     = (mw - 40 - (len(m["options"]) - 1) * 10) // len(m["options"])
            for i, opt in enumerate(m["options"]):
                bx = mx + 20 + i * (bw + 10)
                by = my + mh - 70
                br = pygame.Rect(bx, by, bw, 48)
                if br.collidepoint(*tp):
                    choice     = opt
                    cls._active = None
                    m["on_choice"](choice)
                    return

    @classmethod
    def draw(cls, screen: pygame.Surface):
        if not cls._active:
            return
        m      = cls._active
        sw, sh = screen.get_size()
        # Dim overlay
        dim = pygame.Surface((sw, sh), pygame.SRCALPHA)
        dim.fill((*Theme.get("overlay"), 160))
        screen.blit(dim, (0, 0))
        mw, mh = 400, 220
        mx     = sw // 2 - mw // 2
        my     = sh // 2 - mh // 2
        font_t = Assets.get_font("default", 22)
        font_b = Assets.get_font("default", 18)
        _draw_rounded_rect(screen, Theme.get("modal_bg"),
                           pygame.Rect(mx, my, mw, mh), 10,
                           border=1, border_color=Theme.get("border"))
        title = font_t.render(m["title"], True, Theme.get("text"))
        screen.blit(title, (mx + mw // 2 - title.get_width() // 2, my + 16))
        msg   = font_b.render(m["message"], True, Theme.get("accent"))
        screen.blit(msg, (mx + mw // 2 - msg.get_width() // 2, my + 56))
        bw = (mw - 40 - (len(m["options"]) - 1) * 10) // len(m["options"])
        for i, opt in enumerate(m["options"]):
            bx = mx + 20 + i * (bw + 10)
            by = my + mh - 70
            _draw_rounded_rect(screen, Theme.get("button_bg"),
                               pygame.Rect(bx, by, bw, 48), 6,
                               border=1, border_color=Theme.get("border"))
            t = font_b.render(opt, True, Theme.get("text"))
            screen.blit(t, (bx + bw // 2 - t.get_width() // 2, by + 24 - t.get_height() // 2))


Modal = _ModalManager


class Joystick(_Widget):
    """Visual virtual joystick — registers itself with Input."""

    def __init__(self, cx=120, cy=1200, radius=80):
        super().__init__(cx - radius, cy - radius, radius * 2, radius * 2)
        Input.add_joystick(cx, cy, radius)

    def update(self, dt, events): pass
    def draw(self, screen): pass


class VStack(_Widget):
    def __init__(self, x=0, y=0, gap=8, anchor=None):
        super().__init__(x, y, 0, 0, anchor)
        self.gap        = gap
        self._children: List[_Widget] = []
        self._cy        = y

    def add(self, widget: _Widget):
        widget.x  = self.x
        widget.y  = self._cy
        self._cy  += widget.h + self.gap
        self.h    += widget.h + self.gap
        self.w     = max(self.w, widget.w)
        self._children.append(widget)

    def update(self, dt, events):
        for c in self._children:
            c.update(dt, events)

    def draw(self, screen):
        for c in self._children:
            c.draw(screen)


class HStack(_Widget):
    def __init__(self, x=0, y=0, gap=8, anchor=None):
        super().__init__(x, y, 0, 0, anchor)
        self.gap        = gap
        self._children: List[_Widget] = []
        self._cx        = x

    def add(self, widget: _Widget):
        widget.x  = self._cx
        widget.y  = self.y
        self._cx  += widget.w + self.gap
        self.w    += widget.w + self.gap
        self.h     = max(self.h, widget.h)
        self._children.append(widget)

    def update(self, dt, events):
        for c in self._children:
            c.update(dt, events)

    def draw(self, screen):
        for c in self._children:
            c.draw(screen)


class UIManager:
    """Manages all UI widgets. Handles input and draw order."""

    def __init__(self):
        self._widgets: List[_Widget] = []

    def add(self, widget: _Widget):
        self._widgets.append(widget)
        return widget

    def remove(self, widget: _Widget):
        self._widgets = [w for w in self._widgets if w is not widget]

    def update(self, dt: float):
        events = []
        Toast.update(dt)
        Modal.update(dt)
        for w in self._widgets:
            w.update(dt, events)

    def draw(self, screen: pygame.Surface):
        for w in self._widgets:
            if w.visible:
                w.draw(screen)
        Toast.draw(screen)
        Modal.draw(screen)
        Input.draw_ui(screen)

# =============================================================================
# ===[ DEBUG ]=================================================================
# =============================================================================

class _Debug:
    enabled       = False
    show_hitboxes = False
    show_fps      = True
    show_grid     = False
    show_camera   = False
    show_chunks   = False
    show_paths    = False
    _values:  Dict[str, Any] = {}
    _fps_buf: deque = deque(maxlen=60)

    @classmethod
    def log(cls, key: str, value):
        cls._values[key] = value

    @classmethod
    def _record_fps(cls, fps: float):
        cls._fps_buf.append(fps)

    @classmethod
    def draw(cls, screen: pygame.Surface, clock: pygame.time.Clock,
             world: Optional[World] = None,
             camera: Optional[Camera] = None,
             spatial_hash: Optional[_SpatialHash] = None):
        if not cls.enabled:
            return

        fps     = clock.get_fps()
        cls._record_fps(fps)
        avg_fps = sum(cls._fps_buf) / max(len(cls._fps_buf), 1)

        font    = Assets.get_font("default", 18)
        color   = Theme.get("debug_color")
        lines   = []

        if cls.show_fps:
            lines.append(f"FPS: {fps:.0f}  AVG: {avg_fps:.0f}")

        if world:
            lines.append(f"Entities: {world.entity_count()}")

        for k, v in cls._values.items():
            lines.append(f"{k}: {v}")

        for i, line in enumerate(lines):
            surf = font.render(line, True, color)
            screen.blit(surf, (6, 6 + i * 22))

        if cls.show_grid and spatial_hash and camera:
            spatial_hash.draw_debug(screen, camera)

        if cls.show_camera and camera:
            vp = camera.viewport
            pygame.draw.rect(screen, color, vp, 1)


Debug = _Debug()

# =============================================================================
# ===[ EVENT BUS ]=============================================================
# =============================================================================

class _EventBus:
    """
    Global message bus. Listeners stored as weak references.
    Events queued and dispatched once per frame.
    """

    def __init__(self):
        self._listeners: Dict[str, List] = defaultdict(list)
        self._queue:     deque            = deque()

    def on(self, event: str, callback: Callable):
        key = sys.intern(event)
        try:
            ref = weakref.WeakMethod(callback)
        except TypeError:
            ref = weakref.ref(callback)
        self._listeners[key].append(ref)

    def off(self, event: str, callback: Callable):
        key  = sys.intern(event)
        keep = []
        for ref in self._listeners.get(key, []):
            cb = ref()
            if cb is not None and cb is not callback:
                keep.append(ref)
        self._listeners[key] = keep

    def emit(self, event: str, data: Optional[dict] = None):
        self._queue.append((sys.intern(event), data or {}))

    def flush(self):
        while self._queue:
            event, data = self._queue.popleft()
            dead = []
            for ref in self._listeners.get(event, []):
                cb = ref()
                if cb is None:
                    dead.append(ref)
                else:
                    try:
                        cb(data)
                    except Exception as e:
                        print(f"[EventBus] Error in '{event}': {e}")
            for d in dead:
                self._listeners[event].remove(d)


EventBus = _EventBus()

# =============================================================================
# ===[ SAVE SYSTEM ]===========================================================
# =============================================================================

class _Save:
    _dir = "saves"

    @classmethod
    def _path(cls, slot: int) -> str:
        os.makedirs(cls._dir, exist_ok=True)
        return os.path.join(cls._dir, f"slot_{slot}.json")

    @classmethod
    def write(cls, slot: int, data: dict):
        try:
            with open(cls._path(slot), "w") as f:
                json.dump(data, f)
        except Exception as e:
            print(f"[Save] Write error slot {slot}: {e}")

    @classmethod
    def read(cls, slot: int) -> Optional[dict]:
        path = cls._path(slot)
        if not os.path.exists(path):
            return None
        try:
            with open(path, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"[Save] Read error slot {slot}: {e}")
            return None

    @classmethod
    def delete(cls, slot: int):
        path = cls._path(slot)
        if os.path.exists(path):
            os.remove(path)

    @classmethod
    def exists(cls, slot: int) -> bool:
        return os.path.exists(cls._path(slot))


Save = _Save()

# =============================================================================
# ===[ SCENE MANAGER ]=========================================================
# =============================================================================

class Scene:
    """Base class for all game states."""

    def __init__(self):
        self.sm:     Optional["SceneManager"] = None
        self._children: List["Scene"] = []

    def on_enter(self): pass
    def on_exit(self):  pass
    def update(self, dt: float): pass
    def draw(self, screen: pygame.Surface): pass

    def add_child(self, node: "Scene"):
        self._children.append(node)

    def remove_child(self, node: "Scene"):
        self._children = [c for c in self._children if c is not node]

    # Shared data store (for passing data between scenes)
    def get_shared(self, key: str) -> Any:
        if self.sm:
            return self.sm._shared.get(key)
        return None

    def set_shared(self, key: str, value: Any):
        if self.sm:
            self.sm._shared[key] = value


class SceneManager:
    """Stack-based scene manager. Injected as self.sm into every Scene."""

    def __init__(self, net: Optional[Network] = None):
        self._stack:  List[Scene] = []
        self._shared: Dict[str, Any] = {}
        self.net:     Optional[Network] = net

    def push(self, scene_cls, *args, **kwargs):
        scene     = scene_cls(*args, **kwargs)
        scene.sm  = self
        self._stack.append(scene)
        scene.on_enter()

    def pop(self):
        if self._stack:
            self._stack[-1].on_exit()
            self._stack.pop()
        if self._stack:
            self._stack[-1].on_enter()

    def switch(self, scene_cls, *args, **kwargs):
        if self._stack:
            self._stack[-1].on_exit()
            self._stack.pop()
        self.push(scene_cls, *args, **kwargs)

    def update(self, dt: float):
        if self._stack:
            self._stack[-1].update(dt)

    def draw(self, screen: pygame.Surface):
        if self._stack:
            self._stack[-1].draw(screen)

    @property
    def current(self) -> Optional[Scene]:
        return self._stack[-1] if self._stack else None

# =============================================================================
# ===[ GAME LOOP ]=============================================================
# =============================================================================

_MAX_DT    = 0.05
_SKIP_DT   = 0.1


class Game:
    """
    Entry point. Manages window, clock, and main loop.

    Usage:
        Game(title="My Game", fps=60).run(GameScene)

    Networking:
        Game(title="Host", fps=60, net=NetMode.SERVER, port=5555).run(GameScene)
        Game(title="Join", fps=60, net=NetMode.CLIENT, host="192.168.x.x").run(GameScene)
    """

    def __init__(
        self,
        title:       str  = "EForge Game",
        fps:         int  = 60,
        width:       Optional[int] = None,
        height:      Optional[int] = None,
        net:         Optional[str] = None,
        host:        str  = "127.0.0.1",
        port:        int  = 5555,
        password:    str  = "",
        max_players: int  = 4,
    ):
        # Auto-detect screen size
        if width is None or height is None:
            info = pygame.display.Info()
            width  = width  or 800 or 800
            height = height or info.current_h or 1461

        flags   = pygame.FULLSCREEN | pygame.SCALED
        try:
            self.screen = pygame.display.set_mode((width, height), flags)
        except Exception:
            self.screen = pygame.display.set_mode((width, height))

        pygame.display.set_caption(title)
        self.clock  = pygame.time.Clock()
        self.fps    = fps
        self.width  = width
        self.height = height
        self.running = True

        # Optional networking — lazy initialized
        self._net: Optional[Network] = None
        if net is not None:
            self._net = Network(
                mode=net, host=host, port=port,
                max_players=max_players, password=password,
            )
            self._net.start()

        self.sm = SceneManager(net=self._net)

    def run(self, scene_cls, *args, **kwargs):
        """Start the game with the given Scene class."""
        self.sm.push(scene_cls, *args, **kwargs)

        prev_time = time.perf_counter()
        accum     = 0.0

        while self.running:
            now  = time.perf_counter()
            raw_dt = now - prev_time
            prev_time = now

            # Clamp delta-time — prevents physics explosion on lag spikes
            dt = min(raw_dt, _MAX_DT)

            # Network update (no-op if offline)
            if self._net:
                self._net.update(dt)
                if self._net._interp_enabled:
                    self._net.flush_interpolation(dt)

            # Scene update
            self.sm.update(dt)

            # EventBus flush (after all updates, before draw)
            EventBus.flush()

            # Draw
            self.sm.draw(self.screen)

            # Debug overlay
            Debug.draw(self.screen, self.clock)

            pygame.display.flip()

            # Frame timing
            import platform
            if platform.system() == "Linux" or "android" in sys.platform.lower():
                self.clock.tick(self.fps)
            else:
                self.clock.tick_busy_loop(self.fps)

        if self._net:
            self._net.stop()
        pygame.quit()
        sys.exit()
