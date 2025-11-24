from django.shortcuts import render, get_object_or_404, redirect
from .models import Doctor
from .forms import DoctorForm
from .ml_utils import get_similar_doctors_by_id

# ------------------ CRUD ------------------
def home(request):
    doctors = Doctor.objects.all().order_by('-rating')
    return render(request, 'contactlist/doctor_list.html', {'doctors': doctors})

def doctor_list(request):
    doctors = Doctor.objects.all().order_by('-rating')
    return render(request, 'contactlist/doctor_list.html', {'doctors': doctors})

def doctor_add(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('doctor_list')
    else:
        form = DoctorForm()
    return render(request, 'contactlist/doctor_form.html', {'form': form})

def doctor_update(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('doctor_list')
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'contactlist/doctor_form.html', {'form': form})

def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        doctor.delete()
        return redirect('doctor_list')
    return render(request, 'contactlist/doctor_confirm_delete.html', {'doctor': doctor})

# ------------------ Recommendation ------------------
def recommend_doctors(request):
    specialty = request.GET.get('specialty', '')
    city = request.GET.get('city', '')
    max_fee = request.GET.get('max_fee', '')

    doctors = Doctor.objects.all()
    if specialty:
        doctors = doctors.filter(specialty__icontains=specialty)
    if city:
        doctors = doctors.filter(city__icontains=city)
    if max_fee:
        try:
            doctors = doctors.filter(fee__lte=int(max_fee))
        except ValueError:
            pass

    doctors = doctors.order_by('-rating')

    # ML recommendations
    similar_doctors = []
    for doctor in doctors:
        similar_doctors += get_similar_doctors_by_id(doctor.id)

    # Remove duplicates
    unique_ids = set()
    filtered_similar = []
    for d in similar_doctors:
        # Apply the same filters to AI recommendations
        if d['id'] not in unique_ids:
            if specialty and specialty.lower() not in d['specialty'].lower():
                continue
            if city and city.lower() not in d['city'].lower():
                continue
            if max_fee:
                try:
                    if int(max_fee) < d['fee']:
                        continue
                except ValueError:
                    pass
            filtered_similar.append(d)
            unique_ids.add(d['id'])

    return render(request, 'contactlist/recommend.html', {
        'doctors': doctors,
        'similar_doctors': filtered_similar
    })


