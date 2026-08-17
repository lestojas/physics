Option Explicit

' ============================================================
'  Physics League — Click-to-Start Question Timer
'  One-time setup: paste this whole module into the VBA editor,
'  then run "SetupTimerButtons" once (see the "Host Setup" slide
'  near the start of the deck for full step-by-step instructions).
' ============================================================

Public gTimerEndTime As Double     ' Timer()-based end time (seconds since midnight)
Public gTimerSlideIndex As Long
Public gTimerRunning As Boolean
Public gTimeUpShown As Boolean

' Run this ONCE after pasting the module in. It finds every
' "▶ START" button on every slide and wires it to StartQuestionTimer.
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
    On Error Resume Next
    Dim sld As Slide
    Set sld = SlideShowWindows(1).View.Slide
    If sld Is Nothing Then Exit Sub

    Dim durBox As Shape, dispBox As Shape
    Set durBox = sld.Shapes("TimerDuration")
    Set dispBox = sld.Shapes("TimerDisplay")
    If durBox Is Nothing Or dispBox Is Nothing Then Exit Sub

    Dim secs As Long
    secs = ParseDuration(durBox.TextFrame.TextRange.Text)
    If secs <= 0 Then Exit Sub

    dispBox.TextFrame.TextRange.Font.Color.RGB = RGB(242, 242, 247) ' reset to normal text color
    gTimerEndTime = Timer + secs
    gTimerSlideIndex = sld.SlideIndex
    gTimerRunning = True
    gTimeUpShown = False
    UpdateTimerDisplay
    ScheduleTick
End Sub

Sub ScheduleTick()
    Application.OnTime Now + TimeSerial(0, 0, 1), "TimerTick"
End Sub

Sub TimerTick()
    If Not gTimerRunning Then Exit Sub

    On Error Resume Next
    Dim curIdx As Long
    curIdx = SlideShowWindows(1).View.Slide.SlideIndex
    On Error GoTo 0

    ' Stop if the host has moved off the question slide (or show ended).
    If curIdx = 0 Or curIdx <> gTimerSlideIndex Then
        gTimerRunning = False
        Exit Sub
    End If

    Dim secsLeft As Long
    secsLeft = CLng(gTimerEndTime - Timer + 0.999)
    If secsLeft <= 0 Then
        secsLeft = 0
        gTimerRunning = False
    End If

    UpdateTimerDisplay secsLeft

    If gTimerRunning Then
        ScheduleTick
    Else
        ShowTimeUp
    End If
End Sub

Sub UpdateTimerDisplay(Optional secsLeft As Variant)
    On Error Resume Next
    Dim sld As Slide, dispBox As Shape
    Set sld = ActivePresentation.Slides(gTimerSlideIndex)
    Set dispBox = sld.Shapes("TimerDisplay")
    If dispBox Is Nothing Then Exit Sub

    Dim s As Long
    If IsMissing(secsLeft) Then
        s = CLng(gTimerEndTime - Timer + 0.999)
    Else
        s = secsLeft
    End If
    If s < 0 Then s = 0
    dispBox.TextFrame.TextRange.Text = FormatSecs(s)
End Sub

Sub ShowTimeUp()
    On Error Resume Next
    If gTimeUpShown Then Exit Sub
    gTimeUpShown = True

    Dim sld As Slide, dispBox As Shape
    Set sld = ActivePresentation.Slides(gTimerSlideIndex)
    Set dispBox = sld.Shapes("TimerDisplay")
    If dispBox Is Nothing Then Exit Sub

    dispBox.TextFrame.TextRange.Text = "TIME UP"
    dispBox.TextFrame.TextRange.Font.Color.RGB = RGB(255, 93, 115)
End Sub

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
