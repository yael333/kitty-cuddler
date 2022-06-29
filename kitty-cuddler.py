import argparse, os, music_tag, time
from moviepy.editor import *

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='join some files to make an album')
	parser.add_argument('directory',
	                metavar='directory',
	                type=str,
	                help='da diwectowy')
	parser.add_argument('cover',
	                metavar='cover',
	                nargs='?',
	                default="",
	                type=str,
	                help='da cower')
	args = parser.parse_args()
	directory = args.directory
	cover = args.cover

	if not os.path.isdir(directory):
		print("[</3] invalid directory, quitting....")
		exit()

	print(f"[*] looking for music in {directory} :3")
	tracks = []
	for kitty in os.listdir(directory):
	    kitty = os.path.join(directory, kitty)
	    if os.path.isfile(kitty):
	        if kitty.split('.')[-1].lower() in ['acc', 'aiff', 'dsf', 'flac', 'm4a', 'mp3', 'ogg', 'opus', 'wav', 'wv']:
	        	tracks.append((kitty, music_tag.load_file(kitty)))
	tracks.sort(key=lambda t: t[1]["tracknumber"].value)
	if len(tracks):
		print(f"[<3] found {len(tracks)} tracks on album {tracks[0][1]['album']}")
	else:
		print("[</3] couldn't find any songs, quitting...")
		exit()
	audioClips = []
	for track in tracks :
		audioClips.append(AudioFileClip(track[0]))
	
	if not cover:
		print("[*] image files in directory - ", ', '.join(filter(lambda f: f.endswith(".jpg") or f.endswith("png"), os.listdir(directory))))
		cover = input("[!] please enter cover file: ")
	cover = os.path.join(directory, cover)
	if os.path.isfile(cover):
		print("[<3] found cover, starting to make video :33")
	else:
		print("[</3] couldn't find the cover, quitting...")
		exit()

	audio_clip = concatenate_audioclips(audioClips)
	video_clip = ImageClip(cover)
	video_clip = video_clip.set_audio(audio_clip)
	video_clip.duration = audio_clip.duration
	video_clip.fps = 1

	video_clip.write_videofile(f'{"".join(c for c in tracks[0][1]["album"].value if c.isalnum() or c == " ")}.mp4')
	print("[<3] finished making video, starting to make yt description :D")

	title = f"{tracks[0][1]['artist']} - {tracks[0][1]['album']} ({tracks[0][1]['year']})\n"
	print(title)

	duration = 0
	for t in tracks:
		frmt_string = "%M:%S"
		if duration >= 3600:
			frmt_string = "%H:" + frmt_string 
		print(f"{time.strftime(frmt_string, time.gmtime(duration))} {t[1]['title']}")
		duration += t[1]['#length'].value
