from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Account, Video
from .forms import VideoCreateForm
# from .tasks import handle_ingest_video
import boto3
import shastarainnews.settings as settings

def index(request):
    # log.debug("In the index view")

    accounts = Account.objects.all()
    response = render(request, 'pmvc/select_account.html', {'accounts': accounts})
    response.delete_cookie('pmvc_account_id')
    return response


def AccountHome(request):
    if 'pmvc_account_id' in request.COOKIES:
        account = Account.objects.get(account_id=request.COOKIES['pmvc_account_id'])
        return render(request, 'pmvc/account_selected.html', {'account': account})
    else:
        accounts = Account.objects.all()
        return render(request, 'pmvc/select_account.html', {'accounts': accounts})


def AccountSelectionHandler(request):
    selection = request.POST.get('acct_select')
    if selection == '0':
        # log.debug("Create New Company")
        # form = NewCompanyForm()
        # return render(request, 'setools/create_company_form.html', {'form': form})
        return redirect('pmvc:index')
    else:
        # log.debug("Company " + selection + " selected.")
        return redirect('pmvc:AccountSelected', selection)

def AccountSelected(request, account_id):
    account = Account.objects.get(id=account_id)
    response = render(request, 'pmvc/account_selected.html', {'account': account})
    response.set_cookie('pmvc_account_id', account_id)
    return response


def ListVideos(request, account_id):
    account = Account.objects.get(id=account_id)
    vids = Video.objects.filter(account=account)
    return render(request, 'pmvc/list_videos.html', {'vid_list': vids})

# def IngestVideo(request, account_id):
#     account = Account.objects.get(id=account_id)
#     return render(request, 'pmvc/ingest_video.html', {'account': account})

def handle_ingest_video(video_id, dm):
    video = Video.objects.get(pk=video_id)
    # Need to check the file extension - assuming mp4 for now.
    filename = 'videos/' + video.title + '/digital_master.mp4'
    # file = request.FILES['upload']
    s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    bucket = s3.Bucket(settings.AWS_VIDEO_BUCKET)
    bucket.put_object(Key=filename, Body=dm)

def IngestVideo(request, account_id):
    if request.method == 'POST':
        form = VideoCreateForm(request.POST, request.FILES)
        if form.is_valid():
            account = Account.objects.get(id=account_id)
            # instance = Video(file_field=request.FILES['file'])
            instance = Video(title=request.POST['title'], description=request.POST['description'], account=account)
            instance.save()
            # print (request.FILES['digital_master'].path)
            handle_ingest_video(instance.id, request.FILES['digital_master'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = VideoCreateForm()
    return render(request, 'pmvc/upload_request.html', {'form': form})

