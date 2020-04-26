import json
import os
import re
import shutil
import subprocess
import uuid

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Disease
from api.serializers import UserDataSerializer, DiseaseSerializer
# from keras_covid_19.test import test_covid

lang_dir = os.path.join(settings.BASE_DIR, "language_json")
def subprocess_cmd(command):
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    result = re.search('\-\-\-(.*)\*\*\*', str(proc_stdout))
    print(result.group(1))
    return result.group(1)

class UploadUserData(APIView):
    # serializer_class = UserDataSerializer
    # def get(self, *args, **kwargs):
    #     return Response(status=200)
    #
    def post(self, *args, **kwargs):
        data = self.request.data
        ser_data = UserDataSerializer(data=data)
        if ser_data.is_valid():
            ser_data.save()
            myfile = self.request.FILES.get('image')
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            # save file in main root dir
            path_of_file = fs.path(filename)
            image_path = os.path.join(settings.BASE_DIR, "image_xray/" + uuid.uuid4().hex + "/")
            os.makedirs(image_path, exist_ok=True)
            return_file = shutil.copyfile(path_of_file, image_path + filename)
            result = subprocess_cmd("cd "+os.path.join(settings.BASE_DIR,"keras_covid_19")+";python test.py "+image_path)
            # result = test_covid(image_path)
            response_dict = {"result": result}

            return Response(response_dict, status=200, )
        else:
            print(ser_data.errors)
            return Response(status=200, )


class COVIDTest(APIView):
    def post(self, *args, **kwargs):
        data = DiseaseSerializer(data=self.request.data)
        if data.is_valid():
            data.save()
        else:
            raise Exception
        return Response(status=200)

    def get(self, *args, **kwargs):
        data = Disease.objects.all()
        json_data = DiseaseSerializer(data, many=True)
        return Response(json_data.data, status=200)


class BotApi(APIView):
    def get(self, *args, **kwargs):
        list_language = os.listdir(lang_dir)
        list_language = [x[:-5] for x in list_language]
        print(list_language)
        return Response(status=200, data={"language": list_language})

    def post(self, *args, **kwargs):
        language = self.request.data.get('language', 'english')
        file_path = os.path.join(lang_dir, str(language) + ".json")
        json_file = open(file_path, encoding='utf-8')
        response_json = json.load(json_file)
        return Response(status=200, data=response_json)
