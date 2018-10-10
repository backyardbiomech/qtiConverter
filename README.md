# QTI converter

This script will convert a simply formatted text document containing multiple choice questions into a zip file that can be imported to Canvas to add the questions to a question bank. NOTE: the Canvas import process will also make an actual quiz containing all of the questions in the bank. I suggested deleting that quiz after import.

## Installation and running

1. From the `dist` folder here, download the `atiConverterApp.app` file (it might be a zip archive of that)
2. Save it on the Desktop or somewhere else easily accessible
3. Once you've created your text file and organized images, just drag your text file onto the icon for the app to run it.

## Preparing the files

1. make a simple text file (MS Word can "Save As" a .txt files). Note that no formatting or embedded images will not be saved (formatting, like **bold** and *italics* may be possible in future versions of this software). The exact formatting of this document is **extremely** important. See the bottom of this document for examples:
    - one blank line between questions (hereafter question blocks), no blank lines within question blocks
    - the first line in the block is a 2 letter indicator of question type based on Canvas question types. If no indicator is given, MC is assumed. (MC: multiple choice, MS: multiple selection, MT: matching, SA: short answer (fill in the blank),
 MD: multiple dropdowns, MB: multiple blanks, ES: essay, TX: just text (instructions) **NOTE: right now, multiple choice is the only supported question type.**
    - the second line in the block refers to any image associated with the question. The line should read `image: imageFileName.jpg`. If no image is connected to the question, do not include this line.
    - the third line (or first if no image or question type indicators are required) is a number followed by separator (period or ")"), followed by a space, followed by the text of the question.
    - the question text is followed on the next line (no blank line, just the next line) by answers
        - answers begin with a letter followed by the same separator as the question
        - correct answer(s) are marked with a \* before the letter (at the start of the line)
    - Questions can have any number followed by a period or closing parenthesis (whatever character follows the question number must be the same as whatever character follows the answer letter)
    - NOTE that question numbers and answer letters will not necessarily transfer to Canvas (due to the *shuffle answers* option in Canvas). See below for the import process.
    
2. Save the text file containing questions in it's own folder. 
    + the name of the file will become the name of the test bank in Canvas, which will also produce a Canvas "quiz" by default containing all of the questions
    + save any images you want to include as their own files in that same folder. **NOTE FOR IMAGES:** all images will be sized to a "safe" size for display in Canvas (314px wide). You can drag to resize the image once it's inserted in Canvas.
    + For now, avoid spaces in the name of any of the files (.txt and images). Whatever you name your image files should be what you include on the "image: " line in the text document.
    
## Running the application

1. The easiest is to drag your text file containing the questions onto the app.

2. The harder is to download the actual python script from Bitbucket, and run it from the command line:
The basic call is
```
qtiConverterApp.py /path/to/text/file.txt
```
changing the path to your text file as needed. You can add `--sep ')'` is you use parenthesis after your question numbers and answer letters.

2. The output will be a zip folder that is named for the text file + "\_export". E.g., if your text file is `exam1.txt`, the folder will be `exam1\_export.zip`. This is the folder you will import in Canvas, and it *should* include all of your images and questions.
    
## Canvas Importing and Quiz Making Process

1. in Canvas, go to `Course settings > Import course content`. Select `QTI .zip file`. Choose the zip file from your computer.
    + You don’t need to select a question bank in Canvas. This will create a new question bank and a quiz with the name you input in the python script.
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

+ Right now, this only works for multiple choice questions, with only one correct answer
+ All questions will be imported as being worth 1 point. This can be changed as you are creating your quiz in Canvas and pulling from the question bank
+ To print backup copies of quizzes, you can 
    1. Change the quiz to NOT show "one question at a time. Preview the quiz. Print.


### Sample text document format:

1\. Some question text here  
A. incorrect.  
B. incorrect.  
*C. correct.  
D. incorrect.  
E. incorrect.  

MC  
 1\. Some question text here  
*A. correct.  
B. incorrect.  
C. correct.  
D. incorrect.  
E. incorrect.

MC  
image: imageFileName.jpg  
 1\. Some question text here  
*A. correct.  
B. incorrect.  
C. correct.  
D. incorrect.  
E. incorrect.