# Preparing the document

1. Make a simple text file. The best option is to make this file in a simple free text editor like Visual Studio Code, Notepad++, RStudio, etc. The key is that it saves plain text (.txt, **NOT** .rtf) encoded in UTF-8. You can also save as a markdown file (`.md`)
    + MS Word can "Save As" a .txt file, but make sure when given the option that you select encoding as `Unicode (UTF-8)`, and `End lines with: CR only`. Those options may come up in the save window or in a conversion window that comes up after you hit save in the save window, depending on your version of Word.
    + Note that if you use Word, formatting or embedded images will not be saved in the text file. The exact formatting of this document is **extremely** important. See below for formatting info, how to include images, and [examples](./samples.md)
2. Save the text file of questions in its own folder, with all linked image files copied into that same folder.
    + the name of the **file** will become the name of the test bank or quiz in Canvas.
      + Importing into classic quizzes as a bank will also produce a Canvas "quiz" by default, containing all of the questions, by that same name
    + save any images you want to include as their own files in that same folder. **NOTE FOR IMAGES:** all images will be sized to the width of the viewing window in Canvas (with a max height of 600 px). You can drag to resize the image once it's inserted in Canvas.

### Formatting requirements

+ Each question and related information (hereafter *question blocks*) should be separated by at least one blank line. There should be no blank lines within any question.
    + If you **must** have a paragraph break within a question, use an html line break code (below). You may copy and paste the characters below into your text block wherever you want a new line. See the first example question below. Copy and paste this:
        - `<br>`
+ Each question block may begin with up to three lines of header information. The order of the information does not matter, and you don't need to include any or all of it as described below. 
    + One header line may be a 2 letter (all caps) indicator of question type based on Canvas question types. If no indicator is given, MC is assumed. 
      + `MC`: multiple choice
      + `MA`: multiple answers (select all that apply)
      + `MT`: matching
      + `SA`: short answer (fill in one blank)
      + `MB`: fill in multiple blanks
      + `MD`: multiple dropdowns
      + `ES`: essay, TX: just text, 
      + `NU`: numeric (not well tested)
      + `OR`: ordering
      + `CT`: categorization
      + `HS`: Hot Spot
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
    - Other question types have other formatting requirements for the answers as described below and in the [samples](./samples.md)

### Other Formatting
+ You may use a hash (#) as a comment symbol. Anything on any line that begins with a # will not be processed and uploaded. This lets you write notes to yourself in the text file.
- **Adding formatting**: there are two ways to add formatting like, **bold**, *italics*, ^superscript^, and ~subscript~. This will work in questions **and** in answers.
    1.  The easiest way is to use MarkDown formatting marks.
        + Surrounding some word or characters with two asterices, like `**this**` will make what's between them **bold**. "`this **word**`" yields: "this **word**".
        + One asterix on either side, like `*this*` indicates *italics*
        + surrounding something with carrots like `E = mc^2^` will make it superscript yielding E = mc<sup>2</sup>
        + tildes like `H~2~O` will make it subscript (H<sub>2</sub>O). 
        + The key is to **surround** what you want to format with the marks, without spaces between the modifiers and modifiees.
    2. You may also use standard html tags, where you surround the word or characters you want to format as appropriate:
        + *italics*: `this <em>word</em>` yields: this *word*
        + **bold**: `this <strong>word</strong>` yields: this **word**
        + superscript: `E = mc<sup>2</sup>` yields: E = mc<sup>2</sup>
        + subscript: `H<sub>2</sub>O` yields: H<sub>2</sub>O
    3. You may use both the MarkDown and html styles in the same document

Previous step: [Installation](./installation.md)
Next step: [Importing to Canvas](./importing.md)