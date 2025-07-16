# SmartHome Timer NodeMCU Enclosure

This repository contains the 3D model files and Python scripts for generating a custom enclosure for a timer-based NodeMCU project. The design includes a base container and a top lid, both constructed using Python and the PythonOCC CAD kernel. STL and STEP files are also provided for direct use in 3D printing or CAD editing.

## Project Overview

This enclosure was designed for a NodeMCU-based timer circuit that requires ports for:
- USB Type-B programming input
- 5V barrel jack power adapter
- Wire terminals (signal input/output)
- Screw posts and a removable top lid

The box and lid are precisely modeled using Python, providing high customizability, reusability, and CAD/CAM integration.



## Folder Structure

```text
/model
│
├── container_box.py       # Python script to generate the base enclosure
├── container_lid.py       # Python script to generate the top lid
├── container_box.stl      # Exported STL file for 3D printing (box)
├── container_lid.stl      # Exported STL file for 3D printing (lid)
├── container_box.step     # STEP file for box (for CAD)
├── container_lid.step     # STEP file for lid (for CAD)
└── requirements.txt       # Required Python packages


---


## Requirements

To run the Python scripts, you need Python 3.9+ and the following packages installed in a virtual environment (Anaconda recommended):

- `pythonocc-core`
- `OCC`
- `PyQt5` (for viewer)
- `numpy` (if extending functionality)

Use the following command to install dependencies:

```bash
pip install -r requirements.txt
How to Use
Clone the repository:

bash

git clone https://github.com/harshaltapre/SmartHome-TimerNodeMCU-Enclosure.git
Navigate to the /model directory and activate your virtual environment.

Run either script to generate new .stl and .step files:

bash

python container_box.py
python container_lid.py
Output
STL files are directly usable in Cura, PrusaSlicer, and most 3D printers.

STEP files can be imported into FreeCAD, SolidWorks, or Fusion 360 for further editing.

License
This project is released under the MIT License. See LICENSE for details.

yaml
---

Let me know if you also want:
- A matching `requirements.txt`
- An MIT `LICENSE` file
- A `preview.png` section to embed model screenshots later

You're ready to publish this professionally on GitHub!
