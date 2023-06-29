
from aspose.threed import FileFormat, FileContentType
from aspose.threed.entities import Cylinder
from aspose.threed.formats import PlySaveOptions

# Create a cylinder object and save it to ply file

FileFormat.PLY.encode(Cylinder(), "cylinder.ply")

# using Ply save options

# Save as binary PLY format, the default value is ASCII

opt = PlySaveOptions(FileContentType.BINARY)

# change the components to 's' and 't'
# wrong attribute name!!

#opt.texture_coordinate_components.item1 = "s"
#opt.texture_coordinate_components.item2 = "t"


 
 
 

# save the mesh

FileFormat.PLY.encode(Cylinder(), "cylinder.ply", opt)

