#!/bin/env python3

import argparse

import youtube_dl


def download_video(args):
    ydl = youtube_dl.YoutubeDL({'outtmpl': args.name})
    with ydl:
        print(ydl.download([args.video_url]))


def generate_nginx(args):
    with open('templates/nginx.conf', 'r') as nginx:
        for line in nginx:
            print(line)
            line = line.format(site_path=args.site_path, site_url=args.site_url)
            print(line)

def generate_index(args):
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--video_url', type=str, help='Url of the video on Youtube or elsewhere',
                        required=True)
    parser.add_argument('--name', type=str, help='Name of the bullsite', required=True)
    parser.add_argument('--site_url', type=str, help='URL of the bullsite to create', required=True)
    parser.add_argument('--site_location', type=str,
                        help='Path of the folder where the website will be stored', required=True)

    args = parser.parse_args()


    # download_video(args)
    # generate_nginx(args)
