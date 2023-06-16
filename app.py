from flask import Blueprint, render_template, request, redirect, url_for, make_response
from . import db
from flask_login import login_required, current_user
from .models import User, Event
from werkzeug.utils import secure_filename
import os
import cv2
import zipfile
import numpy as np
from io import BytesIO

app = Blueprint('app', __name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('landing.html', name=current_user.username)

@app.route('/dashboard/')
def dash():
    return render_template('dashboard.html')

@app.route('/create_event', methods=['POST'])
@login_required
def create_event():
    event_name = request.form.get('event_name')
    brandings = request.form.get('brandings')

    # Save certificate templates
    certificate_design_participation = request.files['certificate_design_participation']
    certificate_design_winner = request.files['certificate_design_winner']

    # Generate secure filenames and save templates
    filename_participation = secure_filename(certificate_design_participation.filename)
    filename_winner = secure_filename(certificate_design_winner.filename)
    certificate_design_participation.save(os.path.join('CertificateGenerator', filename_participation))
    certificate_design_winner.save(os.path.join('CertificateGenerator', filename_winner))

    # Example participant and winner names
    participants = request.form.getlist('participants')
    winners = request.form.getlist('winners')

    # Load the participation certificate template
    certificate_participation = cv2.imread(os.path.join('CertificateGenerator', filename_participation))

    # Load the winner certificate template
    certificate_winner = cv2.imread(os.path.join('CertificateGenerator', filename_winner))

    # Function to place the name on the certificate at an appropriate location
    def place_name_on_certificate(certificate, name):
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 2.0  # Increase font size here
        font_color = (0, 0, 0)  # Black
        thickness = 2

        text_size = cv2.getTextSize(name, font, font_scale, thickness)
        text_x = int((certificate.shape[1] - text_size[0][0]) / 2)  # Center horizontally
        text_y = int((certificate.shape[0] + text_size[0][1]) / 2)  # Center vertically
        cv2.putText(certificate, name, (text_x, text_y), font, font_scale, font_color, thickness)

        return certificate

    # Create an in-memory zip file
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        # Add participant certificates to the zip file
        for i, participant in enumerate(participants):
            certificate_participation_copy = certificate_participation.copy()
            certificate_participation_copy = place_name_on_certificate(certificate_participation_copy, participant)
            certificate_data = cv2.imencode('.png', certificate_participation_copy)[1]
            zip_file.writestr(f'participant_certificate_{i}.png', certificate_data)

        # Add winner certificates to the zip file
        for i, winner in enumerate(winners):
            certificate_winner_copy = certificate_winner.copy()
            certificate_winner_copy = place_name_on_certificate(certificate_winner_copy, winner)
            certificate_data = cv2.imencode('.png', certificate_winner_copy)[1]
            zip_file.writestr(f'winner_certificate_{i}.png', certificate_data)

    zip_buffer.seek(0)  # Reset the buffer position to the beginning

    # Create a response with the zip file data
    response = make_response(zip_buffer.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=certificates.zip'
    response.headers['Content-type'] = 'application/zip'

    return response
