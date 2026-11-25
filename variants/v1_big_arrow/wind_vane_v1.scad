// =====================================================================
//  Replacement wind-direction vane for VEVOR YT60231 weather station
//  Parametric OpenSCAD model.  Units: mm.
//
//  Coordinate system (= print orientation = installed orientation):
//    Z  = shaft axis (up).  Bottom face (z=0) sits flat on the print bed.
//    +X = pointer / arrow head (points INTO the wind).
//    -X = tail boom + tail fin.
//  The shaft enters from the bottom; the bore is blind (capped on top)
//  so rain can't run down onto the shaft/bearing.
//  Prints with NO supports: hub upright, arms flat on the bed, fin is a
//  vertical wall standing on the tail boom, set-screw hole is a teardrop.
// =====================================================================

/* [Shaft & bore] */
shaft_d        = 2.8;   // measured shaft diameter
flat_depth     = 0.5;   // depth of the D-flat. across-flat = shaft_d - flat_depth (default 2.3). MEASURE IT!
bore_clearance = 0.15;  // added to diameter AND across-flat (0.10 = snug/ream, 0.20 = loose)
bore_depth     = 10;    // shaft engagement depth
blind_bore     = true;  // true = closed top cap (recommended), false = through bore
bore_chamfer   = 0.4;   // lead-in chamfer at the bore entrance (also kills elephant foot)

/* [Hub] */
hub_d          = 10;    // hub outer diameter
hub_h          = 12;    // hub height (cap thickness = hub_h - bore_depth when blind)
hub_top_chamfer= 1.0;

/* [Set screw] */
screw_size     = "M2";  // "M2" or "M2.5"
// Angle of the set screw (and of the shaft flat it presses on), measured
// CCW from the pointer (+X). 90 = screw on the side of the hub, clear of the arms.
// The flat is always centred under the screw.  Change this if the original
// vane's pointer was oriented differently relative to the flat (calibration!).
screw_angle    = 90;
screw_z        = 5;     // height of screw axis; default = mid engagement (bore_depth/2)
nut_trap       = false; // true = add a top-loading hex pocket for an M2 / M2.5 nut
nut_clear      = 0.3;   // extra clearance for the nut pocket

/* [Arms] */
arm_w          = 3.0;   // arm width (horizontal)  - keep <= 3.6 so it slices solid
arm_h          = 5.0;   // arm height (vertical)
pointer_len    = 58;    // hub axis -> start of arrow head
nose_l         = 32;    // arrow-head length (tip at pointer_len + nose_l)
nose_w         = 28;    // arrow-head base width
nose_h         = 12.0;  // arrow-head height = COUNTERWEIGHT TUNING PARAMETER (balance)

/* [Tail fin] */
fin_x0         = 50;    // hub axis -> fin leading edge (at root)
fin_root       = 60;    // fin chord at the root (on the boom)
fin_tip        = 32;    // fin chord at the top (swept leading edge)
fin_h          = 48;    // fin height above the boom
fin_t          = 1.6;   // fin thickness

$fn = 64;
eps = 0.01;

// ---------------------------------------------------------------------
tap_d   = (screw_size == "M2.5") ? 2.05 : 1.6;   // tap drill for self-tapping in plastic
nut_af  = (screw_size == "M2.5") ? 5.0  : 4.0;   // nut across flats
nut_t   = (screw_size == "M2.5") ? 2.0  : 1.6;   // nut thickness
bore_r  = (shaft_d + bore_clearance) / 2;
flat_y  = (shaft_d - flat_depth) - shaft_d/2 + bore_clearance/2; // flat plane offset from axis
tail_end = fin_x0 + fin_root;

// Horizontal hole along +Y with a 45-degree teardrop point toward +Z
module teardrop_y(d, len) {
    rotate([90,0,0]) translate([0,0,-len]) linear_extrude(len)
        union() {
            circle(d = d);
            rotate(45) square(d/2);
        }
}

// D-shaped bore (flat facing +Y before rotation)
module d_bore() {
    top = blind_bore ? bore_depth : hub_h + 1;
    intersection() {
        translate([0,0,-1]) cylinder(r = bore_r, h = top + 1);
        translate([-5, -5, -2]) cube([10, 5 + flat_y, top + 3]);
    }
    // conical (drill-point) roof: prints without a bridge
    if (blind_bore)
        intersection() {
            translate([0,0,bore_depth - eps]) cylinder(r1 = bore_r, r2 = 0, h = bore_r);
            translate([-5, -5, 0]) cube([10, 5 + flat_y, 30]);
        }
    // entrance chamfer
    translate([0,0,-eps]) cylinder(r1 = bore_r + bore_chamfer, r2 = bore_r, h = bore_chamfer);
}

module screw_features() {
    // radial tap-drill hole, from just inside the flat out through the hub wall
    translate([0, flat_y - 0.5, screw_z]) teardrop_y(tap_d, hub_d);
    if (nut_trap) {
        ny = flat_y + 0.6;                       // inner face of the nut pocket
        R  = (nut_af + nut_clear) / sqrt(3);     // hex circumradius
        translate([0, ny, 0]) rotate([90,0,0]) translate([0,0,-(nut_t + nut_clear)])
            linear_extrude(nut_t + nut_clear)
                hull() {
                    translate([0, screw_z]) rotate(90) circle(r = R, $fn = 6);
                    translate([0, hub_h + 2]) rotate(90) circle(r = R, $fn = 6);
                }
    }
}

module hub() {
    rotate_extrude() polygon([
        [0,0], [hub_d/2, 0], [hub_d/2, hub_h - hub_top_chamfer],
        [hub_d/2 - hub_top_chamfer, hub_h], [0, hub_h]]);
}

module pointer_arm() {
    translate([0, -arm_w/2, 0]) cube([pointer_len + 1, arm_w, arm_h]);
    // arrow head = nose counterweight: plan-view triangle prism.
    // nose_h is tuned so the centre of mass sits on the shaft axis (see README).
    translate([pointer_len, 0, 0]) linear_extrude(nose_h)
        polygon([[0, -nose_w/2], [nose_l, 0], [0, nose_w/2]]);
}

module tail() {
    translate([-tail_end, -arm_w/2, 0]) cube([tail_end, arm_w, arm_h]);
    // fin: vertical plate standing on the boom, swept leading edge
    translate([0, fin_t/2, 0]) rotate([90,0,0]) linear_extrude(fin_t)
        polygon([
            [-fin_x0,              arm_h - 0.5],
            [-tail_end,            arm_h - 0.5],
            [-tail_end,            arm_h + fin_h],
            [-tail_end + fin_tip,  arm_h + fin_h]]);
}

module wind_vane() {
    difference() {
        union() { hub(); pointer_arm(); tail(); }
        rotate(screw_angle - 90) { d_bore(); screw_features(); }
    }
}

wind_vane();
