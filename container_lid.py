from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Ax2, gp_Trsf
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Extend.DataExchange import write_stl_file  # ✅ Add STL export

# Optional viewer
try:
    from OCC.Display.SimpleGui import init_display
    viewer_enabled = True
except ImportError:
    viewer_enabled = False

# === Helper: Convert cm to mm ===
def cm(v): return v * 10.0

# === Lid dimensions ===
length = 10.5     # cm
width = 7.2       # cm
lid_thickness = 0.3  # cm
hole_radius = 1.6  # mm (for screw holes)

# === Create base lid ===
lid = BRepPrimAPI_MakeBox(cm(length), cm(width), cm(lid_thickness)).Shape()

# === Drill screw holes aligned with the box ===
screw_coords = [
    (cm(0.7), cm(0.7)),
    (cm(length - 0.7), cm(0.7)),
    (cm(0.7), cm(width - 0.7)),
    (cm(length - 0.7), cm(width - 0.7)),
]

for x, y in screw_coords:
    hole = BRepPrimAPI_MakeCylinder(
        gp_Ax2(gp_Pnt(x, y, 0), gp_Dir(0, 0, 1)),
        hole_radius, cm(lid_thickness + 0.1)
    ).Shape()
    lid = BRepAlgoAPI_Cut(lid, hole).Shape()

# === Add a raised block for "EISTAtech" logo (placeholder) ===
logo_block = BRepPrimAPI_MakeBox(cm(6), cm(1), cm(0.2)).Shape()
move_logo = gp_Trsf()
move_logo.SetTranslation(
    gp_Pnt(0, 0, 0),
    gp_Pnt(cm((length - 6) / 2), cm((width - 1) / 2), cm(lid_thickness))
)
logo_transformed = BRepBuilderAPI_Transform(logo_block, move_logo, True).Shape()
lid = BRepAlgoAPI_Fuse(lid, logo_transformed).Shape()

# === Export to STEP file ===
step_writer = STEPControl_Writer()
step_writer.Transfer(lid, STEPControl_AsIs)
status = step_writer.Write("D:/model/container_lid.step")
if status == IFSelect_RetDone:
    print("✅ STEP file saved: D:/model/container_lid.step")
else:
    print("❌ Failed to export STEP file")

# === Export to STL file (for 3D printing) ===
write_stl_file(lid, "D:/model/container_lid.stl")
print("✅ STL file saved: D:/model/container_lid.stl")

# === Optional: Display the model ===
if viewer_enabled:
    display, start_display, _, _ = init_display()
    display.DisplayShape(lid, update=True)
    start_display()
else:
    print("ℹ️ Viewer not available. Files generated.")
