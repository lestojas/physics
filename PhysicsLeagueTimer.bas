Option Explicit

' ============================================================
'  Physics League — Click-to-Start Question Timer
'  One-time setup: see the "Host Setup" slide near the start of
'  the deck, or the setup instructions sent alongside this file.
'
'  This module does NOT use Application.OnTime — that scheduler
'  is unreliable during an active slideshow on some PowerPoint
'  builds (especially Mac). Instead it polls Timer() in a tight
'  loop with DoEvents, which keeps ticking reliably and still lets
'  PowerPoint respond to other clicks while it runs.
'
'  Companion file:
'   - PhysicsLeagueTimerEvents.cls (class module) — detects when
'     you return to a slide whose timer already finished, and
'     resets it automatically.
'
'  On some PowerPoint-for-Mac builds, the built-in "ThisPresentation"
'  module doesn't show up in the Project pane, so instead of relying
'  on it to auto-activate on file open, just run ActivateAutoReset
'  (below) once each time you open the file — same one-time-per-session
'  habit as running SetupTimerButtons.
' ============================================================

Public gRunID As Long        ' bumped on each Start/Reset click; cancels an older still-running countdown
Public gTrap As Object       ' holds the PhysicsLeagueTimerEvents instance (declared As Object so this compiles even before that class module is added)

' Run this once per session (each time you open the file) to turn on
' the "auto-reset a finished timer when you return to its slide" behavior.
Sub ActivateAutoReset()
    Set gTrap = New PhysicsLeagueTimerEvents
    Set gTrap.App = Application
    MsgBox "Auto-reset watcher is active for this session.", vbInformation, "Ready"
End Sub

Sub SetupTimerButtons()
    Dim sld As Slide, shp As Shape, n As Long
    n = 0
    For Each sld In ActivePresentation.Slides
        For Each shp In sld.Shapes
            If shp.Name = "TimerStartBtn" Then
                shp.ActionSettings(ppMouseClick).Action = ppActionRunMacro
                shp.ActionSettings(ppMouseClick).Run = "StartQuestionTimer"
                n = n + 1
            ElseIf shp.Name = "TimerResetBtn" Then
                shp.ActionSettings(ppMouseClick).Action = ppActionRunMacro
                shp.ActionSettings(ppMouseClick).Run = "ResetQuestionTimer"
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
        If myRunID <> gRunID Then Exit Sub   ' a newer Start/Reset click superseded this one

        Dim stillHere As Boolean
        stillHere = True
        On Error Resume Next
        stillHere = (SlideShowWindows(1).View.Slide.SlideIndex = slideIdx)
        On Error GoTo 0
        If Not stillHere Then Exit Sub       ' host moved to a different slide — leave the frozen value as-is

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

' Fires when the host clicks "RESET" during the slideshow.
Sub ResetQuestionTimer()
    On Error Resume Next
    Dim sld As Slide
    Set sld = SlideShowWindows(1).View.Slide
    If sld Is Nothing Then Exit Sub
    gRunID = gRunID + 1   ' cancels any countdown currently in progress
    ResetTimerDisplay sld
    On Error GoTo 0
End Sub

' Sets a slide's TimerDisplay back to its TimerDuration value. Used by both
' the manual RESET button and the auto-reset-on-return logic below.
Sub ResetTimerDisplay(sld As Slide)
    On Error Resume Next
    Dim durBox As Shape, dispBox As Shape
    Set durBox = sld.Shapes("TimerDuration")
    Set dispBox = sld.Shapes("TimerDisplay")
    If durBox Is Nothing Or dispBox Is Nothing Then Exit Sub
    dispBox.TextFrame.TextRange.Text = durBox.TextFrame.TextRange.Text
    dispBox.TextFrame.TextRange.Font.Color.RGB = RGB(242, 242, 247)
    On Error GoTo 0
End Sub

' Called (via PhysicsLeagueTimerEvents.cls) every time the visible slide
' changes during the slideshow. If this slide's timer already finished,
' auto-reset it to the original duration so it's ready to run again.
' If the timer was left mid-countdown, this does nothing — that frozen
' value stays until the host clicks RESET or START again.
Sub AutoResetIfFinished(sld As Slide)
    On Error Resume Next
    Dim dispBox As Shape
    Set dispBox = sld.Shapes("TimerDisplay")
    If dispBox Is Nothing Then Exit Sub
    If dispBox.TextFrame.TextRange.Text = "TIME UP" Then
        ResetTimerDisplay sld
    End If
    On Error GoTo 0
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
