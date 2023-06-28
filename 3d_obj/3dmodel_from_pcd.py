import numpy as np
import open3d as o3d

input_path="pcd_data/"
output_path="obj_output/"

#dataname="sample.xyz"

dataname="sample_w_normals.xyz"


point_cloud= np.loadtxt(input_path+dataname,skiprows=1)

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(point_cloud[:,:3])
pcd.colors = o3d.utility.Vector3dVector(point_cloud[:,3:6]/255)
pcd.normals = o3d.utility.Vector3dVector(point_cloud[:,6:9])

o3d.visualization.draw_geometries([pcd])

distances = pcd.compute_nearest_neighbor_distance()
avg_dist = np.mean(distances)
radius = 3 * avg_dist

bpa_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(pcd,o3d.utility.DoubleVector([radius, radius * 2]))

#down sample
#dec_mesh = mesh.simplify_quadric_decimation(100000)

dec_mesh = bpa_mesh.simplify_quadric_decimation(100000)



#if you think the mesh can present some weird artifacts, 
#you can run the following commands to ensure its consistency:


dec_mesh.remove_degenerate_triangles()
dec_mesh.remove_duplicated_triangles()
dec_mesh.remove_duplicated_vertices()
dec_mesh.remove_non_manifold_edges()

poisson_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=8, width=0, scale=1.1, linear_fit=False)[0]



#To get a clean result, it is often necessary to add a cropping step to clean unwanted artifacts 
bbox = pcd.get_axis_aligned_bounding_box()
p_mesh_crop = poisson_mesh.crop(bbox)


#Exporting the data is straightforward with the write_triangle_mesh function.
# We just specify within the name of the created file, the extension that we want from .ply, .obj, .stl or .gltf, and the mesh to export.
# Below, we export both the BPA and Poisson’s reconstructions as .ply files:

o3d.io.write_triangle_mesh(output_path+"bpa_mesh.ply", dec_mesh)
o3d.io.write_triangle_mesh(output_path+"p_mesh_c.ply", p_mesh_crop)


#To quickly generate Levels of Details (LoD), let us write your first function. 
#It will be really simple. The function will take as parameters a mesh, a list of LoD (as a target number of triangles),
# the file format of the resulting files and the path to write the files to. The function (to write in the script) looks like this:

def lod_mesh_export(mesh, lods, extension, path):
    mesh_lods={}
    for i in lods:
        mesh_lod = mesh.simplify_quadric_decimation(i)
        o3d.io.write_triangle_mesh(path+"lod_"+str(i)+extension, mesh_lod)
        mesh_lods[i]=mesh_lod
    print("generation of "+str(i)+" LoD successful")
    return mesh_lods


my_lods = lod_mesh_export(bpa_mesh, [100000,50000,10000,1000,100], ".ply", output_path)

my_lods2 = lod_mesh_export(bpa_mesh, [8000,800,300], ".obj", output_path)


o3d.visualization.draw_geometries([my_lods[100]])