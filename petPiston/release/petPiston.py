import sys, math    
from maya import OpenMaya, OpenMayaMPx

# The name of the node.
kPluginNodeName = 'petPiston' 
# Where this node will be found in the Maya UI.

kPluginNodeClassify = 'utility/general'

# A unique ID associated to this node type.
# Plugs for internal use only can use 0 - 0x7ffff.
# Plugs that AD ships in th edev kit uses 0x80000 - 0xfffff
# if you plan to distribute the plug, get an ID from AD  
kPluginNodeId = OpenMaya.MTypeId(0x00001) 

##########################################################
# Plug-in 
##########################################################
class myNode(OpenMayaMPx.MPxNode):
    # Static variables which will later be replaced by the node's attributes.
    radius = OpenMaya.MObject()
    rod_offset = OpenMaya.MObject()
    angle = OpenMaya.MObject()

    arc_x = OpenMaya.MObject()
    arc_y = OpenMaya.MObject()
    rod_x = OpenMaya.MObject()
    
    def __init__(self):
        ''' Constructor. '''
        OpenMayaMPx.MPxNode.__init__(self)
        
    #def compute(self, pPlug, pDataBlock):
    def compute(self, plug, data):
        '''
        Node computation method.
            - plug: A connection point related to one of our node attributes (could be an input or an output)
            - data: Contains the data on which we will base our computations.
        '''
        
        if(plug == myNode.arc_x or plug == myNode.arc_y or plug == myNode.rod_x):
            
            # Obtain the data handles for each attribute
            radius_data = data.inputValue(myNode.radius)
            rod_offset_data = data.inputValue(myNode.rod_offset)
            angle_data = data.inputValue(myNode.angle)

            out_arc_x = data.outputValue(myNode.arc_x)
            out_arc_y = data.outputValue(myNode.arc_y)
            out_rod_x = data.outputValue(myNode.rod_x)
            
            # Extract the actual value associated to our sample input attribute (we have defined it as a float)
            radius_val = radius_data.asFloat()
            rod_offset_val = rod_offset_data.asFloat()
            angle_val = angle_data.asFloat()

            # perform the desired computation
            ux = math.cos(angle_val)
            uy = math.sin(angle_val)

            arc_x = ux * radius_val
            arc_y = uy * radius_val

            rod_length = radius_val*2 + rod_offset_val

            rod_x = radius_val * ux + math.sqrt(rod_length*rod_length - radius_val*radius_val * uy*uy)

            # Set the output value.
            out_arc_x.setFloat(arc_x)
            out_arc_y.setFloat(arc_y)
            out_rod_x.setFloat(rod_x)
            
            # Mark the output data handle as being clean; it need not be computed given its input.
            out_arc_x.setClean()
            out_arc_y.setClean()
            out_rod_x.setClean()
             
        else:
            return OpenMaya.kUnknownParameter

##########################################################
# Plug-in initialization.
##########################################################
def nodeCreator():
    ''' Creates an instance of our node class and delivers it to Maya as a pointer. '''
    #sys.stdout.write('apa\n')
    return OpenMayaMPx.asMPxPtr(myNode())

def nodeInitializer():
    ''' Defines the input and output attributes as static variables in our plug-in class. '''
    
    # The following MFnNumericAttribute function set will allow us to create our attributes.
    nAttr = OpenMaya.MFnNumericAttribute()
    kFloat = OpenMaya.MFnNumericData.kFloat
    
    #==================================
    # INPUT NODE ATTRIBUTE(S)
    #==================================

    # input_value
    myNode.radius = nAttr.create('radius', 'r', kFloat, 10.0)
    nAttr.setWritable(True)
    nAttr.setStorable(True) 
    nAttr.setHidden(False)
    myNode.addAttribute(myNode.radius)

    # frequency
    myNode.rod_offset = nAttr.create('rodOffset', 'ro', kFloat, 2.0)
    nAttr.setWritable(True)
    nAttr.setStorable(True) 
    nAttr.setHidden(False)
    myNode.addAttribute(myNode.rod_offset)

    # scale
    myNode.angle = nAttr.create('angle', 'a', kFloat, 0.0)
    nAttr.setWritable(True)
    nAttr.setStorable(True) 
    nAttr.setHidden(False)
    myNode.addAttribute(myNode.angle)
    
    #==================================
    # OUTPUT NODE ATTRIBUTE(S)
    #==================================
    myNode.arc_x = nAttr.create('arcx', 'ax', kFloat)
    nAttr.setStorable(False)
    nAttr.setWritable(False)
    nAttr.setReadable(True)
    nAttr.setHidden(False)
    myNode.addAttribute(myNode.arc_x)

    myNode.arc_y = nAttr.create('arcy', 'ay', kFloat)
    nAttr.setStorable(False)
    nAttr.setWritable(False)
    nAttr.setReadable(True)
    nAttr.setHidden(False)
    myNode.addAttribute(myNode.arc_y)

    myNode.rod_x = nAttr.create('rodx', 'rx', kFloat)
    nAttr.setStorable(False)
    nAttr.setWritable(False)
    nAttr.setReadable(True)
    nAttr.setHidden(False)
    myNode.addAttribute(myNode.rod_x)
    
    #==================================
    # NODE ATTRIBUTE DEPENDENCIES
    #==================================
    # If sampleInAttribute changes, the sampleOutAttribute data must be recomputed.
    myNode.attributeAffects(myNode.radius, myNode.arc_x)
    myNode.attributeAffects(myNode.radius, myNode.arc_y)
    myNode.attributeAffects(myNode.radius, myNode.rod_x)

    myNode.attributeAffects(myNode.angle, myNode.arc_x)
    myNode.attributeAffects(myNode.angle, myNode.arc_y)
    myNode.attributeAffects(myNode.angle, myNode.rod_x)

    myNode.attributeAffects(myNode.rod_offset, myNode.rod_x)

    
def initializePlugin( mobject ):
    ''' Initialize the plug-in '''
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerNode( kPluginNodeName, kPluginNodeId, nodeCreator,
                              nodeInitializer, OpenMayaMPx.MPxNode.kDependNode, kPluginNodeClassify )
    except:
        sys.stderr.write( 'Failed to register node: ' + kPluginNodeName )
        raise
    
def uninitializePlugin( mobject ):
    ''' Uninitializes the plug-in '''
    mplugin = OpenMayaMPx.MFnPlugin( mobject )
    try:
        mplugin.deregisterNode( kPluginNodeId )
    except:
        sys.stderr.write( 'Failed to deregister node: ' + kPluginNodeName )
        raise

##########################################################
# Sample usage.
##########################################################
''' 
# Copy the following lines and run them in Maya's Python Script Editor:

import maya.cmds as cmds

cmds.loadPlugin( 'sampleDGNode.py' )
cmds.createNode( 'myNodeName' )
# ...

'''