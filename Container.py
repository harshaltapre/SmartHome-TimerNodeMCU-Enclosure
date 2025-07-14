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

# === Rectangular USB Slit (Back wall, bottom-right - HOLLOW CUTOUT) ===
# Positioned on the back wall at bottom-right, ensuring complete hollow cutout
# Corner post is at (9.8cm, 6.5cm) so slit moved further left for safety
slit_width = 18  # mm — width for USB fit
slit_height = 4  # mm — height for USB insertion
slit_x = cm(7.5)  # moved further away from corner post (more clearance)
slit_y = cm(width - thickness)  # start from inner edge of back wall
slit_z = cm(0.6)  # bottom position with clearance

# Create hollow rectangular cutout that goes completely through the back wall
back_usb_slit = BRepPrimAPI_MakeBox(
    gp_Pnt(slit_x, slit_y, slit_z),
    slit_width,
    cm(thickness + 0.2),  # extends beyond wall thickness for complete cutout
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
# Export with high quality settings for 3D printing
write_stl_file(box, "container_box_3d_print.stl")
print("✅ STL file exported for 3D printing: container_box_3d_print.stl")
print("📏 Box dimensions: 10.5cm × 7.2cm × 4.7cm")
print("🔧 Wall thickness: 0.2cm (2mm)")
print("🖨️ Ready for 3D printing!")
print("")
print("📋 3D Printing Settings Recommendations:")
print("   • Layer height: 0.2mm")
print("   • Infill: 20-30%")
print("   • Print speed: 50-60mm/s")
print("   • Supports: Not needed (hollow design)")
print("   • Print orientation: Bottom face down")
print("   • Nozzle temperature: 200-210°C (PLA)")
print("   • Bed temperature: 60°C (PLA)")
print("")
print("📦 Features included:")
print("   • USB Type-B port (left side)")
print("   • 5V adapter hole (right side)")
print("   • Rectangular USB slit (back wall, 18×4mm)")
print("   • 4 corner screw posts with holes")
print("   • Hollow interior with 2mm walls")

# === Optional: Viewer ===
try:
    display, start_display, _, _ = init_display()
    display.DisplayShape(box, update=True)
    start_display()
except:
    print("ℹ️ Viewer not supported.")