import sys
from maya import OpenMaya, OpenMayaMPx

# The name of the node.
node_name = 'petPneumatic' 

node_classify = 'utility/general'

# A unique ID associated to this node type.
# Plugs for internal use only can use 0 - 0x7ffff.
node_id = OpenMaya.MTypeId(0x00006)

class petPneumatic(OpenMayaMPx.MPxNode):

    # define attrs. This will hold a ref to the MObj that are created in the nodeInitializer
    in_top_matrix = OpenMaya.MObject()
    in_btm_matrix = OpenMaya.MObject()

    out_top_matrix = OpenMaya.MObject()
    out_btm_matrix = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

    def compute(self, plug, data_block):

        # only output plugs will be passed to the compute method
        # we could do different computes for different plugs
        if plug == petPneumatic.out_top_matrix or plug == petPneumatic.out_btm_matrix:

            #--------------------
            # INPUT
            #--------------------
            # get the datahandle from the data block and value from data handle
            in_top_matrix_DH = data_block.inputValue(petPneumatic.in_top_matrix)
            in_top_matrix_V = in_top_matrix_DH.asMatrix()

            in_btm_matrix_DH = data_block.inputValue(petPneumatic.in_btm_matrix)
            in_btm_matrix_V = in_btm_matrix_DH.asMatrix()

            #--------------------
            # COMPUTE
            #--------------------
            out_top_matrix = in_top_matrix_V
            out_btm_matrix = in_btm_matrix_V

            #--------------------
            # OUTPUT
            #--------------------
            # get the datahandle from the data block
            out_top_matrix_DH = data_block.outputValue(petPneumatic.out_top_matrix)
            out_top_matrix_DH.setMMatrix(out_top_matrix)

            out_btm_matrix_DH = data_block.outputValue(petPneumatic.out_btm_matrix)
            out_btm_matrix_DH.setMMatrix(out_btm_matrix)

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
    mfn_attr = OpenMaya.MFnMatrixAttribute()

    #--------------------
    # INPUT
    #--------------------
    # create an attr. params: longname, shortname, datatype, default
    # the default is a double matrix, if we want to save memory we could specify a float matrix instead
    petPneumatic.in_top_matrix = mfn_attr.create('in_top_matrix', 'itm')
    # set the properties of the attr
    mfn_attr.setReadable(True)
    mfn_attr.setWritable(True)
    mfn_attr.setStorable(True)
    mfn_attr.setKeyable(True)

    petPneumatic.in_btm_matrix = mfn_attr.create('in_btm_matrix', 'ibm')
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
    petPneumatic.out_top_matrix = mfn_attr.create('out_top_matrix', 'otm')
    # set the properties of the attr
    # NOTE only readable
    mfn_attr.setReadable(True)
    mfn_attr.setWritable(False)
    mfn_attr.setStorable(False)
    mfn_attr.setKeyable(False)

    petPneumatic.out_btm_matrix = mfn_attr.create('out_btm_matrix', 'obm')
    # set the properties of the attr
    # NOTE only readable
    mfn_attr.setReadable(True)
    mfn_attr.setWritable(False)
    mfn_attr.setStorable(False)
    mfn_attr.setKeyable(False)


    #--------------------
    # ADD ATTR TO NODE
    #--------------------
    petPneumatic.addAttribute(petPneumatic.in_top_matrix)
    petPneumatic.addAttribute(petPneumatic.in_btm_matrix)
    petPneumatic.addAttribute(petPneumatic.out_top_matrix)
    petPneumatic.addAttribute(petPneumatic.out_btm_matrix)

    #--------------------
    # SETUP DEPENDENCY
    #--------------------
    # which attributes needs to be updated if an attribute is changed
    petPneumatic.attributeAffects(petPneumatic.in_top_matrix, petPneumatic.out_top_matrix)
    petPneumatic.attributeAffects(petPneumatic.in_btm_matrix, petPneumatic.out_btm_matrix)

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