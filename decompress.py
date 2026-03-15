import zstandard as zstd

def Decompress(filepath):
    successbit = False
    output_filepath = filepath[:-4]
    dctx = zstd.ZstdDecompressor()
    with open(filepath, 'rb') as ifh, open(output_filepath, 'wb') as ofh:
        # Use copy_stream for efficient, memory-friendly streaming decompression
        dctx.copy_stream(ifh, ofh)
        successbit = True
    return output_filepath,successbit
