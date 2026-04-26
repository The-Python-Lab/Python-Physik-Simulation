# 🎮 PyMunk Physics Sandbox

A real-time 2D physics sandbox built with **Pymunk** and **Pygame**. Spawn objects, trigger explosions, and interact with a fully simulated physics world — all at 60 FPS.

---

## ✨ Features

- **Rigid body physics** — boxes and balls with realistic mass, friction, and elasticity
- **Pendulum simulation** — a constrained body swinging on a pivot joint
- **Mouse interaction** — grab and drag any dynamic object in the scene
- **Explosion system** — impulse-based radial explosion affecting all nearby bodies
- **Live HUD** — real-time FPS counter and object count overlay
- **Arena boundaries** — walls and floor keep everything contained

---

## 🕹️ Controls

| Input | Action |
|---|---|
| **Left Click + Drag** | Grab and move an object |
| **Right Click** | Spawn a new box at cursor |
| **Spacebar** | Trigger explosion at cursor position |
| **Close Window** | Quit |

---

## 📦 Requirements

- Python 3.8+
- [Pygame](https://www.pygame.org/) `>= 2.0`
- [Pymunk](http://www.pymunk.org/) `>= 6.0`

Install dependencies:

```bash
pip install pygame pymunk
```

---

## 🚀 Getting Started

```bash
git clone https://github.com/your-username/pymunk-sandbox.git
cd pymunk-sandbox
python main.py
```

---

## 🏗️ Project Structure

```
pymunk-sandbox/
└── main.py          # All simulation logic, rendering, and input handling
```

---

## ⚙️ Configuration

Key parameters can be tweaked directly in `main.py`:

| Parameter | Location | Default | Description |
|---|---|---|---|
| Window size | `pygame.display.set_mode` | `1000 × 700` | Screen resolution |
| Gravity | `space.gravity` | `900` | Downward pull strength |
| Damping | `space.damping` | `0.9` | Global velocity damping |
| Explosion radius | `trigger_pure_physics_explosion` | `200` | Blast radius in pixels |
| Explosion strength | `trigger_pure_physics_explosion` | `5000` | Impulse force applied |
| Box friction | `create_box` | `0.6` | Surface friction of boxes |
| Ball elasticity | `create_ball` | `0.8` | Bounciness of balls |

---

## 🔭 How It Works

### Physics Engine
The simulation uses **Pymunk** (a Python wrapper around Chipmunk2D) to handle all physics calculations — collision detection, impulse resolution, and joint constraints run at a fixed timestep of `1/60s` per frame.

### Explosion Mechanic
The explosion applies a scaled impulse to every dynamic body within a given radius. The force falls off linearly with distance, so objects closer to the epicenter get a stronger kick.

### Mouse Interaction
A `KINEMATIC` mouse body is used as an anchor. When you click an object, a `PivotJoint` is created between the mouse body and the target, making it follow the cursor while still obeying physics constraints.

---

## 📄 License

MIT License — feel free to use, modify, and distribute.
