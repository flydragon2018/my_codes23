 
import pandas as pd 
import pyglet

import time
import trimesh
import numpy as np

# Callback function responsible for animating the objects
def rotate_objects(scene):

    # create an empty homogenous transformation matrix for rotating the sphere
    matrix = np.eye(4)

    # get the delta of the time. We need this as trimesh does not contain a function for automatic incrementation of movements
    delta_change = time.time()
    # set Y as sin of time. We can change the speed of rotation by multiplying the delta_change with a scalar
    matrix[0][3] = np.sin(-delta_change*2)
    # set Z as cos of time
    matrix[2][3] = np.cos(-delta_change*2)

    # create a y axis rotation for the angel mesh. We use the trimesh.transofmration.rotation_matrix which requires rotation angle and an axis
    yaxis = [0,1,0]
    Ry = trimesh.transformations.rotation_matrix(delta_change*2, yaxis)

    # Get the nodes for the sphere and the mesh. You can also directly call them with their created mesh containers or keep which node is which mesh in a dictionary
    # For our purpose we only have two objects so we just select them in the way they are added to the scene
    node_sphere = s.graph.nodes_geometry[0]
    node_mesh = s.graph.nodes_geometry[1]
    
    # apply the transform to the node and update the scene
    scene.graph.update(node_sphere, matrix=matrix)
    scene.graph.update(node_mesh, matrix=Ry)

if __name__ == '__main__':

    # Load the angel mesh. Trimesh directly detects that the mesh is textured and contains a material
    mesh_path = 'mesh/angelStatue_lp.obj'
    mesh = trimesh.load(mesh_path)

    # create a sphere primitive. Additional primitives can be created like box, capsule, extrusion, etc.
    sphere_mesh = trimesh.primitives.Sphere(radius=0.1)
    # set the color of the sphere
    sphere_mesh.visual.face_colors = [0, 0, 255, 255]

    # Set up a scene containing the sphere and the angel mesh
    s = trimesh.Scene([sphere_mesh,mesh])

    # Print the nodes that the scene contains - each mesh has a separate node
    print(s.graph.nodes)

    # Show the scene and set a callback function, which will be used to rotate the objects
    s.show(callback=rotate_objects)

