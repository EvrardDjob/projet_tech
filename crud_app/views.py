from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def index(request):
    """Affiche la liste de tous les étudiants"""
    students = Student.objects.all()
    context = {'students': students}
    return render(request, 'index.html', context)

def confirmation_suppression(request, id):
    """Affiche la page de confirmation avant suppression"""
    etudiant = get_object_or_404(Student, id=id)
    context = {'etudiant': etudiant}
    return render(request, 'confirmation_suppression.html', context)

def delete_student(request, id):
    """Supprime un étudiant après confirmation"""
    if request.method == 'POST':
        student = get_object_or_404(Student, id=id)
        student_name = student.name
        student.delete()
        messages.success(request, f"L'étudiant {student_name} a été supprimé avec succès!")
        return redirect('index')
    
    # Si la requête n'est pas POST, rediriger vers la confirmation
    return redirect('confirmation_suppression', id=id)

def edit_student(request, id):
    """Édite les informations d'un étudiant"""
    student = get_object_or_404(Student, id=id)
    
    if request.method == 'POST':
        # Récupération et nettoyage des données
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        age = request.POST.get("age")
        gender = request.POST.get("gender", "").strip()
        
        # Validation des données
        errors = validate_student_data(name, email, age, gender)
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'Edit.html', {'student': student})
        
        # Mise à jour des données
        student.name = name
        student.email = email
        student.age = int(age)
        student.gender = gender
        
        try:
            student.save()
            messages.success(request, 'La modification a été effectuée avec succès.')
            return redirect('index')
        except Exception as e:
            messages.error(request, f"Erreur lors de la modification: {str(e)}")
            return render(request, 'Edit.html', {'student': student})
    
    context = {'student': student}
    return render(request, 'Edit.html', context)

def insert_student(request):
    """Ajoute un nouvel étudiant"""
    if request.method == 'POST':
        # Récupération et nettoyage des données
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        age = request.POST.get("age")
        gender = request.POST.get("gender", "").strip()
        
        # Validation des données
        errors = validate_student_data(name, email, age, gender)
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('index')
        
        # Création de l'étudiant
        try:
            student = Student.objects.create(
                name=name,
                email=email,
                age=int(age),
                gender=gender
            )
            messages.success(request, f"L'étudiant {student.name} a été ajouté avec succès.")
            return redirect('index')
        except Exception as e:
            messages.error(request, f"Erreur lors de l'ajout: {str(e)}")
            return redirect('index')
    
    return render(request, 'index.html')


def validate_student_data(name, email, age, gender):
    """
    Valide les données d'un étudiant
    Retourne une liste d'erreurs (vide si pas d'erreurs)
    """
    errors = []
    
    # Validation du nom
    if not name or len(name) < 2:
        errors.append("Le nom doit contenir au moins 2 caractères.")
    
    # Validation de l'email
    try:
        validate_email(email)
    except ValidationError:
        errors.append(f"L'adresse email '{email}' est invalide.")
    
    # Validation de l'âge
    try:
        age_int = int(age)
        if age_int < 0:
            errors.append("L'âge ne peut pas être négatif.")
        elif age_int > 150:
            errors.append("L'âge saisi semble incorrect (supérieur à 150 ans).")
    except (ValueError, TypeError):
        errors.append("L'âge doit être un nombre entier valide.")
    
    # Validation du genre
    valid_genders = ['Male', 'Female']
    if gender and gender not in valid_genders:
        errors.append("Le genre sélectionné n'est pas valide.")
    
    return errors
