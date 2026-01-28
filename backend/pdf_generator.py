from fpdf import FPDF
from datetime import datetime
from typing import Dict
import os

class JanampatriPDF:
    """Generate downloadable PDF Janampatri"""
    
    @staticmethod
    def generate_pdf(chart: Dict, personality: Dict, filename: str = None) -> str:
        """Generate PDF from birth chart data"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"/tmp/janampatri_{chart['name']}_{timestamp}.pdf"
        
        pdf = FPDF()
        pdf.add_page()
        
        # Title
        pdf.set_font('Arial', 'B', 24)
        pdf.set_text_color(139, 28, 28)  # Dark red
        pdf.cell(0, 15, 'Janampatri (Birth Chart)', ln=True, align='C')
        pdf.ln(5)
        
        # Personal Details
        pdf.set_font('Arial', 'B', 16)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 10, 'Personal Details', ln=True)
        pdf.set_font('Arial', '', 12)
        pdf.ln(3)
        
        details = [
            f"Name: {chart['name']}",
            f"Gender: {chart['gender']}",
            f"Date of Birth: {chart['date_of_birth']}",
            f"Time of Birth: {chart['time_of_birth']}",
            f"Place of Birth: {chart['place_of_birth']}",
            f"Latitude: {chart['latitude']}, Longitude: {chart['longitude']}"
        ]
        
        for detail in details:
            pdf.cell(0, 7, detail, ln=True)
        
        pdf.ln(5)
        
        # Astrological Details
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Astrological Details', ln=True)
        pdf.set_font('Arial', '', 12)
        pdf.ln(3)
        
        astro_details = [
            f"Lagna (Ascendant): {chart['lagna']['rashi']} ({chart['lagna']['degree']:.2f}°)",
            f"Moon Sign (Rashi): {chart['moon_rashi']}",
            f"Nakshatra: {chart['nakshatra']['nakshatra']} (Pada: {chart['nakshatra']['pada']})",
            f"Ayanamsa: {chart['ayanamsa']:.2f}°"
        ]
        
        for detail in astro_details:
            pdf.cell(0, 7, detail, ln=True)
        
        pdf.ln(5)
        
        # Planetary Positions
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Planetary Positions', ln=True)
        pdf.ln(3)
        
        # Table header
        pdf.set_font('Arial', 'B', 11)
        pdf.set_fill_color(253, 205, 77)  # Gold
        pdf.cell(50, 8, 'Planet', 1, 0, 'C', True)
        pdf.cell(60, 8, 'Rashi', 1, 0, 'C', True)
        pdf.cell(40, 8, 'Degree', 1, 1, 'C', True)
        
        # Table content
        pdf.set_font('Arial', '', 10)
        for planet, data in chart['planets'].items():
            pdf.cell(50, 7, planet, 1, 0, 'L')
            pdf.cell(60, 7, data['rashi'], 1, 0, 'C')
            pdf.cell(40, 7, f"{data['degree']:.2f}", 1, 1, 'C')
        
        pdf.ln(5)
        
        # Houses
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, '12 Houses (Bhavas)', ln=True)
        pdf.ln(3)
        
        pdf.set_font('Arial', 'B', 11)
        pdf.set_fill_color(253, 205, 77)
        pdf.cell(50, 8, 'House', 1, 0, 'C', True)
        pdf.cell(70, 8, 'Rashi', 1, 1, 'C', True)
        
        pdf.set_font('Arial', '', 10)
        for house in chart['houses']:
            pdf.cell(50, 7, f"House {house['house_num']}", 1, 0, 'L')
            pdf.cell(70, 7, house['rashi'], 1, 1, 'C')
        
        # Add new page for personality analysis
        pdf.add_page()
        
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Personality Analysis', ln=True)
        pdf.ln(5)
        
        # Moon-based personality
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 8, f"Moon Sign Traits ({chart['moon_rashi']}):", ln=True)
        pdf.set_font('Arial', '', 11)
        pdf.ln(2)
        
        moon_traits = personality.get('moon_based', {})
        if moon_traits:
            traits = ', '.join(moon_traits.get('traits', []))
            pdf.multi_cell(0, 6, f"Core Traits: {traits}")
            pdf.ln(2)
            pdf.multi_cell(0, 6, f"Nature: {moon_traits.get('nature', 'N/A')}")
            pdf.ln(2)
            pdf.multi_cell(0, 6, f"Dominant Guna: {moon_traits.get('guna', 'N/A')}")
            pdf.ln(2)
            pdf.multi_cell(0, 6, f"Element: {moon_traits.get('element', 'N/A')}")
        
        pdf.ln(5)
        
        # Lagna-based personality
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 8, f"Ascendant Traits ({chart['lagna']['rashi']}):", ln=True)
        pdf.set_font('Arial', '', 11)
        pdf.ln(2)
        
        lagna_traits = personality.get('lagna_based', {})
        if lagna_traits:
            traits = ', '.join(lagna_traits.get('traits', []))
            pdf.multi_cell(0, 6, f"Physical & Behavioral Traits: {traits}")
            pdf.ln(2)
            pdf.multi_cell(0, 6, f"Life Approach: {lagna_traits.get('nature', 'N/A')}")
        
        pdf.ln(10)
        
        # Disclaimer
        pdf.set_font('Arial', 'I', 9)
        pdf.set_text_color(100, 100, 100)
        pdf.multi_cell(0, 5, 'Disclaimer: This astrological report is for guidance and entertainment purposes only. '
                            'Predictions should not replace professional advice for important life decisions.')
        
        # Save PDF
        pdf.output(filename)
        return filename
