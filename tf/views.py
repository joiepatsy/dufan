from django.shortcuts import render
from django.http import Http404
import requests
import sys
import subprocess
from subprocess import run, PIPE
import json
import glob
from django.views import generic
from django.views.generic.edit import CreateView
from .models import Video
import pathlib
import re
import os

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"\\"

def getvideos():
	base_length = len(base)+12
	videolist = []
	for path in pathlib.Path("data/videos").iterdir():
		path = str(path)
		videolist.append(path[base_length:])
	return videolist

def index(req):
	with open("data.txt") as json_file:
		data = json.load(json_file)
	videos = getvideos()
	return render(req, 'tf/index.html', {'data': data, 'videos': videos})

def tensorflow(req):
	inp = str(req.POST.get('video'))
	if(inp == 'None'):
		with open(base+"data.txt") as json_file:
			data = json.load(json_file)
		videos = getvideos()
		return render(req, 'tf/index.html', {'notif': 'Anda harus memilih salah satu video!', 'data': data, 'videos': videos})	
	else:
		outp = run([sys.executable, base+'detect.py', base+'data/videos/'+inp],shell=False, stdout=PIPE)
		with open(base+"data.txt") as json_file:
			data = json.load(json_file)
		videos = getvideos()
		return render(req, 'tf/index.html', {'notif': 'Detections have been saved successfully!', 'data': data, 'videos': videos})

def atoi(text):
	return int(text) if text.isdigit() else text

def natural_keys(text):
	return [ atoi(c) for c in re.split(r'(\d+)', text)]

def frames(req, id=0):
	if (id>99):
		raise Http404("Sorry the id of detection is more than 99. I'm still working on for the next update")
	if (id==0):
		raise Http404("Sorry Page Not Found, hehe...")
	tempframespath = []
	framespath = []
	frames= glob.glob(base + "tf/static/frames/*.png")
	frameslength = len(base) + 9
	for c in frames:
		if (id>9):
			if(c[-6:-4] == str(id)):
				tempframespath.append(c)
		else:
			if(c[-5:-4] == str(id)):
				tempframespath.append(c)
	for j in tempframespath:
		framespath.append(j[frameslength:])
	framespath.sort(key=natural_keys)
	return render(req, 'tf/frames.html', {'id': id, 'framespath': framespath})
	
def videoresult(req, id=0):
	if (id>99):
		raise Http404("Sorry the id of detection is more than 99. I'm still working on for the next update")
	if (id==0):
		raise Http404("Sorry Page Not Found, hehe...")
	videopath = ''
	videos= glob.glob(base + "tf/static/detections/*.mp4");
	videolength = len(base) + 9
	for c in videos:
		if (id>9):
			if(c[-6:-4] == str(id)):
				videopath = c[9:]
		else:
			if(c[-5:-4] == str(id)):
				videopath = c[videolength:]
	return render(req, 'tf/videoresult.html', {'id': id, 'videopath': videopath})

class uploadvideo(CreateView):
	model = Video
	fields = ['video']

def afterupload(req):
	return render(req, 'tf/afterupload.html')