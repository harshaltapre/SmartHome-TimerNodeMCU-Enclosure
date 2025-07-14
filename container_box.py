from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Ax2
from OCC.Extend.DataExchange import write_stl_file
from OCC.Display.SimpleGui import init_display

def cm(v): return v * 10.0  # Convert cm to mm

# === Box Dimensions ===
length = 10.5
width = 7.2
height = 4.7
thickness = 0.2

# === Create Outer and Inner Hollow Box ===
outer = BRepPrimAPI_MakeBox(cm(length), cm(width), cm(height)).Shape()
inner = BRepPrimAPI_MakeBox(
    gp_Pnt(cm(thickness), cm(thickness), cm(thickness)),
    cm(length - 2 * thickness),
    cm(width - 2 * thickness),
    cm(height - thickness)
).Shape()
box = BRepAlgoAPI_Cut(outer, inner).Shape()

# === USB Type-B Port (Left side, near bottom-left) ===
usb_cutout = BRepPrimAPI_MakeBox(
    gp_Pnt(0, cm(1), cm(0.7)),
    cm(thickness + 0.1),
    16,
    11.5
).Shape()
box = BRepAlgoAPI_Cut(box, usb_cutout).Shape()

# === 5V Adapter Hole (Right side, circular, near bottom) ===
charging_hole = BRepPrimAPI_MakeCylinder(
    gp_Ax2(gp_Pnt(cm(length), cm(1.7), cm(1.1)), gp_Dir(-1, 0, 0)),
    4, cm(thickness + 0.1)
).Shape()
box = BRepAlgoAPI_Cut(box, charging_hole).Shape()

# === Rectangular USB Slit (Back wall, bottom-right - moved away from corner post) ===
# Positioned on the back wall at bottom-right, moved further from corner post for clearance
# Corner post is at (9.8cm, 6.5cm) so slit moved much further left for safety
slit_width = 18  # mm — width for USB fit
slit_height = 4  # mm — height for USB insertion
slit_x = cm(7.5)  # moved further away from corner post (more clearance from 9.8cm post)
slit_y = cm(width)  # back face (Y = full width)
slit_z = cm(0.8)  # bottom position

back_usb_slit = BRepPrimAPI_MakeBox(
    gp_Pnt(slit_x, slit_y, slit_z),
    slit_width,
    cm(thickness + 0.1),  # depth of cut through back wall
    slit_height
).Shape()
box = BRepAlgoAPI_Cut(box, back_usb_slit).Shape()

# === Screw Posts in corners ===
post_radius = 2.5
hole_radius = 1.5
post_height = cm(height - thickness)
corner_positions = [
    (cm(0.7), cm(0.7)),
    (cm(length - 0.7), cm(0.7)),
    (cm(0.7), cm(width - 0.7)),
    (cm(length - 0.7), cm(width - 0.7)),
]

for x, y in corner_positions:
    post = BRepPrimAPI_MakeCylinder(
        gp_Ax2(gp_Pnt(x, y, cm(thickness)), gp_Dir(0, 0, 1)),
        post_radius, post_height
    ).Shape()
    hole = BRepPrimAPI_MakeCylinder(
        gp_Ax2(gp_Pnt(x, y, cm(thickness)), gp_Dir(0, 0, 1)),
        hole_radius, post_height
    ).Shape()
    post = BRepAlgoAPI_Cut(post, hole).Shape()
    box = BRepAlgoAPI_Fuse(box, post).Shape()

# === Export STL for 3D printing ===
write_stl_file(box, "D:/model/container_box.stl")
print("✅ STL exported: D:/model/container_box.stl")

# === Optional: Viewer ===
try:
    display, start_display, _, _ = init_display()
    display.DisplayShape(box, update=True)
    start_display()
except:
    print("ℹ️ Viewer not supported.")