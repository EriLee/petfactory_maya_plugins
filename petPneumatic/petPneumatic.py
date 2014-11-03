import sys, math
from maya import OpenMaya, OpenMayaMPx

# The name of the node.
node_name = 'petPneumatic' 

node_classify = 'utility/general'

# A unique ID associated to this node type.
# Plugs for internal use only can use 0 - 0x7ffff.
node_id = OpenMaya.MTypeId(0x00008)

class petPneumatic(OpenMayaMPx.MPxNode):

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
        if plug == petPneumatic.out_midpoint:

            #--------------------
            # INPUT
            #--------------------
            # get the datahandle from the data block and value from data handle
            in_matrix_1_DH = data_block.inputValue(petPneumatic.in_matrix_1)
            in_matrix_1_V = in_matrix_1_DH.asMatrix()

            in_matrix_2_DH = data_block.inputValue(petPneumatic.in_matrix_2)
            in_matrix_2_V = in_matrix_2_DH.asMatrix()

            #--------------------
            # COMPUTE
            #--------------------

            t_1 = OpenMaya.MVector(in_matrix_1_V(3,0), in_matrix_1_V(3,1), in_matrix_1_V(3,2))
            t_2 = OpenMaya.MVector(in_matrix_2_V(3,0), in_matrix_2_V(3,1), in_matrix_2_V(3,2))

            aim_v = t_2 - t_1
            mid_t = aim_v*.5 + t_1

            aim_vn = aim_v.normal()

            up_vn = OpenMaya.MVector(in_matrix_1_V(0,0), in_matrix_1_V(0,1), in_matrix_1_V(0,2)).normal()
            cross_vn = aim_vn ^ up_vn
            up_ortho_vn = cross_vn ^ aim_vn

            #tm = OpenMaya.MTransformationMatrix([[aim_vn[0], aim_vn[1], aim_vn[2], 0], [cross_vn[0],cross_vn[1],cross_vn[2],0], [up_ortho_vn[0],up_ortho_vn[1],up_ortho_vn[2],0], [mid_t[0], mid_t[1], mid_t[2], 1]])
            tm = OpenMaya.MMatrix([[aim_vn[0], aim_vn[1], aim_vn[2], 0], [cross_vn[0],cross_vn[1],cross_vn[2],0], [up_ortho_vn[0],up_ortho_vn[1],up_ortho_vn[2],0], [mid_t[0], mid_t[1], mid_t[2], 1]])
            '''
            rot_xyz = tm.rotation()

            rx = (180/math.pi)*rot_xyz[0]
            ry = (180/math.pi)*rot_xyz[1]
            rz = (180/math.pi)*rot_xyz[2]
            '''
            out_x = mid_t.x
            out_y = mid_t.y
            out_z = mid_t.z
            
            #out_x = rx
            #out_y = ry
            #out_z = rz

            #--------------------
            # OUTPUT
            #--------------------
            # get the datahandle from the data block
            out_midpoint_DH = data_block.outputValue(petPneumatic.out_midpoint)
            out_midpoint_DH.set3Float(out_x, out_y, out_z)

            # mark the plug clean
            data_block.setClean(plug)

        # optionally we could return unknown here, sine we expect only one output 
        # plug specified to be passed to the compute method
        else:
            return OpenMaya.kUnknownParameter


def nodeCreator():
    # create an instance and return a pointer MObj to it
    return OpenMayaMPx.asMPxPtr(petPneumatic())

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
    petPneumatic.in_matrix_1 = matrix_attr.create('in_matrix_1', 'im1')
    # set the properties of the attr
    matrix_attr.setReadable(True)
    matrix_attr.setWritable(True)
    matrix_attr.setStorable(True)
    matrix_attr.setKeyable(True)

    petPneumatic.in_matrix_2 = matrix_attr.create('in_matrix_2', 'im2')
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
    petPneumatic.out_midpoint = num_attr.create('outMidpoint', 'om', k3_float)

    # set the properties of the attr
    # NOTE only readable
    num_attr.setReadable(True)
    num_attr.setWritable(False)
    num_attr.setStorable(False)
    num_attr.setKeyable(False)

    #--------------------
    # ADD ATTR TO NODE
    #--------------------
    petPneumatic.addAttribute(petPneumatic.in_matrix_1)
    petPneumatic.addAttribute(petPneumatic.in_matrix_2)
    petPneumatic.addAttribute(petPneumatic.out_midpoint)

    #--------------------
    # SETUP DEPENDENCY
    #--------------------
    # which attributes needs to be updated if an attribute is changed
    petPneumatic.attributeAffects(petPneumatic.in_matrix_1, petPneumatic.out_midpoint)
    petPneumatic.attributeAffects(petPneumatic.in_matrix_2, petPneumatic.out_midpoint)

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