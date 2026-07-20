import argparse
import sys


def main():
    sys.stdout.reconfigure(encoding='utf-8', newline='\n')
    parser = argparse.ArgumentParser()
    parser.add_argument('note_id')   # note ID to extract from SSR state
    args = parser.parse_args()

    note_id = args.note_id

    js = f"""
(function() {{
  try {{
    var noteId = '{note_id}';
    var noteMap = window.__INITIAL_STATE__ &&
                  window.__INITIAL_STATE__.note &&
                  window.__INITIAL_STATE__.note.noteDetailMap;
    if (!noteMap) return JSON.stringify({{error: true, message: 'noteDetailMap not found - ensure page has fully loaded'}});
    var ref = noteMap[noteId];
    if (!ref) return JSON.stringify({{error: true, message: 'note not found in state, note_id: ' + noteId, availableIds: Object.keys(noteMap)}});

    var container = ref._value || ref;
    var noteRef = container.note;
    var note = (noteRef && noteRef._value) ? noteRef._value : noteRef;
    if (!note) return JSON.stringify({{error: true, message: 'note data object missing', containerKeys: Object.keys(container)}});

    // Extract video URL (prefer h264, fallback to h265)
    var videoUrl = null;
    var video = note.video;
    if (video && video.media && video.media.stream) {{
      var h264 = video.media.stream.h264;
      if (h264 && h264.length > 0) {{
        videoUrl = h264[0].masterUrl || (h264[0].backupUrls && h264[0].backupUrls[0]) || null;
      }}
      if (!videoUrl) {{
        var h265 = video.media.stream.h265;
        if (h265 && h265.length > 0) videoUrl = h265[0].masterUrl || null;
      }}
    }}

    // Extract image list with default-quality URLs
    var imageList = note.imageList || [];
    var imageUrls = imageList.map(function(img) {{
      var infoList = img.infoList || [];
      var dftInfo = infoList.filter(function(x) {{ return x.imageScene === 'WB_DFT'; }})[0] || infoList[0];
      return {{
        url: (dftInfo && dftInfo.url) || img.urlDefault || img.url_default || null,
        width: img.width || null,
        height: img.height || null
      }};
    }});

    // Extract tag list
    var tagList = (note.tagList || []).map(function(t) {{
      return {{ name: t.name, type: t.type, id: t.id }};
    }});

    var interact = note.interactInfo || {{}};

    return JSON.stringify({{
      noteId: note.noteId,
      title: note.title,
      desc: note.desc,
      type: note.type,
      time: note.time,
      ipLocation: note.ipLocation || null,
      userId: note.user && note.user.userId || null,
      nickname: note.user && note.user.nickname || null,
      avatar: note.user && note.user.avatar || null,
      likedCount: interact.likedCount || null,
      collectedCount: interact.collectedCount || null,
      commentCount: interact.commentCount || null,
      shareCount: interact.shareCount || null,
      tagList: tagList,
      imageList: imageUrls,
      videoUrl: videoUrl
    }});
  }} catch(e) {{
    return JSON.stringify({{error: true, message: e.message}});
  }}
}})()
"""
    print(js)


if __name__ == '__main__':
    main()
