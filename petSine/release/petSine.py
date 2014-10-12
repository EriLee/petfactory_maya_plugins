import sys, math    
from maya import OpenMaya, OpenMayaMPx

# The name of the node.
kPluginNodeName = 'petSine' 
# Where this node will be found in the Maya UI.

kPluginNodeClassify = 'utility/general'

# A unique ID associated to this node type.
# Plugs for internal use only can use 0 - 0x7ffff.
# Plugs that AD ships in th edev kit uses 0x80000 - 0xfffff
# if you plan to distribute the plug, get an ID from AD  
kPluginNodeId = OpenMaya.MTypeId(0x0) 

##########################################################
# Plug-in 
##########################################################
class myNode(OpenMayaMPx.MPxNode):
    # Static variables which will later be replaced by the node's attributes.
    input_value = OpenMaya.MObject()
    frequency = OpenMaya.MObject()
    scale = OpenMaya.MObject()
    out_sine = OpenMaya.MObject()
    
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
        
        if(plug == myNode.out_sine):
            
            # Obtain the data handles for each attribute
            input_data = data.inputValue(myNode.input_value)
            scale_data = data.inputValue(myNode.scale)
            frequency_data = data.inputValue(myNode.frequency)
            out_data = data.outputValue(myNode.out_sine)
            
            # Extract the actual value associated to our sample input attribute (we have defined it as a float)
            input_val = input_data.asFloat()
            scale_val = scale_data.asFloat()
            frequency_val = frequency_data.asFloat()

            # perform the desired computation
            #angle = 6.2831853 * (input_val/frequency_val)
            angle = (6.2831853 / frequency_val) * input_val
            sin_result = math.sin(angle) * scale_val
            
            # Set the output value.
            out_data.setFloat(sin_result)
            
            # Mark the output data handle as being clean; it need not be computed given its input.
            out_data.setClean()
             
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
    myNode.input_value = nAttr.create('input', 'in', kFloat, 0.0)
    nAttr.setWritable(True)
    nAttr.setStorable(True) 
    nAttr.setHidden(False)
    myNode.addAttribute(myNode.input_value)

    # frequency
    myNode.frequency = nAttr.create('frequency', 'fr', kFloat, 48.0)
    nAttr.setWritable(True)
    nAttr.setStorable(True) 
    nAttr.setHidden(False)
    nAttr.setMin(0.0001) 
    myNode.addAttribute(myNode.frequency)

    # scale
    myNode.scale = nAttr.create('scale', 'sc', kFloat, 10.0)
    nAttr.setWritable(True)
    nAttr.setStorable(True) 
    nAttr.setHidden(False)
    myNode.addAttribute(myNode.scale)
    
    #==================================
    # OUTPUT NODE ATTRIBUTE(S)
    #==================================
    myNode.out_sine = nAttr.create('outSine', 'o', kFloat)
    nAttr.setStorable(False)
    nAttr.setWritable(False)
    nAttr.setReadable(True)
    nAttr.setHidden(False)
    myNode.addAttribute(myNode.out_sine)
    
    #==================================
    # NODE ATTRIBUTE DEPENDENCIES
    #==================================
    # If sampleInAttribute changes, the sampleOutAttribute data must be recomputed.
    myNode.attributeAffects(myNode.input_value, myNode.out_sine)
    myNode.attributeAffects(myNode.frequency, myNode.out_sine)
    myNode.attributeAffects(myNode.scale, myNode.out_sine)
    
    
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