# QTI Converter Report Feature

The QTI Converter now automatically generates a comprehensive report each time you convert a text file to QTI format. This report provides valuable insights about your question bank and helps identify potential issues.

## Report Location

The report is saved as a text file in the same directory as your input file with the naming convention:
```
[original_filename]_report.txt
```

For example, if you convert `biology_quiz.txt`, the report will be saved as `biology_quiz_report.txt`.

## Report Contents

The report includes the following sections:

### 1. Question Types Summary
- Count and percentage of each question type (MC, MA, SA, TF, ES, etc.)
- Total number of questions processed
- Breakdown by question type with full question type names

### 2. Images Summary
- Total number of unique images used
- Number of questions that include images
- Complete list of all image files referenced
- Helps verify all required images are present

### 3. Questions Without Correct Answers
- Lists question numbers that don't have correct answers marked
- Particularly useful for identifying incomplete questions
- Provides guidance for manual review

### 4. Multiple Choice Auto-Conversion
- Identifies MC questions that had multiple correct answers
- Shows which questions were automatically converted to MA (Multiple Answer) type
- Helps verify the conversion was intended

### 5. Errors and Issues
- Lists any errors encountered during processing
- Missing image files
- Formatting problems
- Other processing issues

## Sample Report

```
QTI Conversion Report
==================================================
Generated for: biology_quiz

Question Types Summary:
-------------------------
MC (multiple_choice_question): 15 questions (60.0%)
MA (multiple_answers_question): 3 questions (12.0%)
SA (short_answer_question): 4 questions (16.0%)
TF (true_false_question): 2 questions (8.0%)
ES (essay_question): 1 questions (4.0%)
Total Questions: 25

Images Summary:
---------------
Total images used: 5
Questions with images: 8
Image files used:
  - cell_diagram.jpg
  - dna_structure.png
  - mitosis_phases.jpg
  - plant_cell.png
  - protein_synthesis.jpg

Questions Without Correct Answers:
-----------------------------------
Found 2 questions without correct answers:
  - Question 12
  - Question 18
Note: These questions may need manual review.

Multiple Choice Questions with Multiple Correct Answers:
-------------------------------------------------------
Found 1 MC questions with multiple correct answers:
  - Question 7
Note: These have been automatically converted to MA (Multiple Answer) type.
```

## Using the Report

1. **Review Question Distribution**: Ensure you have a good mix of question types appropriate for your assessment
2. **Verify Images**: Check that all listed images are the ones you intended to include
3. **Fix Missing Answers**: Address any questions flagged as having no correct answers
4. **Confirm Auto-conversions**: Verify that MC→MA conversions were intended
5. **Address Errors**: Fix any formatting or missing file issues listed

This report helps ensure your QTI export is complete, properly formatted, and ready for import into Canvas LMS.