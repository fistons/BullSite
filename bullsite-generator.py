#!/bin/env python3

import argparse
import os
import shutil
import tempfile

import youtube_dl
from jinja2 import Environment, PackageLoader


class BullSite:
    """
     Generate a website based on a video.

     It downloads the video, create an index.html with the video in fullscreen/autoplay/loop in the
     background and optionally create a nginx configuration file for the site.
    """

    def __init__(self, config):
        self._config = config
        self._tempdir = tempfile.mkdtemp()
        self._env = Environment(loader=PackageLoader('bullsite-generator', 'templates'))
        print("%s will be used as the output folder" % self._tempdir)

    def download_video(self):
        """
        Donwload the video and store it in the output folder.
        :return: Nothing.
        """
        configuration = self.__youtube_dl_configuration()
        with youtube_dl.YoutubeDL(configuration) as ydl:
            ydl.download([self._config.video_url])
        print("Downloaded video from %s in %s" % (self._config.video_url, self._tempdir + '/site/'))

    def generate_nginx(self):
        """
        Generate the nginx configuration file in the output folder.
        :return: Nothing.
        """
        template = self._env.get_template('nginx.conf')
        os.makedirs(self._tempdir + '/nginx/', exist_ok=True)
        with open(self._tempdir + '/nginx/nginx.conf', 'w') as f:
            f.write(template.render(site_path=self._config.site_location,
                                    site_url=self._config.site_url))
        print("Generated nginx configuration in %s" % self._tempdir + '/nginx/nginx.conf')

    def generate_index(self):
        """
        Generate the index.html of the website.
        :return: Nothing.
        """
        template = self._env.get_template('index.html')
        os.makedirs(self._tempdir + '/site/', exist_ok=True)
        with open(self._tempdir + '/site/index.html', 'w') as f:
            f.write(template.render(site_name=self._config.name))
        print("Generated website in %s" % self._tempdir + '/site')

    def copy_site(self):
        """
        Copy the website in its destination folder.
        :return: Nothing.
        """
        shutil.copytree(self._tempdir + '/site/', self._config.site_location)

    def __youtube_dl_configuration(self):
        """
        Generate the youtube-dl configuration.
        :return: the youtube-dl configuration.
        :rtype: dict
        """
        return {
            'outtmpl': self._tempdir + '/site/video.mp4',
            'format': 'mp4'
        }


YES_ANSWERS = ['Y', 'y', 'O', 'o', '']
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a bullshit website based on a video')
    parser.add_argument('--video_url',
                        type=str,
                        help='Url of the video on Youtube or elsewhere',
                        required=True)
    parser.add_argument('--name',
                        type=str, help='Name of the bullsite',
                        required=True)
    parser.add_argument('--site_url',
                        type=str,
                        help='URL of the bullsite to create',
                        required=True)
    parser.add_argument('--site_location',
                        type=str,
                        help='Path of the folder where the website will be stored',
                        required=True)

    args = parser.parse_args()

    bullsite = BullSite(args)
    bullsite.download_video()
    bullsite.generate_nginx()
    bullsite.generate_index()

    if input("Generate nginx config file? (Y/n)") in YES_ANSWERS:
        bullsite.generate_nginx()
