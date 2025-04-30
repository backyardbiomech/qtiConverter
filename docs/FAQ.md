### Things to consider:

+ If the question types are confusing, try making different sample exam questions in Canvas to get comfortable with how they will appear.
+ All questions (unless noted in a header) will be imported as being worth 1 point. This can be changed when you are creating your quiz in Canvas and pulling from the question bank
+ If you want different point values based on question types (say, 3 points for short answer but 2 points for multiple choice), and want to pull random questions from a bank, save the two question types in separate files, and import as separate question banks. When you make your quiz in Canvas, it's easy to apply point values to questions based on groups.
+ The question numbers and answer letters (in MC questions) in your text file don't really matter. Every question in your text file can be `1.`. 

### Tips

+ If there is a formatting error in one of your questions, you should get a dialog box on screen telling you which question has the problem, and the text from that question. Note that the numbers of your questions in your file don't matter, so this dialog just tells you which question, counted from the top, has the problem. The most likely problems are:
    + a question type indicator that isn't one of the options
    + "new" lines in the question
    + improperly formatted answers
    + missing separators (usually periods or colons or right-parenthesis) after question numbers or answer indicators

### HotSpot Questions

HotSpot Questions prompt students to click on a specific region of an image (e.g. "Click on the stomach in this image"). 

When you create one of these questions in Canvas, it has you draw on the image to highlight the "correct" area of the image. All other areas are *incorrect*. For the import, you need to provide the coordinates of the polygon that you would draw on the image.

I've included a small script to recreate that action of drawing on the image and get coordinates in a format that you can paste into your text file as shown in the [sample](./samples.md).

![hotspot](docs/images/hotspot.png)

If you use the packaged app:
1. click on the `Load Image` button and select an image
2. click to draw a polygon around the area you want to be "correct"
3. hit any key which will bring up a dialog box with the coordinates of the polygon in a format that you can copy and paste into your text file.
4. Copy the coordinates and paste them into your text file below the question.

![hotspot coorinates](docs/images/hotspot_coordinates.png)


#### Command line hotspot coordinates
If you are using the command line, follow these instructions:

1. Be sure you installed `opencv-python` and `matplotlib` as described on the [installation](./installation.md) page.
2. run `python path/to/qtiConverter/imagePolygon.py`
3. That will prompt you to enter the path to the image, which should be in the same folder as your text file. So it may be something like ` "/Users/<your_user_name>/Documents/Courses/My Course/Exams/image1.jpg"`
4. A window should appear containing that image.
5. Click to mark the "correct" area of the image. Double-click to close the polygon.
6. Hit the space bar to:
   1. close the window
   2. Print a the `(x,y)` coordinates to your command line.
7. Copy the whole block of those coordinates and paste below your hot spot question (as show in the [sample](./samples.md))



Previous step: [Importing to Canvas](./importing.md)
Next step: [Samples](./samples.md)