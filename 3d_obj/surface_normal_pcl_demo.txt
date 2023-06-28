'''
Given a geometric surface, it’s usually trivial to infer the direction of the normal at a certain point on the surface as the vector perpendicular to the surface at that point. However, since the point cloud datasets that we acquire represent a set of point samples on the real surface, there are two possibilities:

obtain the underlying surface from the acquired point cloud dataset, using surface meshing techniques, and then compute the surface normals from the mesh;

use approximations to infer the surface normals from the point cloud dataset directly.



The solution for estimating the surface normal is therefore reduced to an analysis of the eigenvectors and eigenvalues (or PCA – Principal Component Analysis) of a covariance matrix created from the nearest neighbors of the query point. More specifically, for each point \boldsymbol{p}_i, we assemble the covariance matrix \mathcal{C} as follows:

\mathcal{C} = \frac{1}{k}\sum_{i=1}^{k}{\cdot (\boldsymbol{p}_i-\overline{\boldsymbol{p}})\cdot(\boldsymbol{p}_i-\overline{\boldsymbol{p}})^{T}}, ~\mathcal{C} \cdot \vec{{\mathsf v}_j} = \lambda_j \cdot \vec{{\mathsf v}_j},~ j \in \{0, 1, 2\}

Where k is the number of point neighbors considered in the neighborhood of \boldsymbol{p}_i, \overline{\boldsymbol{p}} represents the 3D centroid of the nearest neighbors, \lambda_j is the j-th eigenvalue of the covariance matrix, and \vec{{\mathsf v}_j} the j-th eigenvector.



'''

 1  // Placeholder for the 3x3 covariance matrix at each surface patch
 2  Eigen::Matrix3f covariance_matrix;
 3  // 16-bytes aligned placeholder for the XYZ centroid of a surface patch
 4  Eigen::Vector4f xyz_centroid;
 5
 6  // Estimate the XYZ centroid
 7  compute3DCentroid (cloud, xyz_centroid);
 8
 9  // Compute the 3x3 covariance matrix
10  computeCovarianceMatrix (cloud, xyz_centroid, covariance_matrix);

The solution to this problem is trivial if the viewpoint {\mathsf v}_p is in fact known. To orient all normals \vec{\boldsymbol{n}}_i consistently towards the viewpoint, they need to satisfy the equation:

\vec{\boldsymbol{n}}_i \cdot ({\mathsf v}_p - \boldsymbol{p}_i) > 0


 1#include <pcl/point_types.h>
 2#include <pcl/features/normal_3d.h>
 3
 4{
 5  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud (new pcl::PointCloud<pcl::PointXYZ>);
 6
 7  ... read, pass in or create a point cloud ...
 8
 9  // Create the normal estimation class, and pass the input dataset to it
10  pcl::NormalEstimation<pcl::PointXYZ, pcl::Normal> ne;
11  ne.setInputCloud (cloud);
12
13  // Create an empty kdtree representation, and pass it to the normal estimation object.
14  // Its content will be filled inside the object, based on the given input dataset (as no other search surface is given).
15  pcl::search::KdTree<pcl::PointXYZ>::Ptr tree (new pcl::search::KdTree<pcl::PointXYZ> ());
16  ne.setSearchMethod (tree);
17
18  // Output datasets
19  pcl::PointCloud<pcl::Normal>::Ptr cloud_normals (new pcl::PointCloud<pcl::Normal>);
20
21  // Use all neighbors in a sphere of radius 3cm
22  ne.setRadiusSearch (0.03);
23
24  // Compute the features
25  ne.compute (*cloud_normals);
26
27  // cloud_normals->size () should have the same size as the input cloud->size ()*
28}



computePointNormal(const pcl::PointCloud<PointInT> &cloud, const std::vector<int> &indices, Eigen::Vector4f &plane_parameters, float &curvature);

Where cloud is the input point cloud that contains the points, indices represents the set of k-nearest neighbors from cloud, and plane_parameters and curvature represent the output of the normal estimation, with plane_parameters holding the normal (nx, ny, nz) on the first 3 coordinates, and the fourth coordinate is D = nc . p_plane (centroid here) + p. The output surface curvature is estimated as a relationship between the eigenvalues of the covariance matrix (as presented above), as:

\sigma = \frac{\lambda_0}{\lambda_0 + \lambda_1 + \lambda_2}



For the speed-savvy users, PCL provides an additional implementation of surface normal estimation which uses multi-core/multi-threaded paradigms 
using OpenMP to speed the computation. The name of the class is pcl::NormalEstimationOMP, 
and its API is 100% compatible to the single-threaded pcl::NormalEstimation, which makes it suitable as a drop-in replacement.
 On a system with 8 cores, you should get anything between 6-8 times faster computation times.
