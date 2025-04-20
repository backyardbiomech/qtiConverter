### Samples

This should give you some idea of how to format the text document. Note that each sample "question" below contains some instructions for how to format that question type. You can also download a sample file from the [github repository](https://github.com/haliaetus13/qtiConverter) (testFiles > simpleTestForImport > bank1.txt) that will show you the types. Drop that on the app, import the zip to Canvas, and preview the quiz to see what it looks like.

\# This is a comment line because it begins with '\#'.  
\# You can make any notes and they will not become part of the exam in Canvas.  
\# Every new line must begin with a '#\' if you don't want them processed  


1\. This is a multiple choice question by default since there isn't an indicator code above it. Note number followed by a period to start, and the answers below have letters followed by periods. The correct answer is marked by a \*. If you want to start a new line after this, enter a `<br>` <br> This will now be on a new line once you've imported to Canvas. Paste two in a row `<br><br>` <br><br> to get a blank line inserted.  
A. incorrect answer text.  
B. incorrect answer text.  
\*C. correct answer text.  
D. incorrect answer text.  
E. incorrect answer text.  

MA  
1\. This is a multiple answer (select all that apply) question. It will show up as checkboxes to the student, which can be hard to see, so I suggest adding "select all that apply" or similar to the question. **All** of the correct answers are marked by a \*. Canvas awards partial credit based on the number of correct answers, and penalizes for incorrectly selected answers.  
\*A. correct answer text.  
\*B. another correct answer text.  
\*C. another correct answer text.  
D. incorrect answer text.  
E. incorrect answer text.

MC  
image: imageFileName.jpg  
1\. This is a multiple choice question with an image above. Notice no spaces in the image file name, and the file must be in the same folder as this text document.  You can add an image to any question type!  And you can add images as answers to MC and MA questions!  
\*A. image: image1.jpg  
B. image: image2.jpg  
C. image: image3.jpg  
D. image: image4.jpg  
E. image: image5.jpg

(2pts)  
SA  
1\. This question is assigned 2 points. NOTE that I could have made it (2), or (2 points), or (2 pts), or (2 chickens). The key is to have a number inside parentheses in one of the first three lines in the question block. The SA stands for short answer: Fill in a blank \_\_\____ like that one. notice letter followed by period below.  
A. correct answer 1  
B. correct anser too alowing for mispellings  
C. Yet another correct answer

ES  
1\. This is the text for an essay question. Type as much as you want here. The students will get a text box to enter their answers, and you will need to manually grade those answers!

MB  
1\. This is a fill in multiple blanks question. I like using MB questions even if I just have one blank instead of SA questions. Here is the first [blank1] and here is the second [blank2]. Students will get text boxes to fill for each. Put square brackets around any indicator word (no spaces!) and then use that below, followed by a colon, to show correct answers. Multiple correct answers for each blank should be on the same line and separated with commas. Canvas awards partial credit based on the number of blanks.  
blank1: correct answer for 1, another correct answer for 1  
blank2: correct answer for 2, another correct answer for 2

MD  
1\. This is a multiple dropdown question. Here is the first [drop1] and here is another [drop2]. Notice the square brackets around the indicators (no spaces!). Use those indicators below, followed by a colon to provide the options you want students to have for each dropdown. Correct answers for each dropdown are indicated by \*. Canvas awards partial credit based on the number of dropdowns.  
\*drop1: correct answer for 1  
drop1: incorrect answer for 1  
drop1: incorrect answer for 1  
drop2: incorrect answer for 2  
\*drop2: correct answer for 2  

MT  
1\. This is a matching question. It will show in canvas as a list of things on the left, each with its own dropdown menu on the right. All the dropdowns contain the same options. Multiple "left" items can have the same correct answer. Note the formatting below. left1, left2, etc just track the list items that will appear on the left, right1, right2, etc track the options that will show in the dropdowns, and the correct answer for each left item is indicated by putting the right label inside brackets. Notice no spaces in labels or between brackets and labels, and all labels are followed by a colon, then the text to be matched. Canvas awards partial credit based on the number of left side items.  
[right2]left1: first left option  
[right2]left2: second left option  
[right1]left3: third left option  
right1: first right option correct for third left  
right2: second right option correct for first and second left  
right3: third right option distractor  
right4: fourth right option distractor  
right5: fifth right option distractor  

OR
1\. This is an ordering question for new quizzes. It will show as a "top label", like "most superficial", a bottom label like "deepest", and a series of drag and drop options. They are simply put with numbers and order here.  
toplabel: most superficial  
1: epidermis  
2: dermis  
3: hypodermis  
bottomlabel: deepest

TF
1\. This is a true/false question in new quizzes. The answer is after "A" and a colon, and is not case-sensitive.  
A: True

CT
1\. This is a categorization question in new quizzes. Each category can have multiple answers, and you can include multiple distractors that should be left as uncategorized. Make sure that each line begins with the name for a category (and that spelling is exactly the same for  every entry for the same category) or 'distractor'.  
first category name: an answer for first category name  
first category name: another answer for first category name  
second category name: an answer for another category  
second category name: another answer for the second category  
distractor: this answer doesn't go anywhere  

HS
image: organs.jpg
1\. This is a hotspot question where students are directed to click on a part of an image (in new quizzes only). The image is defined above like for other questions, this is the prompt. The coordinates that define the polygon vertices are defined as x,y,x,y,x,y all on one row below (how canvas stores it) or as shown below with (x,y) pairs each on their own line. See the polygon creator doc for more. In both cases, x and y are percentages of width and height of the image. This same image file can be used for other questions, too.  
(0.503731343283582, 0.6557674841053588)  
(0.48134328358208955, 0.6748410535876476)  
(0.5074626865671642, 0.6875567665758402)  
(0.5758706467661692, 0.6939146230699365)  
(0.6417910447761194, 0.6612170753860127)  

See [this part of the FAQs](./FAQ.md#hotspot-questions) for help with getting the coordinates for the hot spot question.
