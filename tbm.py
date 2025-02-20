#old one without any components
import pygame
import random
import sys
from pygame import mixer
import os


# Pygame Setup and Constants

pygame.init()
#game window or game tab
screen_width=800
screen = pygame.display.set_mode((1200,800),pygame.RESIZABLE)
# Scale factor
scale_factor_x = 1
scale_factor_y = 1

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (100, 149, 237)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

# Fonts
font = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont(None, 40)


# Helper: Number to Words for prize

def num_to_words(n):
    if n == 0:
        return "zero"
    
    under_20 = ["", "one", "two", "three", "four", "five", "six", "seven",
                "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen",
                "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy",
            "eighty", "ninety"]
    thousands = ["", "thousand", "million", "billion"]

    def words(num, idx=0):
        if num == 0:
            return []
        elif num < 20:
            return [under_20[num]] + ([thousands[idx]] if thousands[idx] else [])
        elif num < 100:
            return [tens[num // 10]] + words(num % 10, 0) + ([thousands[idx]] if thousands[idx] and num % 10 == 0 else [])
        else:
            return [under_20[num // 100]] + ["hundred"] + words(num % 100, 0) + ([thousands[idx]] if thousands[idx] and num % 100 == 0 else [])
    
    result = []
    idx = 0
    while n:
        n, rem = divmod(n, 1000)
        if rem:
            result = words(rem, idx) + result
        idx += 1
    return " ".join([w for w in result if w])

def format_prize(n):
    # Returns a string with NPR and words 
    return f"NPR {n} – {num_to_words(n).capitalize()} "


# Questions sets (Easy / Medium / Hard )
# Sample questions are provided for each category.

easy_questions = [
    {
        "question": "Which is the largest country by area?",
        "correct": "Russia",
        "wrong": ["Canada", "USA", "China", "Brazil", "Kazakhstan"]
    },
    {
        "question": "Which is the highest mountain in the world?",
        "correct": "Mount Everest",
        "wrong": ["K2", "Kangchenjunga", "Lhotse", "Makalu", "Cho Oyu"]
    },
    {
        "question": "Which is the longest river in the world?",
        "correct": "Nile",
        "wrong": ["Amazon", "Yangtze", "Mississippi", "Danube", "Ganges"]
    },
    {
        "question": "Which country won the FIFA World Cup in 2018?",
        "correct": "France",
        "wrong": ["Germany", "Brazil", "Argentina", "Spain", "Italy"]
    },
    {
        "question": "Which is the smallest country in the world by area?",
        "correct": "Vatican City",
        "wrong": ["Monaco", "Nauru", "Tuvalu", "San Marino", "Liechtenstein"]
    },
    {
        "question": "Which is the largest ocean in the world?",
        "correct": "Pacific Ocean",
        "wrong": ["Atlantic Ocean", "Indian Ocean", "Southern Ocean", "Arctic Ocean", "Mediterranean Sea"]
    },
    {
        "question": "What is the capital of France?",
        "correct": "Paris",
        "wrong": ["Berlin", "London", "Rome", "Madrid"]
    },
    {
        "question": "Who developed the theory of relativity?",
        "correct": "Albert Einstein",
        "wrong": ["Isaac Newton", "Nikola Tesla", "Marie Curie", "Galileo Galilei"]
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "correct": "Mars",
        "wrong": ["Earth", "Venus", "Jupiter", "Saturn"]
    },
    {
        "question": "How many continents are there on Earth?",
        "correct": "7",
        "wrong": ["5", "6", "8", "9"]
    },
    {
        "question": "What is the largest mammal?",
        "correct": "Blue Whale",
        "wrong": ["Elephant", "Giraffe", "Shark", "Polar Bear"]
    },
    {
        "question": "Which element is represented by the symbol 'O'?",
        "correct": "Oxygen",
        "wrong": ["Osmium", "Ozone", "Oganesson", "Oxycodone"]
    },
    {
        "question": "Which country is famous for the Great Wall?",
        "correct": "China",
        "wrong": ["India", "Japan", "Egypt", "Mexico"]
    },
    {
        "question": "Who wrote the play 'Romeo and Juliet'?",
        "correct": "William Shakespeare",
        "wrong": ["Charles Dickens", "J.K. Rowling", "George Orwell", "Jane Austen"]
    },
    {
        "question": "What is the boiling point of water in Celsius?",
        "correct": "100°C",
        "wrong": ["90°C", "110°C", "120°C", "150°C"]
    },
    {
        "question": "What is the capital of Japan?",
        "correct": "Tokyo",
        "wrong": ["Kyoto", "Osaka", "Seoul", "Beijing"]
    },
    {
        "question": "Who was the first President of the United States?",
        "correct": "George Washington",
        "wrong": ["Thomas Jefferson", "Abraham Lincoln", "John Adams", "Benjamin Franklin"]
    },
    {
        "question": "What is the smallest planet in our solar system?",
        "correct": "Mercury",
        "wrong": ["Mars", "Venus", "Earth", "Pluto"]
    },
    {
        "question": "Which gas do plants absorb from the atmosphere during photosynthesis?",
        "correct": "Carbon Dioxide",
        "wrong": ["Oxygen", "Nitrogen", "Hydrogen", "Methane"]
    },
    {
        "question": "What is the hardest natural substance on Earth?",
        "correct": "Diamond",
        "wrong": ["Gold", "Iron", "Platinum", "Emerald"]
    },
    {
        "question": "Which animal is known as the King of the Jungle?",
        "correct": "Lion",
        "wrong": ["Tiger", "Elephant", "Giraffe", "Cheetah"]
    },
    {
        "question": "What is the largest organ in the human body?",
        "correct": "Skin",
        "wrong": ["Liver", "Heart", "Lungs", "Kidneys"]
    },
    {
        "question": "Which fruit is known as the 'King of Fruits'?",
        "correct": "Durian",
        "wrong": ["Mango", "Banana", "Pineapple", "Apple"]
    }
]


medium_questions = [
    {
        "question": "San Siro is a stadium located in which city?",
        "correct": "Milan",
        "wrong": ["Rome", "Paris", "Madrid", "Berlin"]
    },
    {
        "question": "In which city would you find the historic landmark, the Alhambra?",
        "correct": "Granada",
        "wrong": ["Seville", "Madrid", "Barcelona", "Lisbon"]
    },
    {
        "question": "Which city is known as the 'City of Canals'?",
        "correct": "Venice",
        "wrong": ["Amsterdam", "Paris", "Bangkok", "Venice"]
    },
    {
        "question": "In which city is the famous landmark, the Christ the Redeemer statue, located?",
        "correct": "Rio de Janeiro",
        "wrong": ["Sao Paulo", "Buenos Aires", "Mexico City", "Lima"]
    },
    {
        "question": "Which city is home to the historic landmark, the Colosseum?",
        "correct": "Rome",
        "wrong": ["Athens", "Paris", "London", "New York"]
    },
    {
        "question": "What is the SI unit of electric current?",
        "correct": "Ampere",
        "wrong": ["Volt", "Watt", "Ohm", "Joule"]
    },
    {
        "question": "Who is known as the father of modern physics?",
        "correct": "Albert Einstein",
        "wrong": ["Isaac Newton", "Niels Bohr", "Galileo Galilei", "Max Planck"]
    },
    {
        "question": "What is the term for the amount of matter in an object?",
        "correct": "Mass",
        "wrong": ["Weight", "Density", "Volume", "Force"]
    },
    {
        "question": "What is the speed of light in a vacuum?",
        "correct": "approax. 300,000,000 m/s",
        "wrong": ["approax. 350,000,000 m/s", "150,000,000 m/s", "400,000,000 m/s", "200,000,000 m/s"]
    },
    {
        "question": "What is the principle stating that energy cannot be created or destroyed?",
        "correct": "Conservation of Energy",
        "wrong": ["Newton's First Law", "Second Law of Thermodynamics", "Law of Inertia", "Heisenberg Uncertainty Principle"]
    },
    {
        "question": "Oxalic acid is commonly found in which vegetable?",
        "correct": "Spinach",
        "wrong": ["Carrot", "Potato", "Apple", "Lettuce"]
    },
    {
        "question": "What is the chemical symbol for the element gold?",
        "correct": "Au",
        "wrong": ["Ag", "Fe", "Pb", "Cu"]
    },
    {
        "question": "Which gas is most commonly used in light bulbs?",
        "correct": "Argon",
        "wrong": ["Oxygen", "Nitrogen", "Helium", "Carbon Dioxide"]
    },
    {
        "question": "What is the pH level of Vinegar?",
        "correct": "around 3",
        "wrong": ["around 1", "exctly 2", "around 4", "5"]
    },
    {
        "question": "Which element has the chemical symbol 'Na'?",
        "correct": "Sodium",
        "wrong": ["Nitrogen", "Neon", "Nickel", "Nobelium"]
    },
    {
        "question": "Who won the Golden Boot at the 2018 FIFA World Cup?",
        "correct": "Harry Kane",
        "wrong": ["Cristiano Ronaldo", "Lionel Messi", "Kylian Mbappe", "Eden Hazard"]
    },
    {
        "question": "What does the acronym 'IMF' stand for?",
        "correct": "International Monetary Fund",
        "wrong": ["International Management Fund", "Internal Monetary Fund", "International Market Federation", "Investment Money Fund"]
    },
    {
        "question": "Who is the current Secretary-General of the United Nations?",
        "correct": "António Guterres",
        "wrong": ["Ban Ki-moon", "Kofi Annan", "Boutros Boutros-Ghali", "Dag Hammarskjöld"]
    },
    {
        "question": "What is the capital city of Malaysia?",
        "correct": "Kuala Lumpur",
        "wrong": ["Paro", "Bangkok", "Male", "Lhuntsi"]
    },
    {
        "question": "Which country is known as the Land of the Midnight Sun?",
        "correct": "Norway",
        "wrong": ["Japan", "Denmark", "Czech", "Vietnam"]
    },
    {
        "question": "What is the 2nd largest hot desert in the world?",
        "correct": "Arabian Desert",
        "wrong": ["Gobi Desert", "Thar Desert", "Arctic Desert", "Antarctic Desert"]
    },
    {
        "question": "Which planet is known as the Earth's Twins?",
        "correct": "Venus",
        "wrong": ["Keplar", "Uranus", "Neptune", "Saturn"]
    },
    {
        "question": "Who wrote the Hamlet?",
        "correct": "William Shakespeare",
        "wrong": ["Charles Dickens", "J.K. Rowling", "George Orwell", "Jane Austen"]
    },
    {
        "question": "On a TV screen, the pixels are 1/3 red, 1/3 blue, and 1/3 green.If you want to have yellow light, which parts of the pixel have to glow more brightly than the others?",
        "correct": "Red and Green",
        "wrong": ["Red and Yellow", "Only less Green", "Green and Blue", "Only less Red"]
    },
    {
        "question": "What is the old name of Japan?",
        "correct": "Nippon",
        "wrong": ["Yamato", "Sakoku", "Daitō", "Edo"]
    },
    {
        "question": "What is the capital of Japan?",
        "correct": "Tokyo",
        "wrong": ["Kyoto", "Osaka", "Seoul", "Beijing"]
    },
    {
        "question": "Who was the first President of the United States?",
        "correct": "George Washington",
        "wrong": ["Thomas Jefferson", "Abraham Lincoln", "John Adams", "Benjamin Franklin"]
    },
    {
        "question": "What is the smallest bone  in human body?",
        "correct": "Stapes",
        "wrong": ["Incus", "Femur", "Ear", "anvil"]
    },
    {
        "question": "Which gas do plants absorb from the atmosphere during photosynthesis?",
        "correct": "Carbon Dioxide",
        "wrong": ["Oxygen", "Nitrogen", "Hydrogen", "Methane"]
    },
    {
        "question": "Octopus has how many hearts?",
        "correct": "3",
        "wrong": ["2", "1", "4", "0"]
    }
]


hard_questions = [
    {
        "question": "In which year did World War II end?",
        "correct": "1945",
        "wrong": ["1939", "1942", "1950", "1947", "1955"]
    },
    {
        "question": "Who was the first person to walk on the Moon?",
        "correct": "Neil Armstrong",
        "wrong": ["Buzz Aldrin", "Yuri Gagarin", "Michael Collins", "Alan Bean", "Edwin Aldrin"]
    },
    {
        "question": "What does AI stand for?",
        "correct": "Artificial Intelligence",
        "wrong": ["Automated Information", "Applied Innovation", "Advanced Integration", "Analog Input", "Augmented Insight"]
    },
    {
        "question": "In which year was the US Declaration of Independence signed?",
        "correct": "1776",
        "wrong": ["1783", "1492", "1804", "1765", "1770"]
    },
    {
        "question": "Who composed the symphony known as the 'Jupiter Symphony'?",
        "correct": "Wolfgang Amadeus Mozart",
        "wrong": ["Ludwig van Beethoven", "Johann Sebastian Bach", "Franz Schubert", "Pyotr Ilyich Tchaikovsky"]
    },
    {
        "question": "Which country won the first FIFA World Cup in 1930?",
        "correct": "Uruguay",
        "wrong": ["Argentina", "Brazil", "Italy", "Germany"]
    },
    {
        "question": "Who was the first woman to win a Nobel Prize?",
        "correct": "Marie Curie",
        "wrong": ["Rosalind Franklin", "Dorothy Hodgkin", "Lise Meitner", "Ada Lovelace"]
    },
    {
        "question": "In which year did the Apollo 11 mission land the first humans on the Moon?",
        "correct": "1969",
        "wrong": ["1965", "1971", "1963", "1973"]
    },
    {
        "question": "Which element has the chemical symbol 'W'?",
        "correct": "Tungsten",
        "wrong": ["Tantalum", "Thorium", "Wolfram", "Wolframium"]
    },
    {
        "question": "Who is credited with the discovery of penicillin?",
        "correct": "Alexander Fleming",
        "wrong": ["Marie Curie", "Louis Pasteur", "Joseph Lister", "Edward Jenner"]
    },
    {
        "question": "Who is considered the first computer programmer?",
        "correct": "Ada Lovelace",
        "wrong": ["Charles Babbage", "Alan Turing", "John von Neumann", "Grace Hopper"]
    },
    {
        "question": "Which country hosted the 2008 Summer Olympics?",
        "correct": "China",
        "wrong": ["Greece", "Australia", "United Kingdom", "Brazil"]
    },
    {
        "question": "Who won the Academy Award for Best Director in 2019?",
        "correct": "Bong Joon-ho",
        "wrong": ["Quentin Tarantino", "Martin Scorsese", "Sam Mendes", "Greta Gerwig"]
    },
    {
        "question": "Which artist painted the 'Mona Lisa'?",
        "correct": "Leonardo da Vinci",
        "wrong": ["Vincent van Gogh", "Pablo Picasso", "Claude Monet", "Rembrandt"]
    },
    {
        "question": "In which year did the Titanic sink?",
        "correct": "1912",
        "wrong": ["1905", "1920", "1898", "1915"]
    },
    {
        "question": "Who was the first emperor of China?",
        "correct": "Qin Shi Huang",
        "wrong": ["Han Wudi", "Emperor Wu of Han", "Emperor Gaozu of Han", "Emperor Taizong of Tang"]
    },
    {
        "question": "Which planet is known as the 'Morning Star'?",
        "correct": "Venus",
        "wrong": ["Mars", "Mercury", "Jupiter", "Saturn"]
    },
    {
        "question": "Who wrote the novel '1984'?",
        "correct": "George Orwell",
        "wrong": ["Aldous Huxley", "Ray Bradbury", "H.G. Wells", "Isaac Asimov"]
    },
    {
        "question": "Which country was formerly known as Ceylon?",
        "correct": "Sri Lanka",
        "wrong": ["Thailand", "Myanmar", "Nepal", "Bangladesh"]
    },
    {
        "question": "Who developed the theory of general relativity?",
        "correct": "Albert Einstein",
        "wrong": ["Isaac Newton", "Niels Bohr", "Marie Curie", "Erwin Schrödinger"]
    },
    {
        "question": "Which element has the atomic number 79?",
        "correct": "Gold",
        "wrong": ["Silver", "Platinum", "Copper", "Iron"]
    },
    {
        "question": "Who was the first female Prime Minister of the United Kingdom?",
        "correct": "Margaret Thatcher",
        "wrong": ["Theresa May", "Elizabeth II", "Indira Gandhi", "Golda Meir"]
    },
    {
        "question": "Which country was the first to grant women the right to vote?",
        "correct": "New Zealand",
        "wrong": ["United States", "United Kingdom", "Australia", "Finland"]
    },
    {
        "question": "Who invented the telephone?",
        "correct": "Alexander Graham Bell",
        "wrong": ["Thomas Edison", "Nikola Tesla", "Samuel Morse", "Guglielmo Marconi"]
    },
    {
        "question": "Which city is known as the 'City of Light'?",
        "correct": "Paris",
        "wrong": ["New York", "London", "Tokyo", "Rome"]
    },
    {
        "question": "Who painted the 'Starry Night'?",
        "correct": "Vincent van Gogh",
        "wrong": ["Pablo Picasso", "Claude Monet", "Leonardo da Vinci", "Salvador Dalí"]
    },
    {
        "question": "Who was awarded the Grammy for 'Record of the Year' in 2020?",
        "correct": "Billie Eilish",
        "wrong": ["Lizzo", "Ariana Grande", "Post Malone", "Harry Styles"]
    },
    {
        "question": "Which song belongs to Michael Jackson?",
        "correct": "Billie Jean",
        "wrong": ["Like a Virgin", "I Want It That Way", "Purple Rain", "Imagine"]
    },
    {
        "question": "Which country won the most Olympic medals in 2008?",
        "correct": "United States",
        "wrong": ["China", "Russia", "Germany", "Australia"]
    },
    {
        "question": "Who discovered the rabies vaccine?",
        "correct": "Louis Pasteur",
        "wrong": ["Edward Jenner", "Alexander Fleming", "Robert Koch", "Joseph Lister"]
    },
    {
        "question": "Who is known as the founder of Microsoft?",
        "correct": "Bill Gates",
        "wrong": ["Steve Jobs", "Mark Zuckerberg", "Larry Page", "Elon Musk"]
    },
    {
        "question": "Which baseball player holds the record for the most career home runs?",
        "correct": "Barry Bonds",
        "wrong": ["Hank Aaron", "Babe Ruth", "Alex Rodriguez", "Ken Griffey Jr."]
    },
    {
        "question": "Who won the Nobel Peace Prize in 1993 for the Oslo Accords?",
        "correct": "Yasser Arafat",
        "wrong": ["Nelson Mandela", "Mother Teresa", "Jimmy Carter", "Henry Kissinger"]
    },
    {
        "question": "Who was the first woman to receive a Nobel Prize in Physiology or Medicine?",
        "correct": "Gerty Cori",
        "wrong": ["Rosalind Franklin", "Marie Curie", "Barbara McClintock", "Dorothy Crowfoot Hodgkin"]
    },
    {
        "question": "Which year did the first Oscar ceremony take place?",
        "correct": "1929",
        "wrong": ["1932", "1930", "1927", "1935"]
    },
    {
        "question": "Which country did the first woman astronaut, Valentina Tereshkova, represent?",
        "correct": "Soviet Union",
        "wrong": ["United States", "China", "Germany", "United Kingdom"]
    },
    {
        "question": "Who is credited with inventing the first successful airplane?",
        "correct": "Wright brothers",
        "wrong": ["Charles Lindbergh", "Amelia Earhart", "Howard Hughes", "Glenn Curtiss"]
    },
    {
        "question": "What year did World War I start?",
        "correct": "1914",
        "wrong": ["1912", "1915", "1939", "1905"]
    },
    {
        "question": "Which scientist discovered the electron?",
        "correct": "J.J. Thomson",
        "wrong": ["Ernest Rutherford", "Niels Bohr", "Marie Curie", "Albert Einstein"]
    }
]

# For each category, select a fixed number of questions.
selected_easy = random.sample(easy_questions, 3)
selected_medium = random.sample(medium_questions, 6)
selected_hard = random.sample(hard_questions, 6)

# Combine in order: Easy (1-3), Medium (4-9), Hard (10-15)
all_questions = selected_easy + selected_medium + selected_hard

# Prize levels for each correct answer (15 questions)
prize_levels = [25000, 50000, 100000, 200000, 400000, 800000, 1600000, 3200000, 6400000, 12800000, 25600000, 51200000, 102400000, 204800000, 700000000]


# Function to Generate Options for a Question

def get_options(question_data):
    # Always include the correct answer and choose 3 random wrong answers from the set of 5.
    wrong_options = random.sample(question_data["wrong"], 3)
    options = wrong_options + [question_data["correct"]]
    random.shuffle(options)
    return options


# UI Helper: Draw Text Centered

def draw_text_center(surface, text, font, color, center):
    text_obj = font.render(text, True, color)
    rect = text_obj.get_rect(center=center)
    surface.blit(text_obj, rect)


# Main Game Loop

def main():
    current_question_index = 0
    total_questions = len(all_questions)
    current_prize = 0
    running = True
    selected_option = None  # to store clicked option and select it
    feedback = ""
    show_feedback = False
    feedback_timer = 0

    # Timer: Set start time for the current question
    question_start_time = pygame.time.get_ticks()

    clock = pygame.time.Clock()

    # Pre-calculate options for each question.
    questions_options = []
    for q in all_questions:
        questions_options.append(get_options(q))
    
    while running:
        screen.fill(WHITE)
        
        # Determine the time limit based on current question index.
        if current_question_index < 5:
            time_limit = 20
        elif current_question_index < 10:
            time_limit = 30
        else:
            time_limit = 45
        
        # Calculate elapsed time (in seconds) for the current question.
        elapsed_time = (pygame.time.get_ticks() - question_start_time) / 1000
        time_left = max(0, time_limit - int(elapsed_time))
        
        # Check if time has run out for the current question.
        if elapsed_time > time_limit and not show_feedback:
            feedback = "Time's up! Game Over."
            show_feedback = True
            feedback_timer = pygame.time.get_ticks()
        
        # Display timer on the screen (top-right corner).
        timer_text = font.render(f"Time Left: {time_left}s", True, BLACK)
        screen.blit(timer_text, (screen_width, 20))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not show_feedback:
                mx, my = pygame.mouse.get_pos()
                # Determine if an option was clicked.
                option_rects = []
                start_y = 300
                gap = 60
                for i in range(4):
                    rect = pygame.Rect(100, start_y + i * gap, 400, 20)
                    option_rects.append(rect)
                for idx, rect in enumerate(option_rects):
                    if rect.collidepoint(mx, my):
                        selected_option = questions_options[current_question_index][idx]
                        # Check if answer is correct
                        correct_answer = all_questions[current_question_index]["correct"]
                        if selected_option == correct_answer:
                            feedback = "Correct!"
                            current_prize = prize_levels[current_question_index]
                        else:
                            feedback = "Wrong Answer! Game Over."
                        show_feedback = True
                        feedback_timer = pygame.time.get_ticks()
                        break

        # If all questions answered, display winning message
        if current_question_index >= total_questions:
            screen.fill(WHITE)
            draw_text_center(screen, "Congratulations, you won!", big_font, BLUE, (screen_width//2, screen_height//2 - 20))
            prize_text = format_prize(current_prize)
            draw_text_center(screen, f"Your prize: {prize_text}", big_font, GREEN, (screen_width//2, screen_height//2 + 40))
            pygame.display.update()
            pygame.time.delay(5000)
            running = False
            continue

        # Display current question and options.
        qdata = all_questions[current_question_index]
        options = questions_options[current_question_index]

        # Draw question number and prize info at top.
        header_text = f"Question {current_question_index + 1} / {total_questions} | Prize: {format_prize(current_prize)}"
        header_surface = font.render(header_text, True, BLACK)
        screen.blit(header_surface, (50, 20))

        # Display the question text 
        draw_text_center(screen, qdata["question"], big_font, BLACK, (screen_width//2+50, 200))
        
        # Draw option boxes
        option_rects = []
        start_y = 300
        gap = 60
        for i, option in enumerate(options):
            rect = pygame.Rect(100, start_y + i * gap, 600, 40)
            option_rects.append(rect)
            pygame.draw.rect(screen, GRAY, rect)
            draw_text_center(screen, option, font, BLACK, rect.center)

        # If feedback needs to be shown 
        if show_feedback:
            draw_text_center(screen, feedback, big_font, GREEN if feedback=="Correct!" else RED, (screen_width//2, 550))
            # Show feedback for 1.5 seconds before proceeding.
            if pygame.time.get_ticks() - feedback_timer > 1500:
                if feedback == "Correct!":
                    current_question_index += 1
                    # Reset question start time for the next question.
                    question_start_time = pygame.time.get_ticks()
                else:
                    # Game over, so display final prize
                    draw_text_center(screen, f"Final Prize: {format_prize(current_prize)}", big_font, GREEN, (screen_width//2, 600))
                    pygame.display.update()
                    pygame.time.delay(3000)
                    running = False
                show_feedback = False
                selected_option = None

        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main()
