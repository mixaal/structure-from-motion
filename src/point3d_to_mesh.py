import open3d as o3d
import sys

#try:
pf = sys.argv[1]
pcd = o3d.io.read_point_cloud(pf) 
pcd.estimate_normals()
mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=9)
o3d.io.write_triangle_mesh('scene_mesh.ply', mesh)
#except Exception as e:
#    print('Usage: python point3d_to_mesh.py  ./output/<your_id>/point_cloud/iteration_30000/point_cloud.ply')
#    exit(-1)
