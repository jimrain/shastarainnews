from django.core.files.uploadhandler import FileUploadHandler
from requests.utils import requote_uri
from .gcs_utils import get_access_token
from .models import Video
import requests


class GcsFileUploadHandler(FileUploadHandler):
    chunk_size = 128 * 2 ** 12

    # def __init__(self, request):
    #    super().__init__(self, request)
    #     print(args)
    #     print(kwargs)
    #     print ("In INIT!!!!!!!")
    #     # if request.method == 'POST':
    #         # print ("Title: " + request.POST['title'] + " File Size: " + request.META['CONTENT_LENGTH'])
    #         # print(request.META)
    #    self.resumable_uri = None
    #    self.dm_url = None
    #    self.video_id

    def new_file(self, *args, **kwargs):
        print(args)
        print(kwargs.values())
        super().new_file(*args, **kwargs)

        print(self.file_name)
        print(self.field_name)

        video = Video.objects.get(pk=self.video_id)
        print(video)

        access_token = get_access_token()
        destination_file_name = requote_uri('videos/' + self.file_name + '/digital_master.mp4')
        bucket_name = "jrainville_video_bucket_1"

        url = "https://storage.googleapis.com/upload/storage/v1/b/" + bucket_name + "/o?uploadType=resumable&name=" + destination_file_name
        headers = {'Content-Type': 'application/json; charset=UTF-8',
                   'X-Upload-Content-Type': 'video/mp4',
                   'Authorization': 'Bearer ' + access_token}

        r = requests.post(url, data='', headers=headers)

        if 200 <= r.status_code < 300:

            self.resumable_uri = r.headers['Location']
            # JMR - just for testing!! I need to figure out how to get the public url.
            self.dm_url = self.resumable_uri
        else:
            # JMR - need to figure out error handling.
            print("Error")

    def receive_data_chunk(self, raw_data, start):
        access_token = get_access_token()

        print (self.chunk_size)
        the_range = "bytes " + str(start) + "-" + str(start + len(raw_data) - 1) + "/2227641"
        print(the_range)
        headers = {'Content-Length': str(len(raw_data)), "Content-Range": the_range,
                   'Content-Type': 'video/mp4',
                   'Authorization': 'Bearer ' + access_token}
        r = requests.put(self.resumable_uri, headers=headers, data=raw_data)
        print(r.status_code)
        print(r.text)
        print(r.headers)

    def handle_raw_input(self, input_data, META, content_length, boundary, encoding=None):
        print(META)
        print ("Size: " + str(content_length))

    def file_complete(self, file_size):
        # self.file.seek(0)
        self.file_size = file_size
        return self.dm_url