# QTI converter

This program will convert a simply formatted text document containing most question types into a zip file that can be imported to Canvas to add the questions to a question bank. NOTE: the Canvas import process will also make an actual quiz containing all of the questions in the bank. I suggested deleting that quiz after import.

## Installation and basic usage

1. Download the zip `qtiConverterApp.app.zip` file and un-zip it
2. Save the uncompressed application on the Desktop or somewhere else easily accessible
3. Once you've created your text file and organized images, just drag your text file onto the icon for the app to run it.

## Preparing the files

1. make a simple text file (MS Word can "Save As" a .txt files; Note that formatting or embedded images will not be saved). (Formatting, like **bold** and *italics* may be possible in future versions of this software). The exact formatting of this document is **extremely** important. See the bottom of this document for examples:
    - one blank line between questions (hereafter question blocks), no blank lines or new paragraphs within question blocks.
    - If you **must** have a paragraph break within a question, copy and paste the odd characters below into your text block wherever you want a new line. See the first example question below. Copy and paste this:
        - `&lt;br&gt;`
    - the first line in the block is a 2 letter indicator of question type based on Canvas question types. If no indicator is given, MC is assumed. (MC: multiple choice, MA: multiple answers (select all that apply), MT: matching (not yet functional), SA: short answer (fill in the blank), MD: multiple dropdowns, MB: multiple blanks, ES: essay, TX: just text (not yet functional) 
    - the second line in the block refers to any image associated with the question. The line should read `image: imageFileName.jpg`. If no image is connected to the question, do not include this line. The image file of that name should be saved in the same folder as the text document.
    - the third line (or first if no image or question type indicators are required) is a number followed by separator (period or ")"), followed by a space, followed by the text of the question. **a period is the default separator and is preferred**.
    - the question text is followed on the next line (no blank line, just the next line) by answers
        - MC answers begin with a letter followed by the same separator as the question
        - correct answer(s) are marked with a \* before the letter (at the start of the line) for multiple choice and multiple answer questions
    - NOTE that question numbers and answer letters will not necessarily transfer to Canvas (due to the *shuffle answers* option in Canvas). See below for the import process.
    
2. Save the text file containing questions in it's own folder. 
    + the name of the file will become the name of the test bank in Canvas, which will also produce a Canvas "quiz" by default containing all of the questions
    + save any images you want to include as their own files in that same folder. **NOTE FOR IMAGES:** all images will be sized to a "safe" size for display in Canvas (314px wide). You can drag to resize the image once it's inserted in Canvas.
    + For now, avoid spaces in the name of any of the files (.txt and images). Whatever you name your image files should be what you include on the "image: " line in the text document.
    
## Running the application

1. The easiest method is to drag your text file containing the questions onto the app.

2. The harder method is to download the actual python script from Bitbucket, and run it from the command line:
The basic call is
```
qtiConverterApp.py /path/to/text/file.txt
```
changing the path to your text file as needed. You can add `--sep ')'` if you use parentheses after your question numbers and answer letters.

2. The output will be a zip folder that is named for the text file + "\_export". E.g., if your text file is `exam1.txt`, the folder will be `exam1_export.zip`. This is the zip you will import in Canvas, and it *should* include all of your images and questions.
    
## Canvas Importing and Quiz Making Process

1. In Canvas, go to `Course settings > Import course content`. Select `QTI .zip file`. Choose the zip file from your computer.
    + You don’t need to select a question bank in Canvas. It will automatically create a new question bank and a quiz with the name you input in the python script.
    + Note that the default options also mean that it will not overwrite any questions or banks you already have. So you if import multiple times (or different folders with the same name), you will end up with multiple question banks and quizzes with the **same name** in Canvas! This can get very confusing. 

2. Click import and wait for it to finish!  All of the questions will show up in your course test banks (go to quizzes, click the three dots that mean “more options”, and manage question banks).

3. If the quiz made by Canvas during import is all you want, that's it. Edit the quiz to adjust your settings.

4. If you need to "pull" from the question bank, in Canvas, make a new quiz.          
    + Adjust its general settings. 
    + Click on the Questions tab. Make a new **question group**. 
    + You can link that group to a question bank, and enter how many questions the quiz should pull from that bank
    + or you can "find questions", and select individual (or all) questions to add.
    + Either way, then tell the group how many questions to pull from the bank and give a point value to each question.

### Things to consider:

+ If the question types are confusing, try making different sample exam questions in Canvas.
+ Right now, this does not work for numerical, or text box question types.
+ All questions will be imported as being worth 1 point. This can be changed when you are creating your quiz in Canvas and pulling from the question bank
+ If you want different point values for one question type (say, 3 points for short answer but 2 points for multiple choice), save the two question types in separate files, and import as separate question banks. When you make your quiz in Canvas, it's easy to apply point values to each question in a bank.
+ To print backup copies of quizzes, you can change the quiz to NOT show "one question at a time". Preview the quiz. Print.


### Samples

This should give you some idea of how to format the text document. Note that each sample "question" below contains some instructions for how to format that question type. You can also download a sample file from BitBucket (testFiles > simpleTestForImport > bank1.txt) that will show you the types. Drop that on the app, import the zip to Canvas, and preview the quiz to see what it looks like.

```
1\. This is a multiple choice question by default since there isn't an indicator code above it. Note number followed by a period to start, and the answers below have letters followed by periods. The correct answer is marked by a \*. If you want to start a new line after this, &lt;br&gt; This will now be on a new line once you've imported to Canvas. Paste two in a row &lt;br&gt; &lt;br&gt; to get a blank line inserted.  
A. incorrect answer text.  
B. incorrect answer text.  
\*C. correct answer text.  
D. incorrect answer text.  
E. incorrect answer text.  

MA  
1\. This is a multiple answer (select all that apply) question. It will show up as checkboxes to the student, which can be hard to see, so I suggested added "select all that apply" or similar to the question. All of the correct answers are marked by a \*. Canvas awards partial credit based on the number of correct answers.  
\*A. correct answer text.  
\*B. another correct answer text.  
\*C. another correct answer text.  
D. incorrect answer text.  
E. incorrect answer text.

MC  
image: imageFileName.jpg  
1\. Some question text here. This is a multiple choice question with an image above. Notice no spaces in the image file name, and the file must be in the same folder as this text document.  You can add an image to any question type (but not yet to answers)!  
\*A. correct answer text.  
B. incorrect answer text.  
C. correct answer text.  
D. incorrect answer text.  
E. incorrect answer text.

SA  
1\. Fill in a blank \_\_\____ like that one. notice letter followed by period below.  
A. correct answer 1  
B. correct anser too allowing for mispellings

ES  
1\. This is the text for an essay question. Type as much as you want here. The students will get a text box to enter their answers, and you will need to manually grade those answers!

MB  
1\. This is a fill in multiple blanks question. Here is the first [blank1] and here is the second [blank2]. Students will get text boxes to fill for each. Put square brackets around any indicator word (no spaces!) and then use that below, followed by a colon, to show correct answers. Multiple correct answers for each blank should be on the same line and separated with commas. Canvas awards partial credit based on the number of blanks.  
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
```