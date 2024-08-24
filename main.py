import random
import pygame as pg
import asyncio
import time

# Define constants
WIDTH, HEIGHT = 500, 400
TURTLE_WIDTH, TURTLE_HEIGHT = 30, 30
COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
Y_POSITIONS = [50, 100, 150, 200, 250, 300]
LINE_HEIGHT = 30  # Adjusted line height for better text fit

async def get_user_bet(screen, title_font, text_font, input_box):
    color_inactive = pg.Color('lightskyblue3')
    color_active = pg.Color('dodgerblue2')
    bg_color = pg.Color('white')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return None
            if event.type == pg.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
                bg_color = pg.Color('white') if active else pg.Color('lightskyblue3')
            if event.type == pg.KEYDOWN:
                if active:
                    if event.key == pg.K_RETURN:
                        user_bet = text.strip().lower()
                        if user_bet in COLORS:
                            done = True
                        text = ''
                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(pg.Color("white"))  # Clear screen before drawing
        instructions = [
            "Welcome to the Turtle Race!",
            "Place your bet on a turtle's color.",
            "Colors: red, orange, yellow, green, blue, purple.",
            "Click on the text box and type your chosen color.",
            "Press Enter to submit your bet.",
            "Good luck!"
        ]
        y_offset = 20
        max_width = WIDTH - 40  # Margin of 20 on each side

        # Render and display the main title with the title font centered
        title_surface = title_font.render(instructions[0], True, pg.Color("black"))
        title_rect = title_surface.get_rect(center=(WIDTH // 2, y_offset + LINE_HEIGHT // 2))
        screen.blit(title_surface, title_rect)
        y_offset += LINE_HEIGHT

        # Use the normal text font for the rest of the instructions
        for line in instructions[1:]:
            wrapped_lines = []
            words = line.split(' ')
            current_line = words[0]
            
            for word in words[1:]:
                test_line = current_line + ' ' + word
                if text_font.size(test_line)[0] <= max_width:
                    current_line = test_line
                else:
                    wrapped_lines.append(current_line)
                    current_line = word
            wrapped_lines.append(current_line)
            
            for wrapped_line in wrapped_lines:
                text_surface = text_font.render(wrapped_line, True, pg.Color("black"))
                text_rect = text_surface.get_rect(center=(WIDTH // 2, y_offset + LINE_HEIGHT // 2))
                screen.blit(text_surface, text_rect)
                y_offset += LINE_HEIGHT

        # Adjust the input box position below the last instruction line
        input_box.y = y_offset + 20
        # Center the input box horizontally
        input_box.x = (WIDTH - input_box.w) // 2
        
        txt_surface = text_font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        pg.draw.rect(screen, bg_color, input_box)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pg.draw.rect(screen, color, input_box, 2)

        pg.display.flip()
        await asyncio.sleep(0.01)

    return user_bet

async def race(screen, title_font, text_font, user_bet):
    # Seed the random number generator
    random.seed(time.time())

    # Create turtle surfaces
    all_turtles = []
    for color, y in zip(COLORS, Y_POSITIONS):
        turtle_surface = pg.Surface((TURTLE_WIDTH, TURTLE_HEIGHT))
        turtle_surface.fill(pg.Color(color))
        all_turtles.append([turtle_surface, 0, y])  # [surface, x_pos, y_pos]

    # Main loop for the race
    is_race_on = True
    while is_race_on:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return None, None

        screen.fill(pg.Color("white"))  # Clear screen before drawing
        for turtle_surface, x_pos, y_pos in all_turtles:
            screen.blit(turtle_surface, (x_pos, y_pos))
        
        pg.display.flip()
        
        # Move turtles
        for index, turtle in enumerate(all_turtles):
            move_distance = random.randint(0, 10)  # Randomly determine move distance
            turtle[1] += move_distance  # Update x_pos
            if turtle[1] > WIDTH - TURTLE_WIDTH:  # Turtle reached the end
                is_race_on = False
                winning_color = COLORS[index]
                break
        
        await asyncio.sleep(0)  # Yield control back to the event loop

    # Display the result of the race
    screen.fill(pg.Color("white"))
    if winning_color == user_bet:
        result_text = f"You've won! The {winning_color} turtle is the winner!"
    else:
        result_text = f"You've lost! The {winning_color} turtle is the winner!"

    result_surface = title_font.render(result_text, True, pg.Color("black"))
    result_rect = result_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(result_surface, result_rect)

    return winning_color, user_bet

async def show_play_again(screen, text_font):
    button_color = pg.Color("lightblue")  # Change this to your preferred button color
    border_color = pg.Color("darkblue")   # Change this to your preferred border color
    text_color = pg.Color("black")        # Change this to your preferred text color
    
    button_rect = pg.Rect(WIDTH // 2 - 60, HEIGHT // 2 + 40, 120, 40)
    screen.fill(button_color, button_rect)  # Draw button background
    pg.draw.rect(screen, border_color, button_rect, 2)  # Draw button border
    
    button_text = text_font.render("Play Again", True, text_color)
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)
    pg.display.flip()

    waiting_for_response = True

    while waiting_for_response:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return False
            if event.type == pg.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return True
                else:
                    return False

        await asyncio.sleep(0.1)

async def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Turtle Race")

    # Load custom fonts after initializing Pygame
    title_font = pg.font.Font("Matemasie-Regular.ttf", 20)  # Bigger font for titles
    text_font = pg.font.Font("Poppins-Regular.ttf", 18)     # Normal text font
    
    while True:
        input_box = pg.Rect(100, 100, 140, 32)
        user_bet = await get_user_bet(screen, title_font, text_font, input_box)

        if user_bet is None:
            return  # Quit if user closes the game before placing a bet

        winning_color, user_bet = await race(screen, title_font, text_font, user_bet)
        if winning_color is None:
            return  # Quit if user closes the game during the race

        # Show play again button and wait for response
        play_again = await show_play_again(screen, text_font)
        if not play_again:
            break

    pg.quit()

# This is the program entry point:
if __name__ == "__main__":
    asyncio.run(main())
