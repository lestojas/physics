"""
Generate a PDF version of the Problem Set 3 Solution Key for formatting verification.
Uses reportlab to render the same content with aligned equal signs.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.colors import HexColor, black, gray
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)
from reportlab.lib import colors


def build_pdf():
    doc = SimpleDocTemplate(
        '/projects/sandbox/physics/ProblemSet3-SolutionKey.pdf',
        pagesize=letter,
        leftMargin=1*inch,
        rightMargin=1*inch,
        topMargin=1*inch,
        bottomMargin=1*inch
    )

    styles = getSampleStyleSheet()

    # Custom styles
    styles.add(ParagraphStyle(
        name='ProblemHeading',
        parent=styles['Heading1'],
        fontSize=14,
        spaceAfter=6,
        spaceBefore=18,
        fontName='Helvetica-Bold'
    ))

    styles.add(ParagraphStyle(
        name='SectionLabel',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=4,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    ))

    styles.add(ParagraphStyle(
        name='ProblemText',
        parent=styles['Normal'],
        fontSize=11,
        leftIndent=36,
        spaceAfter=6,
        spaceBefore=4,
        fontName='Helvetica'
    ))

    styles.add(ParagraphStyle(
        name='NormalIndent',
        parent=styles['Normal'],
        fontSize=11,
        leftIndent=36,
        spaceAfter=4,
        spaceBefore=4,
        fontName='Helvetica'
    ))

    styles.add(ParagraphStyle(
        name='BulletCustom',
        parent=styles['Normal'],
        fontSize=11,
        leftIndent=50,
        firstLineIndent=-14,
        spaceAfter=2,
        spaceBefore=2,
        fontName='Helvetica'
    ))

    styles.add(ParagraphStyle(
        name='Equation',
        parent=styles['Normal'],
        fontSize=11,
        leftIndent=36,
        spaceAfter=4,
        spaceBefore=4,
        fontName='Helvetica-Oblique'
    ))

    styles.add(ParagraphStyle(
        name='SubHeading',
        parent=styles['Normal'],
        fontSize=11,
        leftIndent=18,
        spaceAfter=4,
        spaceBefore=8,
        fontName='Helvetica-Bold'
    ))

    styles.add(ParagraphStyle(
        name='Commentary',
        parent=styles['Normal'],
        fontSize=11,
        leftIndent=36,
        spaceAfter=6,
        spaceBefore=4,
        fontName='Helvetica-Oblique',
        textColor=HexColor('#404040')
    ))

    elements = []

    def add_aligned_table(rows, col_widths=None):
        """Add a 4-column aligned table for derivation steps."""
        if col_widths is None:
            col_widths = [1.6*inch, 0.3*inch, 2.3*inch, 2.3*inch]

        table_data = []
        for row in rows:
            # Pad row to 4 columns
            padded = list(row) + [''] * (4 - len(row))
            styled_row = []
            for j, cell in enumerate(padded[:4]):
                if j == 3 and cell:  # annotation column
                    styled_row.append(Paragraph(f'<i><font color="#505050">{cell}</font></i>', styles['Normal']))
                else:
                    styled_row.append(Paragraph(cell, styles['Normal']))
            table_data.append(styled_row)

        t = Table(table_data, colWidths=col_widths)
        t.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('ALIGN', (2, 0), (2, -1), 'LEFT'),
            ('ALIGN', (3, 0), (3, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ]))
        # Indent table
        t.hAlign = 'LEFT'
        t._argW[0] = col_widths[0]
        elements.append(Spacer(1, 4))
        elements.append(t)
        elements.append(Spacer(1, 4))

    def add_given_table(rows):
        """Add a Given table with Symbol/Value/Annotation headers."""
        col_widths = [1.0*inch, 1.5*inch, 4.0*inch]
        header = [
            Paragraph('<b>Symbol</b>', styles['Normal']),
            Paragraph('<b>Value</b>', styles['Normal']),
            Paragraph('<b>Annotation</b>', styles['Normal']),
        ]
        table_data = [header]
        for row in rows:
            styled_row = [
                Paragraph(row[0], styles['Normal']),
                Paragraph(row[1], styles['Normal']),
                Paragraph(f'<i>{row[2]}</i>', styles['Normal']),
            ]
            table_data.append(styled_row)

        t = Table(table_data, colWidths=col_widths)
        t.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.grey),
        ]))
        t.hAlign = 'LEFT'
        elements.append(Spacer(1, 4))
        elements.append(t)
        elements.append(Spacer(1, 4))

    # =========================================================================
    # PROBLEM 1
    # =========================================================================
    elements.append(Paragraph('Problem 1', styles['ProblemHeading']))
    elements.append(Paragraph(
        'In the fastest measured tennis serve, the ball left the racquet at 73.14 m/s. '
        'A served tennis ball is typically in contact with the racquet for 30.0 ms and starts from rest. '
        'Assume constant acceleration. (a) What was the ball\u2019s acceleration during this serve? '
        '(b) How far did the ball travel during the serve?',
        styles['ProblemText']
    ))

    # Given
    elements.append(Paragraph('Given', styles['SectionLabel']))
    elements.append(Paragraph('\u2022  v\u2080 = 0 m/s \u2014 "Starts from rest" means initial velocity is zero', styles['BulletCustom']))
    elements.append(Paragraph('\u2022  v = 73.14 m/s \u2014 Final speed as it leaves the racquet', styles['BulletCustom']))
    elements.append(Paragraph('\u2022  t = 30.0 ms = 0.0300 s \u2014 Convert ms \u2192 s by dividing by 1000, since equations need SI units', styles['BulletCustom']))

    # Required
    elements.append(Paragraph('Required', styles['SectionLabel']))
    elements.append(Paragraph('(a)  a = ?', styles['NormalIndent']))
    elements.append(Paragraph('(b)  (x \u2212 x\u2080) = ?   (distance traveled)', styles['NormalIndent']))

    # Solution (a)
    elements.append(Paragraph('Solution', styles['SectionLabel']))
    elements.append(Paragraph('(a) Finding acceleration', styles['SubHeading']))
    elements.append(Paragraph(
        'Which equation?  We are given v\u2080, v, and t. We are not given \u2014 and don\u2019t need \u2014 displacement (x \u2212 x\u2080). Hence, Eq. 1 is our match.',
        styles['NormalIndent']
    ))
    elements.append(Paragraph('v = v\u2080 + at', styles['Equation']))

    elements.append(Paragraph('Isolate a:', styles['NormalIndent']))
    add_aligned_table([
        ['v', '=', 'v\u2080 + at', ''],
        ['v \u2212 v\u2080', '=', 'at', ''],
        ['(v \u2212 v\u2080) / t', '=', 'a', ''],
        ['a', '=', '(v \u2212 v\u2080) / t', ''],
    ])

    elements.append(Paragraph('Substitute values:', styles['NormalIndent']))
    add_aligned_table([
        ['a', '=', '(73.14 \u2212 0) / 0.0300', ''],
        ['a', '=', '2.44 \u00d7 10\u00b3 m/s\u00b2', ''],
    ])

    elements.append(Paragraph(
        'This is roughly 249 times the acceleration due to gravity (g = 9.8 m/s\u00b2) \u2014 that\u2019s how violent a tennis serve impact really is!',
        styles['Commentary']
    ))

    # Solution (b)
    elements.append(Paragraph('(b) Finding distance traveled', styles['SubHeading']))
    elements.append(Paragraph(
        'Which equation?  We now know v\u2080, v, t, and a from part (a). We could use Eq. 2, but since a was a rounded answer, reusing it could introduce rounding error. It is safer to use the equation that doesn\u2019t need acceleration at all \u2014 Eq. 4, which is missing a.',
        styles['NormalIndent']
    ))
    elements.append(Paragraph('(x \u2212 x\u2080) = \u00bd(v\u2080 + v)t', styles['Equation']))

    elements.append(Paragraph('Derivation by transposition \u2014 isolate (x \u2212 x\u2080), the distance traveled:', styles['NormalIndent']))
    add_aligned_table([
        ['(x \u2212 x\u2080)', '=', '\u00bd(v\u2080 + v)t', ''],
        ['(x \u2212 x\u2080)', '=', '\u00bd(v\u2080 + v)t', 'transpose x\u2080: added on the right, becomes subtracted on the left'],
    ])

    elements.append(Paragraph('Substitute values:', styles['NormalIndent']))
    add_aligned_table([
        ['(x \u2212 x\u2080)', '=', '\u00bd(0 + 73.14)(0.0300)', ''],
        ['(x \u2212 x\u2080)', '=', '1.10 m', ''],
    ])

    # =========================================================================
    # PROBLEM 2
    # =========================================================================
    elements.append(Paragraph('Problem 2', styles['ProblemHeading']))
    elements.append(Paragraph(
        'The fastest measured pitched baseball left the pitcher\u2019s hand at a speed of 45.0 m/s. '
        'If the pitcher was in contact with the ball over a distance of 1.50 m and produced constant acceleration, '
        '(a) what acceleration did he give the ball, and (b) how much time did it take him to pitch it?',
        styles['ProblemText']
    ))

    # Given
    elements.append(Paragraph('Given', styles['SectionLabel']))
    add_given_table([
        ['v\u2080', '0 m/s', 'Ball starts at rest in the pitcher\u2019s hand before the throwing motion begins'],
        ['v', '45.0 m/s', 'Speed as the ball leaves the hand'],
        ['(x \u2212 x\u2080)', '1.50 m', 'Distance over which the hand accelerates the ball'],
    ])

    # Required
    elements.append(Paragraph('Required', styles['SectionLabel']))
    elements.append(Paragraph('(a)  a = ?', styles['NormalIndent']))
    elements.append(Paragraph('(b)  t = ?', styles['NormalIndent']))

    # Solution (a)
    elements.append(Paragraph('Solution', styles['SectionLabel']))
    elements.append(Paragraph('(a) Finding acceleration', styles['SubHeading']))
    elements.append(Paragraph(
        'Which equation?  We are given v\u2080, v, and (x \u2212 x\u2080). We are not given, and do not yet need, time t. Eq. 3 is the one missing t, so that\u2019s our match.',
        styles['NormalIndent']
    ))
    elements.append(Paragraph('v\u00b2 = v\u2080\u00b2 + 2a(x \u2212 x\u2080)', styles['Equation']))

    elements.append(Paragraph('Derivation by transposition \u2014 isolate a:', styles['NormalIndent']))
    add_aligned_table([
        ['v\u00b2', '=', 'v\u2080\u00b2 + 2a(x \u2212 x\u2080)', ''],
        ['v\u00b2 \u2212 v\u2080\u00b2', '=', '2a(x \u2212 x\u2080)', 'transpose v\u2080\u00b2: added on the right, becomes subtracted on the left'],
        ['(v\u00b2 \u2212 v\u2080\u00b2) / 2(x \u2212 x\u2080)', '=', 'a', 'transpose 2(x \u2212 x\u2080): multiplying a, becomes a divisor'],
        ['a', '=', '(v\u00b2 \u2212 v\u2080\u00b2) / 2(x \u2212 x\u2080)', ''],
    ])

    elements.append(Paragraph('Substitute values:', styles['NormalIndent']))
    add_aligned_table([
        ['a', '=', '(45.0\u00b2 \u2212 0\u00b2) / 2(1.50)', 'm\u00b2/s\u00b2 \u00f7 m'],
        ['a', '=', '2025 / 3.00', ''],
        ['a', '=', '675 m/s\u00b2', ''],
    ])

    # Solution (b)
    elements.append(Paragraph('(b) Finding time', styles['SubHeading']))
    elements.append(Paragraph(
        'Which equation?  We now know v\u2080, v, (x \u2212 x\u2080), and a (rounded). To avoid propagating rounding error from part (a), use the equation that doesn\u2019t need a \u2014 Eq. 4, missing acceleration.',
        styles['NormalIndent']
    ))
    elements.append(Paragraph('(x \u2212 x\u2080) = \u00bd(v\u2080 + v)t', styles['Equation']))

    elements.append(Paragraph('Derivation by transposition \u2014 isolate t:', styles['NormalIndent']))
    add_aligned_table([
        ['(x \u2212 x\u2080)', '=', '\u00bd(v\u2080 + v)t', 'transpose x\u2080 (as in Problem 1)'],
        ['2(x \u2212 x\u2080)', '=', '(v\u2080 + v)t', 'transpose \u00bd: multiply both sides by 2 to clear the fraction'],
        ['2(x \u2212 x\u2080) / (v\u2080 + v)', '=', 't', 'transpose (v\u2080 + v): multiplying t, becomes a divisor'],
        ['t', '=', '2(x \u2212 x\u2080) / (v\u2080 + v)', ''],
    ])

    elements.append(Paragraph('Substitute values:', styles['NormalIndent']))
    add_aligned_table([
        ['t', '=', '2(1.50) / (0 + 45.0)', 'm \u00f7 (m/s)'],
        ['t', '=', '3.00 / 45.0', ''],
        ['t', '=', '0.0667 s  (66.7 ms)', ''],
    ])

    # =========================================================================
    # PROBLEM 3
    # =========================================================================
    elements.append(PageBreak())
    elements.append(Paragraph('Problem 3', styles['ProblemHeading']))
    elements.append(Paragraph(
        'The human body can survive an acceleration trauma incident if the magnitude of the acceleration '
        'is less than 250 m/s\u00b2. If you are in an automobile accident with an initial speed of 105 km/h '
        'and are stopped by an airbag, over what minimum distance must the airbag stop you to survive?',
        styles['ProblemText']
    ))

    # Given
    elements.append(Paragraph('Given', styles['SectionLabel']))
    add_given_table([
        ['v\u2080', '105 km/h', 'Must convert to m/s (SI unit) before using the equations'],
        ['v', '0 m/s', 'The car (and you) come to a complete stop'],
        ['a', '\u2212250 m/s\u00b2', 'Use the maximum allowed magnitude of deceleration \u2014 gives the minimum stopping distance. Negative sign shows deceleration.'],
    ])

    elements.append(Paragraph('Unit conversion:', styles['NormalIndent']))
    elements.append(Paragraph('v\u2080 = 105 km/h \u00d7 (1000 m / 1 km) \u00d7 (1 h / 3600 s) = 29.17 m/s', styles['NormalIndent']))

    # Required
    elements.append(Paragraph('Required', styles['SectionLabel']))
    elements.append(Paragraph('(x \u2212 x\u2080) = ?   (minimum stopping distance)', styles['NormalIndent']))

    # Solution
    elements.append(Paragraph('Solution', styles['SectionLabel']))
    elements.append(Paragraph(
        'Which equation?  We are given v\u2080, v, and a. We are not given, and don\u2019t need, time t. Eq. 3 is missing t, so that\u2019s our match.',
        styles['NormalIndent']
    ))
    elements.append(Paragraph('v\u00b2 = v\u2080\u00b2 + 2a(x \u2212 x\u2080)', styles['Equation']))

    elements.append(Paragraph('Derivation by transposition \u2014 isolate (x \u2212 x\u2080):', styles['NormalIndent']))
    add_aligned_table([
        ['v\u00b2', '=', 'v\u2080\u00b2 + 2a(x \u2212 x\u2080)', ''],
        ['v\u00b2 \u2212 v\u2080\u00b2', '=', '2a(x \u2212 x\u2080)', 'transpose v\u2080\u00b2: added on the right, becomes subtracted on the left'],
        ['(v\u00b2 \u2212 v\u2080\u00b2) / 2a', '=', '(x \u2212 x\u2080)', 'transpose 2a: multiplying, becomes a divisor'],
        ['(x \u2212 x\u2080)', '=', '(v\u00b2 \u2212 v\u2080\u00b2) / 2a', ''],
    ])

    elements.append(Paragraph('Substitute values:', styles['NormalIndent']))
    add_aligned_table([
        ['(x \u2212 x\u2080)', '=', '(0\u00b2 \u2212 29.17\u00b2) / 2(\u2212250)', 'm\u00b2/s\u00b2 \u00f7 m/s\u00b2'],
        ['(x \u2212 x\u2080)', '=', '(\u2212850.9) / (\u2212500)', ''],
        ['(x \u2212 x\u2080)', '=', '1.70 m', ''],
    ])

    elements.append(Paragraph(
        'The negative signs on top and bottom cancel \u2014 that makes sense, since a distance must be positive! The airbag (plus crumple zone) must stop you within at least 1.70 m, or the deceleration will exceed the survivable limit of 250 m/s\u00b2.',
        styles['Commentary']
    ))

    # =========================================================================
    # PROBLEM 4
    # =========================================================================
    elements.append(Paragraph('Problem 4', styles['ProblemHeading']))
    elements.append(Paragraph(
        'A small block has constant acceleration as it slides down a frictionless incline, released from rest. '
        'Its speed after traveling 6.80 m is 3.80 m/s. What is its speed after traveling only 3.40 m (halfway down)?',
        styles['ProblemText']
    ))
    elements.append(Paragraph(
        'Strategy.  This problem needs two stages. First, use the full trip (0 to 6.80 m) to find the constant acceleration a. Then apply that same a to the shorter trip (0 to 3.40 m) to find the speed at that point.',
        styles['Commentary']
    ))

    # Given
    elements.append(Paragraph('Given', styles['SectionLabel']))
    add_given_table([
        ['v\u2080', '0 m/s', 'Released from rest at the top'],
        ['(x \u2212 x\u2080)\u2081', '6.80 m', 'Full distance to the bottom'],
        ['v\u2081', '3.80 m/s', 'Speed at the bottom (end of the full distance)'],
        ['(x \u2212 x\u2080)\u2082', '3.40 m', 'The shorter distance we care about (exactly half of 6.80 m)'],
    ])

    # Required
    elements.append(Paragraph('Required', styles['SectionLabel']))
    elements.append(Paragraph('v\u2082 = ?   \u2014 the speed when the block has traveled 3.40 m', styles['NormalIndent']))

    # Solution Stage 1
    elements.append(Paragraph('Solution', styles['SectionLabel']))
    elements.append(Paragraph('Stage 1 \u2014 find the acceleration using the full 6.80 m trip', styles['SubHeading']))
    elements.append(Paragraph(
        'Which equation?  We know v\u2080, v\u2081, and (x \u2212 x\u2080)\u2081. We don\u2019t have or need t. Eq. 3 is missing t.',
        styles['NormalIndent']
    ))
    elements.append(Paragraph('v\u00b2 = v\u2080\u00b2 + 2a(x \u2212 x\u2080)', styles['Equation']))

    elements.append(Paragraph('Derivation by transposition \u2014 isolate a:', styles['NormalIndent']))
    add_aligned_table([
        ['v\u2081\u00b2', '=', 'v\u2080\u00b2 + 2a(x \u2212 x\u2080)\u2081', ''],
        ['v\u2081\u00b2 \u2212 v\u2080\u00b2', '=', '2a(x \u2212 x\u2080)\u2081', 'transpose v\u2080\u00b2'],
        ['(v\u2081\u00b2 \u2212 v\u2080\u00b2) / 2(x \u2212 x\u2080)\u2081', '=', 'a', 'transpose 2(x \u2212 x\u2080)\u2081: multiplying, becomes a divisor'],
        ['a', '=', '(v\u2081\u00b2 \u2212 v\u2080\u00b2) / 2(x \u2212 x\u2080)\u2081', ''],
    ])

    elements.append(Paragraph('Substitute values:', styles['NormalIndent']))
    add_aligned_table([
        ['a', '=', '(3.80\u00b2 \u2212 0\u00b2) / 2(6.80)', 'm\u00b2/s\u00b2 \u00f7 m'],
        ['a', '=', '14.44 / 13.60', ''],
        ['a', '=', '1.06 m/s\u00b2  (unrounded: 1.0618 m/s\u00b2)', ''],
    ])

    # Solution Stage 2
    elements.append(Paragraph('Stage 2 \u2014 use this acceleration to find the speed at 3.40 m', styles['SubHeading']))
    elements.append(Paragraph(
        'Same equation, same reasoning.  We still don\u2019t know or need t, so Eq. 3 applies again \u2014 but now we solve for v\u2082 instead of a.',
        styles['NormalIndent']
    ))
    elements.append(Paragraph('v\u2082\u00b2 = v\u2080\u00b2 + 2a(x \u2212 x\u2080)\u2082', styles['Equation']))

    elements.append(Paragraph('This is already solved for v\u2082\u00b2 \u2014 one more transposition step (the square root) isolates v\u2082:', styles['NormalIndent']))
    add_aligned_table([
        ['v\u2082', '=', '\u221a[v\u2080\u00b2 + 2a(x \u2212 x\u2080)\u2082]', 'apply \u221a to both sides'],
    ])

    elements.append(Paragraph('Substitute values (use the un-rounded a = 1.0618 m/s\u00b2 to avoid rounding error):', styles['NormalIndent']))
    add_aligned_table([
        ['v\u2082', '=', '\u221a[0\u00b2 + 2(1.0618)(3.40)]', ''],
        ['v\u2082', '=', '\u221a[7.220]', ''],
        ['v\u2082', '=', '2.69 m/s', ''],
    ])

    elements.append(Paragraph(
        'Since v\u2080 = 0, speed is proportional to the square root of distance traveled. Half the distance does not give half the speed \u2014 it gives speed divided by \u221a2 \u2248 1.414. Check: 3.80 / 1.414 = 2.69 m/s \u2713. Kinematics with acceleration is not "linear" in the intuitive sense!',
        styles['Commentary']
    ))

    # =========================================================================
    # PROBLEM 5
    # =========================================================================
    elements.append(Paragraph('Problem 5', styles['ProblemHeading']))
    elements.append(Paragraph(
        'A Lamborghini Aventador S can go from 0 to 60 mph in 2.7 s. Assume constant acceleration. '
        '(a) What is the magnitude of the acceleration? (b) How far has the car traveled when it reaches 60 mph?',
        styles['ProblemText']
    ))

    # Given
    elements.append(Paragraph('Given', styles['SectionLabel']))
    add_given_table([
        ['v\u2080', '0 mph = 0 m/s', 'Starts from rest'],
        ['v', '60 mph', 'Must convert to m/s'],
        ['t', '2.7 s', 'Time to reach 60 mph'],
    ])

    elements.append(Paragraph('Unit conversion:', styles['NormalIndent']))
    elements.append(Paragraph('v = 60 mph \u00d7 (1609 m / 1 mi) \u00d7 (1 h / 3600 s) = 26.8 m/s', styles['NormalIndent']))

    # Required
    elements.append(Paragraph('Required', styles['SectionLabel']))
    elements.append(Paragraph('(a)  a = ?', styles['NormalIndent']))
    elements.append(Paragraph('(b)  (x \u2212 x\u2080) = ?', styles['NormalIndent']))

    # Solution (a)
    elements.append(Paragraph('Solution', styles['SectionLabel']))
    elements.append(Paragraph('(a) Finding acceleration', styles['SubHeading']))
    elements.append(Paragraph(
        'Which equation?  We are given v\u2080, v, and t. We are not given, and don\u2019t need, displacement. Eq. 1 is missing (x \u2212 x\u2080), so that\u2019s our match.',
        styles['NormalIndent']
    ))
    elements.append(Paragraph('v = v\u2080 + at', styles['Equation']))

    elements.append(Paragraph('Derivation by transposition \u2014 isolate a (same steps as Problem 1):', styles['NormalIndent']))
    add_aligned_table([
        ['v', '=', 'v\u2080 + at', ''],
        ['v \u2212 v\u2080', '=', 'at', 'transpose v\u2080'],
        ['(v \u2212 v\u2080) / t', '=', 'a', 'transpose t'],
        ['a', '=', '(v \u2212 v\u2080) / t', ''],
    ])

    elements.append(Paragraph('Substitute values:', styles['NormalIndent']))
    add_aligned_table([
        ['a', '=', '(26.8 \u2212 0) / 2.7', 'm/s \u00f7 s'],
        ['a', '=', '9.93 m/s\u00b2', ''],
    ])

    elements.append(Paragraph(
        'That\u2019s about 1.01 g \u2014 you\u2019d feel about your own body weight pushing you back into the seat!',
        styles['Commentary']
    ))

    # Solution (b)
    elements.append(Paragraph('(b) Finding distance traveled', styles['SubHeading']))
    elements.append(Paragraph(
        'Which equation?  We know v\u2080, v, t, and a (rounded). To avoid rounding error, use the equation missing a \u2014 Eq. 4.',
        styles['NormalIndent']
    ))
    elements.append(Paragraph('(x \u2212 x\u2080) = \u00bd(v\u2080 + v)t', styles['Equation']))

    elements.append(Paragraph('Derivation by transposition \u2014 isolate (x \u2212 x\u2080) (same steps as Problem 1):', styles['NormalIndent']))
    add_aligned_table([
        ['(x \u2212 x\u2080)', '=', '\u00bd(v\u2080 + v)t', ''],
    ])

    elements.append(Paragraph('Substitute values:', styles['NormalIndent']))
    add_aligned_table([
        ['(x \u2212 x\u2080)', '=', '\u00bd(0 + 26.8)(2.7)', ''],
        ['(x \u2212 x\u2080)', '=', '36.2 m', ''],
    ])

    elements.append(Paragraph(
        'For comparison, that\u2019s roughly the length of two and a half basketball courts, covered in under 3 seconds!',
        styles['Commentary']
    ))

    # =========================================================================
    # SUMMARY TABLE
    # =========================================================================
    elements.append(Spacer(1, 24))
    elements.append(Paragraph('Summary of Final Answers', styles['ProblemHeading']))

    summary_data = [
        ['Problem', 'Part (a)', 'Part (b)'],
        ['1. Tennis serve', 'a = 2.44 \u00d7 10\u00b3 m/s\u00b2', '(x \u2212 x\u2080) = 1.10 m'],
        ['2. Baseball pitch', 'a = 675 m/s\u00b2', 't = 0.0667 s'],
        ['3. Airbag', '(x \u2212 x\u2080) = 1.70 m (minimum)', '\u2014'],
        ['4. Incline block', 'v\u2082 = 2.69 m/s at 3.40 m', '\u2014'],
        ['5. Lamborghini', 'a = 9.93 m/s\u00b2', '(x \u2212 x\u2080) = 36.2 m'],
    ]

    summary_table = Table(summary_data, colWidths=[2.0*inch, 2.5*inch, 2.0*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.9, 0.9, 0.9)),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(summary_table)

    # Footer
    elements.append(Spacer(1, 36))
    elements.append(Paragraph(
        '<para alignment="center"><font size="9">Problem Set 3 \u2014 Uniformly Accelerated Motion (Horizontal)</font></para>',
        styles['Normal']
    ))

    doc.build(elements)
    print('PDF saved to: /projects/sandbox/physics/ProblemSet3-SolutionKey.pdf')


if __name__ == '__main__':
    build_pdf()
