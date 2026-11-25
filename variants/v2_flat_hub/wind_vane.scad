// =====================================================================
//  Replacement wind-direction vane for VEVOR YT60231 weather station  (v2)
//  Parametric OpenSCAD model.  Units: mm.
//
//  v2: profile follows the original VEVOR vane (small half-barb arrow,
//  tall swept tail fin with a concave leading edge, ~175 mm overall).
//  Static balance comes from a small pod of steel hex nuts hidden behind the
//  arrow head, not from a big plastic arrow.  The balance doesn't depend on
//  infill: everything off the axis is <= 3 mm thick, so it slices solid.
//
//  Coordinate system (= print orientation = installed orientation):
//    Z  = shaft axis (up).  Bottom face (z=0) sits flat on the print bed.
//    +X = arrow (points INTO the wind).   -X = tail fin.
//  Prints with NO supports: hub upright, bore opens downward (blind, cone
//  roof), fin/arrow are vertical walls, set-screw hole is a teardrop.
// =====================================================================

/* [Shaft & bore] */
shaft_d        = 2.8;   // measured shaft diameter
flat_depth     = 0.5;   // D-flat depth. across-flat = shaft_d - flat_depth (default 2.3). MEASURE IT!
bore_clearance = 0.15;  // added to diameter AND across-flat (0.10 snug/ream, 0.20 loose)
bore_depth     = 11;    // shaft engagement depth
blind_bore     = true;  // true = closed top cap (keeps rain off the shaft)
bore_chamfer   = 0.4;

/* [Hub] */
hub_d          = 11;
hub_h          = 14;    // cap = hub_h - bore_depth (3 mm)
hub_top_chamfer= 1.2;
hub_recess_d   = 0;     // optional bottom counterbore to clear a boss/tab on the housing (0 = off)
hub_recess_h   = 0;     //   its depth; roof is a 45-degree cone, so it still prints support-free

/* [Set screw] */
screw_size     = "M2";  // "M2" or "M2.5"
screw_angle    = 90;    // CCW from the arrow (+X); the flat is centred under the screw
screw_z        = 5.5;   // = bore_depth/2
nut_trap       = false; // top-loading hex pocket for an M2/M2.5 nut
nut_clear      = 0.3;

/* [Arms] */
arm_w          = 3.0;   // horizontal width of the arm rib
arm_h          = 5.0;   // vertical height of the arm rib (from the bed)
nose_len       = 72;    // axis -> arrow tip           (original ~72 mm)
barb_len       = 18;    // length of the half-barb arrow head
barb_h         = 7;     // barb height above the arm rib

/* [Tail fin] (side-view profile of the original) */
tail_len_top   = 100;   // axis -> top trailing corner (original ~100 mm)
tail_len_bot   = 77;    // axis -> end of boom / bottom trailing corner (original ~77)
fin_top_chord  = 33;    // flat top edge (original ~33)
fin_h          = 45;    // fin top above the bed (original ~44 above the arm bottom)
fin_root_x     = 11;    // where the concave leading edge meets the arm near the hub
fin_curve      = 1.3;   // leading-edge concavity (1 = straight, 2 = strongly concave)
fin_t          = 1.4;   // fin thickness (2 perimeters + gap fill on a 0.4 nozzle)
fin_round      = 2;     // corner rounding

/* [Ballast] */
ballast        = "nuts"; // "nuts" = steel hex-nut pod (balanced), "none" = like the original (tail-heavy)
ballast_nut    = "M6";   // "M4","M5","M6","M8" (DIN 934 / ISO 4032 steel hex nuts)
ballast_count  = 2;      // number of nuts stacked in the pocket
ballast_x      = 37.3;   // pod centre from axis = BALANCE TUNING PARAMETER (tune.py)
pod_wall       = 1.2;
pod_floor      = 1.0;
pocket_clear   = 0.3;    // across-flats clearance (nuts drop in; fix with a dab of silicone/epoxy)

$fn = 64;
eps = 0.01;

// ---------------------------------------------------------------------
tap_d   = (screw_size == "M2.5") ? 2.05 : 1.6;
nut_af  = (screw_size == "M2.5") ? 5.0  : 4.0;
nut_t   = (screw_size == "M2.5") ? 2.0  : 1.6;
bore_r  = (shaft_d + bore_clearance) / 2;
flat_y  = (shaft_d - flat_depth) - shaft_d/2 + bore_clearance/2;

function bn(i) = ballast_nut == "M4" ? [7,3.2][i] : ballast_nut == "M5" ? [8,4][i]
               : ballast_nut == "M8" ? [13,6.5][i] : [10,5][i];
b_af   = bn(0);
b_t    = bn(1);
b_R    = (b_af + pocket_clear) / sqrt(3);          // pocket hex circumradius
pod_r  = b_R + pod_wall;
pocket_h = ballast_count * b_t + 0.4;
pod_h  = pod_floor + pocket_h;

module teardrop_y(d, len) {
    rotate([90,0,0]) translate([0,0,-len]) linear_extrude(len)
        union() { circle(d = d); rotate(45) square(d/2); }
}

module d_bore() {
    top = blind_bore ? bore_depth : hub_h + 1;
    intersection() {
        translate([0,0,-1]) cylinder(r = bore_r, h = top + 1);
        translate([-6, -6, -2]) cube([12, 6 + flat_y, top + 3]);
    }
    if (blind_bore)
        intersection() {
            translate([0,0,bore_depth - eps]) cylinder(r1 = bore_r, r2 = 0, h = bore_r);
            translate([-6, -6, 0]) cube([12, 6 + flat_y, 40]);
        }
    translate([0,0,-eps]) cylinder(r1 = bore_r + bore_chamfer, r2 = bore_r, h = bore_chamfer);
}

module screw_features() {
    translate([0, flat_y - 0.5, screw_z]) teardrop_y(tap_d, hub_d);
    if (nut_trap) {
        ny = flat_y + 0.6;
        R  = (nut_af + nut_clear) / sqrt(3);
        translate([0, ny, 0]) rotate([90,0,0]) translate([0,0,-(nut_t + nut_clear)])
            linear_extrude(nut_t + nut_clear)
                hull() {
                    translate([0, screw_z]) rotate(90) circle(r = R, $fn = 6);
                    translate([0, hub_h + 2]) rotate(90) circle(r = R, $fn = 6);
                }
    }
}

module hub_recess() {
    if (hub_recess_d > 0 && hub_recess_h > 0) {
        translate([0,0,-eps]) cylinder(d = hub_recess_d, h = hub_recess_h + eps);
        translate([0,0,hub_recess_h - eps]) cylinder(r1 = hub_recess_d/2, r2 = 0, h = hub_recess_d/2);
    }
}

module hub() {
    rotate_extrude() polygon([
        [0,0], [hub_d/2, 0], [hub_d/2, hub_h - hub_top_chamfer],
        [hub_d/2 - hub_top_chamfer, hub_h], [0, hub_h]]);
}

// side-view (XZ) profile of arm + barb + fin, extruded to a thickness about y=0
module plate_xz(t) { translate([0, t/2, 0]) rotate([90,0,0]) linear_extrude(t) children(); }

module fin_2d() {
    n = 24;
    lead = [for (i = [0:n]) let(u = i/n)
              [-(tail_len_top - fin_top_chord) + ((tail_len_top - fin_top_chord) - fin_root_x) * u,
               arm_h + (fin_h - arm_h) * pow(1-u, fin_curve)]];
    offset(r = fin_round) offset(delta = -fin_round)
        polygon(concat([[-tail_len_top, fin_h]], lead,
                       [[-fin_root_x, arm_h - 1], [-tail_len_bot, arm_h - 1]]));
}

module barb_2d() {
    x0 = nose_len - barb_len;
    polygon([[x0, 0], [nose_len, 0], [nose_len, 0.8],
             [x0 + 1.0, arm_h + barb_h], [x0, arm_h + barb_h]]);
}

module arms() {
    // arm rib from tail end to arrow tip
    translate([-tail_len_bot, -arm_w/2, 0]) cube([tail_len_bot + nose_len - barb_len + 1, arm_w, arm_h]);
    plate_xz(arm_w) barb_2d();
    plate_xz(fin_t) fin_2d();
    // small root fillet strip so the thin fin is well anchored on the rib
    plate_xz(arm_w) polygon([[-tail_len_bot, arm_h - 0.5], [-fin_root_x, arm_h - 0.5],
                             [-fin_root_x - 6, arm_h + 1.5], [-tail_len_bot + 2, arm_h + 1.5]]);
}

module ballast_pod() {
    if (ballast == "nuts")
        translate([ballast_x, 0, 0]) cylinder(r = pod_r, h = pod_h, $fn = 48);
}
module ballast_pocket() {
    if (ballast == "nuts")
        translate([ballast_x, 0, pod_floor]) rotate(30) cylinder(r = b_R, h = pocket_h + 1, $fn = 6);
}

module wind_vane() {
    difference() {
        union() { hub(); arms(); ballast_pod(); }
        rotate(screw_angle - 90) { d_bore(); screw_features(); }
        hub_recess();
        ballast_pocket();
    }
}

wind_vane();
