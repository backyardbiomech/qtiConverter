#!/usr/bin/env python3

'''
qtiConverterApp.py path/to/file -separator

Create QTI zip files from text files to import to Canvas as quizzes.

Inputs
------

ifile : string
        path to a properly formatted file containing questions and answers
separator : str, optional
            punctuation that separates question and answer numbers from the text. '.' (default) or ')'
            
Returns
-------
zip file : saves a compressed (zip) file containing all material that needs to be uploaded as a QTI file to Canvas
            
Notes
-----
Any images associated with questions or answers must be saved as separate files (jpg or png) in the same folder as the text file.
 
Formatting guidelines for questions are availabe in the README.md file and on Bitbucket.

Tested on macOS 10.12.6 and 10.13.6
Last edited 2018.10.23

Written by Brandon E. Jackson, Ph.D.
brandon.e.jackson@gmail.com
'''
import argparse
from pathlib import Path
import shutil
import zipfile
import re
import html
import re
import xml.etree.ElementTree as ET

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
      
class makeQti():
        def __init__(self, ifile, sep):
            ifile = ifile.replace('\ ', ' ')
            print(ifile)
            self.ifile = Path(ifile)
            # initialize variables
            # get path to folder containing text questions and images
            self.fpath = self.ifile.parent #self.ifile.rsplit('/',1)[0] + '/'
            self.sep = sep
            # make the outputfile and question bank name based on the input file
            self.bankName = str(self.ifile.name)[0:-4]
            # make a new directory within the current to contain the new files
            self.newDirPath = self.fpath / (self.bankName + '_export')
            self.newDirPath.mkdir(exist_ok = True)
            #self.newDirPath will contain images, imsmanifest.xml, and a folder that contains the main xml file
            # make that folder
            self.newXmlPath = self.newDirPath / self.bankName
            self.newXmlPath.mkdir(exist_ok = True)
            # set the path of the new text file
            self.outFile = self.newXmlPath / self.bankName
            self.outFile = self.outFile.with_suffix('.xml')
            # set the path of the manifest file in the root folder self.newDirPath
            self.manFile = self.newDirPath / 'imsmanifest.xml'
            # initialize some blank strings
            self.header = ''
            self.footer = ''
            self.mainText = ''
            self.manHeader = ''
            self.manFooter = ''
            self.manMainText = ''
            # initialize a blank list to hold all of the questions and answers from the file
            self.data = []
            # XML identifiers, don't think these actually matter
            self.assessID = 'assessID'
            # Initialize a list of question types
            self.typeList = ['MC', 'MA', 'MT', 'SA', 'MD', 'MB', 'ES', 'TX']
            self.typeDict = {'MC':'multiple_choice_question', 'MA':'multiple_answers_question', 'SA': 'short_answer_question', 'ES': 'essay_question', 'MB': 'fill_in_multiple_blanks_question', 'MD': 'multiple_dropdowns_question', 'MT': 'matching_question'}
            # Initialize a counting variable to count images
            self.imNum = 0
            
                   
        def run(self):
            #make the header
            self.makeHeader()
            #make the footer
            self.makeFooter()
            
            # open the output files and write the headers
            with self.outFile.open('w') as f:
                f.write(self.header + '\n')
            with self.manFile.open('w') as f:
                f.write(self.manHeader + '\n')
            
            # open the input file and read in the data to self.data
            self.loadBank()
            # parse the questions in a loop
            for q in range(len(self.data)):
                self.imagePath = ''
                # parse the questions and answers based on new lines  
                # self.fullText is a list, each item is a line from the question in the text file
                self.fullText = self.data[q].split('\n')
                # delete any blank linesin fullText (should only happen on the last question)
                self.fullText = [x for x in self.fullText if len(x) > 0]
                # convert Markdown formatting to html formatting before escaping html
                # bold
                # replace characters with html appropriate characters
                self.fullText = [html.escape(x) for x in self.fullText]
                self.questionType = self.fullText[0]
                # if not question type is indicated, assume multiple choice
                if self.questionType not in self.typeList:
                    self.questionType = 'MC'
                # if question type was indicated, delete that line for now
                else:
                    self.fullText = self.fullText[1:]
                # check to see if an image is included
                if self.fullText[0][0:5] == 'image':
                    # add to the image count
                    self.imNum += 1
                    # set imagePath and remove all spaces from either end of the file name
                    self.imagePath = self.fullText[0].split(':')[1].strip()
                    # remove that line so that only questions and answers remain
                    self.fullText = self.fullText[1:]
                    # copy the image
                    imgPath = self.fpath / self.imagePath
                    shutil.copy(str(imgPath), str(self.newDirPath))
                    # add the info to the manifest file
                    self.addResMan(self.imagePath)
                # self.fullText is a list, now the first item is the question, rest are the answers
                else:
                    self.imagePath = ''
                # parse the question based on type
                self.qNumber= q
                # get the question type and parse it
                self.typeChooser()
                # write the question and answers to the file
                with self.outFile.open(mode = 'a', encoding = "utf-8") as f:
                    f.write(self.writeText + '\n')
            with self.outFile.open('a') as f:
                f.write(self.footer)
            with self.manFile.open('a') as f:
                f.write(self.manFooter)
            
            #import with xml parser, clean up, export
            
            ET.register_namespace("", "http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1")
            tree = ET.parse(str(self.manFile))
            root = tree.getroot()
            indent(root)
            mydata = ET.tostring(root, encoding='utf8').decode('utf8')
            myfile = open(str(self.manFile), 'w')
            myfile.write(mydata)
            myfile.close()
            
            ET.register_namespace("", "http://www.imsglobal.org/xsd/ims_qtiasiv1p2")
            tree = ET.parse(str(self.outFile))
            root = tree.getroot()
            mydata = ET.tostring(root, encoding='utf8').decode('utf8')
            myfile = open(str(self.outFile), 'w')
            myfile.write(mydata)
            myfile.close()
            
            # compress the folder    
            shutil.make_archive(str(self.newDirPath), 'zip', str(self.newDirPath))
            #remove the now compressed folder
            shutil.rmtree(str(self.newDirPath))


            
        def typeChooser(self):
            '''
            Choose the question parser based on the question type
            '''
            if self.questionType == 'MC': # multiple choice with one answer
                self.parseMC()
            if self.questionType == 'MA': # multiple choice with more than one answer
                self.parseMC()
            if self.questionType == 'SA':
                self.parseSA()
            if self.questionType == 'ES':
                self.parseES()
            if self.questionType == 'MB':
                self.parseMB()
            if self.questionType == 'MD':
                self.parseMD()
            if self.questionType == 'MT':
                self.parseMT()
            # add other question types here
        
        def processFormatting(self, text):
            # process markdown characters
            # process bold
            text = re.sub('(\*{2}([a-zA-Z0-9\s]+)\*{2})', ' <strong>\\2</strong> ', text)
            # process italics
            text = re.sub('(\*{1}([a-zA-Z0-9\s]+)\*{1})', ' <em>\\2</em> ', text)
            # process superscript
            text = re.sub('(\^{1}([a-zA-Z0-9\s]+)\^{1})', ' <sup>\\2</sup> ', text)
            # process subscript
            text = re.sub('(\~{1}([a-zA-Z0-9\s]+)\~{1})', ' <sub>\\2</sub> ', text)
            # escape html characters
            text = html.escape(text)
            # return
            return text
            
        def parseMT(self):
            quest = self.fullText[0].split(self.sep, 1) [1].strip()
            quest = self.processFormatting(quest)
            # make an identifier for the question
            itid = str(self.questionType) + str(self.qNumber)
            # build the question text
            questionTextStart = self.questionText(quest, itid)
            '''
            answer format is 
            MT
            1. This is a matching question.
            [right2]left1: first left option
            [right2]left2: second left option
            [right1]left3: third left option
            right1: first right option correct for third left
            right2: second right option correct for first and second left
            right3: third right option correct for first and second left
            right4: fourth right option distractor
            right5: fifth right option distractor
            '''
            #initialize a dict to hold matches, each left entry is a dict format will be leftAns[respID] = {'text': 'left side text', 'corr': 'rightRespId'}, each right entry is rightAns[rightRespId] = {'text' : 'right side text'}
            leftAns = {}
            rightAns = {}
            #parse through the lines after the question text
            for a in range(1, len(self.fullText)):
                line = self.fullText[a].split(':',1)
                #if the line begins with a bracket, it is a left answer
                if line[0][0] == '[':
                    #get the name of the answer (between the ] and the :
                    leftName = line[0].split(']',1)[1]
                    #get the number in the bracket corresponding to the correct answer
                    corrNum = re.findall(r'\[(\w+)\]', line[0])
                    #assign to the dict
                    leftAns[leftName] = {'text': self.processFormatting(line[1]), 'corr': corrNum[0]}
                #otherwise, it is a right answer
                else:
                    rightRespId = line[0]
                    rightAns[rightRespId] = {'text': self.processFormatting(line[1])}
            # generate the responses
            questionTextResponse = ''
            for leftID, leftData in leftAns.items():
                questionTextResponse += '''<response_lid ident="{}">
                <material>
                  <mattext texttype="text/html">{}</mattext>
                </material>
                <render_choice>
                    '''.format(leftID, leftData['text'])
                # loop through right side answers
                for rightID, rightData in rightAns.items():
                    questionTextResponse += '''<response_label ident="{}">
                        <material>
                          <mattext>{}</mattext>
                        </material>
                      </response_label>
                    '''.format(rightID, rightData['text'])
                #close off that left side response
                questionTextResponse += '''</render_choice>
                                        </response_lid>
                                        '''
            # close off the question part
            questionTextResponse += '''</presentation>
                <resprocessing>
                  <outcomes>
                    <decvar maxvalue="100" minvalue="0" varname="SCORE" vartype="Decimal"/>
                  </outcomes>'''
            #get the score per left side
            perLeft = 100/len(leftAns)
            #add the score calculations for each drop
            for leftAns, leftData in leftAns.items():
                corrRespId = leftData['corr']
                questionTextResponse += '''<respcondition>
                    <conditionvar>
                      <varequal respident="{}">{}</varequal>
                    </conditionvar>
                    <setvar varname="SCORE" action="Add">{}</setvar>
                  </respcondition>
                    '''.format(leftAns, corrRespId, perLeft)
            # close it out
            questionTextResponse += '''</resprocessing>
                                      </item>'''
            # write it
            self.writeText = questionTextStart + questionTextResponse
            
                                          
            
        def parseMD(self):
            quest = self.fullText[0].split(self.sep, 1) [1].strip()
            quest = self.processFormatting(quest)
            # make an identifier for the question
            itid = str(self.questionType) + str(self.qNumber)
            # build the question text
            questionTextStart = self.questionText(quest, itid)
            # parse through the question looking for drop names surrounded by []
            dropNames = re.findall(r'\[(\w+)\]', quest)
            #format should be *drop1: correct answer for 1 \n
            # initizaliz a dict to hold all answers dropAns[dropName] = {'respID': 'response text', 'corr': 'respID'}
            dropAns = {}
            #loop through drop names
            for dropName in dropNames:
                dropAns[dropName] = {}
            #loop through line of answers
            for a in range(1, len(self.fullText)):
                line = self.fullText[a].split(':',1)
                respID = 'resp' + str(a)
                if line[0][0] == '*':
                    # remove the *
                    line[0] = line[0][1:]
                    dropAns[line[0]]['corr'] = respID
                    
                dropAns[line[0]][respID] = self.processFormatting(line[1])
            # generate the responses
            questionTextResponse = ''
            #loop back through dropAns dict to make the answers
            
            for dropName, resp in dropAns.items():
                # parse the first part fo the responses
                questionTextResponse += '''<response_lid ident="{}">
                                                <material>
                                                  <mattext>{}</mattext>
                                                </material>
                                                <render_choice>
                                                    '''.format('response_' + dropName, dropName)
                #loop through responses for that drop
                for respID, respText in resp.items():
                    # if the item is a response (and not the correct indicator)
                    if 'resp' in respID:       
                        # parse the response
                        questionTextResponse += '''<response_label ident="{}">
                                                    <material>
                                                      <mattext texttype="text/html">{}</mattext>
                                                    </material>
                                                  </response_label>
                        '''.format(respID, respText)
                questionTextResponse += '''</render_choice>
                                      </response_lid>
                                            '''
            questionTextResponse += '''</presentation>
                                        <resprocessing>
                                          <outcomes>
                                            <decvar maxvalue="100" minvalue="0" varname="SCORE" vartype="Decimal"/>
                                          </outcomes>
            '''
            #get the score per drop
            perDrop = 100/len(dropAns)
            #add the score calculations for each drop
            
            for dropName, resp in dropAns.items():
                
                corrRespID = dropAns[dropName]['corr']
                questionTextResponse += '''<respcondition>
                                            <conditionvar>
                                              <varequal respident="{}">{}</varequal>
                                            </conditionvar>
                                            <setvar varname="SCORE" action="Add">{}</setvar>
                                          </respcondition>
                '''.format('response_' + dropName, corrRespID, perDrop)
            # close it out
            questionTextResponse += '''</resprocessing>
                                      </item>'''
            # write it
            self.writeText = questionTextStart + questionTextResponse
                
        def parseMB(self):
            quest = self.fullText[0].split(self.sep, 1) [1].strip()
            quest = self.processFormatting(quest)
            # make an identifier for the question
            itid = str(self.questionType) + str(self.qNumber)
            # build the question text
            questionTextStart = self.questionText(quest, itid)
            # parse through the question looking for blank names surrounded by []
            blankNames = re.findall(r'\[(\w+)\]', quest)
            #loop through each blank answer
            # format should be blank1: answer 1, answer 2 \n
            blankCorr = {}
            for a in range(1, len(self.fullText)):
                ans = []
                #get the blank name and a list of answers
                bName = self.fullText[a].split(':',1)[0]
                ans = self.fullText[a].split(':',1)[1].split(',')
                ans = [x.strip() for x in ans]
                ans = [self.processFormatting(x) for x in ans]
                # put into dict
                blankCorr[bName] = ans
            questionTextResponse = ''
            for blank, ans in blankCorr.items():
                questionTextResponse += '''<response_lid ident="{}">
                                        <material>
                                            <mattext>{}</mattext>
                                        </material>
                                        <render_choice>
                                        '''.format(blank,blank)
                for i in range(len(ans)):
                    resID = 'resp'+str(i)
                    questionTextResponse += '''<response_label ident="{}">
                                                <material>
                                                    <mattext texttype="text/html">{}</mattext>
                                                </material>
                                            </response_label>
                                            '''.format(resID, ans[i])
            
                questionTextResponse +=''' </render_choice>
                                        </response_lid>
                                        '''
            #get the score per blank
            perBlank = 100/len(blankCorr)
            questionTextResponse += '''</presentation>
            <resprocessing>
                <outcomes>
                    <decvar maxvalue="100" minvalue="0" varname="SCORE" vartype="Decimal"/>
                </outcomes>
            '''
            for blank,ans in blankCorr.items():
                questionTextResponse += '''<respcondition>
                                        <conditionvar>
                                            <varequal respident="{}">{}</varequal>
                                        </conditionvar>
                                        <setvar varname="SCORE" action="Add">{}</setvar>
                                    </respcondition>
                '''.format(blank,'resp0',perBlank)
            questionTextResponse += '''</resprocessing>
                        </item>
                        '''
            self.writeText = questionTextStart + questionTextResponse 
            
        def parseES(self):
            quest = self.fullText[0].split(self.sep, 1) [1].strip()
            quest = self.processFormatting(quest)
            # make an identifier for the question
            itid = str(self.questionType) + str(self.qNumber)
            # build the question text
            questionTextStart = self.questionText(quest, itid)
            questionTextResponse = '''<response_str ident="response1" rcardinality="Single">
                                    <render_fib>
                                        <response_label ident="answer1" rshuffle="No"/>
                                    </render_fib>
                                </response_str>
                            </presentation>
                            <resprocessing>
                                <outcomes>
                                    <decvar maxvalue="100" minvalue="0" varname="SCORE" vartype="Decimal"/>
                                </outcomes>
                                <respcondition continue="No">
                                    <conditionvar>
                                        <other/>
                                    </conditionvar>
                                </respcondition>
                            </resprocessing>
                        </item>
                        '''
            self.writeText = questionTextStart + questionTextResponse
            
        def parseSA(self):
            quest = self.fullText[0].split(self.sep, 1) [1].strip()
            quest = self.processFormatting(quest)
            corr = []
            # make a list of correct answers
            for a in range(1, len(self.fullText)):
                answer = self.processFormatting(self.fullText[a].split(self.sep,1)[1])
                corr.append(answer)
            # make an identifier for the question
            itid = str(self.questionType) + str(self.qNumber)
            # build the question text
            questionTextStart = self.questionText(quest, itid)
            questionTextResponse = '''<response_str ident="response1" rcardinality="Single">
                                    <render_fib>
                                        <response_label ident="answer1" rshuffle="No"/>
                                    </render_fib>
                                </response_str>
                            </presentation>
                            <resprocessing>
                                <outcomes>
                                    <decvar maxvalue="100" minvalue="0" varname="SCORE" vartype="Decimal"/>
                                </outcomes>
                                <respcondition continue="No">
                                    <conditionvar>
                                    '''
            for ans in corr:
                questionTextResponse +='''<varequal respident="response1">{}</varequal>
                '''.format(ans)
            questionTextResponse += '''</conditionvar>
                                    <setvar action="Set" varname="SCORE">100</setvar>
                                </respcondition>
                            </resprocessing>
                        </item>
                        '''
            self.writeText = questionTextStart + questionTextResponse
                      
        def parseMC(self):
            quest = self.fullText[0].split(self.sep, 1)[1].strip()
            quest = self.processFormatting(quest)
            answers = []
            corr = []
            # make a list of answers
            for a in range(1,len(self.fullText)):
                ans = self.fullText[a].strip()
                # get the correct answer
                if ans[0] == '*':
                    corr.append(str(a))
                answer = self.processFormatting(ans.split(self.sep, 1)[1][1:])
                answers.append(answer)
            # make an identifier for the question
            itid = str(self.questionType) + str(self.qNumber)
            # build the question text
            questionTextStart = self.questionText(quest, itid)
            questionTextResponse = self.questionTextResponses(answers, corr)
            self.writeText = questionTextStart + questionTextResponse
            
        def questionTextResponses(self, answers, corr):
            # set some strings based on question type
            if self.questionType == 'MC':
                respid = 'response1'
                rcard = 'Single'
            if self.questionType == 'MA':
                respid = 'response1'
                rcard = 'Multiple'
            out1 = '''
            <response_lid ident="{}" rcardinality="{}">
              <render_choice>
            '''.format(respid, rcard,)
            #loop through answers and add
            respList=[]
            for a in range(len(answers)):
                #make a string to track which answer is which
                resp = str(a+1)
                out1 += ''' <response_label ident="{}">
                        <material>
                          <mattext texttype="text/html">{}</mattext>
                        </material>
                        </response_label>
                        '''.format(resp, answers[a])
                respList.append(resp)
            # done with answers, add stuff for end of question
            out1 += '''</render_choice>
                  </response_lid>
                </presentation>
                <resprocessing>
                  <outcomes>
                    <decvar maxvalue="100" minvalue="0" varname="SCORE" vartype="Decimal"/>
                  </outcomes>
                  <respcondition continue="No">
                    <conditionvar>
                    '''
            if len(corr) == 1:
            #single answer multiple choice
                out1 += '''<varequal respident="{}">{}</varequal>
                      '''.format(respid, corr[0])
            if len(corr) > 1: #more than one correct answer
                out1 += '''<and>
                '''
                for ans in range(len(corr)):
                    out1 += '''<varequal respident="{}">{}</varequal>
                    '''.format(respid, corr[ans])
                    respList.remove(corr[ans])
                if len(respList) > 0:
                    out1 += '''<not>
                    '''
                    for ans in range(len(respList)):
                      out1 += '''<varequal respident="{}">{}</varequal>
                      '''.format(respid, respList[ans])
                    out1 += '''</not>
                    '''
                out1 += '''</and>
                '''
            # final bits
            out1 += '''</conditionvar>
                    <setvar action="Set" varname="SCORE">100</setvar>
                  </respcondition>
                </resprocessing>
              </item>
              '''
            return out1
            
        def questionText(self, quest, itid):
            # build the text for each question, starting with a question "header"
            # if there is an associated image, add it above the question text
            if len(self.imagePath) > 0:
                quest = '''&lt;img src="%24IMS-CC-FILEBASE%24/{}" width="314" /&gt;
                &lt;p&gt;{}&lt;/p&gt;
                '''.format(self.imagePath, quest)
            
            out1 = '''
            <item ident="{}" title="Question">
                <itemmetadata>
                  <qtimetadata>
                    <qtimetadatafield>
                      <fieldlabel>question_type</fieldlabel>
                      <fieldentry>{}</fieldentry>
                    </qtimetadatafield>
                    <qtimetadatafield>
                      <fieldlabel>points_possible</fieldlabel>
                      <fieldentry>1.0</fieldentry>
                    </qtimetadatafield>
                    <qtimetadatafield>
                      <fieldlabel>assessment_question_identifierref</fieldlabel>
                      <fieldentry>i29529708ad95a6ff171e20abdfa2a8d9</fieldentry>
                    </qtimetadatafield>
                  </qtimetadata>
                </itemmetadata>
                <presentation>
                  <material>
                      <mattext texttype="text/html">{}</mattext>
                  </material>
                  '''.format(itid, self.typeDict[self.questionType],quest)
            return out1    
                
        def loadBank(self):
            with self.ifile.open(mode = 'r', encoding = "utf-8") as f:
                data=f.read()
            data = re.sub('\n{3,100}', '\n\n', data.strip())
            self.data=data.split('\n\n')
        
        def addResMan(self, img):    
            out1 = '''<resource identifier="{}" type="webcontent" href="{}">
            <file href="{}"/>
        </resource>
            '''.format('pic'+ str(self.imNum), img, img)
            #write to the manifest file
            with self.manFile.open(mode = 'a', encoding = "utf-8") as f:
                f.write(out1)
            
        def makeHeader(self):
            # make the header for the main xml file
            self.header = '''<?xml version="1.0" encoding="UTF-8"?>
<questestinterop xmlns="http://www.imsglobal.org/xsd/ims_qtiasiv1p2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.imsglobal.org/xsd/ims_qtiasiv1p2 http://www.imsglobal.org/xsd/ims_qtiasiv1p2p1.xsd">
              <assessment ident="{}" title="{}">
                <qtimetadata>
                  <qtimetadatafield>
                    <fieldlabel>cc_maxattempts</fieldlabel>
                    <fieldentry>1</fieldentry>
                  </qtimetadatafield>
                </qtimetadata>
                <section ident="root_section">
            '''.format(self.assessID, self.bankName)
            
            #make the header for the manifest file
            self.manHeader = '''<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="i595177d21a726452731ea55437e4c4d4" xmlns="http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1" xmlns:lom="http://ltsc.ieee.org/xsd/imsccv1p1/LOM/resource" xmlns:imsmd="http://www.imsglobal.org/xsd/imsmd_v1p2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1 http://www.imsglobal.org/xsd/imscp_v1p1.xsd http://ltsc.ieee.org/xsd/imsccv1p1/LOM/resource http://www.imsglobal.org/profile/cc/ccv1p1/LOM/ccv1p1_lomresource_v1p0.xsd http://www.imsglobal.org/xsd/imsmd_v1p2 http://www.imsglobal.org/xsd/imsmd_v1p2p2.xsd">
  <metadata>
    <schema>IMS Content</schema>
    <schemaversion>1.1.3</schemaversion>
  </metadata>
  <organizations/>
  <resources>
    <resource identifier="{}" type="imsqti_xmlv1p2">
      <file href="{}"/>
    </resource>'''.format(self.bankName, self.outFile.parent.name + '/' + self.outFile.name)

        def makeFooter(self):
            self.footer = '''
                </section>
              </assessment>
            </questestinterop>
            '''
            
            self.manFooter = '''</resources>
</manifest>
'''
        
if __name__=="__main__":
    parser = argparse.ArgumentParser(description="import text file to export QTI for Canvas Quiz import",epilog=__doc__)
    parser.add_argument("ifile",default=None,
                        help="txt file path and name to process")
    parser.add_argument("--separator", default='.',
                        help="string indicating separator between question/answer number/letter and text, usually '.' or ')'")
    
    args = parser.parse_args()
    inputFile=args.ifile
    sep = args.separator
    doIt = makeQti(inputFile, sep)
    doIt.run()