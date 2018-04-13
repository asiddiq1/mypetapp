from django import forms
from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required



from mypet.forms import UserForm
from mypet.forms import PetForm
from mypet.forms import PetBattleForm




#from django.views import generic
from django.views.generic import View
#from django.template import loader
from django.contrib.auth.models import User
from mypet.models import MypetsImage
from mypet.models import Mypets
from mypet.models import PetBattleImages




# Create your views here.



def home(request):
    """Home view to sign up"""
    return render(request, "mypet/home.html")


@login_required
def index(request):
    """Index view displays the game and several buttons that redirects users to play the game/add/edit pets"""
    battle_list = []
    images_petname = petdict(request)
    battleimages = PetBattleImages.objects.all()
    for battles in battleimages:
        battleimage1 = MypetsImage.objects.get(pk=battles.image1)
        battleimage2 = MypetsImage.objects.get(pk=battles.image2)
        battle_instance = PetBattleImages.objects.get(pk=battles.pk)
        battle_id = battles.pk
        battle_list.append((battleimage1, battleimage2, battle_instance, battle_id))
    return render(request, "mypet/index.html", {'images_petname': images_petname, 'battle_list': battle_list})


def increment_count(request, battle_id, battleinstance):
    """Update the vote count when user clicks photo (Ajax call used with this function)"""
    battle_instance = PetBattleImages.objects.get(pk=battle_id)
    if battle_instance.image1 == battleinstance:
        battle_instance.image1_count += 1
        battle_instance.save()
    else:
        battle_instance.image2_count += 1
        battle_instance.save()

    data = {'image1count': battle_instance.image1_count, 'image2count': battle_instance.image2_count}
    return JsonResponse(data)


def petowner_battlelist(request):
    """Returns a list of PetBattleImage pk's of objects where the user has at least one photo of theirs in the game"""
    battle_id = []
    image_list = []
    images_petname = petdict(request)
    battleimages = PetBattleImages.objects.all()

    for pets, images in images_petname.items():
        if image_list != []:
            image_list += [x[1] for x in images]
        else:
            image_list = [x[1] for x in images]

    for battles in battleimages:
        for i in image_list:
            print(battles.image1)
            print(battles.image2)
            if (str(i) == str(battles.image1) or str(i) == str(battles.image2)):
                if battles.pk not in battle_id:
                    battle_id.append(battles.pk)
    return battle_id




@login_required
def current_battleview(request):
    """View current list of battles of your pet"""
    battle_id = petowner_battlelist(request)
    battle_list = []
    for battleid in battle_id:
        battles = PetBattleImages.objects.get(pk=battleid)
        battleimage1 = MypetsImage.objects.get(pk=battles.image1)
        battleimage2 = MypetsImage.objects.get(pk=battles.image2)
        battle_list.append((battleimage1, battleimage2))


    return render(request, "mypet/current_battle.html", {"battle_list": battle_list})




@login_required
def select_image(request, petid):
    """Allows users to select the image of their pet they would like to play the game in"""
    photo_list = []
    petname = ""
    species = ""
    images_petname = petdict(request)
    for pets in images_petname:
        if pets.pk == int(petid):
            species = pets.species
            petname = pets.petname
            photo_list = images_petname[pets]
            break

    return render(request, "mypet/select_petimage.html", {"photo_list": photo_list, "images_petname": images_petname, "petname":petname, 'petid': petid, 'species':species})


@login_required
def select_relativepet(request, imageid, species):
    """Allows users select image they would like to battle their pet with relative to the species"""
    battleimage = MypetsImage.objects.get(pk=imageid)
    petimages = MypetsImage.objects.filter(mypets__species=species).exclude(pk=imageid)
    form = PetBattleForm(request.POST)
    if request.method == 'POST':

        if form.is_valid():
            form.save()
            return redirect('index')


    return render(request, "mypet/relativepets.html", {'petimages': petimages, 'battleimage':battleimage, 'imageid':imageid})


def logout_view(request):
    """Page logout"""
    logout(request)
    return HttpResponseRedirect('/')


def petdict(request):
    """Create a dictionary of the current users pets with keys as image objects"""
    images_petname = dict()
    current_user = request.user
    petobjects = Mypets.objects.filter(petowner=current_user)
    petimages = MypetsImage.objects.filter(mypets__petowner=current_user)
    for image_obj in petimages:
        images_petname.setdefault(image_obj.mypets, []).append((image_obj.image, image_obj.pk))
    return images_petname


def viewpet(request):
    """Allows users to view the current pets on the page"""
    images_petname = petdict(request)
    return render(request, "mypet/viewedit_pet.html", {'images_petname':images_petname})



def edit_post(request, pk):
    """Allows users to edit petname or species information"""
    current_user = request.user
    images_petname = petdict(request)
    template = "mypet/viewedit_pet.html"
    post = get_object_or_404(Mypets, pk=pk)

    if request.method == 'POST':
        form = PetForm(request.POST, instance=post)

        try:
            if form.is_valid():
                form.save()
                messages.success(request, "Your Blog Post Was Successfully Updated")


        except Exception as e:
            messages.warning(request, 'Your Post Was Not Saved Due To An Error: {}'.format(e))

    else:
        form = PetForm(instance=post)

    context = {
        'form': form,
        'post': post,
        'images_petname': images_petname,
    }
    return render(request, template, context)



def deletepet(request, petdelete):
    """Allows users to delete entire pet object"""
    instance = get_object_or_404(Mypets, pk=petdelete)
    instance.delete()
    return redirect('viewpet')

def deletepetimage(request, deleteimg):
    """Allows user to delete specfic image"""
    battleimages = PetBattleImages.objects.all()
    delete_battle = []
    for battles in battleimages:
        if (str(deleteimg) == str(battles.image1) or str(deleteimg) == str(battles.image2)):
            delete_battle.append(battles.pk)

    images_petname = petdict(request)
    for keys, values in images_petname.items():
        count = len(values)
        petpk = keys.pk
        for items in values:

            if int(deleteimg) == int(items[1]):
                if count == 1:
                    messages.error(request,
                               "No photos will delete entire pet information.")
                    instance = get_object_or_404(Mypets, pk=petpk)
                    for battleid in delete_battle:
                        battleinstance = get_object_or_404(PetBattleImages, pk=battleid)
                        battleinstance.delete()
                    instance.delete()
                    return redirect('viewpet')

    instance = get_object_or_404(MypetsImage, pk=deleteimg)
    for battleid in delete_battle:
        battleinstance = get_object_or_404(PetBattleImages, pk=battleid)
        battleinstance.delete()
    instance.delete()
    return redirect('viewpet')

def addphoto(request, mypetpk):
    """Allows users to add more photos of their pet into the database"""
    images_petname = petdict(request)
    petform = PetForm(request.POST)
    instance = get_object_or_404(Mypets, pk=mypetpk)

    if request.POST.get("submit") == "savephoto":

        for afile in request.FILES.getlist('image'):

            pets = MypetsImage(mypets=instance, image=afile)
            pets.save()

        # messages.success(request, 'Pet saved successfully.')

        return redirect('viewpet')
    else:

        form = PetForm()

    return render(request, 'mypet/viewedit_pet.html', {
        'images_petname': images_petname, 'petform': form
    })







@login_required
def addpet(request):
    """Allows users to add their pet into the database"""
    images_petname = petdict(request)
    if request.method == 'POST':

        form = PetForm(request.POST)

        if form.is_valid():

            petform = form.save(commit=False)
            petform.petowner = request.user
            petform.save()

            for afile in request.FILES.getlist('image'):
                pets = MypetsImage(mypets=petform, image=afile)
                pets.save()


            messages.success(request, 'Pet saved successfully!')

            return redirect('addpet')
    else:

        form = PetForm()

    return render(request, 'mypet/add_userpet.html', {
            'petform': form, 'images_petname':images_petname
        })


class UserFormView(View):
    """Used in home view to allow users to login"""
    form_class = UserForm
    template_name = "mypet/home.html"

    # give user empty form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # post user info to database
    def post(self, request):
        form = self.form_class(request.POST)

        if request.POST.get("submit") == "modal_login":

            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
            else:
                return render(request, self.template_name, {'logged_in': True})

        else:

            if form.is_valid():
                user = form.save(commit=False)

                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user.set_password(password)
                user.save()

                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('index')

            if request.POST.get("submit") == "reg_signup":
                f = {'form': form}
            else:
                f = {'form2': form}

            return render(request, self.template_name, f)










