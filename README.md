# QTI converter

This program will convert a simply formatted text document containing most question types available in Canvas into a zip file that can be imported to Canvas to add the questions to a question bank. NOTE: the Canvas import process will also make an actual quiz containing all of the questions in the bank. If you just want the question bank to pull from, I suggest deleting that quiz after import.

+ Written by Brandon E. Jackson, Ph.D.  
+ jacksonbe3@longwood.edu  
+ last updated: March 13, 2020  

## Installation and basic usage (Mac)

1. Download the [zipped app](https://github.com/haliaetus13/qtiConverter/raw/master/dist/qtiConverterApp.app.zip) (Mac only at this point). 
2. Depending on your settings, the zip may auto unzip into the app in your Downloads folder. If it doesn't, double click on it in your Downloads folder to unzip it.
2. Move the `qtiConverterApp.app` to the Desktop or somewhere else easily accessible. I put it on my desktop, then also drag it to my dock.
3. Once you've created your text file and organized images, just drag your text file onto the icon for the app to run it. You can actually drop multiple text files at once, and it will process each separately.
5. The output will be a zip folder that is named for the text file + "\_export". E.g., if your text file is `exam1.txt`, the folder will be `exam1_export.zip`. This is the zip you will import in Canvas, and it *should* include all of your images and questions.

## Installation and basic usage (Windows - not always tested and updated!)

1. Download the `WindowsQtiConverterExe`.
2. Save the whole folder somewhere easy to remember.
3. Create your quiz txt file and save it. Find the file and right-click on it. Select Open with > Choose another app > More apps > Look for another app on this PC > and then navigate to that downloaded folder and drill in until you can select `qtiConverterApp.exe`
4. Note on Windows, the error display dialogue will not work, so you will have to track down any formatting errors. 
5. The output will be a zip folder that is named for the text file + "\_export". E.g., if your text file is `exam1.txt`, the folder will be `exam1_export.zip`. This is the zip you will import in Canvas, and it *should* include all of your images and questions.

## Preparing the files

1. Make a simple text file. The best option is to make this file in a simple free text editor like Geany, BBedit, Notepad++ etc. The key is that it saves plain text (.txt, **not** .rtf) encoded in UTF-8.
    + MS Word can "Save As" a .txt file, but make sure when given the option that you select encoding as `Unicode (UTF-8)`, and `End lines with: CR only`. Those options may come up in the save window or in a conversion window that comes up after you hit save in the save window, depending on your version of Word.
    + Note that formatting or embedded images will not be saved in the text file. The exact formatting of this document is **extremely** important. See the bottom of this document for formatting info, how to include images, and examples
2. Save the text file of questions in its own folder, with all linked image files copied into that same folder.
    + the name of the **file** will become the name of the test bank in Canvas, which will also produce a Canvas "quiz" by default, containing all of the questions, by that same name
    + save any images you want to include as their own files in that same folder. **NOTE FOR IMAGES:** all images will be sized to the width of the viewing window in Canvas (with a max height of 600 px). You can drag to resize the image once it's inserted in Canvas.

### Formatting requirements

+ Each question and related information (hereafter *question blocks*) should be separated by at least one blank line. There should be no blank lines within any question.
    + If you **must** have a paragraph break within a question, use an html line break code (below). You may copy and paste the characters below into your text block wherever you want a new line. See the first example question below. Copy and paste this:
        - `<br>`
+ Each question block may begin with up to three lines of header information. The order of the information not matter. 
    + One header line may be a 2 letter (all caps) indicator of question type based on Canvas question types. If no indicator is given, MC is assumed. (MC: multiple choice, MA: multiple answers (select all that apply), MT: matching , SA: short answer (fill in the blank), MD: multiple dropdowns, MB: multiple blanks, ES: essay, TX: just text, NU: numerical
    + Another header line may refer to any image to be included before the question text. The line should read `image: imageFileName.jpg`. If no image is connected to the question, simply do not include this line (`image: ` with no name will cause an error). The image file of that name should be saved in the same folder as the text document.
        + you may have a subfolder of images, in which case the line should read `image: imageFolder/imageFileName.jpg` (i.e. the path is relative to the text file). 
        + Only one image may be included with the question text.
        + In multiple choice questions, you can include images as the answers by using `A) image: imageFileName.jpg` as the option.
    + The last header line option allows you to assign a default point value to that question. The number of points must be included in parentheses, and you may or may not have any other words in there. E.g., `(2)`, `(2 pts)`, `(2.5 points)` all work.
        + This point value will only be applied in the automatically created quiz in Canvas at import, and will be overridden if you simply "link" a question group to a bank.
+ After all of the header information (or no header information) the next line should be a digit followed by a "." or a ")", followed by the text of the question. 
    - the question text is followed on the next line (no blank line, just the next line) by answers
    - MC answers begin with a letter followed by a "." or a ")"
    - correct answer(s) are marked with a \* before the letter (at the start of the line) for multiple choice and multiple answer questions
    - NOTE that question numbers and answer letters will not necessarily transfer to Canvas (due to the *shuffle answers* option in Canvas).

### Other Formatting
+ You may use a hash (#) as a comment symbol. Anything on any line that begins with a # will not be processed and uploaded. 
- **Adding formatting**: there are two ways to add formatting like, **bold**, *italics*, ^superscript^, and ~subscript~. This will work in questions **and** in answers.
    1.  The easiest way is to use MarkDown formatting marks.
        + Surrounding some word or characters with two asterices, like `**this**` will make what's between them **bold**. "`this **word**`" yields: "this **word**".
        + One asterix on either side, like `*this*` indicates *italics*
        + surrounding something with carrots like `E = mc^2^` will make it superscript yielding E = mc^2^
        + tildes like `H~2~O` will make it subscript (H~2~O). 
        + The key is to **surround** what you want to format with the marks, without spaces between the modifiers and modifiees.
    2. You may also use standard html tags, where you surround the word or characters you want to format as appropriate:
        + *italics*: `this <em>word</em>` yields: this *word*
        + **bold**: `this <strong>word</strong>` yields: this **word**
        + superscript: `E = mc<sup>2</sup>` yields: E = mc^2^
        + subscript: `H<sub>2</sub>O` yields: H~2~O
        + `<h2> Header text</h2>` makes an html level 2 header (useful to include in a TX text block to break up the exam into sections). Also works with level 3 and 4 headers.
    3. You may use both the MarkDown and html styles in the same document

## Canvas Importing and Quiz Making Process

1. After you have processed your text file with this app, and created the export zip folder:
2. In Canvas, go to `Course settings > Import course content`. Select `QTI .zip file`. Choose the zip file from your computer.
    + You don’t need to select a question bank in Canvas. It will automatically create a new question bank and a quiz with the name you input in the python script.
    + Note that the default options also mean that it will not overwrite any questions or banks you already have. So you if import multiple times (or different folders with the same name), you will end up with multiple question banks and quizzes with the **same name** in Canvas! This can get very confusing. Blame Canvas.
3. Click import and wait for it to finish!  All of the questions will show up in your course test banks (go to Quizzes, click the three dots that mean “more options”, and manage question banks).
4. If the quiz made by Canvas during import is all you want, that's it. Edit the quiz to adjust your settings. If you included any point values in the question blocks, they should be applied there. Otherwise, each question is 1 point.
5. If you need to "pull" from the question bank, in Canvas, make a new quiz.          
    + Adjust its general settings. 
    + Click on the Questions tab. Make a new **question group**. 
    + You can link that group to a question bank, and enter how many questions the quiz should pull from that bank
    + or you can "find questions", and select individual (or all) questions to add.
    + Either way, then tell the group how many questions to pull from the bank and give a point value to each question.

### Things to consider:

+ If the question types are confusing, try making different sample exam questions in Canvas.
+ All questions (unless noted in a header) will be imported as being worth 1 point. This can be changed when you are creating your quiz in Canvas and pulling from the question bank
+ If you want different point values based on question types (say, 3 points for short answer but 2 points for multiple choice), and want to pull random questions from a bank, save the two question types in separate files, and import as separate question banks. When you make your quiz in Canvas, it's easy to apply point values to questions based on groups.
+ To print backup copies of quizzes, you can change the quiz to NOT show "one question at a time". Preview the quiz. Print.

### Tips

+ If there is a formatting error in one of your questions, you should get a dialog box on screen (Mac only) telling you which question has the problem, and the text from that question. Note that the numbers of your questions in your file don't matter, so this dialog just tells you which question, counted from the top, has the problem. The most likely problems are:
    + a question type indicator that isn't one of the options
    + "new" lines in the question
    + improperly formatted answers
    + missing separators (usually periods or colons or right-parenthesis) after question numbers or answer indicators
+ You can drag the app (once you've unzipped the download and moved the app to where ever you want it, like the Desktop) to the Mac Dock so that it is always available to drag and drop a file.
+ One of the most powerful plain text editors on Mac is BBEdit, by BareBones software. You can download and use for free (when the free demo is over, you only lose some very advanced functions. I do all of my coding and writing in the free version). If you make a lot of quizzes, I suggest using BBEdit to edit the text since it is faster and more stable than Word.
    + If you use BBEdit, after installing it, click on the script icon in the menu (looks like a scroll)
    + select `Open Scripts Folder` to open a Finder window to the location where BBEdit scripts are saved. Right-click on the name of that window and it will show you the path to get there.
    + Back in BBEdit, make a new file, and save that file in that scripts folder location. Name the file something easy to recognize like `text2qti.sh`. The `sh` at the end is important!
    + In BBEdit, copy and paste the code below into the file:
    + If you saved the file to anywhere other than the Desktop, you have to edit the cd line to the directory where you saved the app.
    + Save and close the script file
    + Now, when you are done making a quiz in BBEdit, save the quiz, and while it is open, go to the Scripts menu icon, and select your script. It should run the conversion without having to even drag-and-drop the file!
```bash
#!/bin/bash
PATH=$PATH:/usr/local/bin
cd ~/Desktop
./qtiConverterApp.py "$BB_DOC_PATH"
```


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

TX
1\. `<h2>New Section of exam</h2>` This is a "text" question which can be used to insert section labels or instructions, and do not ask for answers. I like to enter just exam section labels. Make the text bold and larger, like the "New section of exam" here by entering `<h2>New Section of exam</h2>`. The "h2" means "header 2" in html formatting.

## Likely errors

If the application crashes after you drop your file on it, you probably have a formatting issue (it is picky). If that's the problem, you should get an error dialog that reports which question has the problem (Mac only). Check for the following:

+ make sure you have a separator (a period ideally) after every question number and answer letter
+ make sure you don't have new lines within a question text
+ make sure you have properly formatted your answers for the selected question type, and have marked correct answer(s)

If you don't get the format error dialog, and you just get a dialog with a crash warning, and buttons for "Terminate" and "Console", then do the following:

1. Open a terminal window (cmd-space, type terminal, enter)
2. In Finder, right-click on qtiConverterApp.app (the thing you drop your file on to) and select `Show package contents`
3. Navigate to `Contents > MacOS` and open
4. Right-click on qtiConverterApp, hold down the `alt-option` key, and select `Copy qtiConverterApp as Pathname'
5. Go to Terminal, enter a single quote, paste, enter another single quote, then add a space
6. In Finder, find your text file, right-click, hold down alt, copy as Pathname
7. In Terminal, enter a single quote, paste, enter a single quote.
8. hit Enter.
9. That will run the app, and you should see the same Terminate/Console window, but some more information should have been printed to the terminal window. Copy and paste that into an email and submit it.

## License

This project is licensed under the GNU Lesser General Public License v3.0; see the LICENSE.md file for details. Note that the software is provided "as is", without warranty of any kind, express or implied.