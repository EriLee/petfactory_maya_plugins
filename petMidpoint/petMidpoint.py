import sys
from maya import OpenMaya, OpenMayaMPx

# The name of the node.
node_name = 'petMidpoint' 

node_classify = 'utility/general'

# A unique ID associated to this node type.
# Plugs for internal use only can use 0 - 0x7ffff.
node_id = OpenMaya.MTypeId(0x00007)

class petMidpoint(OpenMayaMPx.MPxNode):

    # define attrs. This will hold a ref to the MObj that are created in the nodeInitializer
    in_matrix_1 = OpenMaya.MObject()
    in_matrix_2 = OpenMaya.MObject()

    # output
    out_midpoint = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    def compute(self, plug, data_block):

        # only output plugs will be passed to the compute method
        # we could do different computes for different plugs
        if plug == petMidpoint.out_midpoint:

            #--------------------
            # INPUT
            #--------------------
            # get the datahandle from the data block and value from data handle
            in_matrix_1_DH = data_block.inputValue(petMidpoint.in_matrix_1)
            in_matrix_1_V = in_matrix_1_DH.asMatrix()

            in_matrix_2_DH = data_block.inputValue(petMidpoint.in_matrix_2)
            in_matrix_2_V = in_matrix_2_DH.asMatrix()

            #--------------------
            # COMPUTE
            #--------------------
            #out_midpoint_V = 

            tm_1 = OpenMaya.MTransformationMatrix(in_matrix_1_V)
            t_1 = tm_1.translation(OpenMaya.MSpace.kWorld)

            tm_2 = OpenMaya.MTransformationMatrix(in_matrix_2_V)
            t_2 = tm_2.translation(OpenMaya.MSpace.kWorld)

            mid_t = t_1 + (t_2 - t_1)*.5

            out_x = mid_t.x
            out_y = mid_t.y
            out_z = mid_t.z

            #--------------------
            # OUTPUT
            #--------------------
            # get the datahandle from the data block
            out_midpoint_DH = data_block.outputValue(petMidpoint.out_midpoint)
            out_midpoint_DH.set3Float(out_x, out_y, out_z)

            # mark the plug clean
            data_block.setClean(plug)

        # optionally we could return unknown here, sine we expect only one output 
        # plug specified to be passed to the compute method
        else:
            return OpenMaya.kUnknownParameter


def nodeCreator():
    # create an instance and return a pointer MObj to it
    return OpenMayaMPx.asMPxPtr(petMidpoint())

def nodeInitializer():
    # create a function set for numeric attributes, will be used as a
    # factory to create attributes, they will be returned as MObj
    matrix_attr = OpenMaya.MFnMatrixAttribute()

    num_attr = OpenMaya.MFnNumericAttribute()
    k3_float = OpenMaya.MFnNumericData.k3Float


    #--------------------
    # INPUT
    #--------------------
    # create an attr. params: longname, shortname, datatype, default
    # the default is a double matrix, if we want to save memory we could specify a float matrix instead
    petMidpoint.in_matrix_1 = matrix_attr.create('in_matrix_1', 'im1')
    # set the properties of the attr
    matrix_attr.setReadable(True)
    matrix_attr.setWritable(True)
    matrix_attr.setStorable(True)
    matrix_attr.setKeyable(True)

    petMidpoint.in_matrix_2 = matrix_attr.create('in_matrix_2', 'im2')
    # set the properties of the attr
    matrix_attr.setReadable(True)
    matrix_attr.setWritable(True)
    matrix_attr.setStorable(True)
    matrix_attr.setKeyable(True)

    #--------------------
    # OUTPUT
    #--------------------
    # create an attr. params: longname, shortname, datatype, default
    # NOTE that output value has no default value (it will be computed)
    petMidpoint.out_midpoint = num_attr.create('outMidpoint', 'om', k3_float)

    # set the properties of the attr
    # NOTE only readable
    num_attr.setReadable(True)
    num_attr.setWritable(False)
    num_attr.setStorable(False)
    num_attr.setKeyable(False)

    #--------------------
    # ADD ATTR TO NODE
    #--------------------
    petMidpoint.addAttribute(petMidpoint.in_matrix_1)
    petMidpoint.addAttribute(petMidpoint.in_matrix_2)
    petMidpoint.addAttribute(petMidpoint.out_midpoint)

    #--------------------
    # SETUP DEPENDENCY
    #--------------------
    # which attributes needs to be updated if an attribute is changed
    petMidpoint.attributeAffects(petMidpoint.in_matrix_1, petMidpoint.out_midpoint)
    petMidpoint.attributeAffects(petMidpoint.in_matrix_2, petMidpoint.out_midpoint)

def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerNode(   node_name,
                                node_id,
                                nodeCreator,
                                nodeInitializer,
                                OpenMayaMPx.MPxNode.kDependNode,
                                node_classify)
    except:
        sys.stderr.write( 'Failed to register node: ' + node_name )
        raise


def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode(node_id)
    except:
        sys.stderr.write( 'Failed to deregister node: ' + node_name )
        raise