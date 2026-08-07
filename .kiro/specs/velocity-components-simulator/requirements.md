# Requirements Document

## Introduction

The Velocity Components Simulator is a self-contained, browser-based educational
physics simulation focused on **uniform circular motion**. It is intended for use
by a physics teacher / instructional designer to help learners explore and
visualize the interrelated quantities that govern an object moving in a circle at
constant speed.

The simulation lets learners manipulate the independent quantities — radius (r),
mass (m), and one temporal-motion driver (period T, tangential speed v, or angular
speed ω) — and observe, in real time, how the remaining coupled and derived
quantities change. It visualizes the object traveling around a circular path, the
**tangential velocity vector** (showing that velocity is always tangent to the
path, in the direction of motion), and the **centripetal acceleration/force vector**
(showing that acceleration and net force always point toward the center). Live
numeric readouts and the governing equations are displayed alongside the animation.

The governing formula set is:

- Period–speed relationship: `T = 2πr / v`
- Tangential speed: `v = 2πr / T`
- Angular speed: `ω = 2π / T`, and `v = rω`
- Centripetal acceleration: `a_c = v² / r` (equivalently `a_c = rω²`)
- Centripetal force: `F_net = m·a_c = m·v² / r`

A single **unified** interactive simulation is preferred and is pedagogically
feasible, because all of the listed quantities are mathematically coupled and are
best understood together on one moving diagram. This spec therefore defines one
unified simulation rather than a series of separate simulations.

The deliverable is a static web application requiring **no build step and no
server**: a root `index.html` landing page and a self-contained simulation under a
`sims/` folder, all runnable by opening `index.html` directly from the file system
(`file://`). The target delivery branch is `velocity-components-simulator`.

## Glossary

- **Simulator**: The single unified uniform-circular-motion interactive simulation,
  implemented as a self-contained web page under the `sims/` folder.
- **Landing_Page**: The `index.html` file at the repository root that presents the
  project and links to (or embeds) the Simulator.
- **Sims_Folder**: The `sims/` directory at the repository root that contains the
  self-contained Simulator assets (HTML, CSS, JavaScript).
- **Control_Panel**: The set of user-facing input widgets (sliders and/or numeric
  fields) for radius, mass, and the selected motion driver.
- **Motion_Driver**: The single independent temporal-motion input selected by the
  user — one of period (T), tangential speed (v), or angular speed (ω) — that,
  together with radius, determines the object's motion.
- **Animation_View**: The graphical area (e.g., an HTML canvas) that renders the
  circular path and the animated object.
- **Velocity_Vector**: The rendered arrow representing the object's tangential
  velocity, drawn from the object's position, tangent to the circular path, in the
  direction of motion.
- **Force_Vector**: The rendered arrow representing centripetal acceleration and/or
  net centripetal force, drawn from the object's position toward the center of the
  circle.
- **Readout_Panel**: The area displaying live numeric values of r, m, T, v, ω,
  a_c, and F_net with their units.
- **Equation_Panel**: The area displaying the governing equations of uniform
  circular motion.
- **Derived_Quantity**: Any quantity computed from the independent inputs
  (r, m, Motion_Driver): the two non-driver temporal quantities among {T, v, ω},
  plus a_c and F_net.

## Requirements

### Requirement 1: Zero-Build Root Landing Page

**User Story:** As a physics teacher, I want to open a single file in a browser with no setup, so that I can launch the simulation on any computer without installing tools or running a server.

#### Acceptance Criteria

1. THE Landing_Page SHALL exist as a file named `index.html` at the repository root.
2. WHEN a user opens the Landing_Page directly from the file system using a `file://` URL, THE Landing_Page SHALL render its complete content within 2 seconds without requiring any build step, package installation, or running server.
3. THE Landing_Page SHALL display, within the initial viewport, a link or control with a text label identifying that it launches the Simulator.
4. WHEN a user activates the link or control on the Landing_Page, THE Landing_Page SHALL navigate the browser to the Simulator page such that the Simulator's Animation_View becomes visible within 2 seconds.
5. THE Landing_Page SHALL reference the Simulator using a relative path within the repository so that the link resolves correctly when opened via a `file://` URL.
6. IF the referenced Simulator page cannot be loaded when the link or control is activated, THEN THE Landing_Page SHALL display a message indicating that the Simulator could not be opened and SHALL remain on the Landing_Page.

### Requirement 2: Self-Contained Simulation Assets

**User Story:** As an instructional designer, I want the simulation to be self-contained in a `sims/` folder, so that I can copy or host it without external dependencies.

#### Acceptance Criteria

1. THE Sims_Folder SHALL exist as a directory named `sims` at the repository root.
2. THE Simulator SHALL store all of its HTML, CSS, and JavaScript assets within the Sims_Folder, with no Simulator asset stored outside the Sims_Folder.
3. WHEN the Simulator loads, THE Simulator SHALL operate using only files contained within the repository, and THE Simulator SHALL NOT issue any network request to a remote server or external content delivery network.
4. WHEN the Simulator is opened via a `file://` URL, THE Simulator SHALL render its user interface without requiring a build step, package installation, or running server.
5. WHEN the Simulator is opened via a `file://` URL, THE Simulator SHALL run its animation without requiring a build step, package installation, or running server.
6. THE Simulator SHALL reference all of its own assets using relative paths so that each asset resolves correctly when the Simulator is opened via a `file://` URL.
7. IF a referenced Simulator asset fails to load, THEN THE Simulator SHALL display a visible message indicating that a required asset could not be loaded.

### Requirement 3: Independent Input Controls

**User Story:** As a learner, I want to change the radius, mass, and one motion
quantity, so that I can explore how the circular motion changes.

#### Acceptance Criteria

1. THE Control_Panel SHALL provide an input control for radius (r) measured in
   meters.
2. THE Control_Panel SHALL provide an input control for mass (m) measured in
   kilograms.
3. THE Control_Panel SHALL provide a control that allows the user to select which
   Motion_Driver among period (T), tangential speed (v), and angular speed (ω) is
   the independent input.
4. THE Control_Panel SHALL provide an input control for the currently selected
   Motion_Driver, using seconds for period (T), meters per second for tangential
   speed (v), and radians per second for angular speed (ω).
5. THE Control_Panel SHALL constrain radius input to the range 0.1 meters to 10
   meters inclusive.
6. THE Control_Panel SHALL constrain mass input to the range 0.1 kilograms to 100
   kilograms inclusive.
7. THE Control_Panel SHALL constrain period input to the range 0.5 seconds to 60
   seconds inclusive.
8. WHEN the user changes any Control_Panel input, THE Simulator SHALL update the
   Derived_Quantity values within 100 milliseconds.
9. THE Control_Panel SHALL constrain tangential speed (v) input to the range 0.1 meters per second to 100 meters per second inclusive.
10. THE Control_Panel SHALL constrain angular speed (ω) input to the range 0.1 radians per second to 12 radians per second inclusive.
11. WHEN the Simulator loads, THE Control_Panel SHALL have period (T) selected as the default Motion_Driver.

### Requirement 4: Consistent Coupled-Quantity Computation

**User Story:** As a learner, I want the period, tangential speed, and angular speed to stay mathematically consistent when I change one of them, so that I understand they describe the same motion.

#### Acceptance Criteria

1. WHEN the user sets the radius (r) and the selected Motion_Driver, THE Simulator SHALL compute the two non-driver quantities among period (T), tangential speed (v), and angular speed (ω) from the governing equations within 100 milliseconds.
2. THE Simulator SHALL compute tangential speed such that the relationship `v = 2πr / T` holds within a relative tolerance of 0.1 percent.
3. THE Simulator SHALL compute angular speed such that the relationship `ω = 2π / T` holds within a relative tolerance of 0.1 percent.
4. THE Simulator SHALL maintain the relationship `v = rω` within a relative tolerance of 0.1 percent across all valid input combinations.
5. THE Simulator SHALL retain the user-entered value of the currently selected Motion_Driver exactly as entered and compute the two non-driver quantities from that value together with the radius (r).
6. WHEN the user changes the selected Motion_Driver from one quantity to another without changing the radius and without entering a new value for any of period (T), tangential speed (v), or angular speed (ω), THE Simulator SHALL preserve the previously computed period, tangential speed, and angular speed within a relative tolerance of 0.1 percent.
7. WHEN the user changes the selected Motion_Driver from one quantity to another, THE Simulator SHALL populate the input control for the newly selected Motion_Driver with the preserved value of that quantity within 100 milliseconds.

### Requirement 5: Derived Acceleration and Force Computation

**User Story:** As a learner, I want to see the centripetal acceleration and net force values, so that I understand how radius, speed, and mass determine them.

#### Acceptance Criteria

1. WHEN the user sets the radius (r) and the selected Motion_Driver, THE Simulator SHALL compute centripetal acceleration (a_c) such that the relationship `a_c = v² / r` holds within a relative tolerance of 0.1 percent across all valid input combinations defined in Requirement 3.
2. WHEN the user sets the radius (r) and the selected Motion_Driver, THE Simulator SHALL compute centripetal acceleration (a_c) such that the relationship `a_c = rω²` holds within a relative tolerance of 0.1 percent across all valid input combinations defined in Requirement 3.
3. WHEN the user sets the mass (m), radius (r), and the selected Motion_Driver, THE Simulator SHALL compute net centripetal force (F_net) such that the relationship `F_net = m·a_c` holds within a relative tolerance of 0.1 percent across all valid input combinations defined in Requirement 3.
4. WHEN the user sets the mass (m), radius (r), and the selected Motion_Driver, THE Simulator SHALL compute net centripetal force (F_net) such that the relationship `F_net = m·v² / r` holds within a relative tolerance of 0.1 percent across all valid input combinations defined in Requirement 3.
5. THE Simulator SHALL compute the centripetal acceleration (a_c) value from both `a_c = v² / r` and `a_c = rω²` such that the two computed values agree with each other within a relative tolerance of 0.1 percent.
6. THE Simulator SHALL compute centripetal acceleration (a_c) and net centripetal force (F_net) as non-negative magnitudes greater than or equal to zero.
7. WHEN the user changes any Control_Panel input, THE Simulator SHALL update the computed centripetal acceleration (a_c) and net centripetal force (F_net) values within 100 milliseconds.

### Requirement 6: Live Numeric Readouts

**User Story:** As a learner, I want to read the current numeric values with units, so that I can connect the visual motion to concrete numbers.

#### Acceptance Criteria

1. THE Readout_Panel SHALL display the current values of radius (r), mass (m), period (T), tangential speed (v), angular speed (ω), centripetal acceleration (a_c), and net centripetal force (F_net).
2. THE Readout_Panel SHALL display each value with its unit: meters for radius, kilograms for mass, seconds for period, meters per second for tangential speed, radians per second for angular speed, meters per second squared for centripetal acceleration, and newtons for net centripetal force.
3. THE Readout_Panel SHALL display each numeric value rounded to at most 3 decimal places.
4. IF a nonzero value has a magnitude less than 0.001, THEN THE Readout_Panel SHALL display that value in a numeric format that preserves at least one significant figure rather than displaying it as 0.000.
5. WHEN the Simulator loads, THE Readout_Panel SHALL display the values of r, m, T, v, ω, a_c, and F_net computed from the initial default inputs, before any user interaction.
6. WHEN the user changes any Control_Panel input, THE Readout_Panel SHALL update all seven displayed values (r, m, T, v, ω, a_c, F_net) to reflect the newly computed values within 100 milliseconds.
7. IF the user enters a Control_Panel input value that the Simulator rejects or retains as invalid, THEN THE Readout_Panel SHALL continue to display the values corresponding to the last valid inputs.

### Requirement 7: Animated Circular Motion

**User Story:** As a learner, I want to watch the object move around the circle at the correct rate, so that I can see uniform circular motion in action.

#### Acceptance Criteria

1. THE Animation_View SHALL render a circular path whose displayed radius scales monotonically with the current radius (r) value, such that a larger r produces a larger displayed radius, while the entire circular path remains within the visible bounds of the Animation_View.
2. THE Animation_View SHALL render an object positioned on the circular path.
3. WHILE the animation is playing, THE Simulator SHALL move the object around the circular path at a rate such that one complete revolution takes the current period (T) in real time within a relative tolerance of 5 percent.
4. THE Simulator SHALL provide a play control, a pause control, and a reset control for the animation.
5. WHEN the user activates the play control WHILE the animation is paused, THE Simulator SHALL resume motion of the object from its current position along the circular path.
6. WHEN the user activates the pause control WHILE the animation is playing, THE Simulator SHALL halt the object at its current position on the circular path and retain that position until the user next activates the play or reset control.
7. WHEN the user activates the reset control, THE Simulator SHALL return the object to its fixed initial starting position on the circular path (the same reference point occupied at initial load) and place the animation in the paused state.
8. WHILE the animation is playing, THE Simulator SHALL sustain a rendering rate of at least 30 frames per second averaged over any 1-second interval.

### Requirement 8: Tangential Velocity Vector Visualization

**User Story:** As a learner, I want to see the velocity arrow, so that I understand velocity is always tangent to the path in the direction of motion.

#### Acceptance Criteria

1. THE Animation_View SHALL render the Velocity_Vector as an arrow whose tail originates at the object's current position on the circular path and whose head indicates the arrow's pointing direction.
2. THE Simulator SHALL orient the Velocity_Vector tangent to the circular path such that the angle between the Velocity_Vector and the radius line from the center to the object is 90 degrees within a tolerance of 1 degree.
3. THE Simulator SHALL orient the Velocity_Vector in the direction of the object's travel along the path, such that the angle between the Velocity_Vector and the object's instantaneous direction of motion is 0 degrees within a tolerance of 1 degree.
4. WHILE the animation is playing, THE Simulator SHALL update the Velocity_Vector orientation on each rendered frame so that the angle between the Velocity_Vector and the radius line from the center to the object remains 90 degrees within a tolerance of 1 degree and the Velocity_Vector continues to point in the direction of the object's travel within a tolerance of 1 degree.
5. THE Simulator SHALL render the Velocity_Vector visually distinct from the Force_Vector through a different color and a text label identifying it as the velocity vector.
6. THE Simulator SHALL scale the displayed length of the Velocity_Vector in proportion to the current tangential speed (v) magnitude, such that a larger tangential speed produces a longer rendered Velocity_Vector.

### Requirement 9: Centripetal Acceleration/Force Vector Visualization

**User Story:** As a learner, I want to see the acceleration/force arrow, so that I understand it always points toward the center of the circle.

#### Acceptance Criteria

1. THE Animation_View SHALL render the Force_Vector as an arrow whose tail originates at the object's current position on the circular path.
2. THE Simulator SHALL orient the Force_Vector to point from the object's position toward the center of the circular path such that the angle between the Force_Vector and the radius line from the object to the center is 0 degrees within a tolerance of 1 degree.
3. WHILE the animation is playing, THE Simulator SHALL update the Force_Vector orientation on every rendered frame as the object moves so that the Force_Vector continues to point toward the center within a tolerance of 1 degree.
4. THE Simulator SHALL render the Force_Vector with a fill color different from the Velocity_Vector color and with a visible text label identifying it as the acceleration/force vector, so that it is distinguishable from the Velocity_Vector.
5. WHERE the user enables force display, THE Simulator SHALL set the displayed length of the Force_Vector to be linearly proportional to the current net centripetal force (F_net) magnitude using a single constant scale factor, such that the ratio of displayed length to F_net magnitude remains constant within a relative tolerance of 1 percent across all valid input combinations.
6. WHERE the user enables force display, THE Simulator SHALL constrain the displayed length of the Force_Vector to a minimum of 5 percent and a maximum of 100 percent of the rendered circular path radius, clamping any computed length outside this range to the nearest bound.
7. WHERE the user disables force display, THE Simulator SHALL not render the Force_Vector in the Animation_View.

### Requirement 10: Governing Equations Display

**User Story:** As a learner, I want to see the equations, so that I can connect the visuals and numbers to the underlying physics.

#### Acceptance Criteria

1. WHILE the Simulator is displayed, THE Equation_Panel SHALL display the tangential speed equation `v = 2πr / T`.
2. WHILE the Simulator is displayed, THE Equation_Panel SHALL display the angular speed equations `ω = 2π / T` and `v = rω`.
3. WHILE the Simulator is displayed, THE Equation_Panel SHALL display the centripetal acceleration equations `a_c = v² / r` and `a_c = rω²`.
4. WHILE the Simulator is displayed, THE Equation_Panel SHALL display the centripetal force equations `F_net = m·a_c` and `F_net = m·v² / r`.
5. THE Equation_Panel SHALL render each equation with its mathematical symbols — Greek letters (π, ω), superscript exponent (²), subscript identifiers (a_c, F_net), and the multiplication operator (·) — as legible notation rather than as unformatted or placeholder characters.
6. THE Equation_Panel SHALL display a legend that defines each variable symbol (r, m, T, v, ω, a_c, F_net) with its physical quantity name and unit.

### Requirement 11: Input Validation and Error Handling

**User Story:** As a learner, I want the simulation to respond gracefully to invalid input, so that the visualization does not break when I enter an out-of-range value.

#### Acceptance Criteria

1. IF the user enters a radius value less than or equal to zero, THEN THE Simulator SHALL reject the value, retain the last valid radius, and re-display the last valid radius in the radius input within 100 milliseconds.
2. IF the user enters a radius value less than or equal to zero, THEN THE Simulator SHALL display a visible message indicating the entered radius value was rejected.
3. IF the user enters a period value less than or equal to zero, THEN THE Simulator SHALL reject the value, retain the last valid period, re-display the last valid period in the period input within 100 milliseconds, and display a visible message indicating the entered period value was rejected.
4. IF the user enters a mass value less than or equal to zero, THEN THE Simulator SHALL reject the value, retain the last valid mass, re-display the last valid mass in the mass input within 100 milliseconds, and display a visible message indicating the entered mass value was rejected.
5. IF the user enters a numeric value that is greater than zero but outside the allowed range defined for a Control_Panel input, THEN THE Simulator SHALL clamp the value to the nearest allowed bound and display the clamped value in that input within 100 milliseconds.
6. IF a Control_Panel input is non-numeric or empty, THEN THE Simulator SHALL retain the last valid value for that input, re-display the last valid value within 100 milliseconds, and display a visible message indicating the input was ignored.
7. WHEN the user enters a valid value for a Control_Panel input after a rejected, clamped, or ignored input, THE Simulator SHALL remove the associated rejection or ignored-input message within 100 milliseconds.
