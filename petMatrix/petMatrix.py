#import sys, math    
from maya import OpenMaya, OpenMayaMPx

# The name of the node.
node_name = 'petMatrix' 

node_classify = 'utility/general'

# A unique ID associated to this node type.
# Plugs for internal use only can use 0 - 0x7ffff.
node_id = OpenMaya.MTypeId(0x00005)

class petMatrix(OpenMayaMPx.MPxNode):

    # define attrs. This will hold a ref to the MObj that are created in the nodeInitializer
    in_matrix = OpenMaya.MObject()
    out_matrix = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    def compute(self, plug, data_block):

        # only output plugs will be passed to the compute method
        # we could do different computes for different plugs
        if plug == petMatrix.out_matrix:

            #--------------------
            # INPUT
            #--------------------
            # get the datahandle from the data block
            in_matrix_datahandle = data_block.inputValue(petMatrix.in_matrix)

            # get the data (float in this case) from the data handle
            in_matrix_value = in_matrix_datahandle.asMatrix()

            #--------------------
            # COMPUTE
            #--------------------
            out_matrix_value = in_matrix_value

            #--------------------
            # OUTPUT
            #--------------------
            # get the datahandle from the data block
            out_matrix_datahandle = data_block.outputValue(petMatrix.out_matrix)
            out_matrix_datahandle.setMMatrix(out_matrix_value)

            # mark the plug clean
            data_block.setClean(plug)

        # optionally we could return unknown here, sine we expect only one output 
        # plug specified to be passed to the compute method
        else:
            return OpenMaya.kUnknownParameter


def nodeCreator():
    # create an instance and return a pointer MObj to it
    return OpenMayaMPx.asMPxPtr(petMatrix())

def nodeInitializer():
    # create a function set for numeric attributes, will be used as a
    # factory to create attributes, they will be returned as MObj
    mfn_attr = OpenMaya.MFnMatrixAttribute()

    #--------------------
    # INPUT
    #--------------------
    # create an attr. params: longname, shortname, datatype, default
    # the default is a double matrix, if we want to save memory we could specify a float matrix instead
    petMatrix.in_matrix = mfn_attr.create('in_matrix', 'im')
    # set the properties of the attr
    mfn_attr.setReadable(True)
    mfn_attr.setWritable(True)
    mfn_attr.setStorable(True)
    mfn_attr.setKeyable(True)

    #--------------------
    # OUTPUT
    #--------------------
    # create an attr. params: longname, shortname, datatype, default
    # NOTE that output value has no default value (it will be computed)
    petMatrix.out_matrix = mfn_attr.create('out_matrix', 'om')
    # set the properties of the attr
    # NOTE only readable
    mfn_attr.setReadable(True)
    mfn_attr.setWritable(False)
    mfn_attr.setStorable(False)
    mfn_attr.setKeyable(False)


    #--------------------
    # ADD ATTR TO NODE
    #--------------------
    petMatrix.addAttribute(petMatrix.in_matrix)
    petMatrix.addAttribute(petMatrix.out_matrix)

    #--------------------
    # SETUP DEPENDENCY
    #--------------------
    # which attributes needs to be updated if an attribute is changed
    petMatrix.attributeAffects(petMatrix.in_matrix, petMatrix.out_matrix)

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