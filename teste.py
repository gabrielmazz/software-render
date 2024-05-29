import openmesh as om
import numpy as np

# Create a TriMesh object
mesh = om.TriMesh()

# Add vertices and faces to your mesh
vh0 = mesh.add_vertex([0, 0, 0])
vh1 = mesh.add_vertex([1, 0, 0])
vh2 = mesh.add_vertex([0, 1, 0])
fh = mesh.add_face(vh0, vh1, vh2)

# Request face colors
mesh.request_face_colors()

# Define a color (RGBA format, values between 0 and 1)
color = np.array([1.0, 0.0, 0.0, 1.0])  # Red color

# Set the color of the face
mesh.set_color(fh, color)

