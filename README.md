# BKS Image Format encoder/decoder

This project was made to experiment file compression. I decied to create my own image format called .bks the compression and optimization is absolutely terrible but this is an ongoing project as I learn new compression algorithm

# How to run it

To Encode as a bks:
    
`python bks_converter.py compress source_image.png target_image.bks`

To decode from bks:

`python bks_converter.py decompress source_image.bks target_image.png`

# Dependencies

The only one used is pillow
