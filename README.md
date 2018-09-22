# QTI converter READ ME

This script will convert a simply formatted text document containing multiple choice questions into a zip file that can be imported to Canvas to add the questions to a question bank. NOTE: the Canvas import process will also make an actual quiz containing all of the questions in the bank. I suggested deleting that quiz after import.

## Process

1. make a simple text file (can word export .txt files?). I use Bbedit on the mac, but the included textEdit or any plain text program should be fine for copy and paste from word.
    - Format should be similar to the example questions below: one blank line line between questions, no blank lines within questions (the newline character is the basis for parsing)
    - Questions can have any number followed by a period or closing parenthesis (whatever character follows the question number must be the same as whatever character follows the answer letter)
    - Answers should have a letter or number followed by the same character as the question (a period or closing parentheses), and SHOULD NOT BE INDENTED (actually, this may not matter)
    - The correct answer should be marked with an asterix (\*) immediately before the letter
    - NOTE that question numbers and answer letters will not transfer to Canvas (though answer order should transfer if the *shuffle answers* option is turned off in Canvas)

2. Open the python script and near the top edit the strings for `inputFile` (the name of your .txt file containing questions), the name you want for the Question Bank in Canvas and your output files, and your parsing character

3. I suggest putting your input text file in the same folder as the script for simplicity for now

4. Save and run the script from terminal (or if you are using BBEdit, just hit `cmd-R` to run it)

5. You will get an .xml file with the name of your question bank, and a zip file of that file

6. in Canvas, go to `Course settings > Import course content`. Select `QTI .zip file`. Choose the file from your computer. You don’t need to select a question bank. This will create a new question bank and a quiz with the name you input in the python script.

7. Click import and wait for it to finish!  All of the questions will show up in your course test banks (go to quizzes, click the three dots that mean “more options”, and manage question banks).

8. In Canvas, make a quiz. Adjust it's settings. Click on the Questions tab. Make a new **question group**. 
  - You can link that group to a question bank, and enter how many questions the quiz should pull from that bank
  - or you can "find questions", and select individual (or all) questions to add. And then tell the group how many questions to offer.

### Things to consider:

+ Right now, this only works for multiple choice questions, with only one correct answer
+ Any pictures need to be added to the question once it’s already in Canvas
+ All questions will be imported as being worth 1 point. This can be changed as you are creating your quiz in Canvas and pulling from the question bank
+ To print backup copies of quizzes, you can 
    1. Change the quiz to NOT show "one question at a time. Preview the quiz. Print.
    2. Check out [paperscorer](https://www.paperscorer.com)

### Sample Question format:

1\. If a biologist crosses bunnies from a population with all long ears with bunnies from a different population that all has short ears, and all the offspring have short ears, this means that the gene for long ears is likely  
A. codominant.  
B. dominant.  
*C. recessive.  
D. rare.  
E. abnormal.  

1\. At a certain locus of the human genome, 200 different alleles exist in the population. Each person has at most _______ allele(s) at that locus.  
A. 1  
*B. 2  
C. 100  
D. 200  
E. 400  