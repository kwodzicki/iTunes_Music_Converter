# iTunes_Music_Converter

**iTunes_Music_Converter** is a Python package useful for converting files in
your iTunes library to MP3 and FLAC files.

## Main features

* Compatible with Python3
* Will add all metadata available in the iTunes XML library using [mutagen][mutagen]
* Will try to download cover art using [Musicbrainz][Musicbrainz NGS]
* GUI window that displays progress of conversions

## Installation

Whenever it's possible, please always use the latest version from the repository.
To install it using `pip`:

    pip install git+https://github.com/kwodzicki/iTunes_Music_Converter

## Dependencies

* [FFmpeg][ffmpeg] - Used for converting audio

All other dependencies should install through `pip`.

## License

iTunes_Music_Converter is released under the terms of the GNU GPL v3 license.

[mutagen]: https://github.com/quodlibet/mutagen
[Musicbrainz NGS]: https://github.com/alastair/python-musicbrainzngs
[ffmpeg]: https://www.ffmpeg.org/
