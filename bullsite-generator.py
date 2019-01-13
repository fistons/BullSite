#!/bin/env python3

import argparse
import tempfile

import youtube_dl
from jinja2 import Environment, PackageLoader


class BullSite:
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }

    def __init__(self, args):
        self.args = args
        self.tempdir = tempfile.mkdtemp()
        self.env = Environment(loader=PackageLoader('bullsite-generator', 'templates'))
        print("Using %s as temp directory" % self.tempdir)

    def download_video(self):
        with youtube_dl.YoutubeDL(self.__youtube_dl_configuration()) as ydl:
            print(ydl.download([self.args.video_url]))

    def generate_nginx(self):
        template = self.env.get_template('nginx.conf')
        with open('truc', 'w') as f:
            f.write(template.render(site_path=self.args.site_location, site_url=self.args.site_url))

    def generate_index(self):
        template = self.env.get_template('index.html')
        with open('machin', 'w') as f:
            f.write(template.render(video_name=self.args.site_location, video_mime="toto",
                                    site_name=self.args.site_url))

    def __youtube_dl_configuration(self):
        return {
            'outtmpl': self.args.name,
            'format': 'mp4'
        }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a bullshit website based on a video')
    parser.add_argument('--video_url', type=str, help='Url of the video on Youtube or elsewhere',
                        required=True)
    parser.add_argument('--name', type=str, help='Name of the bullsite', required=True)
    parser.add_argument('--site_url', type=str, help='URL of the bullsite to create', required=True)
    parser.add_argument('--site_location', type=str,
                        help='Path of the folder where the website will be stored', required=True)

    args = parser.parse_args()

    bullsite = BullSite(args)
    bullsite.download_video()
    bullsite.generate_nginx()
    bullsite.generate_index()
