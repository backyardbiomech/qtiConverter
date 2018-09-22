#!/usr/bin/env python3

import zipfile

# put the name of the file here (best if it's in the same folder, otherwise need the full path
inputFile = '12_photosynthesis.txt'

# put the desire name for the test bank in Canvas here (don't include spaces in the name)
bankName = '12_photosynthesis'

'''
put the parsing character here (that is after your question or answer identifiers.
It will probably be either '.' or ')'
'''
parseChar = '.'

# make the header
header = ''' <?xml version="1.0" encoding="UTF-8"?>
<questestinterop xmlns="http://www.imsglobal.org/xsd/ims_qtiasiv1p2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.imsglobal.org/xsd/ims_qtiasiv1p2 http://www.imsglobal.org/xsd/ims_qtiasiv1p2p1.xsd">
  <assessment ident="i16a1ee4b717db114ff42a89898fc1512" title="{}">
    <qtimetadata>
      <qtimetadatafield>
        <fieldlabel>cc_maxattempts</fieldlabel>
        <fieldentry>1</fieldentry>
      </qtimetadatafield>
    </qtimetadata>
    <section ident="root_section">
'''.format(bankName)

footer = '''
    </section>
  </assessment>
</questestinterop>
'''
fileName = bankName + '.xml'
with open(fileName, 'w') as out:
    out.write(header + '\n')
#parse parts as needed

# get the file
data = []
with open(inputFile, 'r', encoding = "utf-8") as myfile:
    data=myfile.read()
data=data.split('\n\n')
#go through each question
for q in range(len(data)):
    # parse the questions and answers based on new lines
    foo = data[q].split('\n')
    quest = foo[0].split(parseChar, 1) [1][1:]
    answers = []
    # make a list of answers
    for a in range(1,len(foo)):
        ans = foo[a]
        # get the correct answer
        if ans[0] == '*':
            corr = str(a)
        answers.append(ans.split(parseChar, 1)[1][1:])
    # make an identifier
    itid = 'MC' + str(q)
    # build the text for each question, starting with a question "header"
    out1 = '''
    <item ident="{}" title="Question">
        <itemmetadata>
          <qtimetadata>
            <qtimetadatafield>
              <fieldlabel>question_type</fieldlabel>
              <fieldentry>multiple_choice_question</fieldentry>
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
          <response_lid ident="response1" rcardinality="Single">
            <render_choice>
          '''.format(itid, quest)
    
    # go through each answer and add to the string as necessary
    for a in range(len(answers)):
        resp = str(a+1)
        out1 += ''' <response_label ident="{}">
                <material>
                  <mattext texttype="text/plain">{}</mattext>
                </material>
                </response_label>
                '''.format(resp, answers[a])
    
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
              <varequal respident="response1">{}</varequal>
            </conditionvar>
            <setvar action="Set" varname="SCORE">100</setvar>
          </respcondition>
        </resprocessing>
      </item>
    '''.format(corr)

    
    with open(fileName, 'a', encoding = "utf-8") as out:
        out.write(out1 + '\n')

with open(fileName, 'a') as out:
    out.write(footer)
        
out_zip = zipfile.ZipFile(fileName + '.zip', 'w')
out_zip.write(fileName, compress_type=zipfile.ZIP_DEFLATED)