from maya import cmds

sel= cmds.ls(sl= True)

attr= "displayLocalAxis"

if len(sel) == 0:
    
    sel= cmds.ls()

for node in sel:
    
    if cmds.attributeQuery(attr, n= node, ex= True):
        
        cmds.setAttr('{0}.{1}'.format(node, attr), True)
