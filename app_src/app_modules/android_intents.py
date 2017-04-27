from jnius import autoclass, cast

def android_fileExt_activity(ext,text):
    if platform == 'android':
        PythonActivity = autoclass('org.renpy.android.PythonActivity')
        Intent = autoclass('android.content.Intent')
        Uri = autoclass('android.net.Uri')
        File = autoclass('java.io.File')
        intent = Intent()
        ssdd = File(text)
        intent.setAction(Intent.ACTION_VIEW)
    ##                intent.setData(Uri.parse(ssdd))
        intent.setDataAndType(Uri.fromFile(ssdd), ext)
        currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
        currentActivity.startActivity(intent)
