import yt_dlp

ytdl_opts = {
    'listformats': True,
    'nocheckcertificate': True
}

ydl = yt_dlp.YoutubeDL(ytdl_opts)          
def get_resolution(url):
     formats = ydl.extract_info(url, download=False)["formats"]
     format_id = []
     for format in formats:  
            if 'vbr' in format and 'abr' in format:
               resol = (format["resolution"])
               format_id.append({resol : (format["format_id"])})
     if format_id == []:
       for format in formats:
          if 'vbr' in format:
                    resol = (format["resolution"])
                    format_id.append({resol : (format["format_id"])+"+bestaudio"})
     return format_id
    
