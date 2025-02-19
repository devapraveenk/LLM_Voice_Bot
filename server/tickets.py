from fpdf import FPDF
import os


def generate_ticket(order_id):
    # Create instance of FPDF class
    pdf = FPDF()
    pdf.add_page()

    # Add a border to the ticket
    pdf.set_line_width(1)  # Set the line width for the border
    pdf.rect(10, 10, 190, 277)  # Draw a rectangle for the border (10mm from all sides)

    # Set font and color for the ticket title
    pdf.set_font("Arial", style="B", size=16)
    pdf.set_text_color(0, 51, 102)  # Dark blue color
    pdf.cell(200, 10, txt="Museum Ticket", ln=True, align="C")

    # Add the order ID with a different font style and color
    pdf.set_font("Arial", style="I", size=12)
    pdf.set_text_color(255, 69, 0)  # Red-Orange color
    pdf.cell(200, 10, txt=f"Order ID: {order_id}", ln=True, align="C")

    # # Add user icon (ensure the path to the icon is correct)
    # user_icon_path = 'path/to/user_icon.png'  # Replace with the actual file path
    # pdf.image(user_icon_path, x=20, y=30, w=20, h=20)  # Position it on the left side of the page

    # Add Ministry of Culture logo (ensure the path to the logo is correct)
    ministry_logo_path = "/Users/balanivas/Desktop/SIH/server/static/image.jpeg"  # Replace with the actual file path
    pdf.image(
        ministry_logo_path, x=160, y=30, w=40, h=20
    )  # Position it on the right side of the page

    # Add some other content for demonstration
    pdf.ln(40)  # Move to a new line after images
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)  # Black color
    pdf.cell(200, 10, txt="Welcome to the Museum!", ln=True, align="C")

    # Output the PDF to a file
    output_path = f"static/tickets/{order_id}.pdf"
    pdf.output(output_path)

    return output_path
