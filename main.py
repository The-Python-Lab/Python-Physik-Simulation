import pymunk
import pymunk.pygame_util
import pygame
import sys

# 1. Pygame Initialization
pygame.init()
screen = pygame.display.set_mode((1000, 700))
clock = pygame.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(screen)

# --- PART 7: RENDER SETTINGS ---
font = pygame.font.SysFont('Arial', 18, bold=True)
draw_options.flags = pymunk.pygame_util.DrawOptions.DRAW_SHAPES

# 2. Pymunk Space Setup
space = pymunk.Space()
space.gravity = (0, 900)
space.damping = 0.9

# --- FUNCTIONS FOR ARENA & OBJECTS ---
def create_boundaries(space, width, height):
    static_body = space.static_body
    lines = [
        pymunk.Segment(static_body, (0, height), (width, height), 5),
        pymunk.Segment(static_body, (0, 0), (0, height), 5),
        pymunk.Segment(static_body, (width, 0), (width, height), 5)
    ]
    for line in lines:
        line.elasticity = 0.5
        line.friction = 0.5
    space.add(*lines)

def create_box(space, pos, size=(20, 20)):
    mass = 1
    moment = pymunk.moment_for_box(mass, size)
    body = pymunk.Body(mass, moment)
    body.position = pos
    shape = pymunk.Poly.create_box(body, size)
    shape.friction = 0.6
    shape.elasticity = 0.3
    space.add(body, shape)
    return shape

def create_ball(space, pos):
    mass = 1
    radius = 10
    moment = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, moment)
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.friction = 0.4
    shape.elasticity = 0.8
    space.add(body, shape)
    return shape

def trigger_pure_physics_explosion(space, epicenter_pos, radius=200, strength=5000):
    for shape in space.shapes:
        if shape.body.body_type == pymunk.Body.DYNAMIC:
            body = shape.body
            vec = body.position - epicenter_pos
            distance = vec.length
            if distance < radius and distance > 0:
                distance_factor = (radius - distance) / radius
                impulse_vec = vec.normalized() * (strength * distance_factor)
                body.apply_impulse_at_world_point(impulse_vec, body.position)

# --- PART 7: HUD FUNCTION ---
def draw_hud(screen, space):
    count = len(space.shapes)
    fps = int(clock.get_fps())
    txt = f"FPS: {fps} | Objects: {count}"
    img = font.render(txt, True, (255, 255, 255))
    screen.blit(img, (20, 20))

# --- WORLD INITIALIZATION ---
create_boundaries(space, 1000, 700)

# Pendulum Setup
pivot_anchor = pymunk.Body(body_type=pymunk.Body.STATIC)
pivot_anchor.position = (300, 300)
pendulum_body = pymunk.Body(5, pymunk.moment_for_circle(5, 0, 20))
pendulum_body.position = (400, 300)
pendulum_shape = pymunk.Circle(pendulum_body, 20)
joint = pymunk.PivotJoint(pivot_anchor, pendulum_body, (300, 300))
space.add(pendulum_body, pendulum_shape, joint)

# Mouse Interaction Setup
mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
mouse_joint = None

# Spawn initial wall of boxes and balls
for x in range(50):
    for y in range(18):
        create_box(space, (700 + x * 22, 650 - y * 22))

for x in range(10):
    for y in range(18):
        create_ball(space, (400 + x * 22, 650 - y * 22))

# 3. Main Loop
while True:
    mouse_pos = pygame.mouse.get_pos()
    mouse_body.position = mouse_pos
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # LEFT CLICK: Grab
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            hit = space.point_query_nearest(mouse_pos, 0, pymunk.ShapeFilter())
            if hit and hit.shape.body.body_type == pymunk.Body.DYNAMIC:
                anchor = hit.shape.body.world_to_local(mouse_pos)
                mouse_joint = pymunk.PivotJoint(mouse_body, hit.shape.body, (0,0), anchor)
                mouse_joint.max_force = 50000
                space.add(mouse_joint)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if mouse_joint:
                space.remove(mouse_joint)
                mouse_joint = None

        # RIGHT CLICK: Spawn Box
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            create_box(space, mouse_pos)

        # SPACE: Explosion
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            trigger_pure_physics_explosion(space, mouse_pos)

    # Rendering & Physics
    screen.fill((30, 30, 30))
    
    dt = 1.0 / 60.0
    space.step(dt)
    
    space.debug_draw(draw_options)
    
    # --- PART 7: CALL HUD ---
    draw_hud(screen, space)
    
    pygame.display.flip()
    clock.tick(60)
