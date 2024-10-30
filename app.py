from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Lista de 50 de întrebări
questions = [
    {"question": "Care este capitala Franței?", "options": ["Paris", "Madrid", "Roma", "Berlin"], "answer": "Paris"},
    {"question": "Cine a scris 'Luceafărul'?", "options": ["Mihai Eminescu", "Ion Creangă", "George Coșbuc", "Tudor Arghezi"], "answer": "Mihai Eminescu"},
    {"question": "Care este cel mai lung fluviu din lume?", "options": ["Nil", "Amazon", "Yangtze", "Mississippi"], "answer": "Amazon"},
    {"question": "În ce an a început al Doilea Război Mondial?", "options": ["1939", "1914", "1945", "1929"], "answer": "1939"},
    {"question": "Care este simbolul chimic al apei?", "options": ["H2O", "O2", "CO2", "HO2"], "answer": "H2O"},
    {"question": "Ce țară a găzduit Jocurile Olimpice de vară din 2016?", "options": ["Brazilia", "China", "Grecia", "Marea Britanie"], "answer": "Brazilia"},
    {"question": "Care este capitala Italiei?", "options": ["Roma", "Paris", "Atena", "Madrid"], "answer": "Roma"},
    {"question": "Cine a compus Simfonia a 9-a?", "options": ["Ludwig van Beethoven", "Wolfgang Amadeus Mozart", "Johann Sebastian Bach", "Franz Schubert"], "answer": "Ludwig van Beethoven"},
    {"question": "Care este cel mai mare ocean de pe Pământ?", "options": ["Oceanul Pacific", "Oceanul Atlantic", "Oceanul Indian", "Oceanul Arctic"], "answer": "Oceanul Pacific"},
    {"question": "În ce an a fost fondată NASA?", "options": ["1958", "1945", "1969", "1973"], "answer": "1958"},
    {"question": "Cine a pictat 'Mona Lisa'?", "options": ["Leonardo da Vinci", "Vincent van Gogh", "Michelangelo", "Pablo Picasso"], "answer": "Leonardo da Vinci"},
    {"question": "Ce element are simbolul chimic 'O'?", "options": ["Oxigen", "Aur", "Carbon", "Hidrogen"], "answer": "Oxigen"},
    {"question": "Care este cea mai mare planetă din sistemul solar?", "options": ["Jupiter", "Saturn", "Neptun", "Uranus"], "answer": "Jupiter"},
    {"question": "Care este cel mai mare deșert din lume?", "options": ["Sahara", "Gobi", "Kalahari", "Desertul Arabiei"], "answer": "Sahara"},
    {"question": "Cine a scris romanul 'Ion'?", "options": ["Liviu Rebreanu", "George Călinescu", "Ion Creangă", "Mihai Eminescu"], "answer": "Liviu Rebreanu"},
    {"question": "Care este viteza luminii?", "options": ["299.792 km/s", "150.000 km/s", "400.000 km/s", "100.000 km/s"], "answer": "299.792 km/s"},
    {"question": "Cine a fost primul om pe Lună?", "options": ["Neil Armstrong", "Buzz Aldrin", "Yuri Gagarin", "Michael Collins"], "answer": "Neil Armstrong"},
    {"question": "Câte continente există pe Pământ?", "options": ["7", "5", "6", "8"], "answer": "7"},
    {"question": "Care este capitala Spaniei?", "options": ["Madrid", "Barcelona", "Lisabona", "Sevilia"], "answer": "Madrid"},
    {"question": "Cine a scris 'Amintiri din copilărie'?", "options": ["Ion Creangă", "Mihai Eminescu", "George Coșbuc", "Liviu Rebreanu"], "answer": "Ion Creangă"},
    {"question": "Care este cel mai înalt vârf muntos din lume?", "options": ["Everest", "K2", "Kangchenjunga", "Lhotse"], "answer": "Everest"},
    {"question": "Care este moneda oficială a Japoniei?", "options": ["Yen", "Euro", "Dolar", "Won"], "answer": "Yen"},
    {"question": "Cine a descoperit gravitația?", "options": ["Isaac Newton", "Albert Einstein", "Galileo Galilei", "Nicolaus Copernicus"], "answer": "Isaac Newton"},
    {"question": "Ce țară are cele mai multe insule?", "options": ["Suedia", "Indonezia", "Filipine", "Japonia"], "answer": "Suedia"},
    {"question": "În ce an a căzut Zidul Berlinului?", "options": ["1989", "1991", "1985", "1990"], "answer": "1989"},
    {"question": "Care este cel mai mare mamifer terestru?", "options": ["Elefantul", "Balena Albastră", "Rinocerul", "Hipopotamul"], "answer": "Elefantul"},
    {"question": "Cine a scris 'Mândrie și prejudecată'?", "options": ["Jane Austen", "Emily Brontë", "Charlotte Brontë", "George Eliot"], "answer": "Jane Austen"},
    {"question": "Cine a inventat becul electric?", "options": ["Thomas Edison", "Nikola Tesla", "Alexander Graham Bell", "Guglielmo Marconi"], "answer": "Thomas Edison"},
    {"question": "Care este cel mai mic stat din lume?", "options": ["Vatican", "Monaco", "San Marino", "Liechtenstein"], "answer": "Vatican"},
    {"question": "Cine a descoperit penicilina?", "options": ["Alexander Fleming", "Marie Curie", "Louis Pasteur", "Gregor Mendel"], "answer": "Alexander Fleming"},
    {"question": "Care este limba oficială în Brazilia?", "options": ["Portugheza", "Spaniola", "Engleza", "Franceza"], "answer": "Portugheza"},
    {"question": "Cine a scris piesa 'Hamlet'?", "options": ["William Shakespeare", "Christopher Marlowe", "Ben Jonson", "John Webster"], "answer": "William Shakespeare"},
    {"question": "Care este capitala Greciei?", "options": ["Atena", "Salonic", "Patras", "Heraklion"], "answer": "Atena"},
    {"question": "În ce an a avut loc primul zbor cu avionul al fraților Wright?", "options": ["1903", "1899", "1912", "1921"], "answer": "1903"},
    {"question": "Cine a pictat 'Cina cea de taină'?", "options": ["Leonardo da Vinci", "Michelangelo", "Raphael", "Donatello"], "answer": "Leonardo da Vinci"},
    {"question": "Care este cel mai mic os din corpul uman?", "options": ["Scărița", "Femurul", "Tibia", "Clavicula"], "answer": "Scărița"},
    {"question": "Care este al doilea cel mai mare continent ca suprafață?", "options": ["Africa", "Asia", "America de Nord", "Europa"], "answer": "Africa"},
    {"question": "Cine a inventat telefonul?", "options": ["Alexander Graham Bell", "Thomas Edison", "Nikola Tesla", "Marconi"], "answer": "Alexander Graham Bell"},
    {"question": "Ce organ al corpului uman produce insulina?", "options": ["Pancreasul", "Ficatul", "Rinichii", "Inima"], "answer": "Pancreasul"},
    {"question": "Cine a scris 'Divina Comedie'?", "options": ["Dante Alighieri", "Francesco Petrarca", "Giovanni Boccaccio", "Luigi Pirandello"], "answer": "Dante Alighieri"},
    {"question": "Care este cel mai populat oraș din lume?", "options": ["Tokyo", "Delhi", "New York", "Shanghai"], "answer": "Tokyo"},
    {"question": "Cine a scris romanul 'Moromeții'?", "options": ["Marin Preda", "Tudor Arghezi", "Liviu Rebreanu", "Mihail Sadoveanu"], "answer": "Marin Preda"},
    {"question": "Care este elementul chimic cu simbolul 'Fe'?", "options": ["Fier", "Aur", "Argint", "Platină"], "answer": "Fier"},
    {"question": "În ce an a avut loc revoluția franceză?", "options": ["1789", "1804", "1792", "1776"], "answer": "1789"},
    {"question": "Care este cel mai mare lac din lume?", "options": ["Marea Caspică", "Lacul Superior", "Lacul Victoria", "Lacul Baikal"], "answer": "Marea Caspică"},
    {"question": "Cine a scris romanul 'Enigma Otiliei'?", "options": ["George Călinescu", "Liviu Rebreanu", "Ion Creangă", "Tudor Arghezi"], "answer": "George Călinescu"}
]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/start')
def start_quiz():
    session['questions'] = random.sample(questions, 20)  # Selectăm 20 de întrebări aleatorii
    session['current_question'] = 0
    session['score'] = 0
    session['wrong_answers'] = []
    return redirect(url_for('question'))

@app.route('/question', methods=['GET', 'POST'])
def question():
    if request.method == 'POST':
        selected_answer = request.form.get('answer')
        current_question = session['questions'][session['current_question']]
        if selected_answer == current_question['answer']:
            session['score'] += 1
        else:
            session['wrong_answers'].append({'question': current_question['question'], 'correct_answer': current_question['answer']})

        session['current_question'] += 1

        if session['current_question'] >= len(session['questions']):
            return redirect(url_for('result'))
    
    question_data = session['questions'][session['current_question']]
    return render_template('question.html', question=question_data)

@app.route('/result')
def result():
    score = session['score']
    wrong_answers = session['wrong_answers']
    return render_template('result.html', score=score, wrong_answers=wrong_answers)

if __name__ == '__main__':
    app.run(debug=True)
