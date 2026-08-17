Option Explicit

' ============================================================
'  Run this ONCE if you're updating an existing .pptm that already
'  has the timer working (START button) but is missing the newer
'  RESET button. It draws a RESET button next to the countdown on
'  every question slide, matching the deck's style, without you
'  needing to redo the Save-As-.pptm / re-paste process.
'
'  Safe to re-run — it skips any slide that already has one.
'  You can delete this module afterward if you like; it's not
'  needed for normal operation once the buttons exist.
' ============================================================

Sub AddResetButtons()
    Dim sld As Slide, dispBox As Shape, existing As Shape
    Dim newRect As Shape, newTxt As Shape
    Dim n As Long
    n = 0

    For Each sld In ActivePresentation.Slides
        On Error Resume Next
        Set dispBox = Nothing
        Set dispBox = sld.Shapes("TimerDisplay")
        On Error GoTo 0
        If Not dispBox Is Nothing Then

            On Error Resume Next
            Set existing = Nothing
            Set existing = sld.Shapes("TimerResetBtn")
            On Error GoTo 0

            If existing Is Nothing Then
                Dim gap As Single, rw As Single, rh As Single, rx As Single, ry As Single
                gap = 0.1 * 72   ' inches -> points
                rw = 0.75 * 72
                rh = dispBox.Height
                rx = dispBox.Left + dispBox.Width + gap
                ry = dispBox.Top

                Set newRect = sld.Shapes.AddShape(msoShapeRoundedRectangle, rx, ry, rw, rh)
                newRect.Fill.ForeColor.RGB = RGB(38, 38, 51)     ' matches deck's PANEL2
                newRect.Line.ForeColor.RGB = RGB(154, 154, 176)  ' matches deck's MUTED
                newRect.Line.Weight = 1
                newRect.Adjustments(1) = 0.2

                Set newTxt = sld.Shapes.AddTextbox(msoTextOrientationHorizontal, rx, ry, rw, rh)
                newTxt.Name = "TimerResetBtn"
                With newTxt.TextFrame
                    .VerticalAnchor = msoAnchorMiddle
                    .MarginLeft = 0
                    .MarginRight = 0
                    .MarginTop = 0
                    .MarginBottom = 0
                    With .TextRange
                        .Text = "RESET"
                        .Font.Name = "Calibri"
                        .Font.Size = 11
                        .Font.Bold = True
                        .Font.Color.RGB = RGB(154, 154, 176)
                        .ParagraphFormat.Alignment = ppAlignCenter
                    End With
                End With

                n = n + 1
            End If
        End If
    Next sld

    MsgBox "Added " & n & " RESET button(s)." & vbCrLf & _
           "Now run SetupTimerButtons to wire it (and the Start buttons) up.", _
           vbInformation, "Reset Buttons Added"
End Sub
