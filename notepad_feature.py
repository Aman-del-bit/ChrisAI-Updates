# notepad_feature.py

import android
droid = android.Android()

def open_notepad():
    print("📝 Opening the Notepad app...")
    droid.startActivity(
        action="android.intent.action.MAIN",
        package="com.android.notepad",  # Change if using another app
        className="com.android.notepad.NotesList"
    )
