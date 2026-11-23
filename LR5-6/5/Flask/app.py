
import os
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key')

class ContactForm(FlaskForm):
    name = StringField(
        'Ваше ім’я',
        validators=[
            DataRequired(message='Введіть ім’я.'),
            Length(min=2, max=50, message='Ім’я повинно містити від 2 до 50 символів.')
        ]
    )

    email = EmailField(
        'Електронна пошта',
        validators=[
            DataRequired(message='Введіть електронну пошту.'),
            Email(message='Введіть правильну електронну пошту.')
        ]
    )

    topic = SelectField(
        'Тема повідомлення',
        choices=[
            ('question', 'Запитання'),
            ('suggestion', 'Пропозиція'),
            ('other', 'Інше')
        ],
        validators=[DataRequired(message='Оберіть тему повідомлення.')]
    )

    message = TextAreaField(
        'Ваше повідомлення',
        validators=[
            DataRequired(message='Введіть повідомлення.')
        ]
    )

    submit = SubmitField('Надіслати')

    def validate_name(self, field):
        if any(char.isdigit() for char in field.data):
            raise ValidationError('Ім’я не повинно містити цифр.')

    def validate_message(self, field):
        if len(field.data.split()) < 3:
            raise ValidationError('Повідомлення повинно містити мінімум 3 слова.')


@app.context_processor
def inject_year():
    return {'year': datetime.now().year}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/posts/')
def posts():
    return render_template('posts.html')


@app.route('/contact/', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        flash('Ваше повідомлення успішно надіслано!', 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
