def grade_exam(student_exam):
    total = 0
    for answer in student_exam.answers.all():
        if answer.selected_option.is_correct:
            total += answer.question.marks

    student_exam.score = total
    student_exam.save()

