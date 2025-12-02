# v2_blog/generate_report.py
# Installed fpdf2
from dotenv import load_dotenv
from fpdf import FPDF
import pandas as pd
import os
from datetime import datetime

# loading .env file
load_dotenv()

def generate_pdf_from_csv(df, stats, csv_path: str, pdf_path: str, font_path: str, font_name: str):

# 1. Check file existence
# 2. Load CSV
# 3. Define PDF class
# 4. Create PDF object
# 5. Add summary
# 6. Add table
# 7. Save PDF

    # Check files exist
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"Font file not found: {font_path}")


    # CSV input path
    df = pd.read_csv(csv_path)


    # PDF Class
    class PDF(FPDF):

        def __init__(self, font_path, font_name):
            super().__init__()
            self.add_font(font_name, fname=os.path.expanduser(font_path), uni=True)
            self.set_font(font_name, size=10)  # initial font

        def header(self):
            self.set_font("NotoSans", size=12)
            self.cell(0, 10, text="PostHog Blog Analytics Report", new_x="LMARGIN", new_y="NEXT", align="C")
            self.ln(5)

        def add_table(self, df):
            self.set_font("NotoSans", size=8) # Smaller font for readability

            # col_width = self.epw / len(df.columns)  # equal column width
            # Custom column widths (total should be ~190mm for A4)
            col_widths = {
                'Timestamp': 35,      # 35 → 32 →  35
                'Event': 25,          # 25 → 20 → 25
                'URL': 80,            # 60 → 55 → 60 → 80
                'Referrer': 40        # 40 → 35 → 40
            }


            # Define column order (exclude distinct_id)
            display_columns = ['Timestamp', 'Event', 'URL', 'Referrer']

            # Filter to only display columns that exist in the DataFrame
            columns = [col for col in display_columns if col in df.columns]

            # column
            for col in columns:
                self.cell(col_widths.get(col, 30), 10, col, border=1)
            self.ln()

            # row
            for _, row in df.iterrows():
                for col in columns:
                    width = col_widths.get(col, 30)
                    value = str(row[col])

                    # Format timestamp to be more readable
                    if col == 'Timestamp' and 'T' in value:
                        # Convert "2025-11-27T11:21:22.930000+00:00" to "2025-11-27 11:21"
                        try:
                            dt = pd.to_datetime(value)
                            value = dt.strftime('%Y-%m-%d %H:%M')
                        except:
                            pass

                    # Replace 'nan' with '-'
                    if value.lower() == 'nan':
                        value = '-'

                    if len(str(value)) > 50:
                        value = str(value)[:47] + "..."

                    self.cell(width, 10, value, border=1)

                self.ln()


    # Create PDF
    pdf = PDF(font_path, font_name)
    pdf.add_page()

    # Summary Section
    pdf.set_font("NotoSans", size=12)
    pdf.ln(8)
    pdf.cell(0, 10, "Summary", ln=True)

    pdf.set_font("NotoSans", size=10)
    pdf.cell(0, 8, f"Unique Users: {stats['unique_users']}", ln=True)
    pdf.cell(0, 8, f"Total Pageviews: {stats['total_pageviews']}", ln=True)

    # Format period dates to match table format
    try:
        period_start = pd.to_datetime(stats['period_start']).strftime('%Y-%m-%d %H:%M')
        period_end = pd.to_datetime(stats['period_end']).strftime('%Y-%m-%d %H:%M')
    except:
        period_start = stats['period_start']
        period_end = stats['period_end']

    pdf.cell(0, 8, f"Period: {period_start} → {period_end}", ln=True)
    pdf.ln(4)

    pdf.cell(0, 8, "Top 10 Pages:", ln=True)

    for page, count in stats['top_pages'].items():
        pdf.cell(0, 8, f"{page} — {count} views", ln=True)

    # Data Table Section
    pdf.set_font("NotoSans", size=12)
    pdf.ln(10)
    pdf.cell(0, 10, "Event Data", ln=True)
    pdf.ln(12)
    pdf.add_table(df)


    # Save PDF
    print(f"Saving to: {pdf_path}")
    pdf.output(pdf_path)


if __name__ == "__main__":
    # Example usage
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CSV_PATH = os.path.join(BASE_DIR, "output", "events.csv")
    PDF_PATH = os.path.join(BASE_DIR, "output", "report.pdf")
    FONT_PATH = os.path.join(BASE_DIR, "fonts", "NotoSansJP-Regular.ttf")
    FONT_NAME = "NotoSans"

    generate_pdf_from_csv(CSV_PATH, PDF_PATH, FONT_PATH, FONT_NAME)