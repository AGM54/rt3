import pygame
from pygame.locals import *
from rt import RayTracer
from figures import *
from lights import *
from materials import *

width = 800
height = 800

pygame.init()
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)

raytracer = RayTracer(screen)
raytracer.envMap = pygame.image.load("textures/blanco.jpg")
raytracer.rtClearColor(0.25, 0.25, 0.25)

brick = Material(diffuse=(1, 0.4, 0.4), spec=8, Ks=0.01,matType=REFLECTIVE)
grass = Material(diffuse=(0.4, 1, 0.4), spec=32, Ks=0.1,matType=REFLECTIVE)
water = Material(diffuse=(0.4, 0.4, 1), spec=256, Ks=0.2,matType=OPAQUE)
mirror = Material(diffuse=(0.9, 0.9, 0.9), spec=64, Ks=0.2, matType=OPAQUE)
glass = Material(diffuse=(0.9, 0.9, 0.9), spec=64, Ks=0.15, ior=1.5, matType=TRANSPARENT)
diamond = Material(diffuse=(0.9, 0.9, 0.9), spec=128, Ks=0.2, ior=2.417, matType=TRANSPARENT)
floor_material = Material(diffuse=(1, 0.4, 0.4), spec=8, Ks=0.01, matType=REFLECTIVE)  # Rojo
ceiling_material = Material(diffuse=(0.4, 1, 0.4), spec=32, Ks=0.1, matType=REFLECTIVE) # Verde
front_wall_material = Material(diffuse=(0.4, 0.4, 1), spec=256, Ks=0.2, matType=OPAQUE) # Azul
left_wall_material = Material(diffuse=(1, 1, 0), spec=64, Ks=0.2, matType=OPAQUE)       # Amarillo
right_wall_material = Material(diffuse=(1, 0, 1), spec=64, Ks=0.15, matType=TRANSPARENT) # Morado


#raytracer.scene.append(Sphere(position=(-3, 1, -7), radius=1, material=glass))
#raytracer.scene.append(Sphere(position=(3, 1, -7), radius=1, material=diamond))
#raytracer.scene.append(Sphere(position=(0, 2, -6), radius=1, material=mirror))
#raytracer.scene.append(Sphere(position=(-3, -2, -7), radius=1, material=brick))
#raytracer.scene.append(Sphere(position=(3, -2, -7), radius=1, material=grass))
# Piso (Rojo)
# Piso (Rojo)
raytracer.scene.append(Plane(position=(0, -5, -5), normal=(0, 1, 0), material=floor_material))

# Techo (Verde)
raytracer.scene.append(Plane(position=(0, 5, -5), normal=(0, -1, 0), material=ceiling_material))

# Pared delantera (Azul)
raytracer.scene.append(Plane(position=(0, 0, -10), normal=(0, 0, 1), material=front_wall_material))

# Pared izquierda (Amarillo)
raytracer.scene.append(Plane(position=(-5, 0, -5), normal=(1, 0, 0), material=left_wall_material))

# Pared derecha (Morado)
raytracer.scene.append(Plane(position=(5, 0, -5), normal=(-1, 0, 0), material=right_wall_material))
raytracer.camPosition=[0, 0, 2]


#raytracer.scene.append(Disk(position=(0,-1.5,-5),normal=(0,1,0),radius=1.5,material=mirror))
#raytracer.scene.append(AABB(position=(1.5,1.5,-5),size=(1,1,1),material=brick))
#raytracer.scene.append(Sphere(position=(0, -1, -6), radius=1, material=water))
# Primer cubo cerca de la esquina izquierda y elevado
raytracer.scene.append(AABB(position=(-2.5, 0, -7), size=(1,1,1), material=brick))

# Segundo cubo cerca de la esquina derecha y elevado
raytracer.scene.append(AABB(position=(2.5, 0, -7), size=(1,1,1), material=glass))


raytracer.scene.append(Disk(position=(0, -2, -5), normal=(0, 1, 0), radius=1.5, material=mirror))






raytracer.lights.append(AmbientLight(intensity=0.1))
raytracer.lights.append(DirectionalLight(direction=(-1, -1, -1), intensity=0.9))



raytracer.rtClear()
raytracer.rtRender()

print("\nRender Time:", pygame.time.get_ticks() / 1000, "secs")

isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

pygame.quit()
