#!/usr/bin/env python3

"""
qtiConverterApp.py path/to/file

Create QTI zip files from text files to import to Canvas as quizzes.

Inputs
------

ifile : string
        path to a properly formatted file containing questions and answers
            
Returns
-------
zip file : saves a compressed (zip) file containing all material that needs to be uploaded as a QTI file to Canvas
            
Notes
-----
Any associated images must be saved as separate files (jpg or png) in the same folder as the text file.
 
Formatting guidelines for questions are availabe in the README.md file and on Bitbucket.

Tested on macOS 10.12.6 and 10.13.6 and 14.4.1, 15.3.2
Last edited 2025.04.20

Written by Brandon E. Jackson, Ph.D.
brandon.e.jackson@gmail.com
"""


import argparse
from pathlib import Path
import shutil
import zipfile
import re
import html
import re
import xml.etree.ElementTree as ET
import subprocess
import urllib.parse
import sys
import uuid


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

def errorNoImage(q):
    applescript = """
    display dialog "No image was found for the {}th question in the list. Check the name in the document and make sure the file is in the correct folder."
    """.format(str(q))
    if sys.platform == 'darwin':
        subprocess.call("osascript -e '{}'".format(applescript), shell=True)
    else:
        print(applescript)

def errorDisplay(q, qtext):
    applescript = """
    display dialog "There seems to be a formatting problem with the {}th question in the list: {}. Fix the question and rerun this program."
    """.format(str(q), qtext)
    if sys.platform == 'darwin':
        subprocess.call("osascript -e '{}'".format(applescript), shell=True)
    else:
        print(applescript)
    
def logDisplay():
    applescript = """
    display dialog "
    "
    """.format()
    if sys.platform == 'darwin':
        subprocess.call("osascript -e '{}'".format(applescript), shell=True)
    else:
        print(applescript)


class makeQti():
        def __init__(self, ifile, sep):
            ifile = ifile.replace(r'\ ', ' ')
            self.ifile = Path(ifile)
            # initialize variables
            # get path to folder containing text questions and images
            self.fpath = self.ifile.parent
            self.sep = sep
            # make the outputfile and question bank name based on the input file
            self.bankName = str(self.ifile.name)[0:-4]
            # make a new directory within the current to contain the new files
            self.newDirPath = self.fpath / (self.bankName + '_export')
            self.newDirPath.mkdir(exist_ok = True)
            # make a new html file for a preview, inside the parent folder, but outside the export folder
            self.preview = self.fpath / (self.bankName + '_preview.html')
            # self.newDirPath will contain images, imsmanifest.xml, and a folder that contains the main xml file
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
            self.typeList = ['MC', 'MA', 'MT', 'SA', 'MD', 'MB', 'ES', 'NU', 'OR', 'TF', 'CT', 'HS']
            self.typeDict = {'MC':'multiple_choice_question', 'MA':'multiple_answers_question', 'SA': 'short_answer_question', 'ES': 'essay_question', 'MB': 'fill_in_multiple_blanks_question', 'MD': 'multiple_dropdowns_question', 'MT': 'matching_question', 'NU': 'numerical_question', 'OR': 'ordering_question', 'TF': 'true_false_question', 'CT': 'categorization_question', 'HS' : 'hot_spot_question'}
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
            with self.preview.open('w') as f:
                f.write('<p>This is just a preview!</n>\n')
            # open the input file and read in the data to self.data
            self.loadBank()
            # parse the questions in a loop
            for q in range(len(self.data)):
                self.qPts = '1'
                # advance the count and initialize things
                self.qNumber= q+1
                self.htmlText=''
                # parse the questions and answers based on new lines  
                # make self.fullText as a list, each item is a line from the question in the text file
                self.fullText = self.data[q].split('\n')                
                # delete any blank lines in fullText (should only happen on the last question)
                self.fullText = [x for x in self.fullText if len(x) > 0]
                # before escaping html characters, need to process any formulas
                self.fullText = self.processEquations(self.fullText)
                # replace characters with html appropriate characters
                #self.fullText = [html.escape(x) for x in self.fullText]
                # process the question header
                # sets self.imagePath, self.qPts, self.questionType, and calls self.processImage if needed to copy image to resources dir
                self.qHeader()

                # get the question type and parse it
#                 print(q)
#                 print(self.questionType)
                try:
                    self.typeChooser()
                except:
                    errorDisplay(self.qNumber, self.fullText)
                # write the question and answers to the file
                with self.outFile.open(mode = 'a', encoding = "utf-8") as f:
                    f.write(self.writeText + '\n')
                with self.preview.open(mode = 'a', encoding = "utf-8") as f:
                    f.write(self.htmlText + '\n')
            with self.outFile.open('a') as f:
                f.write(self.footer)
            with self.manFile.open('a') as f:
                f.write(self.manFooter)
            
            #import with xml parser, clean up, export
            
            ET.register_namespace("", "http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1")
            tree = ET.parse(str(self.manFile))
            root = tree.getroot()
            indent(root)
            #mydata = ET.tostring(root, encoding='utf8').decode('utf8')
            mydata = ET.tostring(root).decode()
            myfile = open(str(self.manFile), 'w')
            myfile.write(mydata)
            myfile.close()
            
            ET.register_namespace("", "http://www.imsglobal.org/xsd/ims_qtiasiv1p2")
            tree = ET.parse(str(self.outFile))
            root = tree.getroot()
            #mydata = ET.tostring(root, encoding='utf8').decode('utf8')
            mydata = ET.tostring(root).decode()
            myfile = open(str(self.outFile), 'w')
            myfile.write(mydata)
            myfile.close()
            
            # compress the folder    
            shutil.make_archive(str(self.newDirPath), 'zip', str(self.newDirPath))
            #remove the now compressed folder
            shutil.rmtree(str(self.newDirPath))
            #TODO:
            """
            generate a report that shows:
                the number of questions of each type
                the number of images (and a list of those images?)
                the number (and numbers of) of questions with no correct answer indicated
                if any MC questions had more than one correct answer and should be changed to MA
                
            """
        
        def qHeader(self):
            # search through question using regex to find anything before the question number self.fullText is a list with each item a new line of the text file

            # if it is a two letter capital abbreviation, that is question type, set self.questionType in self.typeList
            self.questionType = ''
            self.imagePath = ''
            self.qPts = '1'
            rws = 3
            try:
                for i in range(rws):
                    qType=re.findall(r'^\s*([A-Z]{2})\s*$', self.fullText[i])
                    if len(qType)==1 and qType[0] in self.typeList:
                        self.questionType = qType[0]
                        self.fullText.pop(i)
                        break
                if self.questionType not in self.typeList:
                    self.questionType = 'MC'
                rws -= 1
            except IndexError:
                print(self.fullText)
            # if it starts with image: that gives a link to the image, self.imagePath, advance self.imNum
            for i in range(3-rws):
                im = re.findall(r'^\s*image:\s*(.*)$', self.fullText[i])
                if len(im)==1:
                    self.imagePath = im[0]
                    self.processImage(self.imagePath)
                    self.fullText.pop(i)
                    break
                else:
                    self.imagePath = ''
            rws -= 1

            # if it is a number inside of parentheses, with or without letters, consider that pts per question
            for i in range(rws):
                pts = re.findall(r'^\(([\d\.]*)[\s\w]*\)$', self.fullText[i])
                if len(pts)==1:
                    self.qPts = pts[i]
                    self.fullText.pop(i)
                    break

        def processImage(self, imgpath):
            self.imNum += 1
            # get the full path to the image
            imgPath = self.fpath / imgpath
            # add error call if imagePath doesn't exist
            if not imgPath.exists():
                errorNoImage(self.qNumber)
            # copy the image file
            shutil.copy(str(imgPath), str(self.newDirPath))
            # add the info to the manifest file
            self.addResMan(imgpath)

        def typeChooser(self):
            '''
            Choose the question parser based on the question type
            '''
            if self.questionType == 'MC' or self.questionType == 'MA': # multiple choice with one answer
                self.parseMC()
#             if self.questionType == 'MA': # multiple choice with more than one answer
#                 print('or here')
#                 self.parseMC()
            if self.questionType == 'SA': # single fill in the blank
                self.parseSA()
            if self.questionType == 'ES': # essay
                self.parseES()
            if self.questionType == 'MB': # multiple fill in the blank
                self.parseMB()
            if self.questionType == 'MD': # multiple drop downs
                self.parseMD()
            if self.questionType == 'MT': # matching
                self.parseMT()
            if self.questionType == 'NU': # numerical question
                self.parseNU()
            if self.questionType == 'OR': # ordering question
                self.parseOR()
            if self.questionType == 'TF': # true false question
                self.parseTF()
            if self.questionType == 'CT': # categorization question
                self.parseCT()
            if self.questionType == 'HS': # hotspot question
                self.parseHS()
            # add other question types here
        
        def processFormatting(self, text):
            # process markdown characters
            # process bold
            text = re.sub(r'(\*{2}([\W\w\s]+?)\*{2})', '<strong>\\2</strong>', text)
            # process italics
            text = re.sub(r'(\*{1}([\W\w\s]+?)\*{1})', '<em>\\2</em>', text)
            # process superscript
            text = re.sub(r'(\^{1}([\W\w\s]+?)\^{1})', '<sup>\\2</sup>', text)
            # process subscript
            text = re.sub(r'(\~{1}([\W\w\s]+?)\~{1})', '<sub>\\2</sub>', text)
            # escape html characters
            text = html.escape(text)
            # return
            return text
            
        def parseMT(self):
            quest = self.extractQuestionText(self.fullText[0])
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
            '''
            answer format is 
            MD  
            1. This is a multiple dropdown question. Here is the first [drop1] and here is another [drop2]. Notice the square brackets around the indicators (no spaces!).  
            *drop1: correct answer for 1  
            drop1: incorrect answer for 1  
            drop1: incorrect answer for 1  
            drop2: incorrect answer for 2  
            *drop2: correct answer for 2 
            '''
            quest = self.extractQuestionText(self.fullText[0])
            quest = self.processFormatting(quest)
            # make an identifier for the question
            itid = str(self.questionType) + str(self.qNumber)
            # build the question text
            questionTextStart = self.questionText(quest, itid)
            # parse through the question looking for drop names surrounded by []
            dropNames = re.findall(r'\[(\w+)\]', quest)
            #format should be *drop1: correct answer for 1 \n
            # initizalize a dict to hold all answers dropAns[dropName] = {'respID': 'response text', 'corr': 'respID'}
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
                # parse the first part of the responses
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
            #reformat answers to make html preview
            answers = []
            for dropName, resp in dropAns.items():
                ans = '{}: '.format(dropName)
                corrid = resp['corr']
                for respID, respText in resp.items():
                    if respID == corrid:
                        ans += 'CORRECT: {}, '.format(respText)
                    else:
                        ans += '{}, '.format(respText)
                answers.append(ans)
            corr = []
            self.htmlText = self.questionTextHtml(itid, quest, answers, corr)
            
        def parseMB(self):
            quest = self.extractQuestionText(self.fullText[0])
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
            #reformat answers to make html preview
            answers = []
            for blank, ans in blankCorr.items():
                answers.append('{}: {}'.format(blank, ans))
            corr = []
            self.htmlText = self.questionTextHtml(itid, quest, answers, corr)
            self.writeText = questionTextStart + questionTextResponse 
            
        def parseES(self):
            quest = self.extractQuestionText(self.fullText[0])
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
            #format for html preview
            corr = []
            answers = []
            self.htmlText = self.questionTextHtml(itid, quest, answers, corr)
            
        def parseTF(self):
            quest = self.extractQuestionText(self.fullText[0])
            quest = self.processFormatting(quest)
            answer = self.fullText[1].split(':',1)[1].strip().lower()
            # make an identifier for the question
            itid = str(self.questionType) + str(self.qNumber)
            # build the question text
            questionTextStart = self.questionText(quest, itid, )
            # build the responses
            questionTextResponse = f'''
                <response_lid ident="response1" rcardinality="Single">
                <render_choice>
                <response_label ident="true_choice">
                    <material>
                    <mattext texttype="text/html">True</mattext>
                    </material>
                </response_label>
                <response_label ident="false_choice">
                    <material>
                    <mattext texttype="text/html">False</mattext>
                    </material>
                </response_label>
                </render_choice>
            </response_lid>
            </presentation>
            <resprocessing>
            <outcomes>
                <decvar maxvalue="100" minvalue="0" varname="SCORE" vartype="Decimal"/>
            </outcomes>
            <respcondition continue="No">
                <conditionvar>
                <varequal respident="response1">{answer}_choice</varequal>
                </conditionvar>
                <setvar action="Set" varname="SCORE">100</setvar>
            </respcondition>
            </resprocessing>
        </item>
            '''
            self.writeText = questionTextStart + questionTextResponse
            #reformat answers to make html preview
            corr = []
            self.htmlText = self.questionTextHtml(itid, quest, [answer], corr)
            
        def parseHS(self):
            '''
            HS
            image: organs.jpg
            1. Click in the stomach.
            (0.5435323383084577, 0.6512261580381471)
            (0.503731343283582, 0.6557674841053588)
            (0.48134328358208955, 0.6748410535876476)
            (0.5074626865671642, 0.6875567665758402)
            (0.5758706467661692, 0.6939146230699365)
            '''
            quest = self.extractQuestionText(self.fullText[0])
            quest = self.processFormatting(quest)
            # make an idendifier for the question
            itid = str(self.questionType) + str(self.qNumber)
            # build the question text
            questionTextStart = self.questionText(quest, itid)
            #save rows of coordinates as a string if given as (x,y)
            if self.fullText[1].startswith('('):
                coordinates = []
                for line in self.fullText[1:]:
                    x, y = line.strip('()').split(',')
                    coordinates.append(f"{x.strip()},{y.strip()}")
                coordinates_str = ','.join(coordinates)
            # or if given as x,y,x,y,x,y...
            else:
                coordinates_str = self.fullText[1]
            
            # generate the responses
            questionTextResponse = f'''
            <render_hotspot>
                <material>
                  <matimage uri="$IMS-CC-FILEBASE$/Uploaded Media/{self.imagePath}"/>
                </material>
                <response_label ident="response1" rarea="bounded">{coordinates_str}</response_label>
              </render_hotspot>
            </response_xy>
          </flow>
        </presentation>
      </item>
            '''
            
            self.writeText = questionTextStart + questionTextResponse
            #reformat answers to make html preview
            corr = []
            answer=''
            self.htmlText = self.questionTextHtml(itid, quest, [answer], corr)

            
        def parseCT(self):
            '''
            CT
            1. This is a categorization question in new quizzes. Each category can have multiple answers, and you can include multiple distractors that should be left as uncategorized. Make sure that each line begins with the name for a category (and that spelling is exactly the same for the every entry for the same category) or distractor.
            first category name: an answer for first category name
            first category name: another answer for first category name
            second category name: an answer for another category
            second category name: another answer for the second category
            distractor: this answer doesn't go anywhere
            '''
            quest = self.extractQuestionText(self.fullText[0])
            quest = self.processFormatting(quest)
            # make an idendifier for the question
            itid = str(self.questionType) + str(self.qNumber)
            # build the question text
            questionTextStart = self.questionText(quest, itid)
            # need to pull category names and correct answers for each one, plus distractors
            #init a dict to hold category names and uuid cats[categoryName] = uuid
            cats = {}
            # initialize a dict to hold all answers catAns[categoryName] = {'respID': 'response text'}
            catAns = {}
            #loop through answers
            
            for a in range(1, len(self.fullText)):
                line = self.fullText[a].split(':', 1)
                respID = 'resp' + str(a)
                if line[0] not in cats:
                    cats[line[0]] = str(uuid.uuid4())
                if line[0] not in catAns:
                    catAns[line[0]] = {}
                catAns[line[0]][respID] = self.processFormatting(line[1])
            
            # generate the responses
            questionTextResponse = ''
            #loop through catAns dict to make the answers
            # each category gets all the reponses in the xml
            catscore = float(100 / (len(cats) - ('distractor' in cats)))
            
            for catName, catid in cats.items():
                if catName.lower().strip() == 'distractor':
                    continue
                
                questionTextResponse += f'''
                <response_lid ident="{catid}" rcardinality="Multiple">
                <material>
                    <mattext texttype="text/plain">{catName}</mattext>
                </material>
                <render_choice>
                '''
                #go through the options
                for cn, resps in catAns.items():
                    for rid, ans in resps.items():
                        questionTextResponse += f'''
                        <response_label ident="{rid}">
                            <material>
                            <mattext texttype="text/plain">{ans}</mattext>
                            </material>
                        </response_label>
                        '''
                
                questionTextResponse += f'''
                    </render_choice>
                </response_lid>
                '''
            questionTextResponse += f'''
            </presentation>
            <resprocessing>
            <outcomes>
                <decvar maxvalue="100" minvalue="0" varname="SCORE" vartype="Decimal"/>
            </outcomes>
            '''
            
            #set correct answers
            for cat, ans in catAns.items():
                if cat.lower().strip() == 'distractor':
                    continue
                
                questionTextResponse += f'''
                    <respcondition>
                        <conditionvar>
                        '''
                catid = cats[cat]
                for rid in ans.keys():
                    questionTextResponse += f'''
                            <varequal respident="{catid}">{rid}</varequal>
                            '''
                
                questionTextResponse += f'''
                    </conditionvar>
                        <setvar action="Add" varname="SCORE">{catscore}</setvar>
                    </respcondition>
                    '''
            questionTextResponse += f'''
            </resprocessing>
            </item>
            '''
            self.writeText = questionTextStart + questionTextResponse
            #reformat answers to make html preview
            answers = []
            for catName, resp in catAns.items():
                for rid, ans in resp.items():
                    answers.append(f'{catName}: {ans}')
            corr = []
            self.htmlText = self.questionTextHtml(itid, quest, answers, corr)
                
        def parseOR(self):
            '''
            OR
            1. This is an ordering question for new quizzes. It will show as a "top label", like "most superficial", a bottom label like "deepest", and a series of drag and drop options. They are simply put with numbers and order here.
            toplabel: most superficial
            1: epidermis
            2: dermis
            3: hypodermis
            bottomlabel: deepest
            '''
            quest = self.extractQuestionText(self.fullText[0])
            quest = self.processFormatting(quest)
            # make an idendifier for the question
            itid = str(self.questionType) + str(self.qNumber)
            # need to pull out toplabel and bottomlabel
            # also need to pull out ordered items and create unique ids for each in the form of 734b8158-6c33-4841-98a5-fe70f6718c40 which are needed in a few placees, and the text of each item
            anss = {}
            # make a list of ids just to make sure sorting stays consistent
            idslist = []
            for a in range(1, len(self.fullText)):
                line = self.fullText[a].split(':',1)
                ansid = 0
                if 'toplabel' in line[0]:
                    toplabel = line[1].strip()
                elif 'bottomlabel' in line[0]:
                    bottomlabel = line[1].strip()
                else:
                    #answers
                    ansid = str(uuid.uuid4())
                    anss[ansid] = line[1].strip()
                    idslist.append(ansid)
            # build the question text
            questionTextStart = self.questionText(quest, itid, orig_ans_ids = idslist)
            # build the responses
            questionTextResponse = f'''<response_lid ident="response1" rcardinality="Ordered">
            <render_extension>
              <material position="top">
                <mattext>{toplabel}</mattext>
              </material>
              <ims_render_object shuffle="No">
                <flow_label>
            '''
            for id in idslist:
                questionTextResponse += f'''<response_label ident="{id}">
                    <material>
                      <mattext texttype="text/html">&lt;p&gt;{anss[id]}&lt;/p&gt;</mattext>
                    </material>
                  </response_label>
                '''

            questionTextResponse += f'''</flow_label>
                </ims_render_object>
                <material position="bottom">
                    <mattext>{bottomlabel}</mattext>
                </material>
                </render_extension>
            </response_lid>
            </presentation>
            <resprocessing>
            <outcomes>
                <decvar defaultval="1" varname="ORDERSCORE" vartype="Integer"/>
            </outcomes>
            <respcondition continue="No">
                <conditionvar>
                '''
            
            for id in idslist:
                questionTextResponse += f'''<varequal respident="response1">{id}</varequal>
                '''
                
            questionTextResponse += f'''</conditionvar>
                <setvar action="Set" varname="SCORE">100</setvar>
                </respcondition>
                </resprocessing>
                </item>
            '''
            
            self.writeText = questionTextStart + questionTextResponse
            #reformat answers to make html preview
            answers = [toplabel]
            for i, id in enumerate(idslist):
                answers.append(f'{i}: {anss[id]}')
            answers.append(bottomlabel)
            corr = []
            self.htmlText = self.questionTextHtml(itid, quest, answers, corr)
            
        def parseSA(self):
            quest = self.extractQuestionText(self.fullText[0])
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
            #reformat answers to make html preview
            answers = corr
            corr = []
            self.htmlText = self.questionTextHtml(itid, quest, answers, corr)
            self.writeText = questionTextStart + questionTextResponse
                      
        def parseNU(self):
            # 1. question
            # ans: 5 (4.99, 5.01), or ans: 5.012 (3) 
            # that is the answer, with min and max, or if one letter, the number of significant digits required (Canvas allows students to not include trailing zeros)
            # can have multiple ans: lines per question
            # make the regex formula to get everything after a digit, then . or ), then zero to some spaces, then everything until the first answer, including new lines. group 1 is the question text
            qreg = re.compile(r'\d[\.|\)]\s{0,4}([\S\s]+?)$', re.M)

            # match in the full question
            fulltext = '\n'.join(self.fullText)
            qmatch = qreg.search(fulltext)
            # get the text of the question
            quest = qmatch.group(1)
            # regex to find lines beginning with ans: then a digit, then maybe something in parentheses. Will use findall
            # for each match, group 1 is the answer, group 3 is the info in parentheses (if it exists) not inclusive of the parentheses. Can split on ","
            areg = re.compile(r'^ans:\s{0,4}([\d|\,|\.]+)(\s{0,4}\((.+)\))?', re.M)
            ansmatch = re.finditer(areg, fulltext)
            answers = []
            


        def parseMC(self):
            #quest = self.fullText[0].split(self.sep, 1)[1].strip()
            # make the regex formula to get everything after a digit, then . or ), then zero to some spaces, then everything until the first answer, including new lines
            qreg = re.compile(r'^\d+(\.|\))\s{0,4}([\S\s]+?)(^\.*[A-Za-z]{1}(\.|\)))', re.M)
            # match in the full question
            fulltext = '\n'.join(self.fullText)
            qmatch = qreg.search(fulltext)
            # get the text of the question
            quest = qmatch.group(2)
            #get the end of the question
            qend = qmatch.span(2)[1]
            atext = fulltext[qend:]
            # make a list of answers
            # match regex based on newline to newline, with . or ) separator after letter or number
            areg = re.compile(r'(^(\*)*[A-Za-z]{1}(\.|\)))\s{0,4}([\S\s]+?)(^|$)', re.M)
            amatch = re.finditer(areg, atext)
            answers = []
            corr = []
            a = 1
            # print(self.questionType)
            for mat in amatch:
                if mat.group(2) is not None:
                    corr.append(str(a))
#                 print(mat.group(4))
                answer = self.processFormatting(mat.group(4))
                answers.append(answer)
                a+=1
            if len(corr) > 1:
                 self.questionType = 'MA'
            quest = self.processFormatting(quest)
            # make an identifier for the question
            itid = str(self.questionType) + str(self.qNumber)
            # build the question text
            questionTextStart = self.questionText(quest, itid)
            questionTextResponse = self.questionTextResponses(answers, corr)
            self.writeText = questionTextStart + questionTextResponse
            self.htmlText = self.questionTextHtml(itid, quest, answers, corr)
            
        def questionTextHtml(self, itid, quest, answers, corr):
            if len(self.imagePath) > 0:
                quest = '<img src="{}" style="max-width: 100%; height: 500px" /><p>{}</>'.format(self.imagePath, html.unescape(quest))
            out = '''
                <ul style="list-style-type:none;">
                <li>{}: {}
                <ol type="A">
                '''.format(itid, quest)
            for i in range(len(answers)):
                ans = answers[i]
                if str(i+1) in corr:
                    ans = 'CORRECT: ' + ans
                out += '''
                <li>{}</li>
                '''.format(html.unescape(ans))
            out += '''
                </ol></li>
                </ul>
                '''
            return out
            
            
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
                # check to see if it's an image
                im = re.findall(r'^\s*image:\s*(.*)$', answers[a])
                if len(im)==1:
                    self.respImagePath = im[0]
                    self.processImage(self.respImagePath)
                    answers[a] = '''&lt;img src="%24IMS-CC-FILEBASE%24/{}" style="max-width: 100%; height: 500px" /&gt;
                    '''.format(self.respImagePath)

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
                <presentation>
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
            
        def processEquations(self, fullData):
            # recieves a question block (a list of lines)
            # go through each line looking for $$...$$
            for i in range(len(fullData)):
                if re.search(r'\$\$.*\$\$', fullData[i], re.M) is not None:
                    # replace > and < with mathjax codes
                    fullData[i] = fullData[i].replace('<', r'\lt')
                    fullData[i] = fullData[i].replace('>', r'\gt')
                    fullData[i] = re.sub(r'\$\$(.*)\$\$', self.processEquation, fullData[i], re.M)
            return fullData
        
        def processEquation(self, eq):
            # receives mathjax/Latex style formula text with surrounding $$
            # returns only the html conversion of the equation
            # converts the equation into a <p><img... of the following format
            #&lt;p&gt;&lt;img class="equation_image" title="\frac{5}{2}" src="https://longwood.instructure.com/equation_images/%255Cfrac%257B5%257D%257B2%257D" alt="LaTeX: \frac{5}{2}" data-equation-content="\frac{5}{2}"&gt;&lt;/p&gt;
            # use regex to extract info between $$
            eqtext = eq.group(1)
            # need to convert symbols in equation to url symbols
            neweq = urllib.parse.quote(eqtext)
            # need to add the odd %25 to each encoded character
            neweq = neweq.replace('%', '%25')
            eqret=f'</p><p><img class="equation_image" title="{eqtext}" src="https://longwood.instructure.com/equation_images/{neweq}" alt="LaTeX: {eqtext}" data-equation-content="{eqtext}"></p><p>'
            return eqret

        def questionText(self, quest, itid, orig_ans_ids = None):
            # build the text for each question, starting with a question "header"
            # if there is an associated image, add it above the question text
            if len(self.imagePath) > 0 and self.questionType != 'HS':
                quest = f'''&lt;img src="%24IMS-CC-FILEBASE%24/{self.imagePath}" style="max-width: 100%; height: 500px" /&gt;
                &lt;p&gt;{quest}&lt;/p&gt;
                '''
            
            out1 = f'''
            <item ident="{itid}" title="Question">
                <itemmetadata>
                  <qtimetadata>
                    <qtimetadatafield>
                      <fieldlabel>question_type</fieldlabel>
                      <fieldentry>{self.typeDict[self.questionType]}</fieldentry>
                    </qtimetadatafield>
                    <qtimetadatafield>
                      <fieldlabel>points_possible</fieldlabel>
                      <fieldentry>{self.qPts}</fieldentry>
                    </qtimetadatafield>
                    '''
            if self.questionType == 'TF':
                out1 += f'''
                <qtimetadatafield>
                    <fieldlabel>original_answer_ids</fieldlabel>
                    <fieldentry>true_choice,false_choice</fieldentry>
                </qtimetadatafield>
                '''
                
            #this might be important for ordering questions
            if orig_ans_ids:
                out1 += f'''
                    <qtimetadatafield>
                        <fieldlabel>original_answer_ids</fieldlabel>
                        <fieldentry>{','.join(orig_ans_ids)}</fieldentry>
                    </qtimetadatafield>
                '''
                
            out1 += f'''
                    <qtimetadatafield>
                      <fieldlabel>assessment_question_identifierref</fieldlabel>
                      <fieldentry>i29529708ad95a6ff171e20abdfa2a8d9</fieldentry>
                    </qtimetadatafield>
                  </qtimetadata>
                </itemmetadata>
                '''
                
            if self.questionType == 'HS':
                out1 += f'''
                <presentation>
                <flow>
                    <response_xy ident="response1" rcardinality="Single" rtiming="No">
                    <material>
                        <mattext texttype="text/html">&lt;p&gt;{quest}&lt;/p&gt;</mattext>
                    </material>
                '''
            else:
                out1 += f'''<presentation>
                  <material>
                      <mattext texttype="text/html">&lt;div&gt;&lt;p&gt;{quest}&lt;/p&gt;&lt;/div&gt;</mattext>
                  </material>
                  '''
            return out1    
                
        def loadBank(self):
            with self.ifile.open(mode = 'r', encoding = "utf-8-sig") as f:
                data=f.read()
            # get rid of hidden spaces on new lines
            data = re.sub('\ +\n', '\n', data.strip(), flags=re.MULTILINE)
            # get rid of hidden tabs before new lines
            data = re.sub('\t+\n', '\n', data.strip(), flags=re.MULTILINE)
            # get rid of hidden spaces and tabsbefore lines
            data = re.sub('^[\ \t]+', '', data.strip(), flags=re.MULTILINE)
            # get rid of lines that begin with # as a comment indicator
            data = re.sub('^#.*$', '', data.strip(), flags=re.MULTILINE)
            # combine multiple new lines into just the needed two
            data = re.sub('\n{3,100}', '\n\n', data.strip(), flags=re.MULTILINE)
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
            self.header = f'''<?xml version="1.0" encoding="UTF-8"?>
<questestinterop xmlns="http://www.imsglobal.org/xsd/ims_qtiasiv1p2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.imsglobal.org/xsd/ims_qtiasiv1p2 http://www.imsglobal.org/xsd/ims_qtiasiv1p2p1.xsd">
              <assessment ident="{self.assessID}" title="{self.bankName}">
                <qtimetadata>
                  <qtimetadatafield>
                    <fieldlabel>cc_maxattempts</fieldlabel>
                    <fieldentry>1</fieldentry>
                  </qtimetadatafield>
                </qtimetadata>
                <section ident="root_section">
            '''
            
            #make the header for the manifest file
            self.manHeader = f'''<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="i595177d21a726452731ea55437e4c4d4" xmlns="http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1" xmlns:lom="http://ltsc.ieee.org/xsd/imsccv1p1/LOM/resource" xmlns:imsmd="http://www.imsglobal.org/xsd/imsmd_v1p2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1 http://www.imsglobal.org/xsd/imscp_v1p1.xsd http://ltsc.ieee.org/xsd/imsccv1p1/LOM/resource http://www.imsglobal.org/profile/cc/ccv1p1/LOM/ccv1p1_lomresource_v1p0.xsd http://www.imsglobal.org/xsd/imsmd_v1p2 http://www.imsglobal.org/xsd/imsmd_v1p2p2.xsd">
  <metadata>
    <schema>IMS Content</schema>
    <schemaversion>1.1.3</schemaversion>
  </metadata>
  <organizations/>
  <resources>
    <resource identifier="{self.bankName}" type="imsqti_xmlv1p2">
      <file href="{self.outFile.parent.name + '/' + self.outFile.name}"/>
    </resource>'''

        def makeFooter(self):
            self.footer = '''
                </section>
              </assessment>
            </questestinterop>
            '''
            
            self.manFooter = '''</resources>
</manifest>
'''

        def extractQuestionText(self, text):
            """
            Extract question text regardless of whether the separator is a period or closing parenthesis.
            Works with formats like "1. Question text" or "1) Question text"
            """
            # If it's already a single line, use regex to extract the question text
            if isinstance(text, str):
                # Match digit followed by period or parenthesis, then capture the rest as question text
                match = re.match(r'^\s*\d+[\.\)]\s*(.*?)$', text)
                if match:
                    return match.group(1)
                return text
            
            # If we have multiple lines (list), extract from the first line
            elif isinstance(text, list) and len(text) > 0:
                # Match digit followed by period or parenthesis, then capture the rest as question text
                match = re.match(r'^\s*\d+[\.\)]\s*(.*?)$', text[0])
                if match:
                    return match.group(1)
                # Fallback to the old method if regex doesn't match
                return text[0].split(self.sep, 1)[1].strip() if self.sep in text[0] else text[0]
            
            return ""

        
if __name__=="__main__":
    parser = argparse.ArgumentParser(description="import text file to export QTI for Canvas Quiz import",epilog=__doc__)
    parser.add_argument("ifile", nargs='+', default=None,
                        help="txt file path and name to process")
    parser.add_argument("--separator", default='.',
                        help="string indicating separator between question/answer number/letter and text, usually '.' or ')'")
    
    args = parser.parse_args()
    for iFile in args.ifile:
#     inputFile=args.ifile
        sep = args.separator
        doIt = makeQti(iFile, sep)
        doIt.run()