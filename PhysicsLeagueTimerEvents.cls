VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "PhysicsLeagueTimerEvents"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit

' ============================================================
'  Watches for slide changes during the slideshow so a FINISHED
'  timer ("TIME UP") resets itself the moment you return to that
'  slide. A timer left mid-countdown is untouched (use the RESET
'  button for that one).
'
'  Import this file via VBA editor: File -> Import File...
'  Also needs a few lines pasted into "ThisPresentation" — see
'  the setup instructions sent alongside this file.
' ============================================================

Public WithEvents App As Application

Private Sub App_SlideShowNextSlide(ByVal Wn As SlideShowWindow)
    On Error Resume Next
    AutoResetIfFinished Wn.View.Slide
    On Error GoTo 0
End Sub

Private Sub App_SlideShowBegin(ByVal Wn As SlideShowWindow)
    On Error Resume Next
    AutoResetIfFinished Wn.View.Slide
    On Error GoTo 0
End Sub
