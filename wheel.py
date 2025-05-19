# fortune_wheel/wheel.py

import pygame
import random
from math import cos, sin, radians

class FortuneWheel:
    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Fortune Wheel')
        self.clock = pygame.time.Clock()
        self.running = True
        self.colors = [
            (255, 69, 0),  # Red
            (0, 128, 0),  # Green
            (0, 0, 255),  # Blue
            (255, 255, 0),  # Yellow
            (255, 0, 255),  # Magenta
            (0, 255, 255)  # Cyan
        ]
        # Updated colors for an appealing display
        self.angle = 0
        self.spin_speed = 0
        self.spinning = False  # Track the spinning state
        self.marker_angle = 0  # Angle for the indicator marker
        self.fortune_messages = [
            "Good luck is coming your way!",
            "A surprise is waiting for you!",
            "You will have a great day!",
            "Expect good news very soon!",
            "Your future looks bright!",
            "A new opportunity is on the horizon!"
        ]

    def spin(self):
        while self.running:
            self.draw_wheel(self.angle, self.marker_angle)  # Draw the wheel immediately

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if not self.spinning:
                        self.spinning = True  # Start spinning when the space bar is pressed
                        self.spin_speed = random.uniform(20, 40)  # Set a random spin speed
                        self.marker_angle = random.uniform(0, 360)  # Set a random marker angle
                    else:
                        self.spinning = False  # Stop spinning when the space bar is pressed again

            if self.spinning:
                self.angle += self.spin_speed
                if self.angle >= 360:
                    self.angle -= 360
                self.draw_wheel(self.angle, self.marker_angle)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def draw_wheel(self, angle=0, marker_angle=0):
        self.screen.fill((255, 255, 255))

        # Draw the wheel
        pygame.draw.circle(self.screen, (0, 0, 0), (250, 250), 200)

        # Draw the colorful sections and associate messages
        for i in range(len(self.fortune_messages)):  # Match the number of sections to the number of messages
            wheel_angle = angle + i * (360 / len(self.fortune_messages))
            section_color = self.colors[i % 3]
            pygame.draw.polygon(self.screen, section_color, [
                (250, 250),
                (250 + 150 * -cos(radians(wheel_angle)), 250 + 150 * -sin(radians(wheel_angle))),
                (250 + 150 * -cos(radians(wheel_angle + 360 / len(self.fortune_messages))), 250 + 150 * -sin(radians(wheel_angle + 360 / len(self.fortune_messages))))
            ])
            # Display fortune message for the current section
            self.display_fortune_message(i, wheel_angle)

        # Draw the indicator arrow with a golden color
        marker_length = 50
        marker_color = (255, 223, 0)  # Golden color
        marker_start = (250 - cos(radians(marker_angle)) * marker_length, 250 - sin(radians(marker_angle)) * marker_length)
        marker_end = (250 + cos(radians(marker_angle)) * marker_length, 250 + sin(radians(marker_angle)) * marker_length)
        pygame.draw.line(self.screen, marker_color, marker_start, marker_end, 5)

        # Draw the sharper arrowhead at the end of the marker line
        arrow_length = 15
        arrow_points = [
            (250 + cos(radians(marker_angle + 150)) * arrow_length, 250 + sin(radians(marker_angle + 150)) * arrow_length),
            (250 + cos(radians(marker_angle)) * (marker_length + 5), 250 + sin(radians(marker_angle)) * (marker_length + 5)),
            (250 + cos(radians(marker_angle - 150)) * arrow_length, 250 + sin(radians(marker_angle - 150)) * arrow_length)
        ]
        pygame.draw.polygon(self.screen, marker_color, arrow_points)

        pygame.display.update()

    def display_fortune_message(self, section, angle):
        font_size = 18
        fortune_font = pygame.font.Font(None, font_size)
        message = self.fortune_messages[section]
        message_lines = self.wrap_text(message, 20)  # Wrap text to fit within the section
        y_offset = 0

        for line in message_lines:
            text_surface = fortune_font.render(line, True, (255, 255, 255))  # White text
            text_rect = text_surface.get_rect()
            text_rect.center = (
                250 + 90 * -cos(radians(angle + (360 / len(self.fortune_messages)) / 2)),
                250 + 90 * -sin(radians(angle + (360 / len(self.fortune_messages)) / 2)) + y_offset
            )
            self.screen.blit(text_surface, text_rect)
            y_offset += 18  # Adjust the line spacing

    def wrap_text(self, text, max_length):
        words = text.split()
        lines = []
        current_line = words[0]

        for word in words[1:]:
            if len(current_line) + len(word) + 1 <= max_length:
                current_line += " " + word
            else:
                lines.append(current_line)
                current_line = word

        lines.append(current_line)
        return lines

if __name__ == '__main__':
    wheel = FortuneWheel(500, 500)
    wheel.spin()