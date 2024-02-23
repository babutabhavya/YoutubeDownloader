from pytube import Playlist, YouTube, exceptions
import os


def get_highest_quality(streams):
    for resolution in ["720p", "1080p"]:
        for stream in streams:
            if resolution in stream.resolution:
                return stream
    return max(streams, key=lambda x: x.resolution)


def download_video(yt, index, output_path="."):
    try:
        streams = yt.streams.filter(file_extension="mp4", progressive=True)
        selected_stream = get_highest_quality(streams)

        file_name = f"{index}.{yt.title}.mp4"
        file_path = os.path.join(output_path, file_name)

        print(
            f"Downloading: {yt.title} ({selected_stream.resolution}, {selected_stream.mime_type})"
        )
        selected_stream.download(output_path, filename=file_name)
        print(f"Download complete! File saved as: {file_path}")
    except exceptions.MembersOnly as e:
        print(e)
    except Exception as e:
        print(e)


def download_playlist(url, output_path="."):
    playlist = Playlist(url)
    playlist_dir = os.path.join(output_path, playlist.title)
    os.makedirs(playlist_dir, exist_ok=True)

    print(f"Downloading Playlist: {playlist.title}")

    for index, video_url in enumerate(playlist.video_urls, start=1):
        yt = YouTube(video_url)
        download_video(yt, index, playlist_dir)

    print(f"Playlist download complete! Check the '{playlist.title}' directory.")


if __name__ == "__main__":
    print("Welcome to YouTube Downloader!")

    user_input = input("Enter YouTube URL (video or playlist): ")
    output_path = (
        input("Enter download directory (default is current directory): ") or "./videos"
    )

    if "playlist" in user_input.lower():
        download_playlist(user_input, output_path)
    else:
        yt = YouTube(user_input)
        download_video(yt, 1, output_path)
