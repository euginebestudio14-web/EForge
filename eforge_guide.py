# ===========================================================================
#  EForge — Complete Beginner Guide
#  Read this top to bottom. Every section tells you WHAT it is,
#  WHERE to put it, and HOW to use it with a working example.
# ===========================================================================

# ---------------------------------------------------------------------------
# STEP 0 — THE GOLDEN RULE
# ---------------------------------------------------------------------------
# Every game file starts with these two lines. Always. No exceptions.
#
#   import pygame
#   from eforge import *
#
# Put eforge.py in the SAME folder as your game file.
# ---------------------------------------------------------------------------




# ===========================================================================
# PART 1 — HOW A GAME IS STRUCTURED
# ===========================================================================
#
# Every EForge game has this exact shape:
#
#   import pygame
#   from eforge import *
#
#   class MyScene(Scene):           <-- your game screen
#       def on_enter(self):         <-- runs ONCE when scene starts
#           ...setup here...
#
#       def update(self, dt):       <-- runs EVERY FRAME (logic)
#           Input.update()          <-- MUST be first line always
#           ...game logic here...
#
#       def draw(self, screen):     <-- runs EVERY FRAME (drawing)
#           screen.fill((0,0,0))    <-- clear screen first always
#           ...drawing here...
#
#   Game(title="My Game", fps=60).run(MyScene)   <-- starts the game
#
# RULES:
#   on_enter  → create worlds, entities, UI, map keys. Runs ONCE.
#   update    → move things, check input, run logic. Runs every frame.
#   draw      → draw everything. Runs every frame after update.
#   Input.update() → FIRST line of update, every time, no exceptions.
#   screen.fill()  → FIRST line of draw, every time. Clears old frame.
# ===========================================================================




# ===========================================================================
# PART 2 — THE SIMPLEST GAME
# ===========================================================================

import pygame
from eforge import *

class Part2_Example(Scene):

    def on_enter(self):
        # on_enter runs once. Put all setup here.
        self.x = 360.0
        self.y = 730.0

    def update(self, dt):
        Input.update()  # always first

        # Move circle to wherever you tap
        if Input.tapped():
            pos = Input.touch_pos()  # returns (x, y) or None
            if pos:
                self.x = float(pos[0])
                self.y = float(pos[1])

    def draw(self, screen):
        screen.fill((30, 30, 30))  # always first — clears screen

        pygame.draw.circle(
            screen,
            (255, 220, 50),        # yellow color (R, G, B)
            (int(self.x), int(self.y)),
            50                     # radius
        )

# Game(title="Part 2", fps=60).run(Part2_Example)
# ^ Remove the # to run this part




# ===========================================================================
# PART 3 — INPUT
# ===========================================================================
#
# WHERE: Input.update() goes FIRST in update(). Everything else goes after.
#        Input.map() and Input.add_button() go in on_enter().
#        Input.draw_ui() goes at the END of draw() so buttons show on top.
#
# TOUCH INPUT:
#   Input.tapped()          True for one frame when you quickly tap
#   Input.touch_pos()       (x, y) of last touch, or None
#   Input.swipe()           "left" "right" "up" "down" or None
#
# KEYBOARD INPUT:
#   Input.map("jump", "space")   link action name to key — put in on_enter
#   Input.just_pressed("jump")   True only on FIRST frame key goes down
#   Input.held("left")           True EVERY frame key is held
#   Input.just_released("jump")  True only on frame key is released
#
# VIRTUAL BUTTONS (on-screen touch buttons):
#   Input.add_button("jump", x=580, y=1260, size=100, label="A")
#   -- put in on_enter --
#   Input.held("jump")           works same as keyboard after that
#   Input.draw_ui(screen)        draws the buttons -- put at end of draw
#
# JOYSTICK (virtual analog stick):
#   Input.add_joystick(x=150, y=1280, radius=100)  -- put in on_enter
#   ax, ay = Input.joystick_axis()   returns -1.0 to 1.0 floats
#   Input.draw_ui(screen)            draws joystick too
# ===========================================================================

class Part3_Input(Scene):

    def on_enter(self):
        # Map keys — do this once in on_enter
        Input.map("jump", "space")
        Input.map("left", "left")
        Input.map("right", "right")

        # Add virtual buttons — do this once in on_enter
        Input.add_button("left",  x=40,  y=1260, size=100, label="◀")
        Input.add_button("right", x=180, y=1260, size=100, label="▶")
        Input.add_button("jump",  x=580, y=1260, size=100, label="▲")

        # Add joystick — do this once in on_enter
        # Input.add_joystick(x=150, y=1280, radius=100)

        self.x = 360.0
        self.msg = "Press buttons!"

    def update(self, dt):
        Input.update()  # always first

        if Input.held("left"):
            self.x -= 300 * dt
            self.msg = "Moving left"
        elif Input.held("right"):
            self.x += 300 * dt
            self.msg = "Moving right"
        else:
            self.msg = "Press buttons!"

        if Input.just_pressed("jump"):
            self.msg = "JUMPED!"

        if Input.tapped():
            self.msg = "Tapped screen!"

    def draw(self, screen):
        screen.fill((30, 30, 50))

        pygame.draw.circle(screen, (100, 200, 255),
                           (int(self.x), 730), 40)

        font = Assets.get_font("default", 32)
        txt  = font.render(self.msg, True, (255,255,255))
        screen.blit(txt, txt.get_rect(center=(360, 200)))

        Input.draw_ui(screen)  # always last in draw

Game(title="Part 3", fps=60).run(Part3_Input)




# ===========================================================================
# PART 4 — ENTITIES AND COMPONENTS
# ===========================================================================
#
# An Entity is a game object (player, enemy, coin, bullet...).
# Components give it data (position, speed, health...).
# You build entities by chaining .add() calls.
#
# WHERE:
#   Create entities in on_enter().
#   Get components in update() or draw() to read/change values.
#
# COMPONENTS YOU'LL USE MOST:
#   Transform(x, y)           position — EVERY entity needs this
#   Velocity(vx, vy)          speed — needed for moving entities
#   Health(amount)            hp — needed for damageable entities
#   Collider(w, h)            box collision shape
#   Collider(radius=r)        circle collision shape
#
# HOW TO GET A COMPONENT:
#   t = entity.get(Transform)    returns the component, or None
#   t.x, t.y                     read position
#   t.x = 100                    change position
#   t.set_pos(x, y)              set both at once
#   t.move(dx, dy)               add to position
#
# THE FLUENT BUILDER (how to create entities):
#   player = (
#       Entity("player")         give it a tag name
#       .add(Transform(x, y))    attach position
#       .add(Velocity())         attach speed
#       .add(Health(100))        attach health
#   )
# ===========================================================================

class Part4_Entities(Scene):

    def on_enter(self):
        # Create player entity with components
        self.player = (
            Entity("player")
            .add(Transform(360, 730))   # position: center of screen
            .add(Velocity())             # starts with vx=0, vy=0
            .add(Health(100))            # starts with 100 hp
        )

        # Create a coin entity
        self.coin = (
            Entity("coin")
            .add(Transform(200, 400))
        )

        Input.add_button("damage", x=580, y=1260, size=100, label="HIT")

    def update(self, dt):
        Input.update()

        # Get components to use them
        t  = self.player.get(Transform)
        hp = self.player.get(Health)

        # Tap to move player to touch position
        if Input.tapped():
            pos = Input.touch_pos()
            if pos:
                t.set_pos(float(pos[0]), float(pos[1]))

        # Button to take damage
        if Input.just_pressed("damage"):
            hp.take_damage(10)     # won't work again for 0.5s

    def draw(self, screen):
        screen.fill((30, 30, 30))

        # Draw coin
        ct = self.coin.get(Transform)
        pygame.draw.circle(screen, (255, 220, 50),
                           (int(ct.x), int(ct.y)), 25)

        # Draw player — color shifts when low health
        t  = self.player.get(Transform)
        hp = self.player.get(Health)
        ratio = hp.hp / hp.max_hp
        color = (int(lerp(220, 100, ratio)),
                 int(lerp(60,  200, ratio)), 80)
        pygame.draw.rect(screen, color,
                         pygame.Rect(int(t.x)-25, int(t.y)-35, 50, 55),
                         border_radius=8)

        # Draw HP text
        font = Assets.get_font("default", 28)
        txt  = font.render(f"HP: {int(hp.hp)}", True, (255,255,255))
        screen.blit(txt, (20, 20))

        Input.draw_ui(screen)

# Game(title="Part 4", fps=60).run(Part4_Entities)




# ===========================================================================
# PART 5 — WORLD AND PHYSICS
# ===========================================================================
#
# World holds all your entities and runs systems automatically.
# PhysicsSystem adds gravity and moves entities using Velocity.
#
# WHERE:
#   Create World in on_enter().
#   Call world.update(dt) near the END of update().
#   Call world.draw(screen) in draw() after clearing screen.
#   Add systems BEFORE adding entities.
#   Add entities AFTER adding systems.
#
# IMPORTANT ORDER IN on_enter():
#   1. self.world = World()
#   2. self.world.add_system(PhysicsSystem())   <- systems first
#   3. self.player = Entity(...).add(...)
#   4. self.world.add(self.player)              <- entities after
#
# IMPORTANT ORDER IN update():
#   1. Input.update()           <- always first
#   2. ... your logic ...
#   3. self.world.update(dt)    <- always last
#
# IMPORTANT ORDER IN draw():
#   1. screen.fill(color)       <- always first
#   2. self.world.draw(screen)  <- draws all entities
#   3. ... your UI ...
#   4. Input.draw_ui(screen)    <- always last
#
# PHYSICS CONFIG (change these anytime):
#   Physics.gravity  = 980    pixels per second squared (default 980)
#   Physics.friction = 0.85   ground slowdown (0=stops, 1=no friction)
#   Physics.gravity  = 0      set to 0 for top-down games
# ===========================================================================

class Part5_Physics(Scene):

    def on_enter(self):
        # 1. Create world
        self.world = World()

        # 2. Add systems FIRST
        self.world.add_system(PhysicsSystem())

        # 3. Create entities
        self.ball = (
            Entity("ball")
            .add(Transform(360, 300))
            .add(Velocity())           # physics needs this
        )

        # 4. Add entities to world AFTER systems
        self.world.add(self.ball)

        Input.add_button("throw", x=580, y=1260, size=100, label="↑")

    def update(self, dt):
        Input.update()  # 1. always first

        vel = self.ball.get(Velocity)
        t   = self.ball.get(Transform)

        # Throw ball up
        if Input.just_pressed("throw"):
            vel.apply_impulse(0, -900)   # negative = up

        # Reset if falls off screen
        if t.y > 1500:
            t.set_pos(360, 300)
            vel.vy = 0
            vel.vx = 0

        self.world.update(dt)  # 2. always last — physics runs here

    def draw(self, screen):
        screen.fill((20, 20, 40))  # 1. clear first

        # Floor line
        pygame.draw.rect(screen, (80, 60, 40),
                         pygame.Rect(0, 1380, 720, 81))

        t = self.ball.get(Transform)
        pygame.draw.circle(screen, (255, 100, 100),
                           (int(t.x), int(t.y)), 35)

        Input.draw_ui(screen)  # last

# Game(title="Part 5", fps=60).run(Part5_Physics)




# ===========================================================================
# PART 6 — VIRTUAL MOVEMENT (Buttons + Joystick)
# ===========================================================================
#
# This part shows the two main ways to move a character on Android:
#
# WAY 1 — Virtual buttons (platformer style: left/right/jump)
# WAY 2 — Joystick (top-down style: move in any direction)
#
# Use WAY 1 for platformers.
# Use WAY 2 for top-down games (RPG, shooter, survival).
#
# For a platformer, Physics.gravity stays at default (980).
# For top-down, set Physics.gravity = 0 in on_enter().
# ===========================================================================

# --- WAY 1: Platformer with buttons ---
class Part6_Platformer(Scene):

    def on_enter(self):
        self.world = World()
        self.world.add_system(PhysicsSystem())

        self.player = (
            Entity("player")
            .add(Transform(360, 900))
            .add(Velocity())
        )
        self.world.add(self.player)

        # Platformer needs left/right/jump buttons
        Input.add_button("left",  x=40,  y=1260, size=100, label="◀")
        Input.add_button("right", x=180, y=1260, size=100, label="▶")
        Input.add_button("jump",  x=580, y=1260, size=100, label="▲")

    def update(self, dt):
        Input.update()

        vel = self.player.get(Velocity)
        t   = self.player.get(Transform)

        # Move left and right
        if Input.held("left"):
            vel.vx = -350
        elif Input.held("right"):
            vel.vx = 350
        else:
            vel.vx = 0   # stop when no button held

        # Jump — only on first frame pressed
        if Input.just_pressed("jump"):
            vel.apply_impulse(0, -750)

        # Simple floor — stop player at y=1200
        if t.y > 1200:
            t.y    = 1200
            vel.vy = 0

        # Keep player on screen horizontally
        t.x = clamp(t.x, 25, 695)

        self.world.update(dt)

    def draw(self, screen):
        screen.fill((30, 30, 60))

        # Floor
        pygame.draw.rect(screen, (80, 60, 40),
                         pygame.Rect(0, 1220, 720, 241))

        t = self.player.get(Transform)
        pygame.draw.rect(screen, (100, 200, 100),
                         pygame.Rect(int(t.x)-22, int(t.y)-38,
                                     44, 56), border_radius=6)

        Input.draw_ui(screen)

# Game(title="Platformer", fps=60).run(Part6_Platformer)


# --- WAY 2: Top-down with joystick ---
class Part6_TopDown(Scene):

    def on_enter(self):
        Physics.gravity = 0   # NO gravity for top-down

        self.world = World()
        self.world.add_system(PhysicsSystem())

        self.player = (
            Entity("player")
            .add(Transform(360, 730))
            .add(Velocity(max_speed=400))
        )
        self.world.add(self.player)

        # Joystick for top-down movement
        Input.add_joystick(x=150, y=1280, radius=100)

    def update(self, dt):
        Input.update()

        vel    = self.player.get(Velocity)
        ax, ay = Input.joystick_axis()   # -1.0 to 1.0

        vel.vx = ax * 400
        vel.vy = ay * 400

        # Keep player on screen
        t   = self.player.get(Transform)
        t.x = clamp(t.x, 30, 690)
        t.y = clamp(t.y, 30, 1380)

        self.world.update(dt)

    def draw(self, screen):
        screen.fill((20, 35, 20))

        t = self.player.get(Transform)
        pygame.draw.circle(screen, (100, 200, 255),
                           (int(t.x), int(t.y)), 30)

        Input.draw_ui(screen)

# Game(title="Top-down", fps=60).run(Part6_TopDown)




# ===========================================================================
# PART 7 — COLLISION
# ===========================================================================
#
# Collision needs THREE things:
#   1. Both entities must have a Collider component
#   2. CollisionSystem must be added to the world
#   3. Call world.collide_groups() to check and get a callback
#
# WHERE:
#   Add Collider in on_enter() when building entities.
#   Add CollisionSystem(self.world) in on_enter() BEFORE entities.
#   Call world.collide_groups() inside update() every frame.
#
# COLLIDER TYPES:
#   Collider(width, height)      box shape
#   Collider(radius=r)           circle shape
#   Collider(w, h, is_trigger=True)  detects but does NOT push
#
# HOW collide_groups WORKS:
#   world.collide_groups("groupA", "groupB", my_callback)
#   -- checks every entity in groupA against every entity in groupB
#   -- calls my_callback(entity_a, entity_b, normal) when they touch
#   -- normal = (nx, ny) direction of collision
#
# ADD ENTITY TO GROUP:
#   world.add(entity, group="coins")   <- second argument is group name
# ===========================================================================

class Part7_Collision(Scene):

    def on_enter(self):
        self.world = World()
        self.world.add_system(PhysicsSystem())
        self.world.add_system(CollisionSystem(self.world))  # add this too

        self.player = (
            Entity("player")
            .add(Transform(360, 900))
            .add(Velocity())
            .add(Collider(44, 56))        # box collider matching player size
        )
        self.world.add(self.player, group="player")  # add to "player" group

        # Coin with circle trigger
        self.coin = (
            Entity("coin")
            .add(Transform(360, 400))
            .add(Collider(radius=28, is_trigger=True))  # trigger = no push
        )
        self.world.add(self.coin, group="coins")   # add to "coins" group

        # Spike with box collider
        self.spike = (
            Entity("spike")
            .add(Transform(550, 1180))
            .add(Collider(50, 40))
        )
        self.world.add(self.spike, group="spikes")

        Input.add_button("left",  x=40,  y=1260, size=100, label="◀")
        Input.add_button("right", x=180, y=1260, size=100, label="▶")
        Input.add_button("jump",  x=580, y=1260, size=100, label="▲")

        self.coin_collected = False
        self.msg = "Collect the coin!"

        self.ui = UIManager()
        self.lbl = Label(self.msg, x=0, y=30,
                         anchor=Anchor.TOP_CENTER,
                         style=Style(font_size=30,
                                     text_color=(255,220,50)))
        self.ui.add(self.lbl)

    def _on_coin(self, player, coin, normal):
        # Called when player touches coin
        if not self.coin_collected:
            self.coin_collected = True
            coin.get(Transform).set_pos(-999, -999)  # hide coin
            self.lbl.set_text("Got it! Now avoid the spike!")
            Toast.show("+1 Coin!", duration=1.5)

    def _on_spike(self, player, spike, normal):
        # Called when player touches spike
        vel = player.get(Velocity)
        vel.apply_impulse(0, -500)   # bounce up
        Toast.show("Ouch!", duration=0.8)

    def update(self, dt):
        Input.update()

        vel = self.player.get(Velocity)
        t   = self.player.get(Transform)

        if Input.held("left"):
            vel.vx = -350
        elif Input.held("right"):
            vel.vx = 350
        else:
            vel.vx = 0

        if Input.just_pressed("jump"):
            vel.apply_impulse(0, -750)

        if t.y > 1200:
            t.y    = 1200
            vel.vy = 0

        # Check collisions every frame
        if not self.coin_collected:
            self.world.collide_groups("player", "coins",  self._on_coin)
        self.world.collide_groups("player", "spikes", self._on_spike)

        self.world.update(dt)
        self.ui.update(dt)

    def draw(self, screen):
        screen.fill((30, 30, 60))

        pygame.draw.rect(screen, (80, 60, 40),
                         pygame.Rect(0, 1220, 720, 241))

        # Coin
        if not self.coin_collected:
            ct = self.coin.get(Transform)
            pygame.draw.circle(screen, (255, 220, 50),
                               (int(ct.x), int(ct.y)), 28)

        # Spike triangle
        st = self.spike.get(Transform)
        sx, sy = int(st.x), int(st.y)
        pygame.draw.polygon(screen, (220, 80, 60),
                            [(sx-25,sy+20),(sx,sy-20),(sx+25,sy+20)])

        # Player
        t = self.player.get(Transform)
        pygame.draw.rect(screen, (100, 200, 100),
                         pygame.Rect(int(t.x)-22, int(t.y)-28,
                                     44, 56), border_radius=6)

        self.ui.draw(screen)
        Input.draw_ui(screen)

# Game(title="Part 7", fps=60).run(Part7_Collision)




# ===========================================================================
# PART 8 — UI WIDGETS
# ===========================================================================
#
# UI = buttons, labels, health bars, and other on-screen elements.
#
# WHERE:
#   Create UIManager in on_enter().
#   Create widgets and add them to UIManager in on_enter().
#   Call ui.update(dt) near end of update() AFTER world.update(dt).
#   Call ui.draw(screen) in draw() AFTER world.draw(screen).
#   Call Input.draw_ui(screen) LAST in draw().
#
# IMPORTANT ORDER IN on_enter():
#   self.ui   = UIManager()
#   self.lbl  = Label(...)
#   self.btn  = Button(...)
#   self.hbar = HealthBar(...)
#   self.ui.add(self.lbl)
#   self.ui.add(self.btn)
#   self.ui.add(self.hbar)
#
# WIDGETS:
#   Label       shows text
#   Button      tappable button with on_click callback
#   HealthBar   colored bar (green to red)
#   ProgressBar plain colored bar
#   Slider      draggable value control
#   Toggle      on/off switch
#   Toast       temporary popup message (no add needed)
#   Modal       blocking yes/no dialog (no add needed)
#
# ANCHOR — where on screen a widget is pinned:
#   Anchor.TOP_LEFT    Anchor.TOP_CENTER    Anchor.TOP_RIGHT
#   Anchor.MID_LEFT    Anchor.CENTER        Anchor.MID_RIGHT
#   Anchor.BOT_LEFT    Anchor.BOT_CENTER    Anchor.BOT_RIGHT
#
# STYLE — change how a widget looks:
#   Style(font_size=30, text_color=(255,0,0), bg=(50,50,50), radius=12)
# ===========================================================================

class Part8_UI(Scene):

    def on_enter(self):
        self.health = 100.0

        # 1. Create UIManager
        self.ui = UIManager()

        # 2. Create widgets
        self.title = Label(
            "UI Demo",
            x=0, y=40,
            anchor=Anchor.TOP_CENTER,          # pinned to top center
            style=Style(font_size=44,
                        text_color=(255,220,50))
        )

        self.hbar = HealthBar(
            x=60, y=120,
            w=600, h=28,
            value=1.0                          # 0.0 to 1.0
        )

        self.info = Label(
            "HP: 100",
            x=0, y=168,
            anchor=Anchor.TOP_CENTER,
            style=Style(font_size=26)
        )

        self.dmg_btn = Button(
            "Take Damage",
            x=0, y=600,
            w=320, h=80,
            anchor=Anchor.TOP_CENTER,
            on_click=self._take_damage,       # function to call on tap
            style=Style(font_size=28,
                        radius=16,
                        bg=(160, 50, 50))
        )

        self.heal_btn = Button(
            "Heal",
            x=0, y=700,
            w=320, h=80,
            anchor=Anchor.TOP_CENTER,
            on_click=self._heal,
            style=Style(font_size=28,
                        radius=16,
                        bg=(50, 140, 50))
        )

        self.reset_btn = Button(
            "Reset",
            x=0, y=800,
            w=320, h=80,
            anchor=Anchor.TOP_CENTER,
            on_click=self._reset,
            style=Style(font_size=28, radius=16)
        )

        # 3. Add widgets to UIManager
        self.ui.add(self.title)
        self.ui.add(self.hbar)
        self.ui.add(self.info)
        self.ui.add(self.dmg_btn)
        self.ui.add(self.heal_btn)
        self.ui.add(self.reset_btn)

    def _take_damage(self):
        self.health = max(0, self.health - 15)
        Toast.show("-15 HP", duration=1.0)     # no add() needed for Toast
        if self.health <= 0:
            Modal.show(                         # no add() needed for Modal
                title   = "You Died",
                message = "Try again?",
                options = ["Yes", "No"],
                on_choice = self._on_modal
            )

    def _heal(self):
        self.health = min(100, self.health + 20)
        Toast.show("+20 HP", duration=1.0)

    def _reset(self):
        self.health = 100.0

    def _on_modal(self, choice):
        if choice == "Yes":
            self.health = 100.0
        else:
            Toast.show("Ok, staying dead.", duration=2.0)

    def update(self, dt):
        Input.update()

        # Update health bar value
        self.hbar.set_value(self.health / 100.0)
        self.info.set_text(f"HP: {int(self.health)}")

        self.ui.update(dt)  # always after your logic

    def draw(self, screen):
        screen.fill((25, 25, 40))
        self.ui.draw(screen)   # draws all widgets + toast + modal
        # Note: no Input.draw_ui needed here since no virtual buttons

# Game(title="Part 8", fps=60).run(Part8_UI)




# ===========================================================================
# PART 9 — MULTIPLE SCENES
# ===========================================================================
#
# A game usually has several screens:
#   Menu → Game → Game Over → back to Menu
#
# Each screen is its own Scene class.
# self.sm is the Scene Manager — it switches between scenes.
#
# WHERE:
#   self.sm is automatically available inside any Scene.
#   Call self.sm.switch(SceneName) to go to a different scene.
#   Call self.sm.push(SceneName) to go to a scene and keep the current one.
#   Call self.sm.pop() to go back to the previous scene.
#
# PASSING DATA BETWEEN SCENES:
#   Define __init__ on the target scene to receive data:
#   class GameOverScene(Scene):
#       def __init__(self, score=0):
#           super().__init__()   <- always call this!
#           self.score = score
#   Then switch with:
#   self.sm.switch(GameOverScene, score=99)
# ===========================================================================

class Part9_Menu(Scene):

    def on_enter(self):
        self.ui = UIManager()
        self.ui.add(Label("MAIN MENU",
                          x=0, y=500,
                          anchor=Anchor.TOP_CENTER,
                          style=Style(font_size=52,
                                      text_color=(255,220,50))))
        self.ui.add(Button("Play",
                           x=0, y=660,
                           w=300, h=80,
                           anchor=Anchor.TOP_CENTER,
                           on_click=lambda: self.sm.switch(Part9_Game),
                           style=Style(font_size=32,
                                       radius=18,
                                       bg=(50,150,50))))

    def update(self, dt):
        Input.update()
        self.ui.update(dt)

    def draw(self, screen):
        screen.fill((20, 20, 40))
        self.ui.draw(screen)


class Part9_Game(Scene):

    def on_enter(self):
        self.score = 0
        self.time  = 0.0

        self.world = World()
        self.world.add_system(PhysicsSystem())

        self.player = (
            Entity("player")
            .add(Transform(360, 900))
            .add(Velocity())
        )
        self.world.add(self.player)

        Input.add_button("left",  x=40,  y=1260, size=100, label="◀")
        Input.add_button("right", x=180, y=1260, size=100, label="▶")
        Input.add_button("jump",  x=580, y=1260, size=100, label="▲")

        self.ui = UIManager()
        self.score_lbl = Label("Score: 0",
                               x=0, y=30,
                               anchor=Anchor.TOP_CENTER,
                               style=Style(font_size=36,
                                           text_color=(255,220,50)))
        self.ui.add(self.score_lbl)

    def update(self, dt):
        Input.update()

        vel = self.player.get(Velocity)
        t   = self.player.get(Transform)

        if Input.held("left"):    vel.vx = -350
        elif Input.held("right"): vel.vx =  350
        else:                     vel.vx =  0

        if Input.just_pressed("jump"):
            vel.apply_impulse(0, -750)

        if t.y > 1200:
            t.y = 1200; vel.vy = 0

        t.x = clamp(t.x, 25, 695)

        self.time  += dt
        self.score  = int(self.time * 10)
        self.score_lbl.set_text(f"Score: {self.score}")

        # Fall off screen = game over
        if t.y > 1400:
            # Switch to game over — pass the score
            self.sm.switch(Part9_GameOver, score=self.score)

        self.world.update(dt)
        self.ui.update(dt)

    def draw(self, screen):
        screen.fill((30, 30, 60))
        pygame.draw.rect(screen, (80,60,40),
                         pygame.Rect(0,1220,720,241))
        t = self.player.get(Transform)
        pygame.draw.rect(screen, (100,200,100),
                         pygame.Rect(int(t.x)-22,int(t.y)-28,
                                     44,56), border_radius=6)
        self.ui.draw(screen)
        Input.draw_ui(screen)


class Part9_GameOver(Scene):

    def __init__(self, score=0):
        super().__init__()      # ALWAYS call this first
        self.score = score

    def on_enter(self):
        self.ui = UIManager()
        self.ui.add(Label("GAME OVER",
                          x=0, y=450,
                          anchor=Anchor.TOP_CENTER,
                          style=Style(font_size=52,
                                      text_color=(220,60,60))))
        self.ui.add(Label(f"Score: {self.score}",
                          x=0, y=560,
                          anchor=Anchor.TOP_CENTER,
                          style=Style(font_size=36)))
        self.ui.add(Button("Play Again",
                           x=0, y=680,
                           w=300, h=80,
                           anchor=Anchor.TOP_CENTER,
                           on_click=lambda: self.sm.switch(Part9_Game),
                           style=Style(font_size=30,
                                       radius=18,
                                       bg=(50,150,50))))
        self.ui.add(Button("Menu",
                           x=0, y=780,
                           w=300, h=80,
                           anchor=Anchor.TOP_CENTER,
                           on_click=lambda: self.sm.switch(Part9_Menu),
                           style=Style(font_size=30, radius=18)))

    def update(self, dt):
        Input.update()
        self.ui.update(dt)

    def draw(self, screen):
        screen.fill((20, 20, 40))
        self.ui.draw(screen)

# Game(title="Part 9", fps=60).run(Part9_Menu)




# ===========================================================================
# PART 10 — SAVE AND LOAD
# ===========================================================================
#
# Save stores data to a JSON file on disk.
# Load reads it back. Data survives closing and reopening the app.
#
# WHERE:
#   Save.write() anywhere — usually in game over or on level complete.
#   Save.read()  usually in on_enter() of Menu or Game scene.
#
# HOW:
#   Save.write(slot, data_dict)   slot is a number (0, 1, 2...)
#   Save.read(slot)               returns dict or None if no save
#   Save.exists(slot)             True / False
#   Save.delete(slot)             delete a save
#
# IMPORTANT:
#   Save.read() can return None if no save exists yet.
#   Always use:   data = Save.read(0) or {}
#   Then:         best = data.get("best", 0)
#   The "or {}"  means use empty dict if no save exists.
#   The .get("best", 0) means use 0 if "best" key is missing.
# ===========================================================================

class Part10_Save(Scene):

    def on_enter(self):
        # Load saved data — use "or {}" in case no save exists yet
        data       = Save.read(0) or {}
        self.best  = data.get("best",  0)    # default 0
        self.coins = data.get("coins", 0)    # default 0

        self.current_score = 0

        self.ui = UIManager()

        self.best_lbl  = Label(f"Best:  {self.best}",
                               x=0, y=300,
                               anchor=Anchor.TOP_CENTER,
                               style=Style(font_size=36,
                                           text_color=(255,220,50)))
        self.coins_lbl = Label(f"Coins: {self.coins}",
                               x=0, y=360,
                               anchor=Anchor.TOP_CENTER,
                               style=Style(font_size=32))
        self.score_lbl = Label("Current: 0",
                               x=0, y=430,
                               anchor=Anchor.TOP_CENTER,
                               style=Style(font_size=28))

        self.ui.add(self.best_lbl)
        self.ui.add(self.coins_lbl)
        self.ui.add(self.score_lbl)

        self.ui.add(Button("+10 Score",
                           x=0, y=600,
                           w=300, h=75,
                           anchor=Anchor.TOP_CENTER,
                           on_click=self._add_score,
                           style=Style(font_size=28,
                                       radius=14,
                                       bg=(50,100,180))))

        self.ui.add(Button("+1 Coin",
                           x=0, y=695,
                           w=300, h=75,
                           anchor=Anchor.TOP_CENTER,
                           on_click=self._add_coin,
                           style=Style(font_size=28,
                                       radius=14,
                                       bg=(180,150,20))))

        self.ui.add(Button("Save",
                           x=0, y=790,
                           w=300, h=75,
                           anchor=Anchor.TOP_CENTER,
                           on_click=self._save,
                           style=Style(font_size=28,
                                       radius=14,
                                       bg=(50,150,50))))

        self.ui.add(Button("Reset Save",
                           x=0, y=885,
                           w=300, h=75,
                           anchor=Anchor.TOP_CENTER,
                           on_click=self._reset,
                           style=Style(font_size=24,
                                       radius=14,
                                       bg=(140,40,40))))

    def _add_score(self):
        self.current_score += 10
        if self.current_score > self.best:
            self.best = self.current_score
        self.score_lbl.set_text(f"Current: {self.current_score}")
        self.best_lbl.set_text(f"Best:  {self.best}")

    def _add_coin(self):
        self.coins += 1
        self.coins_lbl.set_text(f"Coins: {self.coins}")

    def _save(self):
        Save.write(0, {
            "best":  self.best,
            "coins": self.coins,
        })
        Toast.show("Saved!", duration=1.5)

    def _reset(self):
        Save.delete(0)
        self.best  = 0
        self.coins = 0
        self.current_score = 0
        self.best_lbl.set_text("Best:  0")
        self.coins_lbl.set_text("Coins: 0")
        self.score_lbl.set_text("Current: 0")
        Toast.show("Save deleted.", duration=1.5)

    def update(self, dt):
        Input.update()
        self.ui.update(dt)

    def draw(self, screen):
        screen.fill((20, 20, 35))

        font = Assets.get_font("default", 38)
        title = font.render("Save System", True, (255,255,255))
        screen.blit(title, title.get_rect(center=(360, 160)))

        sub = Assets.get_font("default", 22)
        hint = sub.render("Data survives closing the app!",
                          True, (160,160,160))
        screen.blit(hint, hint.get_rect(center=(360, 220)))

        self.ui.draw(screen)

# Game(title="Part 10", fps=60).run(Part10_Save)




# ===========================================================================
# PART 11 — CAMERA
# ===========================================================================
#
# Camera lets you have a world bigger than the screen.
# Only what's inside the camera viewport is visible.
#
# WHERE:
#   Create Camera in on_enter().
#   Call cam.follow(entity) in on_enter() to set what to follow.
#   Call cam.update(dt) in update() BEFORE world.update(dt).
#   Call cam.draw_effects(screen) in draw() early.
#   Use cam.apply_pos(x, y) when drawing ANYTHING in world-space.
#
# KEY METHODS:
#   cam.follow(entity)               smooth follow an entity
#   cam.follow_speed = 6.0           how snappy (higher = faster)
#   cam.clamp(pygame.Rect(...))      stop camera going outside world
#   cam.update(dt)                   move camera — call in update
#   cam.apply_pos(wx, wy)            world pos → screen pos for drawing
#   cam.apply(rect)                  world rect → screen rect for drawing
#   cam.screen_to_world(sx, sy)      screen tap → world position
#   cam.shake(intensity, duration)   screen shake effect
#   cam.flash(color, duration)       screen flash effect
#   cam.draw_effects(screen)         draw parallax + flash effects
# ===========================================================================

class Part11_Camera(Scene):

    def on_enter(self):
        WORLD_W = 2160   # world is 3 screens wide

        self.world = World()
        self.world.add_system(PhysicsSystem())

        self.player = (
            Entity("player")
            .add(Transform(200, 900))
            .add(Velocity())
        )
        self.world.add(self.player)

        # Create camera
        self.cam = Camera(
            viewport=pygame.Rect(0, 0, 720, 1461)
        )
        self.cam.follow(self.player)           # follow player
        self.cam.follow_speed = 5.0            # smooth follow speed
        self.cam.clamp(pygame.Rect(0, 0, WORLD_W, 1461))  # world bounds

        # Platforms in world-space
        self.platforms = [
            pygame.Rect(0,    1200, 800,  40),
            pygame.Rect(900,  1000, 300,  30),
            pygame.Rect(1300, 800,  300,  30),
            pygame.Rect(1800, 1000, 360,  30),
        ]

        # Stars in world-space
        self.stars = [(i*113 % WORLD_W, i*79 % 800)
                      for i in range(40)]

        Input.add_button("left",  x=40,  y=1260, size=100, label="◀")
        Input.add_button("right", x=180, y=1260, size=100, label="▶")
        Input.add_button("jump",  x=580, y=1260, size=100, label="▲")
        Input.add_button("shake", x=580, y=1140, size=70,  label="💥")

    def update(self, dt):
        Input.update()

        vel = self.player.get(Velocity)
        t   = self.player.get(Transform)

        if Input.held("left"):    vel.vx = -380
        elif Input.held("right"): vel.vx =  380
        else:                     vel.vx =  0

        if Input.just_pressed("jump"):
            vel.apply_impulse(0, -750)

        if Input.just_pressed("shake"):
            self.cam.shake(intensity=10, duration=0.4)

        # Platform collision
        t.y   += vel.vy * dt
        vel.vy = min(vel.vy + Physics.gravity * dt,
                     Physics.max_fall)
        t.x   += vel.vx * dt

        pr = pygame.Rect(int(t.x)-22, int(t.y)-28, 44, 56)
        for plat in self.platforms:
            if pr.colliderect(plat) and vel.vy >= 0:
                t.y    = float(plat.top - 28)
                vel.vy = 0

        t.x = clamp(t.x, 22, 2138)

        # Camera must update BEFORE world.update
        self.cam.update(dt)
        self.world.update(dt)

    def draw(self, screen):
        screen.fill((20, 20, 45))

        # Draw effects first (parallax, flash)
        self.cam.draw_effects(screen)

        # Draw stars — convert world pos to screen pos
        for sx, sy in self.stars:
            scx, scy = self.cam.apply_pos(sx, sy)
            if -5 < scx < 725:   # only draw visible ones
                pygame.draw.circle(screen, (200,200,200),
                                   (int(scx), int(scy)), 2)

        # Draw platforms — use cam.apply() on rects
        for plat in self.platforms:
            sr = self.cam.apply(plat)
            if -50 < sr.x < 770:
                pygame.draw.rect(screen, (80,60,40), sr)
                pygame.draw.rect(screen, (100,200,80),
                                 pygame.Rect(sr.x,sr.y,sr.w,8))

        # Draw player — use cam.apply_pos() on position
        t   = self.player.get(Transform)
        px, py = self.cam.apply_pos(t.x, t.y)
        pygame.draw.rect(screen, (100,200,100),
                         pygame.Rect(int(px)-22,int(py)-28,
                                     44,56), border_radius=6)

        Input.draw_ui(screen)

# Game(title="Part 11", fps=60).run(Part11_Camera)




# ===========================================================================
# PART 12 — COMPLETE GAME TEMPLATE
# ===========================================================================
#
# This is the full template for a real game.
# Every section is labelled so you know exactly what goes where.
# Copy this, rename things, and build your game inside it.
# ===========================================================================

class Template_Menu(Scene):

    def on_enter(self):
        # Load saved data
        data = Save.read(0) or {}
        best = data.get("best", 0)

        self.ui = UIManager()
        self.ui.add(Label("MY GAME",
                          x=0, y=440,
                          anchor=Anchor.TOP_CENTER,
                          style=Style(font_size=60,
                                      text_color=(255,220,50))))
        self.ui.add(Label(f"Best: {best}",
                          x=0, y=540,
                          anchor=Anchor.TOP_CENTER,
                          style=Style(font_size=30)))
        self.ui.add(Button("PLAY",
                           x=0, y=680,
                           w=300, h=90,
                           anchor=Anchor.TOP_CENTER,
                           on_click=lambda: self.sm.switch(Template_Game),
                           style=Style(font_size=36,
                                       radius=20,
                                       bg=(50,150,50))))

    def update(self, dt):
        Input.update()
        self.ui.update(dt)

    def draw(self, screen):
        screen.fill((20, 20, 40))
        self.ui.draw(screen)


class Template_Game(Scene):

    def on_enter(self):
        # ---- PHYSICS SETUP ----
        Physics.gravity = 980   # use 0 for top-down

        # ---- WORLD + SYSTEMS ----
        self.world = World()
        self.world.add_system(PhysicsSystem())
        self.world.add_system(CollisionSystem(self.world))

        # ---- ENTITIES ----
        self.player = (
            Entity("player")
            .add(Transform(360, 900))
            .add(Velocity())
            .add(Health(100))
            .add(Collider(44, 56))
        )
        self.world.add(self.player, group="player")

        # ---- CAMERA (optional, remove if not needed) ----
        self.cam = Camera(viewport=pygame.Rect(0,0,720,1461))
        self.cam.follow(self.player)

        # ---- INPUT ----
        Input.add_button("left",  x=40,  y=1260, size=100, label="◀")
        Input.add_button("right", x=180, y=1260, size=100, label="▶")
        Input.add_button("jump",  x=580, y=1260, size=100, label="▲")

        # ---- UI ----
        self.ui    = UIManager()
        self.hbar  = HealthBar(x=60, y=40, w=400, h=22, value=1.0)
        self.score_lbl = Label("0",
                               x=0, y=40,
                               anchor=Anchor.TOP_CENTER,
                               style=Style(font_size=40,
                                           text_color=(255,220,50)))
        self.ui.add(self.hbar)
        self.ui.add(self.score_lbl)

        # ---- GAME STATE ----
        self.score = 0
        self.time  = 0.0

    def update(self, dt):
        Input.update()  # ALWAYS FIRST

        # ---- READ COMPONENTS ----
        vel = self.player.get(Velocity)
        t   = self.player.get(Transform)
        hp  = self.player.get(Health)

        # ---- MOVEMENT ----
        if Input.held("left"):    vel.vx = -350
        elif Input.held("right"): vel.vx =  350
        else:                     vel.vx =  0

        if Input.just_pressed("jump"):
            vel.apply_impulse(0, -750)

        # ---- FLOOR ----
        if t.y > 1200:
            t.y = 1200; vel.vy = 0

        t.x = clamp(t.x, 25, 695)

        # ---- SCORE ----
        self.time  += dt
        self.score  = int(self.time * 10)
        self.score_lbl.set_text(str(self.score))
        self.hbar.set_value(hp.hp / hp.max_hp)

        # ---- DEATH CHECK ----
        if hp.is_dead():
            self.sm.switch(Template_GameOver, score=self.score)

        # ---- ALWAYS AT END ----
        self.cam.update(dt)
        self.world.update(dt)
        self.ui.update(dt)

    def draw(self, screen):
        screen.fill((30, 30, 60))  # ALWAYS FIRST

        # ---- WORLD DRAWING ----
        pygame.draw.rect(screen, (80,60,40),
                         pygame.Rect(0,1220,720,241))

        t  = self.player.get(Transform)
        px, py = self.cam.apply_pos(t.x, t.y)
        pygame.draw.rect(screen, (100,200,100),
                         pygame.Rect(int(px)-22,int(py)-28,
                                     44,56), border_radius=6)

        # ---- CAMERA EFFECTS ----
        self.cam.draw_effects(screen)

        # ---- UI ALWAYS AFTER WORLD ----
        self.ui.draw(screen)

        # ---- INPUT UI ALWAYS LAST ----
        Input.draw_ui(screen)


class Template_GameOver(Scene):

    def __init__(self, score=0):
        super().__init__()   # ALWAYS call this
        self.score = score

    def on_enter(self):
        # Save best score
        data = Save.read(0) or {}
        best = data.get("best", 0)
        if self.score > best:
            best = self.score
            Save.write(0, {"best": best})
            Toast.show("New Best!", duration=2.0)

        self.ui = UIManager()
        self.ui.add(Label("GAME OVER",
                          x=0, y=440,
                          anchor=Anchor.TOP_CENTER,
                          style=Style(font_size=52,
                                      text_color=(220,60,60))))
        self.ui.add(Label(f"Score: {self.score}",
                          x=0, y=550,
                          anchor=Anchor.TOP_CENTER,
                          style=Style(font_size=36)))
        self.ui.add(Label(f"Best:  {best}",
                          x=0, y=614,
                          anchor=Anchor.TOP_CENTER,
                          style=Style(font_size=30,
                                      text_color=(255,220,50))))
        self.ui.add(Button("Play Again",
                           x=0, y=740,
                           w=300, h=80,
                           anchor=Anchor.TOP_CENTER,
                           on_click=lambda: self.sm.switch(Template_Game),
                           style=Style(font_size=30,
                                       radius=18,
                                       bg=(50,150,50))))
        self.ui.add(Button("Menu",
                           x=0, y=840,
                           w=300, h=80,
                           anchor=Anchor.TOP_CENTER,
                           on_click=lambda: self.sm.switch(Template_Menu),
                           style=Style(font_size=30, radius=18)))

    def update(self, dt):
        Input.update()
        self.ui.update(dt)

    def draw(self, screen):
        screen.fill((20, 20, 40))
        self.ui.draw(screen)


# TO RUN THE TEMPLATE:
Game(title="My Game", fps=60).run(Template_Menu)




# ===========================================================================
# QUICK REFERENCE — WHERE DOES EVERYTHING GO?
# ===========================================================================
#
#  on_enter() — runs ONCE when scene starts
#  ├── Physics.gravity = ...
#  ├── self.world = World()
#  ├── self.world.add_system(PhysicsSystem())
#  ├── self.world.add_system(CollisionSystem(self.world))
#  ├── self.player = Entity(...).add(...).add(...)
#  ├── self.world.add(self.player, group="player")
#  ├── self.cam = Camera(viewport=...)
#  ├── self.cam.follow(self.player)
#  ├── Input.map("jump", "space")
#  ├── Input.add_button("jump", ...)
#  ├── Input.add_joystick(...)
#  ├── self.ui = UIManager()
#  ├── self.lbl = Label(...)
#  ├── self.ui.add(self.lbl)
#  └── self.score = 0
#
#  update(dt) — runs EVERY FRAME
#  ├── Input.update()              ← ALWAYS FIRST
#  ├── vel = entity.get(Velocity)
#  ├── t   = entity.get(Transform)
#  ├── hp  = entity.get(Health)
#  ├── ... your game logic ...
#  ├── world.collide_groups(...)
#  ├── self.cam.update(dt)         ← before world.update
#  ├── self.world.update(dt)       ← near end
#  └── self.ui.update(dt)          ← near end
#
#  draw(screen) — runs EVERY FRAME after update
#  ├── screen.fill(color)          ← ALWAYS FIRST
#  ├── self.cam.draw_effects(screen)
#  ├── ... pygame.draw.xxx() ...
#  ├── self.world.draw(screen)
#  ├── self.ui.draw(screen)        ← after world
#  └── Input.draw_ui(screen)       ← ALWAYS LAST
#
# ===========================================================================
