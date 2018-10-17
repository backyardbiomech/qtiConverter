import xml.etree.ElementTree as ET

'''
Making an xml like below
<data>  
    <items>
        <item name="item1">item1abc</item>
        <item name="item2">item2abc</item>
    </items>
</data>  


# create the file structure
data = ET.Element('data')  
items = ET.SubElement(data, 'items')  
item1 = ET.SubElement(items, 'item')  
item2 = ET.SubElement(items, 'item')  
item1.set('name','item1')  
item2.set('name','item2')  
item1.text = 'item1abc'  
item2.text = 'item2abc'

# create a new XML file with the results
mydata = ET.tostring(data)  
myfile = open("items2.xml", "w")  
myfile.write(mydata) 
'''

def indent(elem, level=0):
  i = "\n" + level*"  "
  if len(elem):
    if not elem.text or not elem.text.strip():
      elem.text = i + "  "
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
    for elem in elem:
      indent(elem, level+1)
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
  else:
    if level and (not elem.tail or not elem.tail.strip()):
      elem.tail = i


attrib = {'xmlns':"http://www.imsglobal.org/xsd/ims_qtiasiv1p2", 'xmlns:xsi':"http://www.w3.org/2001/XMLSchema-instance", 'xsi:schemaLocation':"http://www.imsglobal.org/xsd/ims_qtiasiv1p2 http://www.imsglobal.org/xsd/ims_qtiasiv1p2p1.xsd"}
root = ET.Element('questestinterop', attrib)

attrib = {'ident':"i96e822e31f75ab7b85b25901c6d68ef8", 'title':"import quiz with image"}
assessment = ET.SubElement(root, 'assessment', attrib)

qtimetadata = ET.SubElement(assessment, 'qtimetadata')
qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
fieldlabel.text = 'cc_maxattempts'
fieldentry = ET.SubElement(fieldlabel, 'fieldentry')
fieldentry.text = '1'

indent(root)

mydata = ET.tostring(root, encoding='utf8').decode('utf8')

myfile = open('testXML.xml', 'w')
myfile.write(mydata)
