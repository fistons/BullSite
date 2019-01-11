#!/bin/env python3

import argparse

import youtube_dl
from jinja2 import Environment, PackageLoader


def download_video(args):
    ydl = youtube_dl.YoutubeDL({'outtmpl': args.name})
    with ydl:
        print(ydl.download([args.video_url]))


def generate_nginx(args):
    env = Environment(loader=PackageLoader('bullsite-generator', 'templates'))
    template = env.get_template('nginx.conf')
    print(template.render(site_path=args.site_location, site_url=args.site_url))


def generate_index(args):
    env = Environment(loader=PackageLoader('bullsite-generator', 'templates'))
    template = env.get_template('index.html')
    print(
        template.render(video_name=args.site_location, video_mime="toto", site_name=args.site_url))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a bullshit website based on a video')
    parser.add_argument('--video_url', type=str, help='Url of the video on Youtube or elsewhere',
                        required=True)
    parser.add_argument('--name', type=str, help='Name of the bullsite', required=True)
    parser.add_argument('--site_url', type=str, help='URL of the bullsite to create', required=True)
    parser.add_argument('--site_location', type=str,
                        help='Path of the folder where the website will be stored', required=True)

    args = parser.parse_args()

    # download_video(args)
    generate_nginx(args)
    generate_index(args)

