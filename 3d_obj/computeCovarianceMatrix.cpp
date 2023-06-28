void PointCloud::computeCovarianceMatrix() {
	covarianceMatrix[3][3];
	
	double means[3] = {0, 0, 0};
	for (int i = 0; i < points.size(); i++)
		means[0] += points[i].x,
		means[1] += points[i].y,
		means[2] += points[i].z;
	means[0] /= points.size(), means[1] /= points.size(), means[2] /= points.size();
	
	for (int i = 0; i < 3; i++)
		for (int j = 0; j < 3; j++) {
			covarianceMatrix[i][j] = 0.0;
			for (int k = 0; k < points.size(); k++)
				covarianceMatrix[i][j] += (means[i] - points[k].coord(i)) *
                                                          (means[j] - points[k].coord(j));
			covarianceMatrix[i][j] /= points.size() - 1;
		}	
}