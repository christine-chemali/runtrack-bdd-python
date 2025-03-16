import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

load_dotenv()
passw = os.getenv("PASSWORD")

def populate_categories_and_products():
    try:

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=passw,
            database="store" 
        )

        cursor = connection.cursor()

        categories = [
            ("Action Figures",),
            ("Board Games",),
            ("Dolls",),
            ("Educational Toys",),
            ("Puzzles",),
            ("Outdoor Toys",),
            ("Vehicles",)
        ]

        insert_category_query = "INSERT INTO category (name) VALUES (%s)"
        cursor.executemany(insert_category_query, categories)
        connection.commit()
        print("Categories added successfully.")

        products = [
            # Action Figures
            ("Superhero Action Figure", "A detailed superhero action figure.", 20, 50, 1),
            ("Villain Action Figure", "A detailed villain action figure.", 18, 40, 1),
            ("Transforming Robot Figure", "A robot that transforms into a vehicle.", 25, 20, 1),
            ("Classic Action Figure", "An action figure from classic movies.", 23, 30, 1),
            ("Fantasy Warrior Figure", "A warrior figure from a fantasy series.", 26, 25, 1),
            ("Space Explorer Figure", "An astronaut figure for space exploration.", 20, 15, 1),
            ("Monster Action Figure", "A scary monster action figure.", 16, 35, 1),
            ("Ninja Action Figure", "A stealthy ninja figure with accessories.", 22, 30, 1),
            ("Pirate Action Figure", "A rugged pirate ready for adventure.", 21, 25, 1),
            ("Robot Warrior Figure", "A futuristic robot warrior figure.", 27, 20, 1),
            ("Dragon Slayer Figure", "A heroic figure ready to slay dragons.", 28, 15, 1),
            ("Zombie Action Figure", "A creepy zombie figure for horror fans.", 19, 35, 1),
            ("Super Spy Figure", "A secret agent figure with gadgets.", 24, 30, 1),
            ("Monster Hunter Figure", "A figure that hunts down monsters.", 25, 20, 1),
            ("Alien Action Figure", "An extraterrestrial figure from another world.", 30, 15, 1),
            ("Samurai Warrior Figure", "A traditional samurai warrior figure.", 26, 25, 1),
            ("Vampire Action Figure", "A vampire figure with spooky accessories.", 20, 40, 1),
            ("Cyborg Action Figure", "A half-human, half-machine figure.", 29, 10, 1),
            ("Knight Action Figure", "A noble knight in shining armor.", 22, 30, 1),
            ("Superheroine Action Figure", "A powerful superheroine figure.", 21, 25, 1),
            ("Gladiator Action Figure", "A fierce gladiator ready for battle.", 24, 20, 1),
            ("Robot Sidekick Figure", "A friendly robot sidekick figure.", 18, 35, 1),
            
            # Board Games
            ("Classic Board Game", "A timeless board game for family fun.", 25, 30, 2),
            ("Strategy Board Game", "A game that requires strategic thinking.", 30, 15, 2),
            ("Party Board Game", "A fun game for parties and gatherings.", 20, 25, 2),
            ("Trivia Game", "A game that tests your knowledge.", 18, 20, 2),
            ("Word Game", "A fun game that challenges your vocabulary.", 16, 10, 2),
            ("Card Game", "A fast-paced card game for all ages.", 14, 40, 2),
            ("Adventure Board Game", "A game that takes you on an adventure.", 35, 12, 2),
            ("Family Game Night Pack", "A collection of games for family night.", 40, 8, 2),
            ("Mystery Board Game", "A game filled with puzzles and secrets to uncover.", 22, 20, 2),
            ("Word Search Game", "An entertaining game for word search enthusiasts.", 15, 30, 2),
            ("Dice Game", "A classic dice game for family fun.", 12, 50, 2),
            ("Memory Card Game", "A memory challenge game for all ages.", 10, 35, 2),
            ("Classic Chess Set", "A timeless chess set for strategy lovers.", 30, 15, 2),
            ("Checkers Game", "A classic checkers game for two players.", 10, 40, 2),
            ("Family Bingo Game", "A fun bingo game for family gatherings.", 15, 25, 2),
           
            # Dolls
            ("Barbie Doll", "A classic Barbie doll with accessories.", 23, 20, 3),
            ("Baby Doll", "A soft baby doll for nurturing play.", 20, 30, 3),
            ("Fashion Doll Set", "A set of dolls with various outfits.", 25, 15, 3),
            ("Toddler Doll", "A cute doll for toddlers.", 20, 25, 3),
            ("Collectible Doll", "A collectible doll for enthusiasts.", 30, 10, 3),
            ("Dollhouse", "A beautiful dollhouse for imaginative play.", 70, 5, 3),
            ("Doll Accessories Set", "Accessories for your favorite dolls.", 13, 40, 3),
            ("Fashion Doll Car", "A stylish car for fashion dolls.", 25, 12, 3),
            ("Princess Doll", "A beautiful princess doll with a sparkling gown.", 28, 15, 3),
            ("Fairy Doll", "A magical fairy doll with wings and accessories.", 24, 20, 3),
            ("Sports Star Doll", "A sporty doll with athletic gear.", 22, 25, 3),
            ("Vintage Doll", "A classic vintage-style doll for collectors.", 35, 10, 3),
            ("Doctor Doll", "A doctor doll with a medical kit.", 19, 30, 3),
            ("Artist Doll", "A creative artist doll with painting supplies.", 21, 20, 3),
            ("Doll Family Set", "A family set of dolls for playtime adventures.", 40, 8, 3),
            ("Interactive Talking Doll", "A doll that talks and interacts with kids.", 50, 12, 3),
            ("Travel Doll Set", "A set of dolls ready for travel adventures.", 27, 15, 3),
            
            # Educational Toys
            ("STEM Learning Kit", "A kit to enhance learning in science and math.", 35, 15, 4),
            ("Building Blocks Set", "Colorful blocks for creative building.", 20, 25, 4),
            ("Math Puzzle Game", "A fun game that teaches math skills.", 15, 20, 4),
            ("Science Experiment Kit", "Perform exciting science experiments.", 30, 8, 4),
            ("Coding Robot", "A robot that teaches coding basics.", 50, 10, 4),
            ("Art Supplies Kit", "A complete kit for budding artists.", 20, 30, 4),
            ("Interactive Globe", "An interactive globe that teaches geography.", 30, 5, 4),
            ("Language Learning Game", "A fun way to learn a new language.", 25, 15, 4),
            ("Robot Building Kit", "A kit to build and program your own robot.", 45, 12, 4),
            ("Puzzle Map", "A colorful map puzzle to learn geography.", 18, 25, 4),
            ("Engineering Kit", "A kit that teaches engineering concepts through building.", 40, 10, 4),
            ("Creative Writing Kit", "A kit to inspire young authors.", 22, 20, 4),
            ("Math Flashcards", "Flashcards to make learning math fun.", 12, 30, 4),
            ("Science Lab Kit", "A lab kit with experiments for budding scientists.", 35, 8, 4),
            ("Coding Board Game", "A board game that teaches basic coding skills.", 28, 15, 4),
            ("Music Learning Set", "An interactive set to learn music basics.", 25, 18, 4),
            ("Outdoor Science Kit", "Explore nature with this outdoor science kit.", 30, 15, 4),
            ("Memory Game", "A game that enhances memory and cognitive skills.", 15, 25, 4),
            ("Art and Craft Kit", "A fun kit for creative arts and crafts.", 20, 30, 4),
            ("Robotics Learning Kit", "Learn robotics with this comprehensive kit.", 55, 10, 4),
            
            # Puzzles
            ("Jigsaw Puzzle", "A 1000-piece jigsaw puzzle.", 13, 25, 5),
            ("3D Puzzle", "A challenging 3D puzzle to build.", 20, 20, 5),
            ("Puzzle Cube", "A classic cube puzzle for all ages.", 7, 40, 5),
            ("Wooden Puzzle", "A colorful wooden puzzle for toddlers.", 10, 35, 5),
            ("Large Piece Puzzle", "An easy-to-handle puzzle for young children.", 13, 30, 5),
            ("Mystery Puzzle", "A puzzle that reveals a mystery image.", 18, 15, 5),
            ("Puzzle Roll-Up Mat", "A mat to store your unfinished puzzles.", 10, 50, 5),
            ("Puzzle Book", "A book filled with various puzzles to solve.", 15, 25, 5),
            ("Floor Puzzle", "A large floor puzzle for toddlers.", 15, 20, 5),
            ("Puzzle Ball", "A spherical puzzle that challenges your skills.", 20, 15, 5),
            ("Animal Puzzle", "A colorful animal-themed jigsaw puzzle.", 12, 30, 5),
            ("Magnetic Puzzle", "A puzzle with magnetic pieces for easy play.", 22, 18, 5),
            ("Puzzle Challenge Set", "A set of different puzzles for all skill levels.", 28, 15, 5),
            
            # Outdoor Toys
            ("Frisbee", "A flying disc for outdoor fun.", 7, 40, 6),
            ("Kite", "A colorful kite for flying on windy days.", 10, 30, 6),
            ("Water Gun", "A fun water gun for summer play.", 10, 35, 6),
            ("Jump Rope", "A jump rope for active play.", 5, 50, 6),
            ("Badminton Set", "A complete set for badminton play.", 25, 15, 6),
            ("Bubble Maker", "A bubble machine for outdoor fun.", 20, 20, 6),
            ("Sand Play Set", "A set for playing in the sand.", 15, 25, 6),
            ("Outdoor Adventure Kit", "A kit with tools for outdoor exploration.", 30, 10, 6),
            ("Tennis Ball Set", "A set of tennis balls for outdoor sports.", 12, 30, 6),
            ("Outdoor Sports Ball", "A versatile ball for various outdoor games.", 14, 25, 6),
            ("Fishing Rod Set", "A beginner's fishing rod set for kids.", 28, 10, 6),
            ("Outdoor Picnic Set", "A set for outdoor picnics and gatherings.", 40, 12, 6),
            ("Garden Play Set", "A set of tools for gardening fun.", 18, 20, 6),
            
            # Vehicles
            ("Miniature Car Set", "A set of miniature cars for collectors.", 10, 35, 7),
            ("Remote Control Car", "A fast remote-controlled car.", 30, 10, 7),
            ("Toy Train Set", "A toy train set with tracks and accessories.", 25, 15, 7),
            ("Race Car Track Set", "A thrilling race car track set.", 40, 8, 7),
            ("Diecast Model Cars", "Collectible diecast model cars.", 15, 25, 7),
            ("Toy Helicopter", "A remote-controlled toy helicopter.", 25, 15, 7),
            ("Construction Vehicle Set", "A set of toy construction vehicles.", 25, 12, 7),
            ("Fire Truck Toy", "A toy fire truck with lights and sounds.", 20, 20, 7),
            ("Monster Truck", "A large monster truck for off-road fun.", 35, 10, 7),
            ("Police Car Toy", "A toy police car with realistic features.", 20, 25, 7),
            ("Toy Airplane", "A toy airplane for imaginative play.", 28, 15, 7),
            ("Construction Playset", "A playset with construction vehicles and workers.", 45, 8, 7),
            ("Vintage Car Model", "A collectible vintage car model.", 18, 30, 7),
            ("Dragster Car Set", "A set of dragster cars for racing.", 32, 12, 7),
            ("Toy Boat", "A toy boat for water play.", 15, 20, 7),
            ("Electric Train Set", "An electric train set with tracks.", 50, 5, 7),
            ("Tractor Toy", "A toy tractor with detachable accessories.", 22, 18, 7),
            ("RC Drone", "A remote-controlled drone for aerial fun.", 60, 10, 7),
        ]

        insert_product_query = "INSERT INTO product (name, description, price, quantity, id_category) VALUES (%s, %s, %s, %s, %s)"
        cursor.executemany(insert_product_query, products)
        connection.commit()
        print("Products added successfully.")

    except Error as e:
        print(f"An error occurred: {e}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():  
            connection.close()
        print("Database connection is closed.")

if __name__ == "__main__":
    populate_categories_and_products()