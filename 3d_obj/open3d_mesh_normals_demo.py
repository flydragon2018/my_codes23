    
    
    
    # We create a visualizer object that will contain references to the created window, the 3D objects and will listen to callbacks for key presses, animations, etc.
    vis = o3d.visualization.Visualizer()
    # New window, where we can set the name, the width and height, as well as the position on the screen
    vis.create_window(window_name='Angel Visualize', width=800, height=600)

    # We call add_geometry to add a mesh or point cloud to the visualizer
    vis.add_geometry(mesh)

    # We can easily create primitives like cubes, sphere, cylinders, etc. In our case we create a sphere and specify its radius
    sphere_mesh = o3d.geometry.TriangleMesh.create_sphere(radius=0.05)

    # We can compute either vertex or face normals
    sphere_mesh.compute_vertex_normals()
    # Add the sphere to the visualizer
    vis.add_geometry(sphere_mesh)
    # Translate it from the center
    sphere_mesh.translate((1, 0, 0))