"""
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageTk, ImageFont
import math
import random
import arabic_reshaper
from bidi.algorithm import get_display

class SpinnerWheel:
    def __init__(self, root, size=600):
        self.root = root
        self.size = size
        self.margin = 40  # Define margin for padding inside the canvas
        self.center = size // 2
        self.radius = self.center - self.margin  # Adjust radius to account for margin
        self.sector_dict = self.generate_sectors()  # Store key-value pairs
        self.sectors = list(self.sector_dict.keys())  # Only the keys for display
        self.colors = self.generate_colors()
        self.angle_offset = 0
        self.is_spinning = False

        self.create_widgets()

    def generate_sectors(self):
        # Dictionary for keys and values
        return {
            "1": "دَرِّبْنِي فِي حَقِّكَ وَعَلِّمْنِي، فَإِنَّكَ أَنْتَ الإِلَهُ مُخَلِّصِي، وَإِيَّاكَ أَرْجُو طَوَالَ النَّهَارِ.",
            "2": "يَا رَبُّ عَرِّفْنِي طُرُقَكَ، عَلِّمْنِي سُبُلَكَ.",
            "3": "دَرِّبْنِي فِي حَقِّكَ وَعَلِّمْنِي، فَإِنَّكَ أَنْتَ الإِلَهُ مُخَلِّصِي، وَإِيَّاكَ أَرْجُو طَوَالَ النَّهَارِيُطْلِعُ الرَّبُّ خَائِفِيهِ عَلَى مَقَاصِدِهِ الْخَفِيَّةِ، وَيَتَعَهَّدُ تَعْلِيمَهُمْ.",
            "4": "دَرِّبْنِي فِي حَقِّكَ وَعَلِّمْنِي، فَإِنَّكَ أَنْتَ الإِلَهُ مُخَلِّصِي، وَإِيَّاكَ أَرْجُو طَوَالَ النَّهَارِلَا تَذْكُرْ خَطَايَا صِبَايَ الَّتِي ارْتَكَبْتُهَا، وَلَا مَعَاصِيَّ، بَلِ اذْكُرْنِي وَفْقاً لِرَحْمَتِكَ وَمِنْ أَجْلِ جُودِكَ يَا رَبُّ.",
            "5": "فَإِنَّ كُلَّ مَنْ يَرْجُوكَ لَنْ يَخِيبَ. أَمَّا الْغَادِرُونَ بِغَيْرِهِمْ مِنْ غَيْرِ عِلَّةٍ، فَسَيَخْزَوْنَ.",
            "6": "ٱلْبَسُوا سِلَاحَ ٱللهِ ٱلْكَامِلَ لِكَيْ تَقْدِرُوا أَنْ تَثْبُتُوا ضِدَّ مَكَايِدِ إِبْلِيسَ.\n(أَفَسُسَ 6:11)",
            "7": "أَنْتَ سِتْرٌ لِي. مِنَ ٱلضِّيقِ تَحْفَظُنِي. بِتَرَنُّمِ ٱلنَّجَاةِ تَكْتَنِفُنِي. سِلَاهْ.\n(اَلْمَزَامِيرُ 32:‏7)"
        }

    def generate_colors(self):
        # Generate a list of distinct colors for the sectors
        base_colors = [
            "#FF5733", "#33FF57", "#3357FF", "#F333FF",
            "#FF33A8", "#33FFF5", "#F5FF33", "#FF8C33",
            "#8C33FF", "#33FF8C", "#FF3333", "#33A8FF",
            "#FFC300", "#DAF7A6", "#C70039", "#900C3F",
            "#581845", "#1ABC9C", "#2ECC71", "#3498DB",
            "#9B59B6", "#34495E", "#16A085", "#27AE60",
            "#2980B9", "#8E44AD"
        ]
        # Repeat the base colors to match the number of sectors
        return base_colors * (len(self.sectors) // len(base_colors) + 1)

    def create_widgets(self):
        # Top Frame for Title and Spin Button
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)

        # Title Label
        title_label = tk.Label(top_frame, text="رسالة ليك", font=("Arial", 24, "bold"))
        title_label.pack(side=tk.LEFT, padx=10)

        # Spin Button
        spin_button = tk.Button(top_frame, text="لف", command=self.spin, bg="#2196F3", fg="black", font=("Arial", 16, "bold"), width=6, height=1)
        spin_button.pack(side=tk.RIGHT, padx=10)
        self.spin_button = spin_button  # Reference for enabling/disabling

        # Middle Frame for Wheel with padding
        middle_frame = tk.Frame(self.root)
        middle_frame.pack()

        # Canvas for the wheel with padding
        self.canvas = tk.Canvas(
            middle_frame,
            width=self.size,
            height=self.size,
            bg="white",
            borderwidth=2,
            relief="solid"
        )
        self.canvas.pack()

        # Draw initial wheel
        self.update_wheel()

        # Draw pointer
        self.draw_pointer()

        # Bottom Frame for Result Display
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(pady=10)

        self.result_label = tk.Label(bottom_frame, text=" ", font=("Arial", 18), fg="blue")
        self.result_label.pack(side=tk.LEFT, padx=5)

    def draw_pointer(self):
        # Draw a simple triangular pointer at the top center
        pointer_size = 20
        self.canvas.create_polygon(
            self.center - pointer_size, 10,  # Adjusted Y-coordinate for better visibility
            self.center + pointer_size, 10,
            self.center, pointer_size + 10,
            fill="black"
        )

    def update_wheel(self):
        self.num_sectors = len(self.sectors)
        self.angle_step = 360 / self.num_sectors
        self.wheel_image = self.create_wheel_image()
        self.display_image()

    def create_wheel_image(self):
        # Create a blank image with transparent background
        image = Image.new("RGBA", (self.size, self.size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)

        # Load Arabic-supporting font
        font = self.get_font()

        # Draw each sector
        for i, sector_key in enumerate(self.sectors):
            start_angle = i * self.angle_step
            end_angle = start_angle + self.angle_step
            color = self.colors[i % len(self.colors)]

            # Draw the sector with margin
            draw.pieslice(
                [self.margin, self.margin, self.size - self.margin, self.size - self.margin],
                start=start_angle,
                end=end_angle,
                fill=color,
                outline="black"
            )

            # Calculate text position
            text_angle = math.radians(start_angle + self.angle_step / 2)
            text_radius = self.radius * 0.7  # Increase the radius to give more space
            text_x = self.center + text_radius * math.cos(text_angle)
            text_y = self.center - text_radius * math.sin(text_angle)

            # Determine if the sector_key is numeric
            if sector_key.isdigit():
                display_text = sector_key  # Use the key directly for numeric labels
            else:
                # Get the Arabic text value
                arabic_text = sector_key  # Use the key as the sector label
                reshaped_text = arabic_reshaper.reshape(arabic_text)
                display_text = get_display(reshaped_text)

            # Calculate text bounding box
            bbox = draw.textbbox((0, 0), display_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            # Adjust text position to center it
            text_x -= text_width / 2
            text_y -= text_height / 2

            # Ensure text is within bounds
            if text_x < self.margin:
                text_x = self.margin
            elif text_x + text_width > self.size - self.margin:
                text_x = self.size - self.margin - text_width

            if text_y < self.margin:
                text_y = self.margin
            elif text_y + text_height > self.size - self.margin:
                text_y = self.size - self.margin - text_height

            # Draw the text
            draw.text((text_x, text_y), display_text, fill="black", font=font)

        return image

    def get_font(self):
        try:
            # Replace 'Amiri-Regular.ttf' with the path to your Arabic-supporting font file
            return ImageFont.truetype("Amiri-Regular.ttf", 24)
        except IOError:
            # Fallback to default font if the specified font is not found
            return ImageFont.load_default()

    def display_image(self):
        # Rotate the wheel image based on current angle offset
        rotated = self.wheel_image.rotate(self.angle_offset, resample=Image.BICUBIC)
        self.tk_image = ImageTk.PhotoImage(rotated)
        self.canvas.create_image(self.center, self.center, image=self.tk_image)

    def spin(self):
        if self.is_spinning:
            return
        if not self.sectors:
            messagebox.showinfo("Info", "No sectors to spin!")
            return

        self.is_spinning = True
        self.spin_button_state(False)

        # Determine total rotation
        self.total_rotation = random.randint(5, 10) * 360  # 5 to 10 full rotations
        self.final_angle = random.randint(0, 360)
        self.current_rotation = 0
        self.animation_speed = 30  # Milliseconds per frame
        self.rotate_increment = 30  # Degrees per frame

        # Start spinning
        self.animate_spin()

    def animate_spin(self):
        if self.current_rotation < self.total_rotation + self.final_angle:
            # Easing: Slow down as it approaches the final rotation
            if self.current_rotation > self.total_rotation:
                deceleration = self.current_rotation - self.total_rotation
                self.rotate_increment = max(5, self.rotate_increment - deceleration / 100)
            else:
                self.rotate_increment = 30

            self.angle_offset = (self.angle_offset + self.rotate_increment) % 360
            self.display_image()
            self.current_rotation += self.rotate_increment

            self.root.after(self.animation_speed, self.animate_spin)
        else:
            self.is_spinning = False
            self.spin_button_state(True)
            self.show_result()

    def spin_button_state(self, state):
        # Enable or disable the spin button
        self.spin_button.config(state=tk.NORMAL if state else tk.DISABLED)

    def show_result(self):
        # Determine which sector is at the top (where the pointer is)
        normalized_angle = self.angle_offset % 360
        selected_sector_index = (self.num_sectors - int(normalized_angle / self.angle_step)) % self.num_sectors
        selected_key = self.sectors[selected_sector_index]

        # Get the corresponding value
        selected_value = self.sector_dict[selected_key]

        # Create a new window for the result
        result_window = tk.Toplevel(self.root)
        result_window.title("الرسالة")

        # Add a label to display the result
        arabic_text = selected_value
        reshaped_text = arabic_reshaper.reshape(arabic_text)  # Correct its shape
        bidi_text = get_display(reshaped_text)
        result_label = tk.Label(
            result_window,
            text=f"{selected_key}:\n{bidi_text}",
            font=("Arial", 18),
            fg="blue",
            justify="center"  # Center the text alignment
        )
        result_label.pack(padx=20, pady=20)

        # Add a button to close the result window
        close_button = tk.Button(result_window, text="إغلاق", command=result_window.destroy)
        close_button.pack(pady=10)

    @staticmethod
    def run():
        root = tk.Tk()
        root.title("Spinner Wheel Game")
        root.resizable(False, False)

        # Initialize the spinner wheel
        spinner = SpinnerWheel(root, size=600)

        root.mainloop()


if __name__ == "__main__":
    SpinnerWheel.run()
"""

# Worked And Executed
"""
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageTk, ImageFont
import math
import random
import arabic_reshaper
from bidi.algorithm import get_display


class SpinnerWheel:
    def __init__(self, root, size=600):
        self.root = root
        self.size = size
        self.margin = 40  # Define margin for padding inside the canvas
        self.center = size // 2
        self.radius = self.center - self.margin  # Adjust radius to account for margin
        self.sector_dict = self.generate_sectors()  # Store key-value pairs
        self.sectors = list(self.sector_dict.keys())  # Only the keys for display
        self.colors = self.generate_colors()
        self.angle_offset = 0
        self.is_spinning = False

        self.result_window = None  # Initialize the result window reference

        self.create_widgets()

    def generate_sectors(self):
        # Dictionary for keys and values
        return {
            "1": "ٱلْبَسُوا سِلَاحَ ٱللهِ ٱلْكَامِلَ لِكَيْ تَقْدِرُوا أَنْ تَثْبُتُوا ضِدَّ مَكَايِدِ إِبْلِيسَ.",
            "2": "أَنْتَ سِتْرٌ لِي. مِنَ ٱلضِّيقِ تَحْفَظُنِي. بِتَرَنُّمِ ٱلنَّجَاةِ تَكْتَنِفُنِي. سِلَاهْ.",
            "3": "ٱللهُ لَنَا مَلْجَأٌ وَقُوَّةٌ. عَوْنًا فِي ٱلضِّيْقَاتِ وُجِدَ شَدِيدًا.",
            "4": "تَشَدَّدُوا وَتَشَجَّعُوا. لَا تَخَافُوا وَلَا تَرْهَبُوا وُجُوهَهُمْ، لِأَنَّ ٱلرَّبَّ إِلَهَكَ سَائِرٌ مَعَكَ. لَا يُهْمِلُكَ وَلَا يَتْرُكُكَ.",
            "5": "كُلُّ آلَةٍ صُوِّرَتْ ضِدَّكِ لَا تَنْجَحُ، وَكُلُّ لِسَانٍ يَقُومُ عَلَيْكِ فِي ٱلْقَضَاءِ تَحْكُمِينَ عَلَيْهِ. هَذَا هُوَ مِيرَاثُ عَبِيدِ ٱلرَّبِّ وَبِرُّهُمْ مِنْ عِنْدِي، يَقُولُ ٱلرَّبُّ.",
            "6": "حَتَّى إِنَّنَا نَقُولُ وَاثِقِينَ: «ٱلرَّبُّ مُعِينٌ لِي فَلَا أَخَافُ. مَاذَا يَصْنَعُ بِي إِنْسَانٌ؟».",
            "7": "وَتَجْعَلُ لِي تُرْسَ خَلَاصِكَ وَيَمِينُكَ تَعْضُدُنِي، وَلُطْفُكَ يُعَظِّمُنِي. تُوَسِّعُ خُطُوَاتِي تَحْتِي، فَلَمْ تَتَقَلْقَلْ عَقِبَايَ.",
            "8": "اِحْفَظْنِي يَا ٱللهُ لِأَنِّي عَلَيْكَ تَوَكَّلْتُ.",
            "9": "ٱلرَّبُّ يُقَاتِلُ عَنْكُمْ وَأَنْتُمْ تَصْمُتُونَ.",
            "10": "ٱلرَّبُّ لِي فَلَا أَخَافُ. مَاذَا يَصْنَعُ بِي ٱلْإِنْسَانُ؟",
            "11": "سِتْرِي وَمِجَنِّي أَنْتَ. كَلَامَكَ ٱنْتَظَرْتُ.",
            "12": "أَسْتَطِيعُ كُلَّ شَيْءٍ فِي ٱلْمَسِيحِ ٱلَّذِي يُقَوِّينِي.",
            "13": "وَإِلَى ٱلشَّيْخُوخَةِ أَنَا هُوَ، وَإِلَى ٱلشَّيْبَةِ أَنَا أَحْمِلُ. قَدْ فَعَلْتُ، وَأَنَا أَرْفَعُ، وَأَنَا أَحْمِلُ وَأُنَجِّي.",
            "14": "ٱللهُ طَرِيقُهُ كَامِلٌ. قَوْلُ ٱلرَّبِّ نَقِيٌّ. تُرْسٌ هُوَ لِجَمِيعِ ٱلْمُحْتَمِينَ بِهِ.",
            "15": "أَمَّا أَنَا فَأُغَنِّي بِقُوَّتِكَ، وَأُرَنِّمُ بِٱلْغَدَاةِ بِرَحْمَتِكَ، لِأَنَّكَ كُنْتَ مَلْجَأً لِي، وَمَنَاصًا فِي يَوْمِ ضِيقِي.",
            "16": "بِخَوَافِيهِ يُظَلِّلُكَ، وَتَحْتَ أَجْنِحَتِهِ تَحْتَمِي. تُرْسٌ وَمِجَنٌّ حَقُّهُ.",
            "17": "فَوْقَ كُلِّ تَحَفُّظٍ ٱحْفَظْ قَلْبَكَ، لِأَنَّ مِنْهُ مَخَارِجَ ٱلْحَيَاةِ.",
            "18": "فَمَاذَا نَقُولُ لِهَذَا؟ إِنْ كَانَ ٱللهُ مَعَنَا، فَمَنْ عَلَيْنَا؟",
            "19": "أَمَّا أَنْتَ يَا رَبُّ فَتُرْسٌ لِي. مَجْدِي وَرَافِعُ رَأْسِي.",
            "20": "جَعَلْتُ ٱلرَّبَّ أَمَامِي فِي كُلِّ حِينٍ، لِأَنَّهُ عَنْ يَمِينِي فَلَا أَتَزَعْزَعُ."
        }

    def generate_colors(self):
        # Generate a list of distinct colors for the sectors
        base_colors = [
            "#6C88C4", "#8DD7BF", "#FF96C5", "#FF5768", "#FFBF65"
        ]
        # Repeat the base colors to match the number of sectors
        return base_colors * (len(self.sectors) // len(base_colors) + 1)

    def create_widgets(self):
        # Top Frame for Title and Spin Button
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)

        # Title Label
        title_label = tk.Label(top_frame, text="رسالة ليك", font=("Arial", 24, "bold"))
        title_label.pack(side=tk.LEFT, padx=10)

        # Spin Button
        spin_button = tk.Button(
            top_frame,
            text="لف",
            command=self.spin,
            bg="#74737A",
            fg="black",
            font=("Arial", 16, "bold"),
            width=6,
            height=1
        )
        spin_button.pack(side=tk.RIGHT, padx=10)
        self.spin_button = spin_button  # Reference for enabling/disabling

        # Middle Frame for Wheel with padding
        middle_frame = tk.Frame(self.root)
        middle_frame.pack()

        # Canvas for the wheel with padding
        self.canvas = tk.Canvas(
            middle_frame,
            width=self.size,
            height=self.size,  # Increased height for pointer visibility
            bg="white",
            borderwidth=2,
            relief="solid"
        )
        self.canvas.pack()

        # Draw initial wheel
        self.update_wheel()

        # Draw pointer
        self.draw_pointer()

        # Bottom Frame for Result Display
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(pady=10)

        self.result_label = tk.Label(bottom_frame, text=" ", font=("Arial", 18), fg="blue")
        self.result_label.pack(side=tk.LEFT, padx=5)

    '''
    def draw_pointer(self):
        # Draw a simple triangular pointer at the top center
        pointer_size = 20
        self.canvas.create_polygon(
            self.center - pointer_size, 10,  # Adjusted Y-coordinate for better visibility
            self.center + pointer_size, 10,
            self.center, pointer_size + 10,
            fill="black"
        )
    '''

    def draw_pointer(self):
        # Draw a simple triangular pointer on the right side
        pointer_size = 20
        # Position pointer to the right of the wheel
        pointer_x = self.size - 20  # 10 pixels from the right edge
        pointer_y_top = self.center - pointer_size  # Top point of the pointer
        pointer_y_bottom = self.center + pointer_size  # Bottom point of the pointer

        # Clear any previous pointer drawings
        self.canvas.delete("pointer")

        # Create the pointer as a triangle
        self.canvas.create_polygon(
            pointer_x, pointer_y_top,  # Top point
            pointer_x, pointer_y_bottom,  # Bottom point
            pointer_x + pointer_size, self.center,  # Base point of triangle
            fill="black",
            tags="pointer"  # Tag for later deletion if needed
        )

    def update_wheel(self):
        self.num_sectors = len(self.sectors)
        self.angle_step = 360 / self.num_sectors
        self.wheel_image = self.create_wheel_image()
        self.display_image()

        self.draw_pointer()  # Redraw the pointer to ensure it's updated with the wheel -- NEW

    def create_wheel_image(self):
        # Create a blank image with transparent background
        image = Image.new("RGBA", (self.size, self.size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)

        # Load Arabic-supporting font
        font = self.get_font()

        # Draw each sector
        for i, sector_key in enumerate(self.sectors):
            start_angle = i * self.angle_step
            end_angle = start_angle + self.angle_step
            color = self.colors[i % len(self.colors)]

            # Draw the sector with margin
            draw.pieslice(
                [self.margin, self.margin, self.size - self.margin, self.size - self.margin],
                start=start_angle,
                end=end_angle,
                fill=color,
                outline="black"
            )

            # Calculate text position
            text_angle = math.radians(start_angle + self.angle_step / 2)
            text_radius = self.radius * 0.7  # Increase the radius to give more space
            text_x = self.center + text_radius * math.cos(text_angle)
            text_y = self.center - text_radius * math.sin(text_angle)

            # Determine if the sector_key is numeric
            if sector_key.isdigit():
                display_text = sector_key  # Use the key directly for numeric labels
            else:
                # Get the Arabic text value
                arabic_text = sector_key  # Use the key as the sector label
                reshaped_text = arabic_reshaper.reshape(arabic_text)
                display_text = get_display(reshaped_text)

            # Calculate text bounding box
            bbox = draw.textbbox((0, 0), display_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            # Adjust text position to center it
            text_x -= text_width / 2
            text_y -= text_height / 2

            # Ensure text is within bounds
            if text_x < self.margin:
                text_x = self.margin
            elif text_x + text_width > self.size - self.margin:
                text_x = self.size - self.margin - text_width

            if text_y < self.margin:
                text_y = self.margin
            elif text_y + text_height > self.size - self.margin:
                text_y = self.size - self.margin - text_height

            # Draw the text
            draw.text(
                (text_x, text_y),
                display_text,
                fill="black",
                font=font
            )

        return image

    def get_font(self):
        try:
            # Replace 'Amiri-Regular.ttf' with the path to your Arabic-supporting font file
            return ImageFont.truetype("Amiri-Regular.ttf", 24)
        except IOError:
            # Fallback to default font if the specified font is not found
            return ImageFont.load_default()

    def display_image(self):
        # Clear previous wheel images
        self.canvas.delete("wheel")

        # Rotate the wheel image based on current angle offset
        rotated = self.wheel_image.rotate(self.angle_offset, resample=Image.BICUBIC)
        self.tk_image = ImageTk.PhotoImage(rotated)
        self.canvas.create_image(self.center, self.center, image=self.tk_image, tags="wheel")

    def spin(self):
        if self.is_spinning:
            return
        if not self.sectors:
            messagebox.showinfo("Info", "No sectors to spin!")
            return

        # **Close the result window if it's open**
        if self.result_window and self.result_window.winfo_exists():
            self.result_window.destroy()
            self.result_window = None

        self.is_spinning = True
        self.spin_button_state(False)

        # Determine total rotation
        self.total_rotation = random.randint(3, 5) * 360  # 5 to 10 full rotations
        self.final_angle = random.randint(0, 360)
        self.current_rotation = 0
        self.animation_speed = 10  # Milliseconds per frame
        self.rotate_increment = 50  # Degrees per frame

        # Start spinning
        self.animate_spin()

    def animate_spin(self):
        if self.current_rotation < self.total_rotation + self.final_angle:
            # Easing: Slow down as it approaches the final rotation
            if self.current_rotation > self.total_rotation:
                deceleration = self.current_rotation - self.total_rotation
                self.rotate_increment = max(10, self.rotate_increment - deceleration / 50)
            else:
                self.rotate_increment = 30

            self.angle_offset = (self.angle_offset + self.rotate_increment) % 360
            self.display_image()
            self.current_rotation += self.rotate_increment

            self.root.after(self.animation_speed, self.animate_spin)
        else:
            self.is_spinning = False
            self.spin_button_state(True)
            self.show_result()

    def spin_button_state(self, state):
        # Enable or disable the spin button
        self.spin_button.config(state=tk.NORMAL if state else tk.DISABLED)

    def show_result(self):
        # Determine which sector is at the top (where the pointer is)
        normalized_angle = self.angle_offset % 360
        selected_sector_index = (self.num_sectors - int(normalized_angle / self.angle_step)) % self.num_sectors

        print(normalized_angle, selected_sector_index, self.angle_offset)

        selected_key = self.sectors[selected_sector_index]

        # Get the corresponding value
        selected_value = self.sector_dict[selected_key]

        # **Create a new window for the result**
        result_window = tk.Toplevel(self.root)
        self.result_window = result_window  # Assign to instance variable
        result_window.title("الرسالة")

        # Add a label to display the result
        arabic_text = selected_value
        reshaped_text = arabic_reshaper.reshape(arabic_text)
        bidi_text = get_display(reshaped_text)
        result_label = tk.Label(
            result_window,
            text=f"{selected_key}:\n{bidi_text}",
            font=("Arial", 18),
            fg="blue",
            justify="center"  # Center the text alignment
        )
        result_label.pack(padx=20, pady=20)

        # Add a button to close the result window
        close_button = tk.Button(result_window, text="إغلاق", command=self.close_result_window)
        close_button.pack(pady=10)

        # **Handle the window close event to reset the reference**
        result_window.protocol("WM_DELETE_WINDOW", self.close_result_window)

    def close_result_window(self):
        if self.result_window:
            self.result_window.destroy()
            self.result_window = None

    @staticmethod
    def run():
        root = tk.Tk()
        root.title("Spinner Wheel Game")
        root.resizable(False, False)

        # Initialize the spinner wheel
        spinner = SpinnerWheel(root, size=600)

        root.mainloop()


if __name__ == "__main__":
    SpinnerWheel.run()
"""

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageTk, ImageFont
import math
import random
import arabic_reshaper
from bidi.algorithm import get_display
import time
import pygame  # Import pygame for sound

class SpinnerWheel:
    def __init__(self, root, size=600):
        pygame.mixer.init()
        pygame.mixer.music.load("prize_wheel.mp3")
        pygame.mixer.music.set_volume(0.5)

        self.root = root
        self.size = size
        self.margin = 40  # Define margin for padding inside the canvas
        self.center = size // 2
        self.radius = self.center - self.margin  # Adjust radius to account for margin
        self.sector_dict = self.generate_sectors()  # Store key-value pairs
        self.sectors = list(self.sector_dict.keys())  # Only the keys for display
        self.colors = self.generate_colors()
        self.angle_offset = 0
        self.is_spinning = False

        self.result_window = None  # Initialize the result window reference

        self.create_widgets()

    def generate_sectors(self):
        # Dictionary for keys and values
        return {
            "1": "إِنْ أَحَبَّنِي أَحَدٌ يَحْفَظْ كَلاَمِي، وَيُحِبُّهُ أَبِي، وَإِلَيْهِ نَأْتِي، وَعِنْدَهُ نَصْنَعُ مَنْزِلًا.(يو 14: 23)",
            "2": "لاَ يَسْتَهِنْ أَحَدٌ بِحَدَاثَتِكَ، بَلْ كُنْ قُدْوَةً لِلْمُؤْمِنِينَ فِي الْكَلاَمِ، فِي التَّصَرُّفِ، فِي الْمَحَبَّةِ، فِي الرُّوحِ، فِي الإِيمَانِ، فِي الطَّهَارَةِ.(1 تي 4: 12)",
            "3": "لاَحِظْ نَفْسَكَ وَالتَّعْلِيمَ وَدَاوِمْ عَلَى ذلِكَ، لأَنَّكَ إِذَا فَعَلْتَ هذَا، تُخَلِّصُ نَفْسَكَ وَالَّذِينَ يَسْمَعُونَكَ أَيْضًا.(1 تي 4: 16)",
            "4": "كُلُّ الْكِتَابِ هُوَ مُوحًى بِهِ مِنَ اللهِ، وَنَافِعٌ لِلتَّعْلِيمِ وَالتَّوْبِيخِ، لِلتَّقْوِيمِ وَالتَّأْدِيبِ الَّذِي فِي الْبِرِّ،(2 تي 3: 16)",
            "5": "كُلُّ الأَشْيَاءِ تَحِلُّ لِي، لكِنْ لَيْسَ كُلُّ الأَشْيَاءِ تُوافِقُ. كُلُّ الأَشْيَاءِ تَحِلُّ لِي، لكِنْ لاَ يَتَسَلَّطُ عَلَيَّ شَيْءٌ.(1 كو 6: 12)",
            "6": "كُلُّ الأَشْيَاءِ تَحِلُّ لِي، لكِنْ لَيْسَ كُلُّ الأَشْيَاءِ تُوَافِقُ. كُلُّ الأَشْيَاءِ تَحِلُّ لِي، وَلكِنْ لَيْسَ كُلُّ الأَشْيَاءِ تَبْنِي.(1 كو 10: 23)",
            "7": "وَأَمَّا مِنْ جِهَتِي، فَحَاشَا لِي أَنْ أَفْتَخِرَ إِلاَّ بِصَلِيبِ رَبِّنَا يَسُوعَ الْمَسِيحِ، الَّذِي بِهِ قَدْ صُلِبَ الْعَالَمُ لِي وَأَنَا لِلْعَالَمِ.(غل 6: 14)",
            "8": "وَأَمَّا ثَمَرُ الرُّوحِ فَهُوَ: مَحَبَّةٌ، فَرَحٌ، سَلاَمٌ، طُولُ أَنَاةٍ، لُطْفٌ، صَلاَحٌ، إِيمَانٌ، وَدَاعَةٌ، تَعَفُّفٌ. ضِدَّ أَمْثَالِ هذِهِ لَيْسَ نَامُوسٌ.(غل 5: 22-23)",
            "9": "أَمَا أَمَرْتُكَ! تَشَدَّدْ وَتَشَجَّعْ! لاَ تَرْهَبْ وَلاَ تَرْتَعِبْ لأَنَّ الرَّبَّ إِلهَكَ مَعَكَ حَيْثُمَا تَذْهَبُ.(يش 1: 9)",
            "10": "فَلِلْوَقْتِ كَلَّمَهُمْ يَسُوعُ قِائِلًا: تَشَجَّعُوا! أَنَا هُوَ. لاَ تَخَافُوا.(مت 14: 27)",
            "11": "أَنْتَ تَأْتِي إِلَيَّ بِسَيْفٍ وَبِرُمْحٍ وَبِتُرْسٍ، وَأَنَا آتِي إِلَيْكَ بِاسْمِ رَبِّ الْجُنُودِ إِلهِ صُفُوفِ إِسْرَائِيلَ الَّذِينَ عَيَّرْتَهُمْ.(1 صم 17: 45)",
            "12": "اَلْقُرْعَةُ تُبَطِّلُ الْخُصُومَاتِ وَتَفْصِلُ بَيْنَ الأَقْوِيَاءِ.(أم 18: 18)",
            "13": "وَقَالَ دَاوُدُ لِسُلَيْمَانَ ابْنِهِ: تَشَدَّدْ وَتَشَجَّعْ وَاعْمَلْ. لاَ تَخَفْ وَلاَ تَرْتَعِبْ، لأَنَّ الرَّبَّ الإِلهَ إِلهِي مَعَكَ. لاَ يَخْذُلُكَ وَلاَ يَتْرُكُكَ حَتَّى تُكَمِّلَ كُلَّ عَمَلِ خِدْمَةِ بَيْتِ الرَّبِّ.(1 أخ 28: 20)",
            "14": "وَنَطْلُبُ إِلَيْكُمْ أَيُّهَا الإِخْوَةُ: أَنْذِرُوا الَّذِينَ بِلاَ تَرْتِيبٍ. شَجِّعُوا صِغَارَ النُّفُوسِ. أَسْنِدُوا الضُّعَفَاءَ. تَأَنَّوْا عَلَى الْجَمِيعِ.(1 تس 5: 14)",
            "15": "أَخِيرًا يَا إِخْوَتِي تَقَوُّوْا فِي الرَّبِّ وَفِي شِدَّةِ قُوَّتِهِ.(أف 6: 10)",
            "16": "اَلْبَطِيءُ الْغَضَبِ خَيْرٌ مِنَ الْجَبَّارِ، وَمَالِكُ رُوحِهِ خَيْرٌ مِمَّنْ يَأْخُذُ مَدِينَةً.(أم 16: 32)",
            "17": "اَلْجَوَابُ اللَّيِّنُ يَصْرِفُ الْغَضَبَ، وَالْكَلاَمُ الْمُوجعُ يُهَيِّجُ السَّخَطَ.(أم 15: 1)",
            "18": "وَأَمَّا الآنَ فَاطْرَحُوا عَنْكُمْ أَنْتُمْ أَيْضًا الْكُلَّ: الْغَضَبَ، السَّخَطَ، الْخُبْثَ، التَّجْدِيفَ، الْكَلاَمَ الْقَبِيحَ مِنْ أَفْوَاهِكُمْ.(كو 3: 8)",
            "19": "إِذًا يَا إِخْوَتِي الأَحِبَّاءَ، لِيَكُنْ كُلُّ إِنْسَانٍ مُسْرِعًا فِي الاسْتِمَاعِ، مُبْطِئًا فِي التَّكَلُّمِ، مُبْطِئًا فِي الْغَضَبِ،(يع 1: 19)",
            "20": "فَاحْتَرِزُوا مِنَ التَّذَمُّرِ الَّذِي لاَ خَيْرَ فِيهِ، وَكُفُّوا أَلْسِنَتَكُمْ عَنِ الثَّلْب، فَإِنَّ الْمَنْطُوقَ بِهِ فِي الْخُفْيَةِ لاَ يَذْهَبُ سُدًى، وَالْفَمَ الْكَاذِبَ يَقْتُلُ النَّفْسَ.(حك 1: 11)",
            "21": "الْفَمُ الْعَذْبُ يُكَثِّرُ الأَصْدِقَاءَ، وَاللِّسَانُ اللَّطِيفُ يُكَثِّرُ الْمُؤَانَسَاتِ.(سي 6: 5)",
            "22": "وَأَمَّا مَا يَخْرُجُ مِنَ الْفَمِ فَمِنَ الْقَلْب يَصْدُرُ، وَذَاكَ يُنَجِّسُ الإِنْسَانَ،(مت 15: 18)",
            "23": "مِنَ الْفَمِ الْوَاحِدِ تَخْرُجُ بَرَكَةٌ وَلَعْنَةٌ! لاَ يَصْلُحُ يَا إِخْوَتِي أَنْ تَكُونَ هذِهِ الأُمُورُ هكَذَا!(يع 3: 10)",
            "24": "أَعْطَانِيَ الرَّبُّ اللِّسَانَ جَزَاءً؛ فَبِهِ أُسَبِّحُهُ.(سي 51: 30)",
            "25": "لاَ تُخَاصِمِ الْفَتِيقَ اللِّسَانِ، وَلاَ تَجْمَعْ عَلَى نَارِهِ حَطَبًا.(سي 8: 4)",
            "26": "لاَ تُبْدِلْ صَدِيقًا بِشَيْءٍ زَمَنِيٍّ، وَلاَ أَخًا خَالِصًا بِذَهَبِ أُوفِيرَ.(سي 7: 20)",
            "27": "ضَرْبَةُ السَّوْطِ تُبْقِي حَبَطًا، وَضَرْبَةُ اللِّسَانِ تَحْطِمُ الْعِظَامَ.(سي 28: 21)",
            "28": "الْقَلْبُ الْحَكِيمُ الْعَاقِلُ يَمْتَنِعُ مِنَ الْخَطَايَا، وَيَنْجَحُ فِي أَعْمَالِ الْبِرِّ.(سي 3: 32)",
            "29": "الْوَجْهُ يَدُلُّ عَلَى تَغَيُّرِ الْقَلْبِ. أَرْبَعَةٌ تَصْدُرُ مِنَ الْقَلْبِ: الْخَيْرُ وَالشَّرُّ وَالْحَيَاةُ وَالْمَوْتُ، وَالْمُتَسَلِّطُ عَلَى هذِهِ فِي كُلِّ حِينٍ هُوَ اللِّسَانُ.(سي 37: 21)",
            "30": "طُوبَى لِلأَنْقِيَاءِ الْقَلْبِ، لأَنَّهُمْ يُعَايِنُونَ اللهَ.(مت 5: 8)",
            "31": "اهْرُبْ مِنَ الْخَطِيئَةِ هَرَبَكَ مِنَ الْحَيَّةِ؛ فَإِنَّهَا إِنْ دَنَوْتَ مِنْهَا لَدَغَتْكَ.(سي 21: 2)",
            "32": "أَمَّا الشَّهَوَاتُ الشَّبَابِيَّةُ فَاهْرُبْ مِنْهَا، وَاتْبَعِ الْبِرَّ وَالإِيمَانَ وَالْمَحَبَّةَ وَالسَّلاَمَ مَعَ الَّذِينَ يَدْعُونَ الرَّبَّ مِنْ قَلْبٍ نَقِيٍّ.(2 تي 2: 22)",
            "33": "فَاذْكُرْ خَالِقَكَ فِي أَيَّامِ شَبَابِكَ، قَبْلَ أَنْ تَأْتِيَ أَيَّامُ الشَّرِّ أَوْ تَجِيءَ السِّنُونَ إِذْ تَقُولُ: لَيْسَ لِي فِيهَا سُرُورٌ.(جا 12: 1)",
            "34": "فَلْنَسْمَعْ خِتَامَ الأَمْرِ كُلِّهِ: اتَّقِ اللهَ وَاحْفَظْ وَصَايَاهُ، لأَنَّ هذَا هُوَ الإِنْسَانُ كُلُّهُ.(جا 12: 13)",
            "35": "أَمَا تَعْلَمُونَ أَنَّكُمْ هَيْكَلُ اللهِ، وَرُوحُ اللهِ يَسْكُنُ فِيكُمْ؟(1 كو 3: 16)",
            "36": "إِنْ كَانَ أَحَدٌ يُفْسِدُ هَيْكَلَ اللهِ فَسَيُفْسِدُهُ اللهُ، لأَنَّ هَيْكَلَ اللهِ مُقَدَّسٌ الَّذِي أَنْتُمْ هُوَ.(1 كو 3: 17)",
            "37": "أَمَّا أَنَا فَبِكَثْرَةِ رَحْمَتِكَ أَدْخُلُ بَيْتَكَ. أَسْجُدُ فِي هَيْكَلِ قُدْسِكَ بِخَوْفِكَ.(مز 5: 7)",
            "38": "مَكْرَهَةُ الرَّبِّ طَرِيقُ الشِّرِّيرِ، وَتَابعُ الْبِرِّ يُحِبُّهُ.(أم 15: 9)",
            "39": "الصَّدِيقُ الأَمِينُ مَعْقِلٌ حَصِينٌ، وَمَنْ وَجَدَهُ فَقَدْ وَجَدَ كَنْزًا.(سي 6: 14)",
            "40": "أَحْبِبِ الصَّدِيقَ، وَكُنْ مَعَهُ أَمِينًا،(سي 27: 18)",
            "41": "يَا ابْنِي أَعْطِنِي قَلْبَكَ، وَلْتُلاَحِظْ عَيْنَاكَ طُرُقِي.(أم 23: 26)",
            "42": "إِنِ اعْتَرَفْنَا بِخَطَايَانَا فَهُوَ أَمِينٌ وَعَادِلٌ، حَتَّى يَغْفِرَ لَنَا خَطَايَانَا وَيُطَهِّرَنَا مِنْ كُلِّ إِثْمٍ.(1 يو 1: 9)",
            "43": "اِحْسِبُوهُ كُلَّ فَرَحٍ يَا إِخْوَتِي حِينَمَا تَقَعُونَ فِي تَجَارِبَ مُتَنَوِّعَةٍ،(يع 1: 2)",
            "44": "لأَنَّ غَضَبَ الإِنْسَانِ لاَ يَصْنَعُ بِرَّ اللهِ.(يع 1: 20)",
            "45": "الْمَحَبَّةُ تَتَأَنَّى وَتَرْفُقُ. الْمَحَبَّةُ لاَ تَحْسِدُ. الْمَحَبَّةُ لاَ تَتَفَاخَرُ، وَلاَ تَنْتَفِخُ،(1 كو 13: 4)",
            "46": "أَكْرِمْ أَبَاكَ وَأُمَّكَ لِكَيْ تَطُولَ أَيَّامُكَ عَلَى الأَرْضِ الَّتِي يُعْطِيكَ الرَّبُّ إِلهُكَ.(خر 20: 12)",
            "47": "أَيُّهَا الأَوْلاَدُ، أَطِيعُوا وَالِدِيكُمْ فِي كُلِّ شَيْءٍ لأَنَّ هذَا مَرْضِيٌّ فِي الرَّبِّ.(كو 3: 20)",
            "48": "لأَنَّ الَّذِي يُحِبُّهُ الرَّبُّ يُؤَدِّبُهُ، وَيَجْلِدُ كُلَّ ابْنٍ يَقْبَلُهُ.(عب 12: 6)",
        }

    def generate_colors(self):
        # Generate a list of distinct colors for the sectors
        base_colors = [
            "#6C88C4", "#8DD7BF", "#FF96C5", "#FF5768", "#FFBF65"
        ]
        # Repeat the base colors to match the number of sectors
        return base_colors * (len(self.sectors) // len(base_colors) + 1)

    def create_widgets(self):
        # Top Frame for Title and Spin Button
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)

        # Title Label
        title_label = tk.Label(top_frame, text="رسالة ليك", font=("Arial", 24, "bold"))
        title_label.pack(side=tk.LEFT, padx=10)

        # Spin Button
        spin_button = tk.Button(
            top_frame,
            text="لف",
            command=self.spin,
            bg="#74737A",
            fg="black",
            font=("Arial", 16, "bold"),
            width=6,
            height=1
        )
        spin_button.pack(side=tk.RIGHT, padx=10)
        self.spin_button = spin_button  # Reference for enabling/disabling

        # Middle Frame for Wheel with padding
        middle_frame = tk.Frame(self.root)
        middle_frame.pack()

        # Canvas for the wheel with padding
        self.canvas = tk.Canvas(
            middle_frame,
            width=self.size,
            height=self.size,  # Increased height for pointer visibility
            bg="white",
            borderwidth=2,
            relief="solid"
        )
        self.canvas.pack()

        # Draw initial wheel
        self.update_wheel()

        # Draw pointer
        # self.draw_pointer()

        # Bottom Frame for Result Display
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(pady=10)

        self.result_label = tk.Label(bottom_frame, text=" ", font=("Arial", 18), fg="blue")
        self.result_label.pack()

    '''
    def update_wheel(self):
        # Clear the canvas
        self.canvas.delete("all")

        # Draw each sector with text
        for i, sector in enumerate(self.sectors):
            angle = 2 * math.pi * i / len(self.sectors) + self.angle_offset
            x1 = self.center + self.radius * math.cos(angle)
            y1 = self.center + self.radius * math.sin(angle)
            x2 = self.center + self.radius * math.cos(angle + 2 * math.pi / len(self.sectors))
            y2 = self.center + self.radius * math.sin(angle + 2 * math.pi / len(self.sectors))

            # Draw the sector
            self.canvas.create_polygon(self.center, self.center, x1, y1, x2, y2, fill=self.colors[i], outline="black")

            # Draw the sector text
            reshaped_text = arabic_reshaper.reshape(sector)
            display_text = get_display(reshaped_text)
            text_x = self.center + (self.radius / 2) * math.cos(angle + math.pi / len(self.sectors))
            text_y = self.center + (self.radius / 2) * math.sin(angle + math.pi / len(self.sectors))
            self.canvas.create_text(text_x, text_y, text=display_text, fill="black", font=("Arial", 10, "bold"))

        # Draw the pointer
        #self.draw_pointer()
    '''

    def update_wheel(self):
        # Clear the canvas
        self.canvas.delete("all")

        # Draw each sector with text
        for i, sector in enumerate(self.sectors):
            angle = 2 * math.pi * i / len(self.sectors) + self.angle_offset
            x1 = self.center + self.radius * math.cos(angle)
            y1 = self.center + self.radius * math.sin(angle)
            x2 = self.center + self.radius * math.cos(angle + 2 * math.pi / len(self.sectors))
            y2 = self.center + self.radius * math.sin(angle + 2 * math.pi / len(self.sectors))

            # Draw the sector
            self.canvas.create_polygon(self.center, self.center, x1, y1, x2, y2, fill=self.colors[i], outline="black")

            # Draw the sector text, pushing it ahead towards the outer edge
            reshaped_text = arabic_reshaper.reshape(sector)
            display_text = get_display(reshaped_text)

            # Increase the radial distance for the text to push it outward
            text_x = self.center + (self.radius * 2 / 3) * math.cos(
                angle + math.pi / len(self.sectors))  # Increase distance
            text_y = self.center + (self.radius * 2 / 3) * math.sin(
                angle + math.pi / len(self.sectors))  # Increase distance

            self.canvas.create_text(text_x, text_y, text=display_text, fill="black", font=("Arial", 10, "bold"))

    def spin(self):
        if self.is_spinning:
            return

        # **Close the result window if it's open**
        if self.result_window and self.result_window.winfo_exists():
            self.result_window.destroy()
            self.result_window = None

        self.is_spinning = True
        self.spin_button.config(state=tk.DISABLED)  # Disable button

        # Play the music when the spinning starts
        pygame.mixer.music.play(-1)  # Play music indefinitely

        # Spin for a random duration and angle
        spin_duration = random.uniform(1, 3)
        spin_angle = random.uniform(720, 1080)  # Spin a random number of degrees

        self.final_angle = (spin_angle % 360) + self.angle_offset  # Final angle
        self.angle_offset -= spin_angle % 360  # Update angle offset for the next spin

        # Animation loop
        self.animate_spin(spin_duration)

    def animate_spin(self, duration):
        start_time = time.time()  # Get the current time in seconds
        end_time = start_time + duration  # End time after the duration

        def update():
            now = time.time()  # Current time
            elapsed = now - start_time
            progress = elapsed / duration

            if progress < 1:
                self.angle_offset += (random.uniform(-10, 10))  # Add a bit of random movement
                self.update_wheel()
                self.root.after(30, update)
            else:
                self.angle_offset = self.final_angle  # Set the final angle
                self.update_wheel()  # Update to show final position
                self.show_result()  # Show the result
                self.is_spinning = False
                self.spin_button.config(state=tk.NORMAL)  # Re-enable button

                # Stop the music after spinning is done
                pygame.mixer.music.stop()

        update()

    def show_result(self):
        # Determine the selected sector based on the final angle
        selected_sector_index = int((self.final_angle + 360) % 360 / (360 / len(self.sectors))) % len(self.sectors)
        selected_sector = self.sectors[selected_sector_index]

        # Create a new window to display the result
        self.result_window = tk.Toplevel(self.root)
        self.result_window.title("الرسالة")

        # Retrieve and reshape the Arabic text
        arabic_text = self.sector_dict[selected_sector]
        reshaped_text = arabic_reshaper.reshape(arabic_text)
        bidi_text = get_display(reshaped_text)

        # Result label displaying the selected sector
        result_label = tk.Label(self.result_window, text=f"رقمك: {selected_sector}", font=("Arial", 50), fg="blue", justify="center")
        result_label.pack(padx=20, pady=20)

        # Label to display the Arabic text (initially hidden)
        self.text_label = tk.Label(self.result_window, text="", font=("Arial", 20), fg="blue", justify="center")
        self.text_label.pack(padx=20, pady=10)

        show_button = tk.Button(self.result_window, text="الاية", command=lambda: self.display_text(show_button, bidi_text, result_label))
        show_button.pack(pady=10)

        # Add a button to close the result window
        close_button = tk.Button(self.result_window, text="إغلاق", command=self.close_result_window)
        close_button.pack(pady=10)

        # Handle the window close event to reset the reference
        self.result_window.protocol("WM_DELETE_WINDOW", self.close_result_window)

    def display_text(self, button, bidi_text, result_label):
        # Update the label text and show it
        self.text_label.config(text=bidi_text)
        button.destroy()
        result_label.config(font=("Arial", 18))

    def close_result_window(self):
        if self.result_window:
            self.result_window.destroy()
            self.result_window = None

    @staticmethod
    def run():
        root = tk.Tk()
        root.title("Spinner Wheel Game")
        root.resizable(False, False)

        # Initialize the spinner wheel
        spinner = SpinnerWheel(root, size=600)

        root.mainloop()

if __name__ == "__main__":
    SpinnerWheel.run()
