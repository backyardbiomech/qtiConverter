# Converting

Once you've created your text file, the main operation will convert it to a zip file in the QTI format that you can import.

![main screen](docs/images/mainWindow.png)

If you downloaded the pre-packaged app, just open the app, select your text file, and click the button to convert. It will create a zip file in the same folder as your text file. You can skip the rest of this section and jump to the [Canvas importing section](#canvas-importing-and-quiz-making-process).

## Command line

The exact code you need to run depends a bit on your python installation and the location where you downloaded and then saved this code, and whether you're using Windows or Mac.

Basically, on the command line you need to run:

```bash
python "path/to/this/qtiConverterApp.py" "path/to/your/textfile.txt"
```

That tells the computer to use `python` to run this app, and points it at your text file. 

For example, let's say you saved this code on your desktop, and your text file is in a folder in your Documents folder. On a mac, the code would look something like:

```bash
python "/Users/<your_user_name>/Desktop/qtiConverter/qtiConverterApp.py" "/Users/<your_user_name>/Documents/Courses/My Course/Exams/exam1.txt"
```

Or on Windows:

```bash
python "C:\Users\<your_user_name>\Desktop\qtiConverter\qtiConverterApp.py" "C:\Users\<your_user_name>\Documents\Courses\My Course\Exams\exam1.txt"
```

Both mac and Windows have options to find the file and copy the path to make that easier. In mac, you can even drag a file into the terminal window to "paste" the path to that file at the cursor.

After the conversion, you will see two new outputs:

1. The zip file is the one to upload to Canvas
2. The html preview file should open in any browser. It just gives you a quick way to visualize a representation of your questions to check images and answers. 

## Canvas Importing and Quiz Making Process

You have several decisions to make here. First, are you sticking with **Classic Quizzes** or using **New Quizzes**. The other is are you importing a **Quiz** specifically, or importing an **Item Bank**. I **strongly** recommend you see this as importing to a bank, then make a quiz from that. 

### New Quizzes Item Bank (my recommendation)

This will let you create an *Item Bank* with your questions. You can then create a quiz (or several) in Canvas that pull all or some questions from that bank.

1. In Canvas, go to `Item Banks`
2. Create a new bank. The name doesn't really matter because it will be renamed upon import to the name of your original text file. I usually create it as `aaa` so it shows up at the top of my item bank list.
3. Find the new bank you just created and click on its name
4. On the page for the specific bank, don't add any new questions. If you do, you won't be able to import your file. **Instead** click on the three dots in the upper right and select `Import Content`
5. Select the zip file on your computer created by the app. 

That will create all of the questions in that bank. It may take a few minutes to import, depending on how many questions you have.

If you want to add more questions later, you can do that in Canvas. But I prefer to add them to my text file and reimport. This will not overwrite your item bank (Canvas allows duplicate item bank names unfortunately) and you will have to relink it to any quizzes.

I generally create two banks per chapter or topic (one for easier questions, one for harder questions) with many questions per bank. 

Then I create a new quiz. In that quiz window (after setting options):

1. Select `Build`
2. Click the `plus` to add a question, but instead of selecting a question select the `Item Bank` icon
3. Select the item bank.
4. Either select specific questions, or my preference is to select `All/Random`. It will add all questions from the bank by default.
5. On the quiz builder page, edit the grouping to indicate the number of questions to pull randomly from the bank, and the point values per question.
6. If desired, add another grouping to pull from a different item bank, or add other specific questions.

### New Quizzes Quiz Import
You could set up your text file as a specific quiz rather than a bank. In that case, be sure to include point values per question in your text file (see [formatting](./formatting.md)).

1. In Canvas, make a new quiz.
2. Don't create any questions! That will lock out the import option (blame Canvas). After importing you can edit and add questions all you want.
3. Click on the three dots in the upper right and select `Import Content`
4. Select your zip file. All of your questions should show up in the quiz. 
5. Adjust settings and per-question settings as needed


### Classic Quizzes

If you are still using Classic Quizzes, any import will create both a *question bank* and a *quiz*. 

1. In Canvas, go to you Home page and select `Import Existing Content`. Select `QTI .zip file`. Choose the zip file from your computer. Don't click "Import as new quizzes".
    + You don’t need to select a question bank in Canvas. It will automatically create a new question bank and make a quiz with the name of your text file.
    + Note that the default options also mean that it will not overwrite any questions or banks you already have. So you if import multiple times (or different folders with the same name), you will end up with multiple question banks and quizzes with the **same name** in Canvas! This can get very confusing. Blame Canvas.
2. Click import and wait for it to finish!  All of the questions will show up in your course test banks (go to Quizzes, click the three dots that mean “more options”, and manage question banks).
3. If the quiz made by Canvas during import is all you want, that's it. Edit the quiz to adjust your settings. If you included any point values in the question blocks, they should be applied there. Otherwise, each question is 1 point.
4. If you need to "pull" from the question bank, in Canvas, make a new quiz.          
    + Adjust its general settings. 
    + Click on the Questions tab. Make a new **question group**. 
    + You can link that group to a question bank, and enter how many questions the quiz should pull from that bank
    + or you can "find questions", and select individual (or all) questions to add.
    + Either way, then tell the group how many questions to pull from the bank and give a point value to each question.

Previous step: [Preparing the document](formatting.md)
Next step: [Tips and FAQ](FAQ.md)