Option Explicit

' ============================================================
'  Physics League — Click-to-Start Question Timer
'  One-time setup: paste this whole module into the VBA editor,
'  then run "SetupTimerButtons" once (see the "Host Setup" slide
'  near the start of the deck for full step-by-step instructions).
'
'  This version does NOT use Application.OnTime — that scheduler
'  is unreliable during an active slideshow on some PowerPoint
'  builds (especially Mac). Instead it polls Timer() in a tight
'  loop with DoEvents, which keeps ticking reliably and still lets
'  PowerPoint respond to other clicks while it runs.
' ============================================================

Public gRunID As Long   ' bumped on each Start click; lets a newer click cancel an older still-running countdown

Sub SetupTimerButtons()
    Dim sld As Slide, shp As Shape, n As Long
    n = 0
    For Each sld In ActivePresentation.Slides
        For Each shp In sld.Shapes
            If shp.Name = "TimerStartBtn" Then
                shp.ActionSettings(ppMouseClick).Action = ppActionRunMacro
                shp.ActionSettings(ppMouseClick).Run = "StartQuestionTimer"
                n = n + 1
            End If
        Next shp
    Next sld
    MsgBox "Wired up " & n & " timer button(s)." & vbCrLf & _
           "Now save this file as a Macro-Enabled Presentation (.pptm) if you haven't already.", _
           vbInformation, "Timer Setup Complete"
End Sub

' Fires when the host clicks "▶ START" during the slideshow.
Sub StartQuestionTimer()
    Dim sld As Slide
    On Error Resume Next
    Set sld = SlideShowWindows(1).View.Slide
    On Error GoTo 0
    If sld Is Nothing Then Exit Sub

    Dim durBox As Shape, dispBox As Shape
    On Error Resume Next
    Set durBox = sld.Shapes("TimerDuration")
    Set dispBox = sld.Shapes("TimerDisplay")
    On Error GoTo 0
    If durBox Is Nothing Or dispBox Is Nothing Then Exit Sub

    Dim secs As Long
    secs = ParseDuration(durBox.TextFrame.TextRange.Text)
    If secs <= 0 Then Exit Sub

    dispBox.TextFrame.TextRange.Font.Color.RGB = RGB(242, 242, 247) ' reset to normal text color

    gRunID = gRunID + 1
    Dim myRunID As Long
    myRunID = gRunID

    Dim slideIdx As Long
    slideIdx = sld.SlideIndex

    Dim endTime As Double
    endTime = Timer + secs

    Dim remaining As Long
    Do
        remaining = CeilSecs(endTime - Timer)
        If remaining < 0 Then remaining = 0

        On Error Resume Next
        dispBox.TextFrame.TextRange.Text = FormatSecs(remaining)
        On Error GoTo 0

        If remaining <= 0 Then Exit Do
        If myRunID <> gRunID Then Exit Sub   ' a newer Start click superseded this one

        Dim stillHere As Boolean
        stillHere = True
        On Error Resume Next
        stillHere = (SlideShowWindows(1).View.Slide.SlideIndex = slideIdx)
        On Error GoTo 0
        If Not stillHere Then Exit Sub       ' host moved to a different slide

        Dim waitUntil As Single
        waitUntil = Timer + 1
        Do While Timer < waitUntil
            DoEvents
            If myRunID <> gRunID Then Exit Sub
        Loop
    Loop

    If myRunID = gRunID Then
        On Error Resume Next
        dispBox.TextFrame.TextRange.Text = "TIME UP"
        dispBox.TextFrame.TextRange.Font.Color.RGB = RGB(255, 93, 115)
        On Error GoTo 0
    End If
End Sub

' Ceiling for positive Doubles: CeilSecs(14.97) = 15, CeilSecs(15.0) = 15.
Function CeilSecs(x As Double) As Long
    CeilSecs = -Int(-x)
End Function

Function FormatSecs(s As Long) As String
    If s >= 60 Then
        FormatSecs = Format(s \ 60, "0") & ":" & Format(s Mod 60, "00")
    Else
        FormatSecs = CStr(s)
    End If
End Function

' Accepts "15", "300", or "5:00" style text from the editable duration box.
Function ParseDuration(t As String) As Long
    Dim tt As String
    tt = Trim(t)
    If InStr(tt, ":") > 0 Then
        Dim parts() As String
        parts = Split(tt, ":")
        On Error Resume Next
        ParseDuration = CLng(Val(parts(0))) * 60 + CLng(Val(parts(1)))
        On Error GoTo 0
    Else
        ParseDuration = CLng(Val(tt))
    End If
End Function
