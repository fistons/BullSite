#!/bin/env python3

import argparse
import logging
import os
import tempfile

import youtube_dl
from jinja2 import Environment, PackageLoader


class BullSite:

    def __init__(self, config):
        self._config = config
        self._tempdir = tempfile.mkdtemp()
        self._env = Environment(loader=PackageLoader('bullsite-generator', 'templates'))
        logging.info("Using %s as temp directory", self._tempdir)

    def download_video(self):
        configuration = self.__youtube_dl_configuration()
        with youtube_dl.YoutubeDL(configuration) as ydl:
            ydl.download([self._config.video_url])
            logging.debug("Downloaded video from %s", self._config.video_url)

    def generate_nginx(self):
        template = self._env.get_template('nginx.conf')
        os.makedirs(self._tempdir + '/nginx/', exist_ok=True)
        with open(self._tempdir + '/nginx/nginx.conf', 'w') as f:
            f.write(template.render(site_path=self._config.site_location,
                                    site_url=self._config.site_url))
        logging.debug("Generated nginx configuration in %s", self._tempdir + '/nginx/nginx.conf')

    def generate_index(self):
        template = self._env.get_template('index.html')
        os.makedirs(self._tempdir + '/site/', exist_ok=True)
        with open(self._tempdir + '/site/index.html', 'w') as f:
            f.write(template.render(site_name=self._config.name))
        logging.debug("Generated website in %s", self._tempdir + '/site')

    def __youtube_dl_configuration(self):
        return {
            'outtmpl': self._tempdir + '/site/video.mp4',
            'format': 'mp4'
        }


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
