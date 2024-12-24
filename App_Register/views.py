from django.http import JsonResponse
from django.shortcuts import render
from . models import Register
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from App_Register.serializers import RegSerializer
from . utils import is_valid_email, send_activation_email, handle_exceptions
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import os
from django.http import HttpResponse
from django.conf import settings
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch




class RegistrationView(viewsets.ViewSet):
    serializer_class = RegSerializer


    @handle_exceptions
    def register(self, request):
        email: str = request.data["email"]
        phone: str = request.data["phone"]

        if Register.objects.filter(email=email):
            return Response({"status": "failed", "message": "Email already registered"}, status=status.HTTP_409_CONFLICT)
        if not is_valid_email(email):
            return Response({"status": "failed", "message": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)
        elif Register.objects.filter(phone=phone):
             return Response({"status": "failed", "message": "Phone already registered"}, status=status.HTTP_409_CONFLICT)
        
        else:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            send_activation_email(user)

            return Response({"status": "success", "message": "Registered successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)

class GeneratePDF(viewsets.ViewSet):
    def get_pdf(self, request, *args, **kwargs):
        try:
            pdf_filename = os.path.join(settings.BASE_DIR, 'output.pdf')

            doc = SimpleDocTemplate(pdf_filename, pagesize=landscape(letter))
            elements = []

            records = Register.objects.all()

            data = [["Full Name", "Email", "Phone Number", "Location", "Tech Skills", "Date"]]  # Table headers
            for record in records:
                data.append([record.full_name(), record.email, record.phone, record.location, f"{'Yes'if record.technical_skill == True else 'No'}", record.date.strftime('%Y-%m-%d')])

            col_widths = [2.2 * inch, 3.2 * inch, 1.0 * inch, 0.9 * inch, 0.9 * inch, 1.0 * inch]  # Adjust widths as needed

            # Create a Table
            table = Table(data, colWidths=col_widths)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Vertically align content
                ('ALIGN', (0, 1), (-1, -1), 'LEFT'),     # Align price and discount columns to the left
            ]))

            elements.append(table)
            doc.build(elements)

            # Read the PDF file and serve as response for download
            with open(pdf_filename, 'rb') as pdf_file:
                response = HttpResponse(pdf_file.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="output.pdf"'
                return response

        except Exception as e:
            return Response({'fail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)