from math import pi, sin, cos, acos
from random import uniform

from pyray import *
from raylib import ffi


W, H = 1280, 720  # Window dimensions
R = 32.0  # Billboard radius
SUN = Vector3(10.0, 0.0, -10.0)  # Sunlight direction from the camera


class Billboard:
    def __init__(self) -> None:
        # Random spherical coordinates for billboard positioning
        self.theta = acos(1.0 - 2.0 * uniform(0.0, 1.0))
        self.phi = uniform(0.0, 2.0 * pi)

        # Spherical coordinates to Cartesian
        self.x = R * sin(self.theta) * cos(self.phi)
        self.y = R * cos(self.theta)
        self.z = R * sin(self.theta) * sin(self.phi)

        self.pos = Vector3(self.x, self.y, self.z)

        # Random size and rotation for each billboard
        self.size = uniform(48.0, 64.0)
        self.rotation = uniform(-45.0, 45.0)

    def draw(self) -> None:
        # Lighting effect based on sunlight and camera position
        light_dir = vector3_normalize(vector3_subtract(SUN, self.pos))
        camera_to_billboard = vector3_add(
            vector3_subtract(camera.position, self.pos), Vector3(-64.0, 64.0, 0.0)
        )
        billboard_normal = vector3_negate(vector3_normalize(camera_to_billboard))
        dot_product = vector_3dot_product(light_dir, billboard_normal)

        # Brightness of the billboard based on light direction with global illumination
        MIN_BRIGHTNESS = 0.7
        if dot_product < MIN_BRIGHTNESS:
            brightness = int(255 * MIN_BRIGHTNESS)
        else:
            brightness = int(255 * dot_product)

        # Set the color based on brightness
        color = Color(brightness, brightness, brightness, 255)

        draw_billboard_pro(
            camera,
            foliage,
            Rectangle(0, 0, 324, 324),
            self.pos,
            Vector3(0.0, 1.0, 0.0),
            Vector2(self.size, self.size),
            Vector2(0.0, 0.0),
            self.rotation,
            color,
        )


# Initialize window and setup
init_window(W, H, "Ghibli Style Billboard Foliage")
set_target_fps(60)

# Load shader and texture
shader = load_shader("", "res/waving.fsh")
foliage = load_texture("res/leaves.png")
set_texture_filter(foliage, TextureFilter.TEXTURE_FILTER_POINT)

# Setup camera
camera = Camera3D(
    Vector3(0.0, 0.0, -128.0),  # Camera position
    Vector3(0.0, 0.0, 0.0),  # Target position
    Vector3(0.0, 1.0, 0.0),  # Up vector
    90.0,  # Field Of View
    CameraProjection.CAMERA_PERSPECTIVE,
)

# 16: Good, 24: Very good, 32: Don't need more
billboards = [Billboard() for _ in range(32)]

while not window_should_close():
    # Update
    update_camera(camera, CameraMode.CAMERA_ORBITAL)

    billboards.sort(
        key=lambda b: (vector_3distance(camera.position, b.pos)),
        reverse=True,
    )
    set_shader_value(
        shader,
        get_shader_location(shader, "time"),
        ffi.new("float*", get_time()),
        ShaderUniformDataType.SHADER_UNIFORM_FLOAT,
    )

    # Render
    begin_drawing()
    clear_background(Color(234, 225, 225, 255))

    begin_mode_3d(camera)
    # Avoid central holes
    draw_sphere(Vector3(0.0, 0.0, 0.0), R * 0.7, Color(66, 126, 55, 255))
    
    begin_shader_mode(shader)
    for billboard in billboards:
        billboard.draw()
    end_shader_mode()
    
    end_mode_3d()

    end_drawing()
