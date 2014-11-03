import maya.api.OpenMaya as om
import pymel.core as pm

rot_order = 0

kRotateOrders = [om.MEulerRotation.kXYZ,
                om.MEulerRotation.kYZX,
                om.MEulerRotation.kZXY,
                om.MEulerRotation.kXZY,
                om.MEulerRotation.kYXZ,
                om.MEulerRotation.kZYX]

def position_nodes(top_obj, btm_obj):
 
    m_top = om.MMatrix(top_obj.getMatrix())
    m_btm = om.MMatrix(btm_obj.getMatrix())
    
    #tm_top = om.MTransformationMatrix(m_top)
    #tm_btm = om.MTransformationMatrix(m_btm)
    
    #top_vec = tm_top.translation(om.MSpace.kWorld)
    #btm_vec = tm_btm.translation(om.MSpace.kWorld)
    
    top_vec = om.MVector(m_top.getElement(3,0), m_top.getElement(3,1), m_top.getElement(3,2))
    btm_vec = om.MVector(m_btm.getElement(3,0), m_btm.getElement(3,1), m_btm.getElement(3,2))
      
    top_aim_v = top_vec - btm_vec
    btm_aim_v = top_aim_v
    #mid_point = aim_v*.5 + btm_vec
    
    
    ################
    # TOP
    ################
    
    # use x axis as up
    top_up_vn = om.MVector(m_top.getElement(0,0), m_top.getElement(0,1), m_top.getElement(0,2)).normal()
    
    top_aim_vn = top_aim_v.normal()
    top_cross_vn = top_aim_vn ^ top_up_vn
    top_up_ortho_n = top_cross_vn ^ top_aim_vn
    
    top_rot_m = om.MMatrix([top_up_ortho_n.x, top_up_ortho_n.y, top_up_ortho_n.z, 0,
                        top_aim_vn.x, top_aim_vn.y, top_aim_vn.z, 0,
                        top_cross_vn.x, top_cross_vn.y, top_cross_vn.z, 0,
                        0,0,0,1])
                                
    top_rot_tm = om.MTransformationMatrix(top_rot_m)
    
    # get the euler angles, rotation order
    top_rot = top_rot_tm.rotation().reorder(kRotateOrders[rot_order])
        
    
    ################
    # BTM
    ################
    
    # use x axis as up
    btm_up_vn = om.MVector(m_btm.getElement(0,0), m_btm.getElement(0,1), m_btm.getElement(0,2)).normal()
    
    btm_aim_vn = btm_aim_v.normal()
    btm_cross_vn = btm_aim_vn ^ btm_up_vn
    btm_up_ortho_n = btm_cross_vn ^ btm_aim_vn
    
    btm_rot_m = om.MMatrix([btm_up_ortho_n.x, btm_up_ortho_n.y, btm_up_ortho_n.z, 0,
                        btm_aim_vn.x, btm_aim_vn.y, btm_aim_vn.z, 0,
                        btm_cross_vn.x, btm_cross_vn.y, btm_cross_vn.z, 0,
                        0,0,0,1])
                                
    btm_rot_tm = om.MTransformationMatrix(btm_rot_m)
    
    # get the euler angles, rotation order
    btm_rot = btm_rot_tm.rotation().reorder(kRotateOrders[rot_order])
    
    
    
    # return info
    top_pos = (top_vec.x, top_vec.y, top_vec.z)
    top_rot = (top_rot.x, top_rot.y, top_rot.z)
    
    btm_pos = (btm_vec.x, btm_vec.y, btm_vec.z)
    btm_rot = (btm_rot.x, btm_rot.y, btm_rot.z)
    
    
    ret_dict = {'top_pos':top_pos, 'top_rot':top_rot, 'btm_pos':btm_pos, 'btm_rot':btm_rot}
    
    return ret_dict


top_ctrl = pm.PyNode('nurbsCircle1')
btm_ctrl = pm.PyNode('nurbsCircle2')
top_cube = pm.PyNode('pCube1')
btm_cube = pm.PyNode('pCube2')


t_info = position_nodes(top_ctrl, btm_ctrl)

top_cube.rotate.set(pm.util.degrees(t_info.get('top_rot')))
top_cube.translate.set(t_info.get('top_pos'))

btm_cube.rotate.set(pm.util.degrees(t_info.get('btm_rot')))
btm_cube.translate.set(t_info.get('btm_pos'))




